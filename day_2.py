from day_1 import BankAccount
from exception import AccountFrozenError, AccountClosedError,InvalidOperationError,InsufficientFundsError

class SavingsAccount (BankAccount):
    
    MAX_LIMIT = 2_000_000
    MIN_BALANCE = 100
    INTEREST_RATE = 0.5
    
    def __init__(self, account_id, name, surname, lastname, account_balance, status, currency):
        super().__init__(account_id, name, surname, lastname, account_balance, status, currency)
        
        if account_balance < self.MIN_BALANCE :
            raise InvalidOperationError (f"Ошибка. Невозможно создать счет. Минимальный баланс долежн быть {self.MIN_BALANCE}")

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
        print (f"Cчет пополнен на {amount}, сумма на счете {self.account_balance}\n")

#   метод снятия наличных
 
    def withdraw(self, amount):
    
    #   проверка на указание суммы

        if amount is None:
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
    
    #   проверка на минимальный остаток

        if self.account_balance - amount < self.MIN_BALANCE:
            raise InvalidOperationError (f"Ошибка. Недостаточно средств, минимальный остаток должен быть {self.MIN_BALANCE}")   

    #   операция снятия

        self.account_balance = self.account_balance - amount 
        print (f"Снятие {amount}, баланс {self.account_balance}\n")

#   метод начисления процетов 

    def  apply_monthly_interest (self):

    #   проверка статуса счета 

        if self.status != "active":
            raise InvalidOperationError (f"Ошибка. Счет {self.status}")
        
    #   операция начисления процентов

        self.monthly_interest = self.account_balance * (self.INTEREST_RATE / 100) 
        self.account_balance += self.monthly_interest           
        print (f"Начислены проценты {self.monthly_interest}. Баланс {self.account_balance}\n")

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
            "max_limit": self.MAX_LIMIT,
            "min_balance": self.MIN_BALANCE,
            "interest_rate": self.INTEREST_RATE
            }
        print (f"Номер счета: {account_info['account_id']}")
        print (f"Владелец: {account_info['owner'] ['surname']} {account_info['owner']['name']} {account_info ['owner'] ['lastname']}")
        print (f"Баланс счета: {account_info['balance']} {account_info ['currency']}")
        print (f"Статус: {account_info['status']}")
        print (f"Максимальный лимит: {account_info['max_limit']}")
        print (f"Минимальный лимит: {account_info['min_balance']}")
        print (f"Накопительная ставка: {account_info['interest_rate']}")

    def __str__(self):
        return (
            f"Номер счета: {self.account_id[-4:]}\n"
            f"Имя: {self.name}\n" 
            F"Фамилия: {self.lastname}\n"
            F"Отчество: {self.surname}\n"
            F"Статус счета: {self.status}\n" 
            F"Баланс: {self.account_balance}\n"
            f"Валюта счета: {self.currency}\n"
            f"Максимальный лимит: {self.MAX_LIMIT}\n"
            f"Минимальный отстаток на счете: {self.MIN_BALANCE}\n"
            f"Месячная ставка доходности счета, %: {self.INTEREST_RATE} " 
                )
    
class PremiumAccount (BankAccount):

#   лимит овердрафта  
    
    OVERDRAFT_LIMIT = 500_000

#   максимальный лимит средств на счете
    
    MAX_LIMIT = 5_000_000
   
    def __init__(self, account_id, name, surname, lastname, account_balance, status, currency):
        super().__init__(account_id, name, surname, lastname, account_balance, status, currency)
        
        self.overdraft_used = 0
        self.overdraft_comission = 100

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
        
    #   проверка корректности статуса счета

        if self.status != "active":
            raise InvalidOperationError (f"Ошибка. Некорректный статус счета {self.status}")
    
    #   операция зачисления средств
     
        self.account_balance += amount
        print (f"Cчет пополнен на {amount}, сумма на счете {self.account_balance}\n")
         
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
   
    #   проверка превышения суммы (с учетом овердрафта)
    
        available = self.account_balance + self.OVERDRAFT_LIMIT
        if amount > available :
            raise InsufficientFundsError (f"Ошибка. Недостаточно средств, баланс {self.account_balance}\n")

    #   операция снятия средств

        if amount <= self.account_balance:
            self.account_balance = self.account_balance- amount
            print (f"Снятие {amount}, баланс {self.account_balance}\n")
   
    #   условия снятия с комиссией и  возможностью овердрафта

        else:
            remainder = (amount + self.overdraft_comission) - self.account_balance 
            self.account_balance = 0 
            self.overdraft_used += remainder
            credit = self.OVERDRAFT_LIMIT - self.overdraft_used
            print (f"Снятие {amount}. Комиссия за снятие {self.overdraft_comission}. Текущий баланс {self.account_balance}. Использовано лимита {self.overdraft_used}.Остаток {credit}\n")

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
            "max_limit": self.MAX_LIMIT,
            "overdraft_limit": self.OVERDRAFT_LIMIT
            }
        print (f"Номер счета: {account_info['account_id']}")
        print (f"Владелец: {account_info['owner'] ['surname']} {account_info['owner']['name']} {account_info ['owner'] ['lastname']}")
        print (f"Баланс счета: {account_info['balance']} {account_info ['currency']}")
        print (f"Статус: {account_info['status']}")
        print (f"Максимальный лимит: {account_info['max_limit']}")
        print (f"Лимит овердрафта: {account_info['overdraft_limit']}")


    def __str__(self):
        return (
            f"Номер счета: {self.account_id[-4:]}\n"
            f"Имя: {self.name}\n" 
            F"Фамилия: {self.lastname}\n"
            F"Отчество: {self.surname}\n"
            F"Статус счета: {self.status}\n" 
            F"Баланс: {self.account_balance}\n"
            f"Валюта счета: {self.currency}\n"
            f"Максимальный лимит: {self.MAX_LIMIT}\n"
            f"Лимит овердрафта: {self.OVERDRAFT_LIMIT}\n"
                )
    
