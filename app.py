from flask import Flask, request, redirect, render_template
# import csv
# import os
# import sqlite3
# import secrets

app = Flask(__name__)

# Set up SQLite database for storing click data

@app.route("/",methods=["GET","POST"])
def helloWorld():
    return "Hello World! The Project is Set Up successFully"

if __name__ == "__main__":
    app.run(port=5001 , debug=True)
