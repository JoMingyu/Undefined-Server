from flask import request
from flask_restful import Resource

from support.mysql import query

import uuid
import smtplib
from email.mime.text import MIMEText

from_email = 'city7312@naver.com'


def send_email(title, content, target):
    message = MIMEText(content, _charset='utf-8')
    message['subject'] = title
    message['from'] = from_email
    message['to'] = target

    s = smtplib.SMTP('smtp.naver.com', 587)
    s.starttls()
    s.login('city7312', 'uursty199')
    s.sendmail(from_email, target, message.as_string())
    s.quit()


class FindIdDemand(Resource):
    def post(self):
        # 아이디 찾기 : 인증 메일 전송
        email = request.form['email']
        if not query("SELECT * FROM account WHERE email='{0}'".format(email)):
            return '', 204

        code = str(uuid.uuid4())[:6]

        query("DELETE FROM email_codes WHERE email='{0}'".format(email))
        query("INSERT INTO email_codes VALUES('{0}', '{1}')".format(email, code))
        send_email('[Bubble] 이메일 인증 코드입니다.', '인증 코드 : {0}'.format(code), email)

        return '', 200


class FindIdVerify(Resource):
    def post(self):
        # 아이디 찾기 : 코드 인증
        email = request.form['email']
        code = request.form['code']

        if query("SELECT * FROM email_codes WHERE email='{0}' AND code='{1}'".format(email, code)):
            query("DELETE FROM email_codes WHERE email='{0}'".format(email))
            res = query("SELECT * FROM account WHERE email='{0}'".format(email))
            return {'id': res[0]['id']}
        else:
            return '', 204


class FindPwDemand(Resource):
    def post(self):
        # 비밀번호 찾기 : 인증 메일 전송
        email = request.form['email']
        _id = request.form['id']
        if not query("SELECT * FROM account WHERE email='{0}' AND id='{1}'".format(email, _id)):
            return '', 204

        code = str(uuid.uuid4())[:6]

        query("DELETE FROM email_codes WHERE email='{0}'".format(email))
        query("INSERT INTO email_codes VALUES('{0}', '{1}')".format(email, code))
        send_email('[Bubble] 이메일 인증 코드입니다.', '인증 코드 : {0}'.format(code), email)

        return '', 200


class FindPwVerify(Resource):
    def post(self):
        # 비밀번호 찾기 : 코드 인증
        email = request.form['email']
        code = request.form['code']

        if query("SELECT * FROM email_codes WHERE email='{0}' AND code='{1}'".format(email, code)):
            query("DELETE FROM email_codes WHERE email='{0}'".format(email))
            return '', 200
        else:
            return '', 204


class ChangePassword(Resource):
    def post(self):
        email = request.form['email']
        new_pw = request.form['pw']

        query("UPDATE account SET pw='{0}' WHERE email='{1}'".format(new_pw, email))

        return '', 200
