from flask import Flask
from flask import request, jsonify
import sqlite3

app = Flask(__name__)

def createTable():
    dbConnection = sqlite3.connect("patate.db")
    dbCursor = dbConnection.cursor()
    dbCursor.execute("CREATE TABLE IF NOT EXISTS log(method, is_wasm, duration)")
    dbConnection.close()

def clearTable():
    dbConnection = sqlite3.connect("patate.db")
    dbCursor = dbConnection.cursor()
    dbCursor.execute("DELETE FROM log")
    dbConnection.commit()
    dbConnection.close()

def saveLogs(payload):
    dbConnection = sqlite3.connect("patate.db")
    dbCursor = dbConnection.cursor()
    log_list = []
    for log in payload:
        method = log['method']
        duration = log['duration']
        is_wasm = log['is_wasm']
        log_list.append((method, is_wasm, duration))
    dbCursor.executemany("INSERT INTO log VALUES(?, ?, ?)", log_list)
    dbConnection.commit()
    dbConnection.close()

def getLogs():
    dbConnection = sqlite3.connect("patate.db")
    dbCursor = dbConnection.cursor()
    dbCursor.execute("SELECT * FROM log")
    rows = dbCursor.fetchall()
    result = ""
    for row in rows:
        print(row)
        result += row[0] + (": ", "_WASM: ")[row[1]] + str(row[2]) + " us\n"
    dbConnection.close()
    return result

createTable()

@app.route('/')
def root():
    return 'Patate log server up !'

@app.route('/logs',methods = ['POST', 'GET'])
def logs():
    if request.method == 'POST':
        saveLogs(request.json)
        return 'SAVED'
    if request.method == 'GET':
        return getLogs()
    else:
        return 'NONE'

@app.route('/clear',methods = ['POST'])
def clear():
    if request.method == 'POST':
        clearTable()
        return 'CLEARED'
    else:
        return 'NONE'
