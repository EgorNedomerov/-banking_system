import json
import csv
import matplotlib.pyplot as plt
from datetime import date
from day_3 import Bank, Client
from day_4 import Transaction, TransactionProcessor
from day_5 import AuditLog

class ReportBuilder:
    def __init__(self, bank = None, audit_log = None, transaction = None):
        self.bank = bank
        self.audit_log = audit_log
        self.transaction = transaction or []
        self.reports = []

#   отчет по клиенту 

    def client_report (self, client):
        report = []
        for account in self.bank.account:
            if account.account_id in client.account:
                report.append ({
                    "client_id": client.client_id,
                    "client_name": f"{client.surname} {client.name} {client.lastname}",
                    "account_id": account.account_id,
                    "account_type": account.__class__.__name__,
                    "currency": account.currency,
                    "balance": account.account_balance,
                    "status": account.status
                    })
        return report

#   отчет по банку
 
    def bank_report (self):

        active_accounts = 0
        frozen_accounts = 0
        closed_accounts = 0
        total_balance = 0
        
        for account in self.bank.account:
            if account.status == "active":
                active_accounts += 1
            elif account.status == "frozen":
                frozen_accounts += 1
            elif account.status == "closed":
                closed_accounts += 1
            
            if account.status != "closed":
                total_balance += account.account_balance
        report = [
            {"index": "Название банка", "value": self.bank.name},
            {"index": "Количество клиентов", "value": len(self.bank.client)},
            {"index": "Количество счетов", "value": len(self.bank.account)},
            {"index": "Активные счета", "value": active_accounts},
            {"index": "Замороженные счета", "value": frozen_accounts},
            {"index": "Закрытые счета", "value": closed_accounts},
            {"index": "Общий баланс", "value": total_balance}  
                ]
        return report

#   отчет по рискам
    
    def risk_report (self):

        report = []
        for entry in self.audit_log.log_entries:
            report.append({
                "time": entry[0],
                "transaction_id": entry[1],
                "type": entry[2],
                "amount": entry[3],
                "currency": entry[4],
                "sender": entry[5],
                "recipient": entry[6],
                "status": entry[7],
                "importance": entry[8],
                "failure_reason": entry[10],
                "risk_score": entry[11],
                "risk_level": entry[12],
                "flags": entry[13]
                })
                
        return report
    
#   круговая диаграмма

    def pie_chart_accounts_status (self, filename = "accounts_status_pie.png"):
        
        active_accounts = 0
        frozen_accounts = 0
        closed_accounts = 0                               
        
        for account in self.bank.account:
            if account.status == "active":
                active_accounts += 1
            elif account.status == "frozen":
                frozen_accounts += 1
            elif account.status == "closed":
                closed_accounts += 1

        labels = []
        values = []
        
        if active_accounts > 0:
            labels.append("active")
            values.append(active_accounts)

        if frozen_accounts > 0:
            labels.append("frozen")
            values.append(frozen_accounts)

        if closed_accounts > 0:
            labels.append("closed")
            values.append(closed_accounts)

        plt.figure(figsize=(7, 7))
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title("Структура счетов по статусам")
        plt.savefig(filename)
        plt.close()

        print(f"Круговая диаграмма сохранена: {filename}")

#       столбчатая диаграмма

    def bar_chart_risk_level (self, filename = "risk_levels_bar.png"):
        
        low_count = 0
        medium_count = 0
        high_count = 0

        for entry in self.audit_log.log_entries:
            risk_level = entry[12]

            if risk_level == "low":
                low_count += 1
            elif risk_level == "medium":
                medium_count += 1
            elif risk_level == "high":
                high_count += 1

        labels = ["low", "medium", "high"]
        values = [low_count, medium_count, high_count]
 
        plt.figure(figsize=(8, 5))
        plt.bar(labels, values)
        plt.title("Количество операций по уровням риска")
        plt.xlabel("Уровень риска")
        plt.ylabel("Количество операций")
        plt.savefig(filename)
        plt.close()

        print(f"Столбчатая диаграмма сохранена: {filename}")

