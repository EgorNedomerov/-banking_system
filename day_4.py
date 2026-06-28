from datetime import datetime, timedelta
from day_2 import PremiumAccount, SavingsAccount, InvestmentAccount
from day_1 import BankAccount
from day_5 import RiskAnalyzer
from exception import InvalidOperationError
class Transaction:
    def __init__(self, transaction_id, type, transaction_amount, currency, sender, recipient):
        self.transaction_id = transaction_id
        self.type = type
        self.transaction_amount = transaction_amount
        self.currency = currency
        self.comission = 0.0 
        self.sender = sender
        self.recipient = recipient
        self.status = "pending"
        self.failure_reason = None
        self.created_transaction = datetime.now ()
    
    #   метод расчета комиссии
    
    def CalculateComission (self, external = False):
        
        if isinstance (self.sender, PremiumAccount):
            percent = 0
        
        elif isinstance (self.sender, InvestmentAccount):
            percent = 0.5
        
        elif isinstance (self.sender, SavingsAccount):
            percent = 1
        
        else:
            percent = 1.5
        
        if external:
            percent += 1
            print (f"Перевод в другой банк, комиссия 1%")

        comission = self.transaction_amount * (percent/100)

        return comission
    
    # метод валидации транзакции

    def ValidateTransaction(self):
        
        if self.sender.status == "frozen":
            print (f"Создание транзакции невозможно, счет {self.sender.status}")
            return False
        
        if self.recipient.status == "frozen":
            print (f"Создание транзакции невозможно, счет {self.recipient.status}")
            return False
        
        if self.transaction_amount <=0:
            return False
        
        self.comission = self.CalculateComission (external=False)

        total_cost = self.transaction_amount + self.comission

        if isinstance (self.sender, PremiumAccount):
            available = self.sender.account_balance + self.sender.OVERDRAFT_LIMIT
            if total_cost > available:
                print (f"Недостаточно средств. Транзакция невозможна.")
                return False
        else:
            if total_cost> self.sender.account_balance:
               print (f"Недостаточно средств. Транзакция невозможна.")
               return False
                     
        return True
    
class TransactionQueue:
    
    def __init__(self):
        
        self.high_queue = []
        self.medium_queue = []
        self.low_queue = []
        
        self.pending = [] 
        self.processed = []

        self.total_added = 0
        self.total_cancelled = 0
        self.total_processed = 0

#   метод добавления тразакции

    def add_transaction (self, transaction, priority):
        
        if priority not in ["high", "medium", "low"]:
            print(f"Ошибка! Неправильный приоритет: {priority}")
            return False
        
        if self._find_transaction(transaction.transaction_id) is not None:
            print(f"Транзакция {transaction.transaction_id} уже есть в очереди")
            return False
        
        if priority == "high":
            self.high_queue.append(transaction)
        elif priority == "medium":
            self.medium_queue.append(transaction)    
        elif priority == "low":
            self.low_queue.append(transaction)

        self.total_added = self.total_added + 1
        return True
    
#   метод добавления транзакции с высоким приоритетом

    def add_high_priority(self, transaction):
        return self.add_transaction(transaction, "high")
    
#   метод добавления транзакции со средним приоритетом 

    def add_medium_priority(self, transaction):
        return self.add_transaction(transaction, "medium")
    
#   метод добавления транзакции с низким приоритетом

    def add_low_priority(self, transaction):
        return self.add_transaction(transaction, "low")

#   метод добавления отложенной транзакции 
    
    def add_delayed_transaction(self, transaction, delay_hours, priority):
        
        process_time = datetime.now() + timedelta(hours=delay_hours) 

        self.pending.append({
            "transaction": transaction,
            "priority": priority,
            "process_after": process_time
        })
        return True

#   метод получения следующей транзакции

    def get_next(self):
        now = datetime.now()
        
        for i in range(len(self.pending)):
            pending_item = self.pending[i]

            if pending_item["process_after"] <= now:
                transaction = pending_item["transaction"]
                priority = pending_item["priority"]    

                self.pending.pop(i)

                if priority == "high":
                    self.high_queue.append(transaction)
                elif priority == "medium":
                    self.medium_queue.append(transaction)
                else:
                    self.low_queue.append(transaction)
                break

        if len(self.high_queue) > 0:
            next_transaction = self.high_queue.pop(0)
            return next_transaction 
        
        if len(self.medium_queue) > 0:
            next_transaction = self.medium_queue.pop(0)
            return next_transaction
        
        if len(self.low_queue) > 0:
            next_transaction = self.low_queue.pop(0)
            return next_transaction
        return None
    
#   метод поиска транзакции
 
    def _find_transaction(self, transaction_id):
  
        for transaction in self.high_queue:
            if transaction.transaction_id == transaction_id:
                return transaction
    
        for transaction in self.medium_queue:
            if transaction.transaction_id == transaction_id:
                return transaction
    
        for transaction in self.low_queue:
            if transaction.transaction_id == transaction_id:
                return transaction

        for item in self.pending:
            if item["transaction"].transaction_id == transaction_id:
                return item["transaction"]
    
        return None
    
