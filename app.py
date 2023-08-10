from flask import Flask, request, redirect, render_template
import csv
import os
import sqlite3
import secrets

app = Flask(__name__)

#Connection to SQLITE DB and creating a table If not exists
db_conn = sqlite3.connect("db/click_data.db")
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS clicks (
        masked_link TEXT,
        original_link TEXT,
        click_count INTEGER DEFAULT 0,
        PRIMARY KEY (masked_link)
    )
""")
db_conn.commit()

print("DB Connection Established Successfully")

@app.route("/",methods=["GET","POST"])
def helloWorld():
    return "Hello World! The Project is Set Up successFully"

if __name__ == "__main__":
    app.run(port=5001 , debug=True)
