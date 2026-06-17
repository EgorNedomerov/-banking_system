from exception import AccountFrozenError, AccountClosedError,InvalidOperationError,InsufficientFundsError
from abc import ABC, abstractmethod
import shortuuid
class AbstractAccount (ABC):
    account_id: int
    name: str
    surname: str
    lastname: str
    account_balance: float
    status: str
    max_limit: float
    used_id = set()
    def __init__(self, account_id,name,surname,lastname,account_balance,status):
        
        if account_id in AbstractAccount.used_id:
            raise ValueError (f"ID {account_id} уже существует")
        AbstractAccount.used_id.add(account_id)
        self.account_id = account_id
        self.name = name
        self.surname = surname
        self.lastname = lastname
        self.account_balance = account_balance
        
        allowed_status = ['active', 'frozen', 'closed']
        
        if status not in allowed_status:
            raise ValueError ("Некорректный статус")
        self.status = status
   
    @abstractmethod
    def deposit (self, amount):
        pass 
    @abstractmethod
    def withdraw (self,amount):
        pass
   
    @abstractmethod
    def get_account_info(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass

class BankAccount (AbstractAccount):
    
    MAX_LIMIT = 1_000_000
    
    def __init__(self, account_id, name, surname, lastname, account_balance, status, currency):
        
        #   проверка id счета и вызов метода генерации id

        if account_id == "" or account_id is None:
           account_id = self.generate_uuid ()
        super().__init__(account_id, name, surname, lastname, account_balance, status) 
        
        self.allowedcurrency = ['RUB','USD','EUR','KZT','CNY']
        self.currency = currency

    #   валидация входящих данных  

        if not isinstance (name, str):
            raise TypeError ("В поле имя введен некорректный формат данных") 
        
        if not isinstance (surname, str):
            raise TypeError ("В поле фамилия введен некорректный формат данных") 
        
        if not isinstance (lastname, str):
            raise TypeError ("В поле отчество введен некорректный формат данных") 
        
        if not name and not surname and not lastname:
            raise ValueError ("Фамилия, имя, отчество обязательный для заполнения")
        
        if account_balance <0:
           raise ValueError (f"Сумма {account_balance} не может быть отрицательной") 
        
        # добавлена валидация валюты счета
                                                                                    
        if currency not in self.allowedcurrency:
        
            raise InvalidOperationError (f"Необходимо указать валюту для открытия счета. Список допустимых валют {self.allowedcurrency}")
        
    #   исправлена проверка статуса счета

        if status == "closed":
            raise ValueError ("Операции со счетом невозможны")
        
 
#   метод пополнения баланса
 
    def deposit (self, amount):
    
    #   проверки доступности счета 
    
        if self.status == "frozen":
            raise AccountFrozenError (f"Пополнение невозможно, счет {self.status}")
        
        if self.status == "closed":
            raise AccountClosedError (f"Пополнение невозможно, счет {self.status}")
   
    #   проверка корректности суммы
        
        if amount <0:
            raise InvalidOperationError ("Сумма не может быть отрицательной") 
        
     #   проверка максимального лимита   
        
        if amount + self.account_balance > self.MAX_LIMIT:
            raise   InvalidOperationError (f"Ошибка. Сумма не может быть больше установленного лимита {self.MAX_LIMIT}")
        
    #   операция зачисления средств
     
        self.account_balance += amount
        print (f"Cчет пополнен на {amount}, сумма на счете {self.account_balance}")
        
        
#   метод снятия наличных

    def withdraw (self,amount):
         
    #   проверка на указание суммы

        if amount is None or amount == "":
            raise InvalidOperationError ("Ошибка. Необходимо указать сумму")
   
    #   проверка на корректность введенной суммы

        if amount <=0:
            raise InvalidOperationError ("Ошибка. Сумма снятия должна быть положительной")
   
    #   проверка статуса счета 

        if self.status =="closed":
            raise AccountClosedError (f"Ошибка, счет {self.status}")
    
        if self.status == "frozen":
            raise AccountFrozenError (f"Ошибка, счет {self.status}")
   
    #   проверка превышения суммы
    
        if amount > self.account_balance:
            raise InsufficientFundsError (f"Ошибка. Недостаточно средств, баланс {self.account_balance}")

    #   операция снятия

        self.account_balance = self.account_balance - amount 
        print (f"Снятие {amount}, баланс {self.account_balance}")

#   генерация уникального id 

    def generate_uuid (self):
            return shortuuid.uuid()
            # print (f"Создан id счета '{self.account_id}'")
    
    def get_account_info(self):
        
        if self.status == "closed":
            return {
                "error": "Счет закрыт",
                "account_id": self.account_id,
                "status": self.status
                }     
        
        account_info = {
            "account_id": self.account_id,
            "owner": {
                "name": self.name,
                "surname": self.surname,
                "lastname": self.lastname
                },
            "balance": self.account_balance,
            "status": self.status,
            "currency": self.currency,
            "max_limit": self.MAX_LIMIT
            }
        print (f"Номер счета: {account_info['account_id']}")
        print (f"Владелец: {account_info['owner'] ['surname']} {account_info['owner']['name']} {account_info ['owner'] ['lastname']}")
        print (f"Баланс счета: {account_info['balance']} {account_info ['currency']}")
        print (f"Статус: {account_info['status']}")
        print (f"Максимальный лимит: {account_info['max_limit']}")
        
        return account_info

    def __str__(self):
        return (
            f"Номер счета: {self.account_id[-4:]}\n"
            f"Имя: {self.name}\n" 
            F"Фамилия: {self.lastname}\n"
            F"Отчество: {self.surname}\n"
            F"Статус счета: {self.status}\n" 
            F"Баланс: {self.account_balance}\n"
            f"Валюта счета: {self.currency}\n"
                )

# создание счета 

# client_1 = BankAccount ("", "Ivan", 'Ivanovich', 'Ivanov', 10000, "active", "RUB")
# client_1.get_account_info()

# создание замороженного счета

# client_2. deposit (500)

# валидация пополнения больше максимального лимита
# client_1. deposit (1_000_000)

# валидация снятия больше текущей суммы
# client_1.withdraw (10_000_000)

# корректное попополнение счета 
# client_1.deposit (1000)

# корректное снятие со счета
# client_1.withdraw (1000)

# client_2.get_account_info ()
# info = client_2.get_account_info()
# print(info)