#   метод отмены транзакции
 
    def cancel_transaction(self, transaction_id):

        for i in range(len(self.high_queue)):
            if self.high_queue[i].transaction_id == transaction_id:
                transaction = self.high_queue.pop(i)
                transaction.status = "cancelled"
                transaction.failure_reason = "Отменена пользователем"
                self.processed.append(transaction)
                self.total_cancelled = self.total_cancelled + 1
                print(f"Транзакция {transaction_id} отменена (HIGH очередь)")
                return True 

        for i in range(len(self.medium_queue)):
            if self.medium_queue[i].transaction_id == transaction_id:
                transaction = self.medium_queue.pop(i)
                transaction.status = "cancelled"
                transaction.failure_reason = "Отменена пользователем"
                self.processed.append(transaction)
                self.total_cancelled = self.total_cancelled + 1
                print(f"Транзакция {transaction_id} отменена (MEDIUM очередь)")
                return True
        
        for i in range(len(self.low_queue)):
            if self.low_queue[i].transaction_id == transaction_id:
                transaction = self.low_queue.pop(i)
                transaction.status = "cancelled"
                transaction.failure_reason = "Отменена пользователем"
                self.processed.append(transaction)
                self.total_cancelled = self.total_cancelled + 1
                print(f"Транзакция {transaction_id} отменена (LOW очередь)")
                return True
        
        for i in range(len(self.pending)):
            if self.pending[i]["transaction"].transaction_id == transaction_id:
                item = self.pending.pop(i)
                transaction = item["transaction"]
                transaction.status = "cancelled"
                transaction.failure_reason = "Отменена пользователем"
                self.processed.append(transaction)
                self.total_cancelled = self.total_cancelled + 1
                print(f"Отложенная транзакция {transaction_id} отменена")
                return True
        
        print(f"Транзакция {transaction_id} не найдена")
        return False

class TransactionProcessor:
     
    def __init__(self, risk_analyzer = None):
        self.exchange_rates = {
            'RUB': 1.0,
            'USD': 90.0,
            'EUR': 100.0,
            'KZT': 0.2,
            'CNY': 12.5
        }
        self.max_retries = 3
        self.error_log = []
        self.risk_analyzer = risk_analyzer or RiskAnalyzer ()
        self.total_processed = 0
        self.total_success = 0
        self.total_failed = 0
        self.total_retried = 0

#   метод обработки транзакций 

    def process_transaction(self, transaction):
        
        if transaction.status == "completed":
            print(f"Транзакция {transaction.transaction_id} уже выполнена")
            return True
        
        if transaction.status == "failed":
            print(f"Транзакция {transaction.transaction_id} уже была неудачной")
            return False

        sender = transaction.sender
        recipient = transaction.recipient
      
    #   перенес сюда анализ риска, т.к в комментарии сказано, что риск-анализ не связан с Bank или общей обработкой транзакций
      
        risk_result = self.risk_analyzer.analyze (transaction, sender)
        transaction.risk_analysis = risk_result    
        
        if risk_result[2]: 
            transaction.status = "blocked"
            transaction.failure_reason = f"ЗАБЛОКИРОВАНО: {risk_result[1]}"

            return False

        if sender.status == "frozen":
            error_msg = "Счет отправителя заморожен"
            self._log_error(transaction, error_msg)
            return False
        
        if recipient.status == "frozen":
            error_msg = "Счет получателя заморожен"
            self._log_error(transaction, error_msg)
            return False
        
        if sender.status == "closed":
            error_msg = "Счет отправителя закрыт"
            self._log_error(transaction, error_msg)
            return False
        
        if recipient.status == "closed":
            error_msg = "Счет получателя закрыт"
            self._log_error(transaction, error_msg)
            return False
        
        is_external = (transaction.type == "external")
        transaction.comission = transaction.CalculateComission(external=is_external)

#       переписал логику конвертации валюты транзакции
 
        base_currency = transaction.currency
        amount = transaction.transaction_amount

        sender_amount = self._convert_currency(
            amount,
            base_currency,
            sender.currency
            )

        recipient_amount = self._convert_currency(
                amount,
                base_currency,
                recipient.currency
                )

        total_cost = sender_amount + transaction.comission

        if isinstance(sender, SavingsAccount):
            if sender.account_balance - total_cost < sender.MIN_BALANCE:
                error_msg = f"Недостаточно средств. Минимальный остаток: {sender.MIN_BALANCE}"
                self._log_error(transaction, error_msg)
                return False
        
        if isinstance(sender, PremiumAccount):
            available = sender.account_balance + sender.OVERDRAFT_LIMIT
            if total_cost > available:
                error_msg = f"Недостаточно средств. Доступно: {available}, нужно: {total_cost}"
                self._log_error(transaction, error_msg)
                return False
        
        else:
            if total_cost > sender.account_balance:
                error_msg = f"Недостаточно средств. Баланс: {sender.account_balance}, нужно: {total_cost}"
                self._log_error(transaction, error_msg)
                return False
            
    #   добавил проверку превышения максимального лимита 
             
        if recipient.account_balance + recipient_amount > recipient.MAX_LIMIT:
            self._log_error(transaction, "Превышен лимит получателя")
            return False

        self._execute_balance_change(sender, recipient, sender_amount, recipient_amount)

        print(f"  Баланс получателя: {recipient.account_balance}")

        transaction.status = "completed"
        transaction.completed_at = datetime.now()

        self.total_success += 1
        self.total_processed += 1
        return True
    
