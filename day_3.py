from datetime import date, datetime
from day_1 import BankAccount
from day_2 import SavingsAccount, PremiumAccount, InvestmentAccount
import shortuuid

class Client:
    
    ALLOWED_STATUS = ['active', 'frozen', 'closed']

    def __init__(self, name, surname, lastname,  contact_number, birth_date, client_id = None):
        
        #   валидация возраста

        today = date.today ()
        age = today.year - birth_date.year
            
        if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
        if age < 18:
             raise ValueError ("Невозможно создать аккаунт. Клиент должен быть старше 18 лет.")
            
        if client_id is None:
            self.client_id = self._generate_client_id ()
        else:
            self.client_id = client_id

        self.account = []

        self.name = name

        self.surname = surname

        self.lastname = lastname

        self.contact_number = contact_number

        self.birth_date = birth_date
            
        self.status = "active"
            
        self.failed_attempts = 0

        self. is_blocked = False

        self.suspicious_activities = []

    def _generate_client_id(self):
        return f"CL{shortuuid.uuid()[:4].upper()}"    

class Bank:
    
    def __init__(self, name):
        
        self.name = name
        self.client= []
        self.account= []
        self.account_counter = 0
    
    def add_client (self, client):

        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Добавить клиента невозможно с 00:00 до 05:00")
        
        for existing_client in self.client:
            if existing_client.client_id == client.client_id:
                print(f"Клиент с ID {client.client_id} уже существует")
                return False
        
        self.client.append(client)

        print(f"Клиент {client.surname} {client.name} (ID: {client.client_id}) добавлен")

#   метод создания аккаунта

    def open_account (self, client, currency, account_type = "standart", opening_balance = 0):

        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Открыть счет невозможно с 00:00 до 05:00")
        
        if client not in self.client:
            print (f"Клиента {client.name} {client.surname} не зарегистрирован в банке")
            return None
        
        if account_type == "savings":
            new_account = SavingsAccount(
            account_id= None,
            name = client.name,
            surname= client.surname,
            lastname= client.lastname,
            account_balance= opening_balance,
            status = "active",
            currency = currency
            )   

        elif account_type == "premium":
            new_account = PremiumAccount(
            account_id= None,
            name = client.name,
            surname= client.surname,
            lastname= client.lastname,
            account_balance= opening_balance,
            status = "active",
            currency = currency   
            )

        elif account_type == "investment":
            new_account = InvestmentAccount(
            account_id= None,
            name = client.name,
            surname= client.surname,
            lastname= client.lastname,
            account_balance= opening_balance,
            status = "active",
            currency = currency   
            )
        else:
            new_account = BankAccount (
            account_id= None,
            name = client.name,
            surname= client.surname,
            lastname= client.lastname,
            account_balance= opening_balance,
            status = "active",
            currency= currency
        )
        self.account.append(new_account)
        client.account.append (new_account.account_id)
        return new_account

#   метод закрытия аккаунта   

    def close_account (self, client, account_id):
        
        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Закрыть счет невозможно с 00:00 до 05:00")
        
        if client not in self.client:
            print (f"Клиент {client.name} {client.surname} не зарегистрирован в банке")
            return False

        if account_id not in client.account:
            print (f"Счет {account_id} не найден")
            return False
        Obj_account = None
        for acc in self.account:
            if acc.account_id == account_id:
                Obj_account = acc
                break
        
        if Obj_account is None:
            print (f"Счет не найден")
            return False
        
        if Obj_account.status == "closed":
            print (f"Счет {account_id} закрыт")
            return False
        
        Obj_account.status = "closed"
        print (f"Счет {account_id} закрыт")
        return True
    
#   метод заморозки акканута
  
    def freeze_account (self, client, account_id):
        
        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Заморозить счет невозможно с 00:00 до 05:00")
        
        if client not in self.client:
            print (f"Клиент {client.name} {client.surname} не зарегистрирован в банке")
            return False
            
        
        if account_id not in client.account:
            print (f"Счет {account_id} не найден")
            return False
        Obj_account = None
        for acc in self.account:
            if acc.account_id == account_id:
                Obj_account = acc
                break
        
        if Obj_account is None:
            print (f"Счет не найден")
            return False
        
        if Obj_account.status == "closed":
            print (f"Счет {account_id} закрыт")
            return False
        
        Obj_account.status = "frozen"
        print (f"Счет {account_id} заморожен")
        return True
    
