import json
from datetime import datetime
from day_4 import TransactionProcessor, Transaction
from day_2 import PremiumAccount, BankAccount, SavingsAccount, InvestmentAccount
class AuditLog:
    
    log_entries = []
    log_file: str
    IMPORTANCE_LEVELS = ["LOW","MEDIUM","HIGH"
    ]

    def __init__(self, log_file="audit.log"):
        self.log_entries = []
        self.log_file = log_file
    
    def log (self, transaction, status, risk_analysis = None):
         
        if status == "blocked":
            importance = "HIGH"
            importance_value = 3
        
        elif status == "failed":
            importance = "MEDIUM"
            importance_value = 2
        
        else:
            importance = "LOW"
            importance_value = 1


        entry = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            transaction.transaction_id,                   
            transaction.type,                              
            transaction.transaction_amount,                
            transaction.currency,                          
            f"{transaction.sender.surname} {transaction.sender.name}",  
            f"{transaction.recipient.surname} {transaction.recipient.name}",  
            status,                                       
            importance,                                    
            importance_value,                              
            transaction.failure_reason if transaction.failure_reason else "",  
            0.0,                                           
            "low",                                        
            []                                             
        ]
        
        if risk_analysis:
            
            entry[11] = risk_analysis[0]   
            entry[12] = risk_analysis[1]  
            entry[13] = risk_analysis[3] 
        
        self.log_entries.append(entry)
        return entry
    
    def filter_by_importance(self, importance):
        
        result = []
        for entry in self.log_entries:
            if entry[8] == importance: 
                result.append(entry)
        return result

    def save(self):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.log_entries, f, ensure_ascii=False, indent=2)

class RiskAnalyzer:
    
    LARGE_AMOUNT_THRESHOLD = 100000      
    MAX_OPERATIONS_PER_HOUR = 5     
    NIGHT_START = 00                    
    NIGHT_END = 6 

    def __init__(self):
        
        self. account_operations = []
        self.known_accounts = set ()
    

    def analyze (self, transaction, account):
        flags = []
        risk_score = 0.0

        if transaction.transaction_amount >= self.LARGE_AMOUNT_THRESHOLD:
           flags.append ("large_amount")
           risk_score += 0.4
        
        account_id = account.account_id
        now = datetime.now()

        recent_ops = []
            
        count_recent = 0
        for acc_id, op_time in self.account_operations:
            if acc_id == account_id and (now - op_time).total_seconds() < 3600:
                recent_ops.append(op_time)

        if len(recent_ops) >= self.MAX_OPERATIONS_PER_HOUR:
            risk_score += 0.4
            flags.append("frequent_operations")

        self.account_operations.append((account_id, now))

        recipient_id = transaction.recipient.account_id
        
        if recipient_id not in self.known_accounts:
            risk_score += 0.3
            flags.append("new_account")

        self.known_accounts.add(recipient_id)

        hour = now.hour
        if hour >= 23 or hour < 6:
            risk_score += 0.1
            flags.append("night_op")

        if transaction.type == "external":
            risk_score += 0.2
            flags.append("external")

        if risk_score >= 0.7:
            risk_level = "high"
            should_block = True
        elif risk_score >= 0.3:
            risk_level = "medium"
            should_block = False
        else:
            risk_level = "low"
            should_block = False

        return [risk_score, risk_level, should_block, flags]
    
#   метод блокировки транзакции при превышении значения риска

    def blocked_transaction(self, transaction, account, processor, audit_log):
        
        risk_result = self.analyze(transaction, account)
        
        if risk_result[2]:  
            transaction.status = "failed"
            transaction.failure_reason = f"Блокировка: {', '.join(risk_result[3])}"
            audit_log.log(transaction, "blocked", risk_result)
            print (f"Транзакция заблокирована {transaction.transaction_id}")
            return False
        
        result = processor.process_transaction(transaction)

        if result:
            audit_log.log(transaction, "success", risk_result)
        else:
            audit_log.log(transaction, "failed", risk_result)
        
        return result


class AuditReports:
    
    def __init__(self, audit_log):
        self.log = audit_log.log_entries

#   отчет по подозрительным операциям

    def report_suspicious(self):
        
        suspicious = []
        
        for entry in self.log:
            risk_level = entry[12]

            if risk_level in ['high', 'medium']:
                suspicious.append({
                    'id': entry[1],
                    'отправитель': entry[5],
                    'получатель': entry[6],
                    'сумма': entry[3],
                    'валюта': entry[4],
                    'статус': entry[7],
                    'риск': risk_level,
                    'флаги': entry[13] if len(entry) > 13 else []
                })

        for op in suspicious:
            print(f"ID: {op['id']}")
            print(f"  {op['отправитель']} -> {op['получатель']}")
            print(f"  Сумма: {op['сумма']} {op['валюта']}")
            print(f"  Статус: {op['статус']}, Риск: {op['риск']}")
            if op['флаги']:
                print(f"  Флаги: {', '.join(op['флаги'])}")
            print()
        
        return suspicious

