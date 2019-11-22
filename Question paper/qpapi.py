import sqlite3
import random
import fpdf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import *
import requests
from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
import json
from bson import json_util
import base64
import datetime
from flask_cors import CORS
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'calendar'
app.config['MONGO_URI'] = "mongodb://localhost/calendar"
CORS(app)
mongo = PyMongo(app)

pdf = fpdf.FPDF(format='letter')

@app.route('/', methods=['GET'])
def start():
    if(request.method=='GET'):
        return render_template('/MDB-Free/test.html')

@app.route('/submit', methods=['POST'])
def submit():
    date = request.form.get('date')
    subject = request.form.get('subject')
    mark = request.form.get('marks1a')
    print(mark)
    sections = ['1','2','3','4','5']
    questions = ['a','b','c','d','e']
    qlist=[]
    for i in sections:
        jlist = []
        for j in questions:
            k=str(i+j)
            q = request.form.get(k)
            # print(k, q)
            jlist.append(q)
            # print(jlist)
        qlist.append(jlist)
        # print(qlist)

    print(qlist)
    pdf.add_page()
    pdf.set_font("Times", size=20)
    pdf.cell(200, 15, subject, ln=1, align="C")
    pdf.cell(200, 15, date, ln=1, align="C")

    pdf.set_font("Times", size=12)
    for i in range(len(qlist)):
        for j in range(len(questions)):
            pdf.cell(170, 6, str(i + 1)+ " ("+str(questions[j])+")      " + qlist[i][j],0, align="left")
            pdf.cell(20,6,mark,0,1,align='right')
        pdf.cell(170,15,'',ln=1,align="left")
    pdf.output("file.pdf")

    return jsonify({"output":"file generated"})

def random_num_gen(n):
    rlist = random.sample(range(n),5)
    rlist = [x+1 for x in rlist]
    return rlist

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
