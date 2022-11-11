import requests, json
import datetime
from urllib.parse import urlparse
from jwtTokenUtil import *

 
encoding = lambda obj: (obj.isoformat()
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date)
    else None
)

 

# CRUD - 조회
def userlist(hdr, app):
    try:
        ##if (isAuthorized(hdr, app) == False):
        ##    raise AuthError("token is unauthorized.")

        # postgreSQL일때 스키마 지정
        ##if app.database == 'postgresql':
        ##    app.database.execute("SET search_path TO %s", app.config['SCHEMA'])

        sql = '''
            SELECT *
            from employee
            order by id
            '''

        #data = app.database.execute(sql)
        #res = [dict(row.items()) for row in data]

        response = app.response_class(
            response = json.dumps({'returnCode': 'OK', 'message': '', 'data': ''}, default=encoding),
            status = 200,
            mimetype = 'application/json'
        )
        return response
    except Exception as e:
        # 잘못된 토큰 (로그아웃/만료)
        if str(e) == "token is unauthorized.":
            response = app.response_class(
                response = json.dumps({'returnCode': 'NG', 'message': str(e)}),
                status = 401,
                mimetype = 'application/json'
            )
            return response

 
        response = app.response_class(
            response = json.dumps({'returnCode': 'NG', 'message': str(e)}),
            status = 200,
            mimetype = 'application/json'
        )

        return response


# CRUD - 생성
def add_user(hdr, req, app):

    try:
        if (isAuthorized(hdr, app) == False):
            raise AuthError("token is unauthorized.")

        # req: dict / encode: string(유니코드) -> bytes (암호화)

        if 'empNo' not in req:
            raise Exception('[empNo] key does not exist in your parameters.')

        empNo = req['empNo']
        sql = '''
            SELECT COUNT(*)
            FROM employee
            WHERE empNo = %s
            '''
    
        get_exists = app.database.execute(sql, (empNo)).fetchone()
        cnt = get_exists[0]
        if cnt > 0:
            raise Exception("empNo(" + empNo + ") already exists.")
        empName = req.get('empName', '')
        empDeptName = req.get('empDeptName', '')
        empTelNo = req.get('empTelNo', '')
        empMail = req.get('empMail', '')

        sql = '''
            INSERT INTO employee
            (empNo, empName, empDeptName, empTelNo, empMail)
            VALUES
            (%s, %s, %s, %s, %s)
            '''

        app.database.execute(sql, empNo, empName, empDeptName, empTelNo, empMail)
        response = app.response_class(
            response = json.dumps({'returnCode': 'OK', 'message': empNo + ' is added.', 'data': ''}),
            status = 200,
            mimetype = 'application/json'
        )
        return response
    except Exception as e:
        # 잘못된 토큰 (로그아웃/만료)
        if str(e) == "token is unauthorized.":
            response = app.response_class(
                response = json.dumps({'returnCode': 'NG', 'message': str(e)}),
                status = 401,
                mimetype = 'application/json'
            )
            return response
        response = app.response_class(
            response = json.dumps({'returnCode': 'NG', 'message': str(e)}),
            status = 200,
            mimetype = 'application/json'
        )
        return response
