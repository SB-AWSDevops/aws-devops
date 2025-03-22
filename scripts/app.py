from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os
import boto3
import logging
import os
import watchtower

app = Flask(__name__)

CORS(app)

# Ensure logs directory exists
LOG_DIR = "../data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create CloudWatch logger
LOG_GROUP = "backend-logs"  # Change if needed

# Configure logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Add CloudWatch logging handler
logging.getLogger().addHandler(watchtower.CloudWatchLogHandler(log_group=LOG_GROUP))

logging.info("CloudWatch Logging Enabled Successfully")

# RDS Connection Details
DB_HOST = "banking-app.cz20mkuc2xt5.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "adminn"
DB_PASS = "Surisetty1234"

S3_BUCKET = "banking-statements"  # Replace with your actual S3 bucket name
# Initialize S3 client
s3_client = boto3.client("s3")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    logging.info(f"User {user_id} requested transactions")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC LIMIT 10", (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    transactions = [
        {"id": row[0], "user_id": row[1], "date": str(row[2]), "type": row[3], "amount": float(row[4]), "balance": float(row[5])}
        for row in rows
    ]
    return jsonify(transactions)

@app.route('/statements/<int:user_id>', methods=['GET'])
def get_statement(user_id):
     logging.info(f"User {user_id} downloaded bank statement")
     file_key = f"user_{user_id}.csv"
     try:
        # Generate a pre-signed URL for secure download
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": file_key},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return jsonify({"download_url": url})
    
     except Exception as e:
        logging.error(f"Error fetching statement for User {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
