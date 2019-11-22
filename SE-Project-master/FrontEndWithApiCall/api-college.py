from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import jsonify
from flask import request
from flask import make_response
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'SE_DB'
app.config["MONGO_URI"] = "mongodb://localhost:27017/SE_DB"
mongo = PyMongo(app)


#not found handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}),404)


#student related apis
#Add student api
@app.route('/api/v1/student', methods=['POST'])
def add_student():
    _json=request.json
    print(_json)
    _name=_json['name']
    _usn=_json['usn']
    _password=_json['pwd']
    _section = _json['section']
    flag = mongo.db.student.find_one({'usn':_usn})
    print(flag)
    if(flag):
        resp=jsonify('student already exist')
        resp.status_code=409
        return resp
    elif _name and _usn and _password and _section and request.method=='POST':
        _hashed_password=generate_password_hash(_password)
        print(_hashed_password  )
        id = mongo.db.student.insert({'name': _name, 'usn': _usn, 'section':_section, 'pwd': _hashed_password})
        resp = jsonify('student added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


#list all student records
@app.route('/api/v1/student',methods=['GET'])
def list_students():
    students=mongo.db.student.find()
    print(type(students))
    resp=dumps(students)
    print(type(resp))
    if resp!='[]':
        return resp
    elif resp=='[]':
        res=jsonify('No students in database')
        res.status_code = 204
        return res


#list specific student
@app.route('/api/v1/student/<usn>', methods=['GET'])
def student(usn):
    student=mongo.db.student.find_one({'usn':usn})
    resp=dumps(student)
    if resp!='null':
        return resp
    elif resp=='null':
        res=jsonify('student does not exist')
        res.status_code = 204
        return res

#student login
@app.route('/api/v1/student/login', methods=['POST'])
def student_login():
    data=request.json
    usn=data['usn']
    passw=data['password']
    student=mongo.db.student.find_one({'usn':usn})
    resp=dumps(student)
    if resp=='null':
        resp=jsonify('student does not exist')
        resp.status_code=204
        return resp
    elif resp!='null':
        pass1=student['pwd']
        if passw==pass1:
            res=jsonify('Student Login successfully')
            res.status_code=200
        else:
            res=jsonify('Student does not exist')
            res.status_code=204
        return res

#faculty login
@app.route('/api/v1/faculty/login', methods=['POST'])
def faculty_login():
    data=request.json
    fcode=data['fcode']
    passw=data['password']
    faculty=mongo.db.faculty.find_one({'fcode':fcode})
    resp=dumps(faculty)
    if resp=='null':
        resp=jsonify('faculty does not exist')
        resp.status_code=204
        return resp
    elif resp!='null':
        pass1=faculty['pwd']
        if passw==pass1:
            res=jsonify('faculty Login successfully')
            res.status_code=200
        else:
            res=jsonify('faculty does not exist')
            res.status_code=204
        return res



#Delete specific Student
@app.route('/api/v1/student/<usn>',methods=['DELETE'])
def delete_student(usn):
    student=mongo.db.student.find_one({'usn':usn})
    res1=dumps(student)
    if(res1=='null'):
        resp=jsonify('student does not exist')
        return resp
    else:
        mongo.db.student.delete_one({'usn':usn})
        resp=jsonify('student deleted successfully')
        resp.status_code=200
        return resp


#Delete all Student
@app.route('/api/v1/student',methods=['DELETE'])
def delete_all_student():
    mongo.db.student.remove({})
    resp=jsonify('All student records are deleted');
    resp.status_code=200
    return resp


#Update Student
@app.route('/api/v1/student',methods=['PUT'])
def update_student():
    _json=request.json
    _id=_json['_id']
    _name = _json['name']
    _usn=_json['usn']
    _password = _json['pwd']
    flag=mongo.db.student.find_one({'usn':_usn})
    print(flag)
    print(type(flag))
    if flag == 'None':
        resp=jsonify('User does not exist')
    if _name and _usn and _password and _id and request.method=='PUT':
        _hashed_password=generate_password_hash(_password)
        mongo.db.student.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set': {'name': _name, 'usn': _usn, 'pwd': _hashed_password}})
        resp = jsonify('User updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


#courses releated apis
#Add course
@app.route('/api/v1/courses', methods=['POST'])
def add_course():
    _json=request.json
    print(_json)
    _cname=_json['coursename']
    _ccode=_json['coursecode']
    _credits=_json['credits']
    print(_cname,_ccode,_credits)
    flag=mongo.db.courses.find_one({'coursename':_cname})
    print(flag)
    if(flag):
        resp=jsonify('course already exist')
        resp.status_code=409
    elif _cname and _ccode and _credits and request.method == 'POST':
        id = mongo.db.courses.insert({'coursename': _cname, 'coursecode': _ccode, 'credits': _credits})
        resp = jsonify('course added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


#Delete course
@app.route('/api/v1/courses/<coursecode>',methods=['DELETE'])
def delete_course(coursecode):
    course = mongo.db.courses.find_one({'coursecode':coursecode})
    res1=dumps(course)
    if(res1=='null'):
        resp=jsonify('course does not exist')
        return resp
    else:
        mongo.db.courses.delete_one({'coursecode':coursecode})
        resp=jsonify('course deleted successfully')
        resp.status_code=200
        return resp


#Delete all courses
@app.route('/api/v1/courses',methods=['DELETE'])
def delete_all_courses():
    mongo.db.courses.remove({})
    resp=jsonify('All Courses are removed')
    resp.status_code=200
    return resp


#Update course
@app.route('/api/v1/courses',methods=['PUT'])
def udate_course():
    _json=request.json
    _id=_json['_id']
    _cname = _json['coursename']
    _ccode=_json['coursecode']
    _credits = _json['credits']
    if _cname and _cname and _credits and _id and request.method=='PUT':
        mongo.db.courses.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set': {'coursename': _cname, 'coursecode': _ccode, 'credits': _credits}})
        resp = jsonify('course updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


#list all courses
@app.route('/api/v1/courses',methods=['GET'])
def list_course():
    courses=mongo.db.courses.find()
    resp=dumps(courses)
    if resp!='[]':
        return resp
    elif resp=='[]':
        res = jsonify('No courses exist in database')
        res.status_code = 204
        return res


#list perticular course
@app.route('/api/v1/courses/<coursecode>',methods=['GET'])
def list_pert_course(coursecode):
    course=mongo.db.courses.find_one({'coursecode':coursecode})
    resp=dumps(course)
    if resp!='null':
        return resp
    elif resp=='null':
        res = jsonify('student does not exist')
        res.status_code = 204
        return res


#Faculty apis
#Add Faculty
@app.route('/api/v1/faculty', methods=['POST'])
def add_faculty():
    _json=request.json
    print(_json)
    _name=_json['name']
    _fcode=_json['fcode']
    _email=_json['email']
    _dname=_json['Dname']
    _password=_json['pwd']
    flag=mongo.db.faculty.find_one({'fcode':_fcode})
    print(flag)
    if(flag):
        resp=jsonify('Faculty already exist')
        resp.status_code=409
        return resp
    elif _name and _fcode and _email and _dname  and _password and request.method=='POST':
        _hashed_password=generate_password_hash(_password)
        print(_hashed_password )
        id = mongo.db.faculty.insert({'name': _name, 'fcode': _fcode,'email':_email,'Dname':_dname, 'pwd': _hashed_password})
        resp = jsonify('Faculty added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


#Delete Faculty
@app.route('/api/v1/faculty/<fcode>',methods=['DELETE'])
def delete_faculty(fcode):
    faculty = mongo.db.faculty.find_one({'fcode':fcode})
    res1=dumps(faculty)
    if(res1=='null'):
        resp=jsonify('faculty does not exist')
        return resp
    else:
        mongo.db.faculty.delete_one({'fcode':fcode})
        resp=jsonify('faculty deleted successfully')
        resp.status_code=200
        return resp

#Delete all faculties
@app.route('/api/v1/faculty',methods=['DELETE'])
def delete_all_faculties():
    mongo.db.faculty.remove({})
    resp=jsonify('Removed all faculties')
    resp.status_code=200
    return resp

#Update Faculty
@app.route('/api/v1/faculty',methods=['PUT'])
def update_faculty():
    _json=request.json
    _id=_json['_id']
    _name = _json['name']
    _email=_json['email']
    _dname=_json['Dname']
    _fcode=_json['fcode']
    _password = _json['pwd']
    if _name and _email and _fcode and _id and _password and _dname and request.method=='PUT':
        _hashed_password=generate_password_hash(_password)
        mongo.db.faculty.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set': {'name': _name, 'fcode': _fcode, 'Dname':_dname,'email':_email, 'pwd': _hashed_password}})
        resp = jsonify('Faculty updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()



#list all Faculties
@app.route('/api/v1/faculty',methods=['GET'])
def list_faculties():
    faculty=mongo.db.faculty.find()
    resp=dumps(faculty)
    if resp!='[]':
        return resp
    elif resp=='[]':
        res=jsonify('No faculties exist in database')
        res.status_code = 204
        return res

#List any specific Faculty
@app.route('/api/v1/faculty/<fcode>',methods=['GET'])
def list_pert_faculty(fcode):
    faculty=mongo.db.faculty.find_one({'fcode':fcode})
    resp=dumps(faculty)
    if resp!='null':
        return resp
    elif resp=='null':
        res = jsonify('faculty does not exist')
        res.status_code = 204
        return res

if __name__ == '__main__':
    app.run(debug=True)
