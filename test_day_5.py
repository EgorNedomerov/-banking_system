from day_2 import PremiumAccount
from day_4 import Transaction, TransactionProcessor
from day_5 import  AuditLog, AuditReports

audit = AuditLog("my_audit.log")

processor = TransactionProcessor()

sender1 = PremiumAccount (None, "Ivan", "Ivanovich", "Ivanov", 500000, "active", "RUB")
recipient_premium = PremiumAccount (None, "Petr", "Petrovich", "Petrov", 100000, "active", "RUB")
transactions = [
    Transaction("TX000", "internal", 140000, "RUB", sender1, recipient_premium),
    Transaction("TX001", "internal", 3000, "RUB", sender1, recipient_premium),
    Transaction("TX002", "external", 500000, "RUB", sender1, recipient_premium),
    Transaction("TX003", "internal", 10, "RUB", sender1, recipient_premium),
    Transaction("TX004", "internal", 10, "RUB", sender1, recipient_premium),
    Transaction("TX005", "internal", 10, "RUB", sender1, recipient_premium),
]

for transaction in transactions:
    print(f"\nОбработка транзакции {transaction.transaction_id}")

    result = processor.process_transaction(transaction)

    if transaction.status == "blocked":
        audit.log(transaction, "blocked")
        print(f"Транзакция заблокирована: {transaction.failure_reason}")

    elif result:
        audit.log(transaction, "success")
        print("Транзакция выполнена успешно")

    else:
        audit.log(transaction, "failed")
        print(f"Транзакция не выполнена: {transaction.failure_reason}")

# отчеты аудита
reports = AuditReports(audit)
suspicious = reports.report_suspicious() 
clients_data = reports.report_client_risk()
stats = reports.report_statistics()

#  сохранение в файл
audit.save()