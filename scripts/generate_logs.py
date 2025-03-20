import random  # Random log level select cheyyataniki
from faker import Faker  # Fake log messages generate cheyyataniki
import os  # Folder structure maintain cheyyataniki
from datetime import datetime, timedelta  # Time calculations cheyyataniki

# Fake data generator
fake = Faker()

# Output folder for logs
log_folder = "../data/logs/"
os.makedirs(log_folder, exist_ok=True)  # Folder create if not exists

# Log file path
log_file = os.path.join(log_folder, "app.log")

# Possible log levels
log_levels = ["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"]

# Generate 500+ logs
with open(log_file, "w") as f:
    for _ in range(500):
        timestamp = datetime.now() - timedelta(seconds=random.randint(0, 86400))  # Last 24 hrs lo random timestamp
        log_level = random.choice(log_levels)  # Random log level
        message = fake.sentence()  # Random log message
        user_id = random.randint(1, 20)  # Random user ID (1 to 20)

        log_entry = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {log_level}: User {user_id} - {message}\n"
        f.write(log_entry)

print("✅ 500+ Application Logs Generated Successfully!")
