from datetime import date, datetime
class Client:
    ALLOWED_STATUS = ['active', 'frozen', 'closed']

    def __init__(self, client_id, name, surname, lastname, contact_number, birth_date):
        
        #   валидация возраста

            today = date.today ()
            age = today.year - birth_date.year
            
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
            if age < 18:
                 raise ValueError ("Невозможно создать аккаунт. Клиент должен быть старше 18 лет.")
            
            self.name = name

            self.surname = surname

            self.lastname = lastname

            self.client_id = client_id

            self.contact_number = contact_number

            self.birth_date = birth_date
            
            self.status = "active"
            
            self.failed_attempts = 0

            self. is_blocked = False

            self.suspicious_activities = []

class Bank:
    
    def __init__(self, name):
        
        self.name = name
        self.client= {}
        self.account= {}
        self.account_counter = 0
    
    #  метод генерации номера счета

    def generate_account_number(self):
        self.account_counter += 1
        return self.account_counter
    
    def add_client (self, client):

        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Добавление клиента невозможно с 00:00 до 05:00")
        
        if client.client_id in self.client:
            print(f"Клиент с ID {client.client_id} уже существует")
            return False
        
        self.client[client.client_id] = client

        print(f"Клиент {client.surname} {client.name} (ID: {client.client_id}) добавлен")

#   метод создания аккаунта

    def open_account(self, client, currency = "RUB", account_type = "standart"):
         
        if client.client_id not in self.client:
            raise ValueError ("Клиент не найден")  
        
        if self.client[client.client_id] is not client:
            raise ValueError("Клиент не зарегистрирован в банке")

        if client.status!= "active":
              raise ValueError ("У клиента нет активного аккаунта")
        
        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Создание счета невозможно с 00:00 до 05:00")
        
        account_number = self.generate_account_number ()
        
        status = "active"
        
        account_info ={
             "account_number": account_number,
             "client_id": client.client_id,
             "status": status,
             "currency": "RUB",
             "account_type": account_type,
             "balance": 0.0
        }
        
        self.account[account_number] = account_info

        print (f"Создан счет {account_number}. Клиент {client.name} {client.surname}")
        return account_number

#   метод закрытия аккаунта   

    def close_account (self, client_id, account_number):
        
        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Закрыть счет невозможно с 00:00 до 05:00")
        
        if client_id not in self.client:
            print(f"Клиент {client_id} не найден")
            return False
            
        client = self.client[client_id]

        if account_number not in self.account:
            print (f"Счет {account_number} не найден")
            return False
        
        account = self.account [account_number]
        
        if account["client_id"] != client_id:
            print(f"Счет {account_number} не принадлежит клиенту")
            return False


        if account["status"] == "closed":
            print(f"Счет {account_number} уже закрыт")
            return False
        
        account["status"] = "closed"
        print(f"Счет {account_number} закрыт. Клиент {client.name} {client.surname}")
        return True

#   метод заморозки акканута
  
    def freeze_account (self, client_id, account_number):
        

        if client_id not in self.client:
            print (f"Клиент {client_id} не найден")
            
        client = self.client[client_id]
        
        if account_number not in self.account:
            print (f"Счет {account_number} не найден")
            return False
        
        account = self.account [account_number]

        if account["client_id"] != client_id:
            print (f"Счет {account_number} не принадлежит клиенту")
            return False
        
        if account ["status"] == "closed":
            print (f"Счет {account_number} уже закрыт")
            return False
        
        if account ["status"] == "frozen":
            print (f"Счет {account_number} уже заморожен")
            return False
        
        account ["status"] = "frozen"
        print (f"Счет {account_number} заморожен. Клиент {client.name} {client.surname}")
        return True
    