#   метод обработки транзакции с повторными ошибками 

    def process_with_retry(self, transaction):
        
        for attempt in range(1, self.max_retries + 1):
            print(f"Попытка {attempt} из {self.max_retries}")
            
            result = self.process_transaction(transaction)
            
            if result:
                return True
            
            if attempt < self.max_retries:
                print(f"Будет выполнена повторная попытка...")
                self.total_retried += 1
        
        print(f"Транзакция не удалась после {self.max_retries} попыток")
        self.total_failed += 1
        return False
    
#   метод конвертации валют 
 
    def _convert_currency(self, amount, from_currency, to_currency):
        
        if from_currency == to_currency:
            return amount
        
        if from_currency not in self.exchange_rates:
            print(f" Неизвестная валюта: {from_currency}")
            return amount
        
        if to_currency not in self.exchange_rates:
            print(f"Неизвестная валюта: {to_currency}")
            return amount
        
        amount_in_rub = amount * self.exchange_rates [from_currency]
        converted = amount_in_rub / self.exchange_rates [to_currency]
        
        return converted
    
#   метод изменения баланса в транзакции

    def _execute_balance_change (self, sender, recipient, sender_amount, recipient_amount):
        sender.withdraw(sender_amount)
        recipient.deposit(recipient_amount)

#   метод логирования ошибок 

    def _log_error(self, transaction, error_message):

        transaction.status = "failed"
        transaction.failure_reason = error_message
        
        error_record = {
            'time': datetime.now(),
            'transaction_id': transaction.transaction_id,
            'type': transaction.type,
            'amount': transaction.transaction_amount,
            'currency': transaction.currency,
            'sender': f"{transaction.sender.surname} {transaction.sender.name}",
            'recipient': f"{transaction.recipient.surname} {transaction.recipient.name}",
            'error': error_message
        }
        self.error_log.append(error_record)
         
if __name__ == "__main__":

    premium_sender_acc = PremiumAccount (None, "Ivan", "Ivanovich", "Ivanov", 4_500_000, "active", "RUB")
    def_recipient_acc = PremiumAccount (None, "Petr", "Petrovich", "Petrov", 4_000_000, "active", "RUB")
    recipient_acc = BankAccount (None, "Andrey", "Andreev", "Andreevich", 3000, "active", "RUB")
    transactions = [
        Transaction("TX001", "internal", 3_000_000, "RUB", premium_sender_acc, recipient_acc),
        Transaction("TX002", "internal", 10, "RUB", premium_sender_acc, def_recipient_acc),
        Transaction("TX003", "internal", 30, "RUB", premium_sender_acc, recipient_acc),
        
        
        Transaction("TX004", "external", 1500, "RUB", premium_sender_acc, def_recipient_acc),
        Transaction("TX005", "external", 7000, "RUB", premium_sender_acc, recipient_acc),
        

        Transaction("TX006", "internal", 15000, "RUB", premium_sender_acc, def_recipient_acc),
        

        Transaction("TX007", "external", 1_000_000, "RUB", def_recipient_acc, premium_sender_acc),
        

        Transaction("TX008", "internal", 1_000_000, "RUB", def_recipient_acc, premium_sender_acc),
        Transaction("TX009", "internal", 4000, "RUB", premium_sender_acc, recipient_acc),
        
    
        Transaction("TX010", "external", 3000000, "RUB", premium_sender_acc, def_recipient_acc),
    ]

    queue = TransactionQueue()

    queue.add_transaction(transactions[0], "high")
    queue.add_transaction(transactions[1], "high")
    queue.add_transaction(transactions[2], "medium")
    queue.add_transaction(transactions[3], "high")
    queue.add_transaction(transactions[4], "medium")
    queue.add_transaction(transactions[5], "medium")
    queue.add_transaction(transactions[6], "high")
    queue.add_transaction(transactions[7], "low")
    queue.add_transaction(transactions[8], "low")
    queue.add_transaction(transactions[9], "high")

    processor = TransactionProcessor()
    tx = queue.get_next()
    while tx is not None:
        print(f"\nОбработка: {tx.transaction_id}")
        print(f"  Сумма: {tx.transaction_amount} {tx.currency}")
        print(f"  Тип: {tx.type}")
        print(f"  От: {tx.sender.name} {tx.sender.surname}")
        print(f"  Кому: {tx.recipient.name} {tx.recipient.surname}")
        
        result = processor.process_transaction(tx)
        
        if result:
            print(f"  Результат: УСПЕШНО")
        else:
            print(f"  Результат: ОШИБКА - {tx.failure_reason}")
        
        tx = queue.get_next()


