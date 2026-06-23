from datetime import date
from day_3 import Bank, Client
from day_4 import TransactionProcessor, Transaction, TransactionQueue
from day_5 import AuditLog, RiskAnalyzer, AuditReports

# создание банка, клиентов, счетов
if __name__ == "__main__":
    bank = Bank ("VTB")

    client1= Client (
        name= "Ivan",
        surname= "Ivanov",
        lastname= "Ivanovich",
        contact_number="+79219998877",
        birth_date= date(1996, 5, 15)
        )
    bank.add_client (client1)
    account1 = bank.open_account(client1, currency="RUB", account_type="premium", opening_balance=10000)
    account2 = bank.open_account(client1, currency="RUB", account_type="standard", opening_balance=1000)

    client2= Client (
        name= "Petr",
        surname= "Petrov",
        lastname= "Petrovich",
        contact_number="+79219438756",
        birth_date=date(1991, 4, 19)
    )

    bank.add_client (client2)

    account3 = bank.open_account(client2, currency="RUB", account_type="savings", opening_balance=1000000)
    account4 = bank.open_account(client2, currency="RUB", account_type="standard", opening_balance=0)

    client3= Client (
        name= "Andrey",
        surname= "Andreev",
        lastname= "Andreevich",
        contact_number="+79116473419",
        birth_date=date(1988, 2, 15)
    )

    bank.add_client (client3)

    account5 = bank.open_account(client3, currency="RUB", account_type="Ivestment", opening_balance=1000)
    account6 = bank.open_account(client3, currency="RUB", account_type="standard", opening_balance=100)

    client4= Client (
        name= "Aleksandr",
        surname= "Sergeev",
        lastname= "Silvestrovich",
        contact_number="+79116473419",
        birth_date=date(1978, 9, 15)
    )

    bank.add_client (client4)

    account7 = bank.open_account(client4, currency="RUB", account_type="Premium", opening_balance=0)
    account8 = bank.open_account(client4, currency="RUB", account_type="Investment", opening_balance=100)

    client5= Client (
        name= "Semen",
        surname= "Labanov",
        lastname= "Andreevich",
        contact_number="+79116473419",
        birth_date=date(1964, 4, 21)
    )

    bank.add_client (client5)

    account9 = bank.open_account(client5, currency="RUB", account_type="Premium", opening_balance=1000)
    account10 = bank.open_account(client5, currency="RUB", account_type="Investment", opening_balance=100)

    client6= Client (
        name= "Boris",
        surname= "Levin",
        lastname= "Arkadievich",
        contact_number="+79116473419",
        birth_date=date(1981, 7, 15)
    )

    bank.add_client (client6)

    account11 = bank.open_account(client6, currency="RUB", account_type="standard", opening_balance=0)

    client7= Client (
        name= "Andrey",
        surname= "Bykov",
        lastname= "Evgenievich",
        contact_number="+79116473419",
        birth_date=date(1984, 5, 15)
    )

    bank.add_client (client7)

    account11 = bank.open_account(client7, currency="RUB", account_type="standard", opening_balance=0)

    # создание транзакций, ошибочные, заблокированные и обычные
    transactions = [
        Transaction("TX001", "internal", 5000, "RUB", account1, account2),
        Transaction("TX002", "internal", 10000, "RUB", account4, account2),
        Transaction("TX003", "internal", 3000, "RUB", account11, account5),
        Transaction("TX004", "internal", 15000, "RUB", account6, account4),
        Transaction("TX005", "internal", 7000, "RUB", account2, account3),
        Transaction("TX006", "internal", 15000, "RUB", account4, account6),
        Transaction("TX007", "external", 500000, "RUB", account3, account10),
        Transaction("TX008", "internal", 8000, "RUB", account2, account7),
        Transaction("TX009", "internal", 4000, "RUB", account8, account9),
        Transaction("TX010", "external", 300000, "RUB", account11, account4),
        Transaction("TX011", "external", 30, "RUB", account4, account7),
        Transaction("TX012", "external", 30, "RUB", account11, account3),
        Transaction("TX013", "external", 30, "RUB", account8, account11),
        Transaction("TX014", "external", 30, "RUB", account3, account5),
        Transaction("TX015", "external", 30, "RUB", account1, account4),
        Transaction("TX016", "external", 30, "RUB", account3, account9),
        Transaction("TX017", "external", 30, "RUB", account10, account9),
        Transaction("TX018", "external", 30, "RUB", account5, account4),
        Transaction("TX019", "external", 30, "RUB", account2, account1),
        Transaction("TX020", "external", 30, "RUB", account1, account2),
        Transaction("TX021", "external", 30, "RUB", account9, account4),
        Transaction("TX022", "external", 30, "RUB", account8, account5),
        Transaction("TX023", "external", 30, "RUB", account7, account1),
        Transaction("TX024", "external", 30, "RUB", account5, account2),
        Transaction("TX025", "external", 30, "RUB", account4, account8),
        Transaction("TX026", "external", 30, "RUB", account1, account5),
        Transaction("TX027", "external", 30, "RUB", account3, account7),
        Transaction("TX028", "external", 30, "RUB", account8, account2),
        Transaction("TX029", "external", 30, "RUB", account2, account3),
        Transaction("TX030", "external", 30, "RUB", account8, account10),
        Transaction("TX031", "external", 30, "RUB", account9, account11),
        Transaction("TX032", "external", 30, "RUB", account5, account1),
        Transaction("TX033", "external", 30, "RUB", account4, account6),
        Transaction("TX034", "external", 30, "RUB", account6, account9),
        Transaction("TX035", "external", 30, "RUB", account6, account11),
        Transaction("TX036", "external", 30, "RUB", account4, account11),
        Transaction("TX037", "external", 30, "RUB", account5, account7),
        Transaction("TX038", "external", 30, "RUB", account1, account4),
        Transaction("TX039", "external", 30, "RUB", account8, account4),
        Transaction("TX040", "external", 30, "RUB", account11, account4),
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
    queue.add_transaction(transactions[10], "high")
    queue.add_transaction(transactions[11], "medium")
    queue.add_transaction(transactions[12], "high")
    queue.add_transaction(transactions[13], "low")
    queue.add_transaction(transactions[14], "high")
    queue.add_transaction(transactions[15], "low")
    queue.add_transaction(transactions[16], "high")
    queue.add_transaction(transactions[17], "low")
    queue.add_transaction(transactions[18], "medium")
    queue.add_transaction(transactions[19], "high")
    queue.add_transaction(transactions[20], "medium")
    queue.add_transaction(transactions[21], "high")
    queue.add_transaction(transactions[22], "high")
    queue.add_transaction(transactions[23], "low")
    queue.add_transaction(transactions[24], "medium")
    queue.add_transaction(transactions[25], "low")
    queue.add_transaction(transactions[26], "high")
    queue.add_transaction(transactions[27], "medium")
    queue.add_transaction(transactions[28], "medium")
    queue.add_transaction(transactions[29], "low")
    queue.add_transaction(transactions[30], "medium")
    queue.add_transaction(transactions[31], "high")
    queue.add_transaction(transactions[32], "low")
    queue.add_transaction(transactions[33], "medium")
    queue.add_transaction(transactions[34], "high")
    queue.add_transaction(transactions[35], "low")
    queue.add_transaction(transactions[36], "medium")
    queue.add_transaction(transactions[37], "medium")
    queue.add_transaction(transactions[38], "low")
    queue.add_transaction(transactions[39], "high")

    print ("\n ДЕМОНСТРАЦИЯ ПОПАДАНИЯ В ОЧЕРЕДЬ, ИСПОЛНЕНИЯ, ОТКЛОНЕНИЯ")

    processor = TransactionProcessor()
    risk_analyzer = RiskAnalyzer()
    tx = queue.get_next()
    audit = AuditLog("audit.log")
    while tx is not None:
        print(f"\nОбработка: {tx.transaction_id}")
        print(f"  Сумма: {tx.transaction_amount} {tx.currency}")
        print(f"  Тип: {tx.type}")
        print(f"  От: {tx.sender.name} {tx.sender.surname}")
        print(f"  Кому: {tx.recipient.name} {tx.recipient.surname}")
        
        risk = risk_analyzer.analyze(tx, tx.sender)
        tx.risk_analysis = risk

        result = processor.process_transaction(tx)
        
        risk_analysis = getattr(tx, "risk_analysis", None)

        if tx.status == "blocked":
            audit.log(tx, "blocked", risk_analysis)
        elif result:
            audit.log(tx, "success", risk_analysis)
        else:
            audit.log(tx, "failed", risk_analysis)

        if result:
            print(f"  Результат: УСПЕШНО")
        else:
            print(f"  Результат: ОШИБКА - {tx.failure_reason}")
        
        tx = queue.get_next()

    print ("\n СЧЕТА КЛИЕНТОВ\n")

    for client in bank.client:
        if client.account:
            for acc_id in client.account:
                for acc in bank.account:
                    if acc.account_id == acc_id:
                        acc.get_account_info()
                        print()

    print ("\n ИСТОРИЯ ТРАНЗАКЦИЙ\n")
    if audit.log_entries:
        for entry in audit.log_entries:
            print(f"{entry[0]} | {entry[1]}")
            print(f"  {entry[5]} -> {entry[6]}")
            print(f"  Сумма: {entry[3]} {entry[4]}")
            print(f"  Статус: {entry[7]}")
            if entry[10]:
                print(f"  Причина: {entry[10]}")
            print()

    print ("\n ПОДОЗРИТЕЛЬНЫЕ ОПЕРАЦИИ")
    reports = AuditReports(audit)
    suspicious = reports.report_suspicious()

    print ("\n Отчеты")
    print ("\n ТОП - 3 клиента")
    ranking = bank.get_clients_ranking()
    print ("\n СТАТИСТИКА ТРАНЗАКЦИЙ\n")

    if audit.log_entries:
        total = len(audit.log_entries)
        success = 0
        failed = 0
        blocked = 0
        
        for entry in audit.log_entries:
            if entry[7] == "success":
                success += 1
            elif entry[7] == "failed":
                failed += 1
            elif entry[7] == "blocked":
                blocked += 1
        
        print("  Всего: " + str(total))
        print("  Успешно: " + str(success))
        print("  Ошибок: " + str(failed))
        print("  Заблокировано: " + str(blocked))
        
    print ("\n ОБЩИЙ БАЛАНС")
    total_balance = bank.get_total_balance ()