#   метод разморозки аккаунта 

    def unfreeze_account (self, client_id, account_number):
        
        now = datetime.now()
        if 0 <= now.hour < 5:
            raise ValueError (f"Операция запрещена. Разблокировать Счет невозможно с 00:00 до 05:00")

        if client_id not in self.client:
            print (f"Клиент {client_id} не найден")
            
        client = self.client[client_id]
        
        if account_number not in self.account:
            print (f"Счет {account_number} не найден")
            return False
        
        account = self.account [account_number]
        
        if account["client_id"] != client_id:
            print (f"Счет {account_number} не принадлежит клиенту")
            return False
        
        if account ["status"] == "closed":
            print ("Ошибка. Счет закрыт")
            return False

        if account ["status"] != "frozen":
            print (f"Счет не заморожен. Актуальный статус: {account["status"]}")
            return False        
        account ["status"] = "active"
        print (f"Счет {account_number} разморожен. Клиент {client.name} {client.surname}")
        return True
    
    def authenticate_client (self, client_id, password):
        
        if client_id not in self.client:
            print(f"Клиент с ID {client_id} не найден")
            return None
        
        client = self.client[client_id]
        
        if client.status != "active":
            print(f"Клиент {client.name} {client.surname} не активен. Статус: {client.status}")
            return None
        
        if password == f"pass_{client_id}": 
            client.failed_attempts = 0 
            print(f"Клиент {client.name} {client.surname} (ID: {client_id}) успешно аутентифицирован")
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

        for account_number, account_info in self.account.items():
            match = True

            for key, value in criteria.items():
                if key == "client_id":
                    if account_info["client_id"] != value:
                        match = False
                        break

                elif key == "status":
                    if account_info["status"] != value:
                        match = False
                        break

                elif key == "account_type":
                    if account_info.get("account_type") != value:
                        match = False
                        break
            
                elif key == "currency":
                    if account_info.get("currency") != value:
                        match = False
                        break
            
            if match:
                results.append(account_info)
        
        if results:
            print(f"Найдено счетов: {len(results)}")
            for acc in results:
                print(f"  - Счет {['account_number']} (статус: {['status']}, клиент: {['client_id']})")
        else:
            print("Счета не найдены")
    
        return results

    def get_total_balance (self):
        
        total = 0.0 
        active_account_count = 0
        for account_info in self.account.values():
        
            if account_info["status"] != "closed":
                total += account_info.get("balance", 0)
                active_account_count += 1   
        print (f"Общий баланс банка {self.name}")
        print (f"Всего активных счетов {active_account_count}")
        print (f"Общая сумма средств {total}")

    def get_clients_ranking (self):
        
        client_balance = {}
        
        for account_info in self.account.values():
            client_id = account_info["client_id"]
            balance = account_info.get("balance", 0)

            if account_info ["status"] != "closed":
                if client_id in client_balance:
                    client_balance [client_id] += balance
                else:
                    client_balance [client_id] = balance

        for client_id in self.client.keys():
            if client_id not in client_balance:
                client_balance [client_id] = 0.0

        sorted_clients = sorted (client_balance.items(), key=lambda x: x[1], reverse=True)

        for position, (client_id, balance) in enumerate(sorted_clients, 1):
            client = self.client.get(client_id)
            
            if client:
                client_name = f"{client.name} {client.surname}"

                print(f"{position}. ID: {client_id} | {client_name} | Баланс: {balance:.2f} ₽")
            else:
                print(f"{position}. ID: {client_id} | Баланс: {balance:.2f} ₽")

        return [client_id for client_id in sorted_clients]
    

client1 = Client ("1", "Ivan", "Ivanov", "Ivanovich", "+709134", date(1998 , 4, 15))
client2 = Client ("2", "Petr", "Petrov", "Petrovich", "+709134", date(2000 , 8, 17))
bank = Bank ("VTB") 
# создание клиентов
bank.add_client (client1)
bank.add_client (client2)

# открытие счетов 
bank.open_account(client1)
bank.open_account(client2)

# попытка входа 
bank.authenticate_client (1, "pass_1")
# заморозка счета
bank.freeze_account (1, 1)

# ac1 = bank.open_account(client1)
# ac2 = bank.open_account(client2)
# bank.account[ac1]["balance"] = 5000   
# bank.account[ac2]["balance"] = 15000 
# ranking = bank.get_clients_ranking()