#   граф движения баланса

    def line_chart_balance (self, account, filename = "balance_line.png"):
        
        steps = list(range(len(account.balance_history)))
        balances = balances = account.balance_history

        plt.figure(figsize=(8, 5))
        plt.plot(steps, balances, marker="o")
        plt.title("Движение баланса счета")
        plt.xlabel("Операция")
        plt.ylabel("Баланс")
        plt.grid(True)
        plt.savefig(filename)
        plt.close()

        print(f"График движения баланса сохранен: {filename}")

#   сохранение диаграмм

    def save_charts (self, account):
        
        self.pie_chart_accounts_status(filename="accounts_status_pie.png")
        self.bar_chart_risk_level(filename="risk_levels_bar.png")
        self.line_chart_balance(account, filename="balance_line.png")

        print (f"Диаграммы сохранены")

    def print_report (self, report, title):
        
        print(f"\n{title}")

        if not report:
            print("Отчет пустой")
            return

        for row in report:
            for key, value in row.items():
                print(f"{key}: {value}")
                print("-" * 50)

#   экспорт в Json 

    def export_to_json (self, filename, report):
        with open (filename, "w", encoding="utf-8") as file:
            json.dump(report, file, ensure_ascii=False, indent=4)
    
#   экспорт в CSV

    def export_to_csv (self, filename, report):
        if not report:
            print (f"Отчет пустой, экспорт невозможен")
            return False
        
        headers = report [0]. keys ()
        
        with open (filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(report)

        return True
    
if __name__ == "__main__":
       
    bank = Bank ("VTB") 
    
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
    client4= Client (
        name= "Aleksandr",
        surname= "Sergeev",
        lastname= "Silvestrovich",
        contact_number="+79116473419",
        birth_date=date(1978, 9, 15)
    )

    client5= Client (
        name= "Semen",
        surname= "Labanov",
        lastname= "Andreevich",
        contact_number="+79116473419",
        birth_date=date(1964, 4, 21)
    )

    bank.add_client (client1)
    bank.add_client (client2)
    bank.add_client (client3)
    bank.add_client (client4)
    bank.add_client (client5)
    account1 = bank.open_account(client1, currency="RUB", account_type="premium", opening_balance=1000000)
    account2 = bank.open_account(client2, currency="USD", account_type="savings", opening_balance=100)
    account3 = bank.open_account(client3, currency="USD", account_type="investment", opening_balance=100)
    account4 = bank.open_account(client4, currency="RUB", account_type="Premium", opening_balance=0)
    account5 = bank.open_account(client5, currency="RUB", account_type="Premium", opening_balance=0)
    
    bank.close_account (client4, account4.account_id)
    bank.freeze_account (client5, account5.account_id)
    
    audit = AuditLog("my_audit.log")
    processor = TransactionProcessor()
    transactions = [
        Transaction("TX001", "external", 504, "RUB", account1, account2),
        Transaction("TX002", "internal", 105, "RUB", account1, account3),
        Transaction("TX003", "internal", 303, "RUB", account1, account3),
        Transaction("TX004", "internal", 150, "RUB", account1, account3),
        Transaction("TX005", "internal", 7000, "RUB", account1, account3),
        ]
    
    for transaction in transactions:

        result = processor.process_transaction(transaction)

        risk_analysis = getattr(transaction, "risk_analysis", None)
       
        if transaction.status == "blocked":
            audit.log(transaction, "blocked", risk_analysis)

        elif result:
            audit.log(transaction, "success", risk_analysis)

        else:
            audit.log(transaction, "failed", risk_analysis)

    report_builder = ReportBuilder(bank=bank,audit_log=audit,transaction=transaction)

    client_report = report_builder.client_report(client1)
    bank_report = report_builder.bank_report()
    risk_report = report_builder.risk_report()

    report_builder.print_report(client_report, "ОТЧЕТ ПО КЛИЕНТУ")
    report_builder.print_report(bank_report, "ОТЧЕТ ПО БАНКУ")
    report_builder.print_report(risk_report, "ОТЧЕТ ПО РИСКАМ")

    report_builder.export_to_json("client_report.json", client_report)
    report_builder.export_to_json("bank_report.json", bank_report)
    report_builder.export_to_json("risk_report.json", risk_report)

    report_builder.export_to_csv("client_report.csv", client_report)
    report_builder.export_to_csv("bank_report.csv", bank_report)
    report_builder.export_to_csv("risk_report.csv", risk_report)

    report_builder.save_charts (account1)