from flask import Flask, render_template, request, g
from flask_cors import CORS
import json
from employee import *

 
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
#app.config.from_pyfile('config.py')



# elsastic APM agent 셋팅
#from elasticapm.contrib.flask import ElasticAPM


@app.route("/")
def template_test():
    return render_template(
                'index.html',                      #렌더링 html 파일명
                title="Flask Template Test",       #title 텍스트 바인딩1
                my_str="Hello Flask!",             #my_str 텍스트 바인딩2
                my_list=[x + 1 for x in range(10)] #30개 리스트 선언(1~30)
            )


# 로그인 시도
@app.route('/api/login', methods = ['POST'])
def signin():
    if request.method == 'POST':
        # json.dumps(dict): dict('') -> json("")
        # json.loads(json): json("") -> dict('')
        # request.get_json(): dict object
        #response = signinwithotp(request.get_json())
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6ImVkdSIsImlhdCI6MTUxNjIzOTAyMn0.Uy8TjN5hMqLxZiQ16iqG29sxXBFXNRjFStRth-xlfkU"
        token2 = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJlZHUiLCJleHAiOjE2NjgxNDE5MzEsImlhdCI6MTY2ODEyMzkzMX0._R9Hop6ckLPxwVTMv3FC6eWU1fg4xUXhozOKE7I9Cs111m0Ag6sQYVP8elAGkA8B2yR9SR5v_cSO5P4MuyKuGA"
        return json.dumps({'token':  token2})
    else:
        return json.dumps({'returnCode': 'NG', 'message': 'Method  not allowed.'}, status=405)


'''
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6ImVkdSIsImlhdCI6MTUxNjIzOTAyMn0.Uy8TjN5hMqLxZiQ16iqG29sxXBFXNRjFStRth-xlfkU
        response = app.response_class(
            response = json.dumps({'returnCode': 'OK', 'message': empNo + ' is added.', 'data': ''}),
            status = 200,
            mimetype = 'application/json'
        )
''' 

# CRUD - Read
@app.route('/api/v1/employees', methods = ['GET'])
def getEmployees():
    if request.method in ['GET']:
        response = userlist(request.headers, app)
        return response
    else:
        return json.dumps({'returnCode': 'NG', 'message': 'Method ' + request.method + ' not allowed.'}, status=405)
'''
# CRUD - Create
@app.route('/api/v1/employees', methods = ['POST'])
def addNewEmployee():
    if request.method == 'POST':
        response = add_user(request.headers, request.get_json(), app)
        return response
    else:
        return json.dumps({'returnCode': 'NG', 'message': 'Method ' + request.method + ' not allowed.'}, status=405)
'''

# health_check
@app.route('/health_check', methods = ['GET'])
def health_check():
    if request.method == 'GET':
        return json.dumps({'returnCode': 'OK'})
    else:
        return json.dumps({'returnCode': 'NG', 'message': 'Method ' + request.method + ' not allowed.'}, status=405)


if __name__ == '__main__':

    #app.run(host='0.0.0.0',)
    app.run(host='0.0.0.0',port=8080,debug=True)
