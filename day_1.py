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
    MAX_LIMIT = 1_000_000
    used_id = set()
    def __init__(self,account_id,name,surname,lastname,account_balance,status, max_limit):
        
        if account_id in AbstractAccount.used_id:
            raise ValueError (f"ID {account_id} уже существует")
        AbstractAccount.used_id.add(account_id)
        self.account_id = account_id
        self.name = name
        self.surname = surname
        self.lastname = lastname
        self.account_balance = account_balance
        
        if max_limit is None:
            max_limit = self.MAX_LIMIT
        
        self.max_limit = max_limit
        
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
class BankAccount (AbstractAccount):
    def __init__(self, account_id, name, surname, lastname, account_balance, status, currency, max_limit = None):
        super().__init__(account_id, name, surname, lastname, account_balance, status, max_limit) 
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
       
        if status != "active":
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
        
        if amount + self.account_balance > self.max_limit:
            raise   InvalidOperationError (f"Ошибка. Сумма не может быть больше установленного лимита {self.max_limit}")
        
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
        
        if self.account_id is None or self.account_id == "":

            self.account_id = shortuuid.uuid()
            print (f"Создан id счета {self.account_id}")
    
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
            "max_limit": self.max_limit
            }
        
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

client_1 = BankAccount ("14597345987", "Ivan", 'Ivanovich', 'Ivanov', 10000, "active", "RUB")
print (client_1)

# создание замороженного счета
client_2 = BankAccount ("458475", "Petr", "Petrovich", "Petrov", 100, "frozen", "RUB")
print (client_2)

# попытка пополнить замороженный счет
client_2. deposit (500)

# валидация пополнения больше максимального лимита
client_1. deposit (1_000_000)

# валидация снятия больше текущей суммы
client_1.withdraw (10_000_000)

# корректное попополнение счета 
client_1.deposit (1000)

# корректное снятие со счета
client_1.withdraw (1000)

client_2.get_account_info ()
info = client_2.get_account_info()
print(info)


