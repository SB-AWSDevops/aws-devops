import pandas as pd  # CSV file create cheyyataniki
from faker import Faker  # Dummy data generate cheyyataniki
import random  # Random transaction amounts generate cheyyataniki
import os  # Folder create cheyyataniki

# Fake data generate cheyyataniki Faker instance create cheyyali
fake = Faker()

# Output folder
output_folder = "../data/customer-statements/"
os.makedirs(output_folder, exist_ok=True)  # Folder create if not exists

# 20 users ki transaction data generate cheyyadam
for user_id in range(1, 21):
    transactions = []
    balance = 10000  # Starting balance

    for _ in range(5):  # Each user ki 5 transactions
        date = fake.date_this_year()  # Random recent date generate chesthadi
        transaction_type = random.choice(["Deposit", "Withdrawal"])
        amount = random.randint(500, 5000)  # Random amount generate chesthadi

        # Balance calculation
        if transaction_type == "Withdrawal" and balance - amount < 0:
            continue  # Negative balance avoid cheyyataniki

        balance = balance + amount if transaction_type == "Deposit" else balance - amount

        # Append transaction details
        transactions.append([date, transaction_type, amount, balance])

    # DataFrame create cheyyali
    df = pd.DataFrame(transactions, columns=["Date", "Transaction Type", "Amount", "Balance"])

    # CSV file save cheyyadam
    file_path = os.path.join(output_folder, f"user_{user_id}.csv")
    df.to_csv(file_path, index=False)

print("✅ 20 User Transaction CSV Files Generated Successfully!")
