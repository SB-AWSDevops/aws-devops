import random  # Random transaction amount & type select cheyyataniki
from faker import Faker  # Random dates generate cheyyataniki

# Faker instance create cheyyali
fake = Faker()

# Generate 100+ transactions for 20 users
transactions = []
for user_id in range(1, 21):  # 20 Users
    balance = 10000  # Starting balance
    for _ in range(5):  # Each user ki 5 transactions generate cheyyali
        date = fake.date_this_year()  # Random transaction date
        transaction_type = random.choice(["Deposit", "Withdrawal"])
        amount = random.randint(500, 5000)  # Transaction amount
        
        # Balance calculation
        if transaction_type == "Withdrawal" and balance - amount < 0:
            continue  # Negative balance avoid cheyyataniki

        balance = balance + amount if transaction_type == "Deposit" else balance - amount

        # Insert Query Format
        transactions.append(f"({user_id}, '{date}', '{transaction_type}', {amount}, {balance})")

# SQL Queries Save to File
with open("../data/transactions.sql", "w") as f:
    f.write("INSERT INTO transactions (user_id, date, transaction_type, amount, balance) VALUES\n")
    f.write(",\n".join(transactions) + ";\n")

print("✅ SQL Data File Generated: data/transactions.sql")