#   метод разморозки аккаунта 

    def unfreeze_account (self, client, account_id):
        
        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Разморозить Счет невозможно с 00:00 до 05:00")

        if client not in self.client:
            print (f"Клиент {client} не найден")
            return False
        
        if account_id not in client.account:
            print (f"Счет {account_id} не найден")
            return False
    
        Obj_account = None
        for acc in self.account:
            if acc.account_id == account_id:
                Obj_account = acc
                break
        
        if Obj_account is None:
            print (f"Счет не найден")
            return False
        
        if Obj_account.status == "closed":
            print (f"Счет {account_id} закрыт")
            return False
        
        Obj_account.status = "active"
        print (f"Счет {account_id} разморожен")
        return True
    
    def authenticate_client (self, client, password):
        
        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Аутентификация клиента невозможна с 00:00 до 05:00")
        
        if client not in self.client:
            print(f"Клиент с ID {client.client_id} не найден")
            return None
        
        if client.status != "active":
            print(f"Клиент {client.name} {client.surname} не активен. Статус: {client.status}")
            return None
        
        if password == f"pass": # не делал автоматическую генерацию, чтобы удобно было проверять
            client.failed_attempts = 0 
            print(f"Клиент {client.name} {client.surname} (ID: {client.client_id}) успешно аутентифицирован")
            return client

        else:
            client.failed_attempts += 1
            remaining_attempts = 3 - client.failed_attempts
            print(f"Неверный пароль. Осталось попыток: {remaining_attempts}")
        
            if client.failed_attempts >= 3:
                client.is_blocked = True
                client.status = "blocked"
                print(f"Клиент {client.name} {client.surname} заблокирован")
            
                client.suspicious_activities.append ({
                "timestamp": datetime.now(),
                "action": "Попытка входа в заблокированный аккаунт"
                })
                return None

#   метод поиска акккаунтов

    def search_accounts(self,**criteria):
        
        results = []

        for account in self.account:
            match = True

            for key, value in criteria.items():
                if key == "client_id":
                    found = None 
                    for client in self.client:
                        if account.account_id in client.account:
                            if client.client_id == value:
                                found = True
                            break
                    if not found:
                        match = False
                        break
                elif key == "status":
                    if account.status != value:
                        match = False
                        break

                elif key == "account_type":
                    if not hasattr (account, 'account_type') or account.account_type !=value:
                        match = False
                        break
            
                elif key == "currency":
                    if account.currency != value:
                        match = False
                        break
            
            if match:
                results.append(account)
        
        if results:
            print(f"Найдено счетов: {len(results)}")
            for acc in results:
                client_id = "Неизвестно"
                for client in self.client:
                    if acc.account_id in client.account:
                        client_id = client.client_id
                        break
                print(f"  - Счёт {acc.account_id} (статус: {acc.status}, клиент: {client_id})")
        else:
            print("Счета не найдены")
        return results

    def get_total_balance (self):
        
        total = 0.0 
        active_account_count = 0
        for account in self.account:
        
            if account.status != "closed":
                total += account.account_balance
                active_account_count += 1   
        print (f"\nОбщий баланс банка {self.name}")
        print (f"Всего активных счетов {active_account_count}")
        print (f"Общая сумма средств {total}")

        return total
    
    def get_clients_ranking (self):
        
        client_balance = []
        
        for client in self.client:
            total_balance = 0.0
            
            for account in self.account:
                if (account.surname == client.surname and 
                    account.name == client.name and 
                    account.lastname == client.lastname and
                    account.status != "closed"):
                    total_balance += account.account_balance
        
            client_balance.append ((client, total_balance))
        sorted_clients = sorted(client_balance, key=lambda x: x[1], reverse=True)
        
        top_3 = sorted_clients[:3]

        print(f"\nРейтинг клиентов банка {self.name}")
        
        for position, (client, balance) in enumerate (top_3, 1):
            print(f"{position}. {client.surname} {client.name} (ID: {client.client_id}) | Баланс: {balance:.2f}")
        
        return top_3
                
    
if __name__ == "__main__":

    client1= Client (
    name= "Ivan",
    surname= "Ivanovich",
    lastname= "Ivanov",
    contact_number="+709134",
    birth_date= date(1998, 4, 15)
    
    )

    client2= Client (
        name= "Petr",
        surname= "Petrovich",
        lastname= "Petrov",
        contact_number="+709134",
        birth_date=date(1998, 4, 15)
    )
    client3= Client (
        name= "Semen",
        surname= "Lobanov",
        lastname= "Petrovich",
        contact_number="+709134",
        birth_date=date(1998, 4, 15)
    )
    bank = Bank ("VTB") 
    bank.add_client (client1)
    bank.add_client (client2)
    bank.add_client (client3)
    account1 = bank.open_account(client1, currency="RUB", account_type="premium", opening_balance=1000)
    account2 = bank.open_account(client2, currency="USD", account_type="savings", opening_balance=100)
    account3 = bank.open_account(client3, currency="USD", account_type="investment", opening_balance=100)

    print(f"\nСчёт: {account1.account_id[-4:]}")
    print(f"Баланс: {account1.account_balance} {account1.currency}")
    print(f"Владелец: {account1.surname} {account1.name}")
    print (client1.account)

    print(f"\nСчёт: {account2.account_id[-4:]}")
    print(f"Баланс: {account2.account_balance} {account2.currency}")
    print(f"Владелец: {account2.surname} {account2.name}")
    print (client2.account)

    print(f"\nСчёт: {account3.account_id[-4:]}")
    print(f"Баланс: {account3.account_balance} {account3.currency}")
    print(f"Владелец: {account3.surname} {account3.name}")
    print (client3.account)

#   заморозка/разморозка аккаунта
#    
    freeze = bank.freeze_account (client3,account3.account_id)
    unfreze = bank.unfreeze_account (client3,account3.account_id)

    # попытка входа 
    auth= bank.authenticate_client (client1, "pass1")
    auth= bank.authenticate_client (client1, "pass") 
    
    rank = bank.get_clients_ranking()
    total = bank.get_total_balance()


