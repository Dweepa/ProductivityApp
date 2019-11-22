import requests
from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
import json
from bson import json_util
import base64
import datetime
from flask_cors import CORS
import os

from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'calendar'
app.config['MONGO_URI'] = "mongodb://localhost/calendar"
CORS(app)
mongo = PyMongo(app)

scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
scheduler.start()

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "pesuprod@gmail.com",
    "MAIL_PASSWORD": "pesu@123"
    # "MAIL_USERNAME": "xyz41607@gmail.com",
    # "MAIL_PASSWORD": "abcxyz12345"
}

app.config.update(mail_settings)
mail = Mail(app)

app.config['MONGO_DBNAME'] = 'calendar'
app.config['MONGO_URI'] = "mongodb://localhost:27017/calendar"
CORS(app)
mongo = PyMongo(app)


# @app.route('/schedulePrint', methods=['POST'])
def schedule_to_print(data):
    # get time to schedule and text to print from the json
    # time = "2019-11-13 21:50:00"
    # convert to datetime
    student = mongo.db.student
    # data = request.get_json(force=True)
    print(data)
    time = data["time"]
    body = data["body"]
    sec = data["section"]
    docs = list(student.find({"section": sec}))
    print(docs)
    output = []
    for i in docs:
        output.append(i['email'])
        print(i)

    date_time = datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S')
    print(date_time)
    print(output)
    job = scheduler.add_job(notification, trigger='date', next_run_time=str(date_time), args=[output, body])
    return "job details: %s" % job


def notification(output, body):
    print(output)
    with app.app_context():
        msg = Message(subject="Hello", sender=app.config.get("MAIL_USERNAME"), recipients=output,
                      body="Today is the deadline for your assignment ! " + body)
        mail.send(msg)


@app.route('/show/<date>/<month>/<year>', methods=['GET'])
def show(date, month, year):
    calendar = mongo.db.calendar
    print(date, month, year)
    docs_list = list(calendar.find({"D": int(date), "M": month, "Y": int(year)}))
    output = []
    for i in docs_list:
        # output.append({'day': i['day'], 'D': i['D'], 'M': i['M'], "Y": i['Y'], "type": i['event.type'],
        #                "course": i['event.course'], "section": i['event.section'], "team": i['event.team'],
        #                "description": i['event.description']})
        output.append({'D': i['D'], 'M': i['M'], "Y": i['Y'], "event": i['event']})
        print(i)
    print(output)
    return jsonify({"output": output})


@app.route('/add', methods=['POST'])
def add():
    calendar = mongo.db.calendar
    req = request.json
    # print('in post ',req)
    event_dict = {'type': req['title'], 'course': req['course'],
                  'section': req['section'], 'team': req['team'],
                  'description': req['description']}
    uid = calendar.insert(
        {'D': int(req['d']), 'M': req['m'], 'Y': int(req['y']), 'event': event_dict, 'status': 'pending'})
    print(uid)

    req_dict = dict()
    req_dict['section'] = req['section']
    req_dict['body'] = req['description']
    date = str(req['y']) + "-" + str(req['m']) + "-" + str(req['d']) + " " + "08:00:00"
    # print(date)
    req_dict['time'] = (datetime.strptime(date, '%Y-%B-%d %H:%M:%S')).strftime("%Y-%m-%d %H:%M:%S")
    print(schedule_to_print(req_dict))
    # op = list(calendar.find({"_id":uid}))
    return jsonify({"output": 'insert done'})


@app.route('/statusupdate', methods=['PUT'])
def status():
    calendar = mongo.db.calendar
    req = request.json
    print(req)
    print("list")
    output = []
    ev = req['event']
    event_dict = {'type': ev['type'], 'course': ev['course'],
                  'section': ev['section'], 'team': ev['team'],
                  'description': ev['description']}
    calendar.update({"D": req['D'], "M": req['M'], "Y": req['Y'], "event": event_dict}, {"$set": {"status": "done"}})
    return jsonify({"output": "done"})


@app.route('/submissions/<course>', methods=['GET'])
def getSubmissions(course):
    calendar = mongo.db.calendar
    course = course.split('_')
    course = ' '.join(course)
    print(course)
    for i in calendar.find({"status":"done"}):
        print(i['D'])
    pending = calendar.find({"event.course": course, "status":"pending"}).count()
    done = calendar.find({"event.course": course, "status":"done"}).count()
    return jsonify(done)

@app.route('/sentiment', methods=['GET'])
def sent():
    # t = os.system("python /Users/dweepa/Documents/SE/Sentiment-Analysis-Twitter/sentiment.py")
    # return t

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