class InvestmentAccount (BankAccount):

#   справочник активов

    AVAILABLE_ASSETS = {
        "YAND": {"name": "YANDEX", "type": "stock", "current_price": 150.00},
        "NVD": {"name": "NVIDIA", "type": "stock", "current_price": 500.00},
        "RVLT": {"name": "REVOLUT", "type": "etf", "current_price": 5000.00},
        "OFZ": {"name": "ОФЗ РФ", "type": "bond", "current_price": 2000.00 }
    }

#   прогнозные ставки дохода 

    BASE_GROWTH_RATE = 10
    OPTIMISTIC_GROWTH_RATE = 15
    PESSIMISTIC_GROWTH_RATE = - 10

    def __init__(self, account_id, name, surname, lastname, account_balance, status, currency):
        super().__init__(account_id, name, surname, lastname, account_balance, status, currency)
        self.portfolio = {}

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

#   метод покупки актива
     
    def buy_assets (self, position, quantity):

    #   проверка доступности счета    
 
        if self.status != "active":
            raise InvalidOperationError (f" Ошибка. Счет {self.status}")
    
    #   проверка положительного количества   

        if quantity <=0:
            raise InvalidOperationError ("Количество должно быть положительным")
    
    #   проверка корректности покупаемого актива 

        if position not in self.AVAILABLE_ASSETS:
            raise InvalidOperationError (f"Актив недоступен. Доступные активы {self.AVAILABLE_ASSETS}")
    
    #   стоимость актива 
    
        price = quantity * self. AVAILABLE_ASSETS [position] ["current_price"]

    #   проверка баланса счета

        if price > self.account_balance:
            raise InvalidOperationError (f"Недостаточно средств. Баланс {self.account_balance}")
        
        self.account_balance -= price 
        self.portfolio [position] = {"quantity" : quantity, "current_price": price} 
        
        print(f"Куплено {quantity} {position} на сумму {price}\n")
        print(f"Остаток на счёте: {self.account_balance}\n")
        print(f"Портфель: {self.portfolio}\n")

#   метод прогнозирования дохода 

    def project_yearly_growth (self):
        
        portfolio_value = 0
        for pos in self.portfolio:
            price = self.AVAILABLE_ASSETS[pos]["current_price"]
            qty = self.portfolio[pos]["quantity"]
            portfolio_value += price * qty
    
    #   Проверка если активы не куплены

        if portfolio_value == 0:
            print("Портфель пуст")
            return None
        
        print(f"\n Стоимость активов: {portfolio_value:.2f}")
        print(f"Базовый прогноз (+10%): {portfolio_value * 1.10:.2f}")
        print(f"Оптимистичный (+15%): {portfolio_value * 1.15:.2f}")
        print(f"Пессимистичный (-10%): {portfolio_value * 0.90:.2f}")

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
            "max_limit": self.MAX_LIMIT,
            "available_assets": self.AVAILABLE_ASSETS
            }
        print (f"Номер счета: {account_info['account_id']}")
        print (f"Владелец: {account_info['owner'] ['surname']} {account_info['owner']['name']} {account_info ['owner'] ['lastname']}")
        print (f"Баланс счета: {account_info['balance']} {account_info ['currency']}")
        print (f"Статус: {account_info['status']}")
        print (f"Максимальный лимит: {account_info['max_limit']}")
        print (f"Доступные активы: {account_info['available_assets']}")

    def __str__(self):
        return (
            f"Номер счета: {self.account_id[-4:]}\n"
            f"Имя: {self.name}\n" 
            F"Фамилия: {self.lastname}\n"
            F"Отчество: {self.surname}\n"
            F"Статус счета: {self.status}\n" 
            F"Баланс: {self.account_balance}\n"
            f"Валюта счета: {self.currency}\n"
            f"Доступные для покупки активы: {self.AVAILABLE_ASSETS}\n"\
            f"Приобретенные активы: {self.portfolio}"
                )

# создание инвестиционного счета
# client_1 = PremiumAccount ("", "Ivan", 'Ivanovich', 'Ivanov', 5_000, "active", "")
# print (client_1)
# client_1.get_account_info ()
# print (client_1)
# info = client_1.get_account_info 
# print (info)
# print (client_1)
# client_1.  ("NVD", 1)
# client_1.buy_assets (70000)
# print (client_1)
# # покупка активов + прогноз доходности
# client_1. buy_assets ("NVD", 1)
# client_1. project_yearly_growth ()

# # создание премиум счета
# client_2 = PremiumAccount ("1", "Ivan", 'Ivanovich', 'Ivanov', 100000, "active")

# # снятие в овердрафт и пополнение  
# client_2. deposit (500)
# client_2. withdraw (150_000)
