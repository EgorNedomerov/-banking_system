from day_1 import AbstractAccount
from exception import AccountFrozenError, AccountClosedError,InvalidOperationError,InsufficientFundsError
class SavingsAccount (AbstractAccount):
    min_balance: float
    monthly_interest: float
    
    def __init__(self, account_id, name, surname, lastname, account_balance, status, max_limit, min_balance, monthly_interest):
        super().__init__(account_id, name, surname, lastname, account_balance, status,max_limit)
        
        self.min_balance = min_balance

        if account_balance < min_balance:
            raise InvalidOperationError (f"Ошибка. Невозможно создать счет. Минимальный баланс долежн быть {self.min_balance}")
        
        self.monthly_interest = monthly_interest
    
    def deposit(self, amount):
       pass

    def get_account_info(self):
        pass

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

        if self.account_balance - amount < self.min_balance:
            raise InvalidOperationError (f"Ошибка. Недостаточно средств, минимальный остаток должен быть {self.min_balance}")   

    #   операция снятия

        self.account_balance = self.account_balance - amount 
        print (f"Снятие {amount}, баланс {self.account_balance}")

#   метод начисления процетов 

    def  apply_monthly_interest (self):

    #   проверка статуса счета 

        if self.status != "active":
            raise InvalidOperationError (f"Ошибка. Счет {self.status}")
        
    #   операция начисления процентов

        self.monthly_interest = self.account_balance * (self.monthly_interest / 100) 
        self.account_balance += self.monthly_interest
        print (f"Начислены проценты {self.monthly_interest}. Баланс {self.account_balance}")
    
class PremiumAccount (AbstractAccount):

#   лимит овердрафта  
    overdraft_limit: float
    OVERDRAFT_LIMIT = 500_000

#   максимальный лимит средств на счете
    MAX_LIMIT = 5_000_000
   
    def __init__(self, account_id, name, surname, lastname, account_balance, status, max_limit = None, overdraft_limit = None):
        super().__init__(account_id, name, surname, lastname, account_balance, status, max_limit)
        
        if overdraft_limit is None:
            overdraft_limit = self.OVERDRAFT_LIMIT
        self.overdraft_limit = overdraft_limit
        self.overdraft_used = 0
        self.overdraft_comission = 100

    def get_account_info(self):
        pass

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
        
    #   проверка корректности статуса счета

        if self.status != "active":
            raise InvalidOperationError (f"Ошибка. Некорректный статус счета {self.status}")
    
    #   операция зачисления средств
     
        self.account_balance += amount
        print (f"Cчет пополнен на {amount}, сумма на счете {self.account_balance}")
         
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
    
        available = self.account_balance + self.overdraft_limit
        if amount > available :
            raise InsufficientFundsError (f"Ошибка. Недостаточно средств, баланс {self.account_balance}")

    #   операция снятия средств

        if amount <= self.account_balance:
            self.account_balance = self.account_balance- amount
            print (f"Снятие {amount}, баланс {self.account_balance}")
   
    #   условия снятия с комиссией и  возможностью овердрафта

        else:
            remainder = (amount + self.overdraft_comission) - self.account_balance 
            self.account_balance = 0 
            self.overdraft_used += remainder
            credit = self.overdraft_limit - self.overdraft_used
            print (f"Снятие {amount}. Комиссия за снятие {self.overdraft_comission}. Текущий баланс {self.account_balance}. Использовано лимита {self.overdraft_used}.Остаток {credit}")

class InvestmentAccount (AbstractAccount):

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

    def __init__(self, account_id, name, surname, lastname, account_balance, status, max_limit = None):
        super().__init__(account_id, name, surname, lastname, account_balance, status, max_limit)
        self.portfolio = {}

    def deposit(self, amount):
        pass
    def withdraw(self, amount):
        pass
    def get_account_info(self):
        pass

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
        print(f"Куплено {quantity} {position} на сумму {price}")
        print(f"Остаток на счёте: {self.account_balance}")
        print(f"Портфель: {self.portfolio}")

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

# создание инвестциионного счета
client_1 = InvestmentAccount ("1", "Ivan", 'Ivanovich', 'Ivanov', 100000, "active")

# покупка активов + прогноз доходности
client_1. buy_assets ("NVD", 1)
client_1. project_yearly_growth ()

# создание премиум счета
client_2 = PremiumAccount ("1", "Ivan", 'Ivanovich', 'Ivanov', 100000, "active")

# снятие в овердрафт и пополнение  
client_2. deposit (500)
client_2. withdraw (150_000)
