from abc import ABC, abstractmethod
import json
class Book:
    def __init__(self, book_id, title, author, book_num):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.book_num = book_num
        self.__available_num = book_num
    def borrow_books(self):  # 借阅图书
        if self.__available_num >= 1:
            self.__available_num -= 1
            return True
        else:
            return False #图书不在books.json中，借阅失败
    def return_books(self):  # 归还图书
        self.__available_num += 1
    def get_available_num(self): return self.__available_num


class Member(ABC):
    def __init__(self, member_id,member_name,member_password):
        self.member_id = member_id
        self.member_name = member_name
        self.__member_password = member_password
        self.__borrow_books = []
    def borrow_books(self, book:Book):
        # 是否达到会员借书上限
        if len(self.__borrow_books) >= self.get_max_books():
            print('可借阅图书数量达到上限，借阅失败。')
            return False
        else: # 图书是否能借
            if book.borrow_books():
                self.__borrow_books.append(book)
                print(f'{self.member_name} 已成功借阅图书 {book.title}。')
                return True
            else:
                print(f'图书{book.title}已无库存,借阅失败。')
                return False
    def return_books(self,book:Book):
        if book not in self.__borrow_books:
            print('您未借阅过此图书，归还失败。')
        else:
            self.__borrow_books.remove(book)
            book.return_books()
            print(f'{self.member_name} 已成功归还图书 {book.title}。')
    def get_password(self):
        return self.__member_password
    def get_borrowed_books(self):
        return self.__borrow_books
    @abstractmethod
    def get_max_books(self): # 子类定义
        pass

class NormalMember(Member):
    def get_max_books(self) -> int:
        return 3

class VIPMember(Member):
    def __init__(self,member_id,member_name,member_password,VIP_level):
        super().__init__(member_id,member_name,member_password)
        self.VIP_level = VIP_level
    def get_max_books(self) -> int:
        return self.VIP_level+6

class library_system:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.current_member:Member|None = None
        self.load_books_data()
        self.load_members_data()
    def get_current_member(self):
        pass

    def load_books_data(self):
        with open('books.json','r',encoding='utf-8') as f:
            book_json=json.load(f)
            for book in book_json:
                self.books[book['编号']]=Book(book['编号'],book['标题'],book['作者'],book['数量'])
            print('书籍数据上传成功。')

    def load_members_data(self):
        with open('members.json', 'r', encoding='utf-8') as f:
            member_json = json.load(f)
            for member in member_json:
                if member['卡号'].startswith('V'):
                    self.members[member['卡号']] = VIPMember(member['卡号'],member['姓名'],member['密码'],member['会员等级'])
                elif member['卡号'].startswith('N'):
                    self.members[member['卡号']] = NormalMember(member['卡号'], member['姓名'], member['密码'])
            print('会员数据上传成功。')

    def login_system(self):
        while True:
            print('\n【登录】')
            input_member_id=input('请输入会员卡号：')
            input_password=input('请输入密码：')
            if input_member_id not in self.members:
                print('会员卡号不存在，请重新输入！')
                continue
            else:
                member = self.members[input_member_id]
                if input_password not in self.members[input_member_id].get_password():
                    print('密码不正确，请重新输入！')
                    continue
                else:
                    print(f'登录成功，欢迎您，{member.member_name}！')
                    self.current_member = member
                    return True
    def run(self):
        if self.login_system():
            while True:
                print('\n1.借阅图书')
                print('2.归还图书')
                print('3.查看借阅')
                print('4.退出系统')
                choice = input('请输入操作(1-4)：')
                match choice:
                    case '1':
                        self.borrow_book()
                    case '2':
                        self.return_book()
                    case '3':
                        self.show_borrowed_books()
                    case '4':
                        subchoice=input('确认退出系统(y/n)？')
                        if subchoice=='y' or subchoice=='Y':
                            print('退出系统，bye~')
                            break
                        elif subchoice=='n' or subchoice=='N':
                            print('撤回退出，请继续输入操作。')
                            continue

    def borrow_book(self):  # 借阅图书
        # 展示现有书籍
        for book in self.books.values():
            print(f'编号：{book.book_id}，标题：{book.title}，作者：{book.author}，总数：{book.book_num}，可用：{book.get_available_num()}')
        # 输入借阅书籍
        while True:
            input_book_id = input('请输入要借阅的图书编号：')
            if input_book_id not in self.books:
                print('图书编号不存在，请重新输入！')
                continue
            else:
                self.current_member.borrow_books(self.books[input_book_id])
                break

    def return_book(self):  # 归还图书
        # 展示已借阅列表
        print('【您已借阅的图书列表：】')
        borrowed_books = self.current_member.get_borrowed_books()
        for book in borrowed_books:
            print(f'编号：{book.book_id}，标题：{book.title}')
        # 输入归还书籍
        while True:
            input_book_id = input('请输入要归还的图书编号：')
            if input_book_id not in self.books:
                print('图书编号不存在，请重新输入！')
                continue
            else:
                self.current_member.return_books(self.books[input_book_id])
                break

    def show_borrowed_books(self):
        borrowed_books = self.current_member.get_borrowed_books()
        if len(borrowed_books) > 0:
            print('【您已借阅的图书列表：】')
            for book in borrowed_books:
                print(f'编号：{book.book_id}，标题：{book.title}')
        else:
            print('您尚未借阅任何图书。')

if __name__ == '__main__':
    system = library_system()
    system.run()