#   риск профиль клиента

    def report_client_risk(self, client_name=None):
        
        clients_name = []
        clients_transaction = []
        clients_high_risk = []
        clients_medium_risk = []
        clients_blocked = []
        clients_failed = []
        
        for entry in self.log:
            sender = entry[5]

            if client_name is not None and client_name not in sender:
                continue
        
            found = False 
            for i in range (len(clients_name)):
                
                if clients_name [i] == sender:
                    found  = True
                    clients_transaction [i] += 1

                    risk = entry [12]
                    
                    if risk == "high":
                        clients_high_risk[i] +=1
                    
                    elif risk  == "medium":
                        clients_medium_risk [i] += 1
                    
                    if entry [7] == "blocked":
                        clients_blocked [i] += 1
                    
                    elif entry [7] == "failed":
                        clients_failed [i] +=1
                    
                    break    
                
            if not found:
                
                clients_name.append (sender)
                clients_transaction.append (1)

                risk = entry [12]
                
                if risk == "high":
                    clients_high_risk.append (1)
                    clients_medium_risk.append (0)
                
                elif risk  == "medium":
                    clients_high_risk.append (0)
                    clients_medium_risk.append (1)
                
                else:
                    clients_high_risk.append (0)
                    clients_medium_risk.append (0)
            
                if entry [7] == "blocked":
                    
                    clients_blocked.append (1)
                    clients_failed.append (0)
                
                elif entry [7] == "failed":
                    
                    clients_blocked.append (0)
                    clients_failed.append (1)
                
                else:
                    
                    clients_blocked.append (0)
                    clients_failed.append (0)

        for i in range(len(clients_name)):

            print(f"\nКлиент: {clients_name[i]}")
            print(f"  Всего операций: {clients_transaction[i]}")
            print(f"  Высокий риск: {clients_high_risk[i]}")
            print(f"  Средний риск: {clients_medium_risk[i]}")
            print(f"  Заблокировано: {clients_blocked[i]}")
            print(f"  Ошибок: {clients_failed[i]}")
        
        return [clients_name, clients_transaction, clients_high_risk, 
                clients_medium_risk, clients_blocked, clients_failed]

#   статистика ошибок 

    def report_statistics (self):
        total = len(self.log)
        success = 0
        failed = 0
        blocked = 0
        
        error_reasons = []
        error_counts = []

        for entry in self.log:
            status = entry [7]

            if status == "success":
                success += 1
            elif status == "failed":
                failed += 1
                reason = entry [10] if entry [10] else "Неизвестная ошибка"

                found = False 
                for i in range(len (error_reasons)):
                    if error_reasons[i] == reason:
                        error_counts[i] += 1
                        found = True
                        break

                if not found:
                    error_reasons.append(reason)
                    error_counts.append(1)

            elif status == 'blocked':
                blocked += 1
                reason = entry[10] if entry[10] else 'Заблокировано системой'
                
                found = False
                for i in range(len(error_reasons)):
                    if error_reasons[i] == reason:
                        error_counts[i] += 1
                        found = True
                        break
                
                if not found:
                    error_reasons.append(reason)
                    error_counts.append(1)
        
        success_rate = 0
        if total > 0:
            success_rate = round((success / total) * 100, 2)

        if len(error_reasons) > 0:
            print("\n Причины ошибок:")
            for i in range(len(error_reasons)):
                print(f"  {error_reasons[i]}: {error_counts[i]}")

        return [total, success, failed, blocked, success_rate, error_reasons, error_counts]

# audit = AuditLog("my_audit.log")

# risk_analyzer = RiskAnalyzer()
# processor = TransactionProcessor()

# sender1 = PremiumAccount (None, "Ivan", "Ivanovich", "Ivanov", 500000, "active", "RUB")
# recipient_premium = PremiumAccount (None, "Petr", "Petrovich", "Petrov", 100000, "active", "RUB")

# tx = Transaction ("TX000", "internal", 14, "RUB", sender1,recipient_premium )
# tx1 = Transaction ("TX001", "internal", 30000, "RUB", sender1, recipient_premium)
# tx2 = Transaction ("TX002", "external", 500000, "RUB", sender1, recipient_premium)
# tx3 = Transaction ("TX003", "internal", 10, "RUB", sender1, recipient_premium)
# tx4 = Transaction ("TX004", "internal", 10, "RUB", sender1, recipient_premium)
# tx5 = Transaction ("TX005", "internal", 10, "RUB", sender1, recipient_premium)

# result1 = risk_analyzer.blocked_transaction(tx,  sender1, processor, audit)
# result2 = risk_analyzer.blocked_transaction(tx1, sender1, processor, audit)
# result3 = risk_analyzer.blocked_transaction(tx2, sender1, processor, audit)
# result4 = risk_analyzer.blocked_transaction(tx3, sender1, processor, audit)
# result5 = risk_analyzer.blocked_transaction(tx4, sender1, processor, audit)
# result6 = risk_analyzer.blocked_transaction(tx5, sender1, processor, audit)

# # отчеты аудита
# reports = AuditReports(audit)
# suspicious = reports.report_suspicious() 
# clients_data = reports.report_client_risk()
# stats = reports.report_statistics()

# #  сохранение в файл
# audit.save()