import pytest
import requests
import json

url = 'http://127.0.0.1:2000' # The root url of the flask app

def test_cal_add():
    d = {
	"title":"test",
        "description":"unit test",
        "course": "Cloud",
        "section":"C",
         "team":"A",
         "d":"20",
         "m":"11",
         "y":"2019"
	
	}
    headers= {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         }
    r = requests.post(url+'/add',data=json.dumps(d),headers=headers) # Assumses that it has a path of "/"
    assert r.status_code == 200 # Assumes that it will return a 200 response

def test_index_page():
    d = "20"
    m = "11"
    y = "2019"
    r = requests.get(url+'/show/'+d+'/'+m+'/'+y) 
    assert r.status_code == 200 # Assumes that it will return a 200 response

