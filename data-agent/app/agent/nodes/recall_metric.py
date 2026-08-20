from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.entities.metric_info import MetricInfo
from app.prompt.prompt_loader import load_prompt

async def recall_metric(state: DataAgentState, runtime: Runtime[DataAgentContext]):
      writer = runtime.stream_writer
      writer({"type": "progress", "step": "召回指标", "status": "running"})
      # 接收关键词+llm扩展的关键词->Qdrant进行指标信息的向量检索

      query = state["query"]
      keywords = state["keywords"]

      embedding_client = runtime.context['embedding_client']
      metric_qdrant_repository = runtime.context['metric_qdrant_repository']

      try:
            # 借助llm扩展关键词--根据query
            #   --配置llm(langchain：chain=prompt[PromptTemplate:template模板,input_variables变量["query"]]|llm|output_parser[JsonOutputParser])
            #   --template模板--load .prompt文件(Path("__file__"[当前文件路径]).parent[2]/'prompts'/f"{name}.prompt")--Path对象.read_text(encoding="utf-8"中文)
            #   --合并关键词(可能重复->set集合去重)   set(keywords+llm_result)
            prompt = PromptTemplate(template=load_prompt("extend_keywords_for_metric_recall"), input_variables=["query"])
            output_parser = JsonOutputParser()

            chain = prompt | llm | output_parser

            result = await chain.ainvoke({"query": query})

            # 使用扩展后的关键词召回指标信息
            retrieved_metrics_map: dict[str, MetricInfo] = {}
            # 在qdrant中进行向量检索->关键词要embedding为向量(配置context：embedding_client,取出使用runtime.context['embedding_client'])aembed_query(异步)
            #   --在graph实际操作需要embedding_client.init(),需要在context参数中对应增加
            #   --qdrant(context配置qdrant_repository)中search->query_ponits(相关性阈值score_threshold=0.6,数量限制limit=20)--可能对应找到的数据是重复的->利用字典的key不能重复：保存到字典中(以id为key)--转换为定义的业务类--传入state用于后续node
            keywords = list(set(keywords + result))
            logger.info(f"召回指标信息扩展关键词：{keywords}")
            for keyword in keywords:
                  embedding = await embedding_client.aembed_query(keyword)
                  payloads: list[MetricInfo] = await metric_qdrant_repository.search(embedding)
                  for payload in payloads:
                        metric_id = payload.id
                        if metric_id not in retrieved_metrics_map:
                              retrieved_metrics_map[metric_id] = payload

            retrieved_metrics = list(retrieved_metrics_map.values())

            writer({"type": "progress", "step": "召回指标", "status": "success"})
            logger.info(f"召回指标信息：{list(retrieved_metrics_map.keys())}")
            return {"retrieved_metrics": retrieved_metrics}
      except Exception as e:
            writer({"type": "progress", "step": "召回指标", "status": "error"})
            logger.error(f"召回指标信息失败: {str(e)}")
            raise