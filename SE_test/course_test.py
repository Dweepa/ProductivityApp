import pytest
import requests
import json

url = 'http://127.0.0.1:2000' # The root url of the flask app

def test_student_add():
    d = {
	"name":"xyz",
	"usn":"01FB16ECS123",
	"pwd":"@#$%12321",
	"section":"c"
	}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.post(url+'/api/v1/student',data=json.dumps(d),headers=headers) 
    assert r.status_code == 200

def test_student_add_again():      #Check if student with same value of key(usn) can be added
    d = {
	"name":"xyz",
	"usn":"01FB16ECS123",
	"pwd":"@#$%1232",
	"section":"c"
	}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.post(url+'/api/v1/student',data=json.dumps(d),headers=headers) 
    assert r.status_code == 409

def test_student_get():		#List all student
    
    r = requests.get(url+'/api/v1/student') 
    assert r.status_code == 200 

def test_student_specific():	#List specific student
    
    usn = "01FB16ECS456"
    r = requests.get(url+'/api/v1/student/'+usn) 
    assert r.status_code == 204

    usn = "01FB16ECS123"
    r = requests.get(url+'/api/v1/student/'+usn) 
    assert r.status_code == 200

def test_student_update1():
    d = {
	"name":"Gourishankar",
	"usn":"01FB16ECS456",
	"pwd":"@#$%12321"
}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.put(url+'/api/v1/student',data=json.dumps(d),headers=headers) #try updating a record that does not exist
    assert r.status_code == 204

    d = {
	"name":"Gourishankar",
	"usn":"01FB16ECS123",
	"pwd":"@#$%12321"
}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.put(url+'/api/v1/student',data=json.dumps(d),headers=headers) #update a record that exists
    assert r.status_code == 200


def test_del_student_specific():	#Delete specific student record
    
    usn = "01FB16ECS123"
    r = requests.delete(url+'/api/v1/student/'+usn) 
    assert r.status_code == 200

def test_del_student_all():	#Delete all student records
    

    r = requests.delete(url+'/api/v1/student') 
    assert r.status_code == 200



#Course related APIs

def test_course_add():
    d = {
  "coursename":"BD",
	"coursecode":"BD1122",
	"credits":"4"
}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.post(url+'/api/v1/courses',data=json.dumps(d),headers=headers) #Add course
    assert r.status_code == 200

    d = {
  "coursename":"BD",
	"coursecode":"BD1122",
	"credits":"4"
}
    
    r = requests.post(url+'/api/v1/courses',data=json.dumps(d),headers=headers) #Add course with same course id again
    assert r.status_code == 409



def test_course_get():		#List all courses
    
    r = requests.get(url+'/api/v1/courses') 
    assert r.status_code == 200 


def test_course_update():

    d = {
  "coursename":"BD",
	"coursecode":"BD1122",
	"credits":"4"
}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.put(url+'/api/v1/courses',data=json.dumps(d),headers=headers) #update a record that exists
    assert r.status_code == 200

def test_del_course_specific():	#Delete specific course
    
    cc = "BD1122"
    r = requests.delete(url+'/api/v1/courses/'+cc) 
    assert r.status_code == 200

def test_del_course_all():	#Delete all courses
    

    r = requests.delete(url+'/api/v1/courses') 
    assert r.status_code == 200

def test_course_get():		#List all courses
    
    r = requests.get(url+'/api/v1/courses') 
    assert r.status_code == 204 


#Faculty related APIs



def test_faculty_add():
    d = {
	"name":"Badree",
	"fcode":"bd5112",
	"email":"badree@pes.edu",
	"Dname":"Mechanical  Engineering",
	"pwd":"Mebadree"
}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.post(url+'/api/v1/faculty',data=json.dumps(d),headers=headers) #Add Faculty
    assert r.status_code == 200

    d = {
	"name":"Badree",
	"fcode":"bd5112",
	"email":"badree@pes.edu",
	"Dname":"Mechanical  Engineering",
	"pwd":"Mebadree"
}
    
    r = requests.post(url+'/api/v1/faculty',data=json.dumps(d),headers=headers) #Add course with same course id again
    assert r.status_code == 409



def test_faculty_get():		#List all courses
    
    r = requests.get(url+'/api/v1/faculty') 
    assert r.status_code == 200 


def test_faculty_update():

    d = {
	"name":"Badree",
	"fcode":"bd5112",
	"email":"badree@pes.edu",
	"Dname":"Mechanical  Engineering",
	"pwd":"Mebadree"
}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.put(url+'/api/v1/faculty',data=json.dumps(d),headers=headers) #update a record that exists
    assert r.status_code == 200

    d = {
	"name":"Badree",
	"fcode":"bd5113",
	"email":"badree@pes.edu",
	"Dname":"Mechanical  Engineering",
	"pwd":"Mebadree"
}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.put(url+'/api/v1/faculty',data=json.dumps(d),headers=headers) 
    assert r.status_code == 204



def test_del_faculty_specific():	#Delete specific faculty record
    
    fc = "bd5112"
    r = requests.delete(url+'/api/v1/faculty/'+fc) 
    assert r.status_code == 200

def test_del_faculty_all():	#Delete all faculty records
    

    r = requests.delete(url+'/api/v1/faculty') 
    assert r.status_code == 200

def test_faculty_get():		#List all faculty
    
    r = requests.get(url+'/api/v1/faculty') 
    assert r.status_code == 204 

