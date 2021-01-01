#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
    @author     :   xstatus
    @time       :   2020/12/30 19:52
    @email      :   crawler@88.com
    @project    :   1.recaptcha v3验证码demo -> index.py
    @IDE        :   PyCharm
    @describe   :   ooops
"""

import requests,functools
from flask import Flask,render_template,request,jsonify
from config import Keys
app = Flask(__name__)


def verify_recaptcha(SECRET_KEY):
    def outter(f):
        @functools.wraps(f)
        def wrapper(*args,**kwargs):
            request.verify_response = {}
            request.recaptcha_passed = False
            token = request.form.get('g-recaptcha-response')
            api = 'https://www.recaptcha.net/recaptcha/api/siteverify'
            data = {
                'response': token,
                'secret': SECRET_KEY,
                'remoteip': request.remote_addr
            }
            response = requests.post(api, data=data)
            result = response.json()
            if result.get('success'):
                request.verify_response = result
                request.recaptcha_passed = True
                return f(*args,**kwargs)
            else:
                return result,403
        return wrapper
    return outter


# --- html模板路由 ---
@app.route('/v3')
def recaptcha_v3():
    return render_template('recaptcha-v3.html',site_key=Keys.V3.localhost.site_key)

@app.route('/v3/programmatically')
def recaptcha_v3_programmatically():
    return render_template('recaptcha-v3-programmatically.html',site_key=Keys.V3.localhost.site_key)

@app.route('/v2/checkbox')
def recaptcha_v2_checkbox():
    return render_template('recaptcha-v2-checkbox.html',site_key=Keys.V2.localhost.checkbox.site_key)

@app.route('/v2/checkbox/explicit')
def recaptcha_v2_checkbox_explicit_rendering():
    return render_template('recaptcha-v2-checkbox-explicit-rendering.html',site_key=Keys.V2.localhost.checkbox.site_key)

@app.route('/v2/invisible')
def recaptcha_v2_invisible():
    return render_template('recaptcha-v2-invisible.html',site_key=Keys.V2.localhost.invisible.site_key)

@app.route('/v2/invisible/explicit')
def recaptcha_v2_invisible_explicit_rendering():
    return render_template('recaptcha-v2-invisible-explicit-rendering.html',site_key=Keys.V2.localhost.invisible.site_key)

@app.route('/v2/invisible/invoke')
def recaptcha_v2_invisible_invoke():
    return render_template('recaptcha-v2-invisible-invoke.html',site_key=Keys.V2.localhost.invisible.site_key)


# ---- 验证路由 ----
@app.route('/v2/verify/checkbox',methods=['POST'])
@verify_recaptcha(Keys.V2.localhost.checkbox.secret_key)
def v2_verrify_checkbox():
    data = {
        'data':request.form,
        'verify':request.verify_response
    }
    return jsonify(data)

@app.route('/v2/verify/invisible',methods=['POST'])
@verify_recaptcha(Keys.V2.localhost.invisible.secret_key)
def v2_verrify_invisible():
    data = {
        'data':request.form,
        'verify':request.verify_response
    }
    return jsonify(data)

@app.route('/v3/verify',methods=['POST'])
@verify_recaptcha(Keys.V3.localhost.secret_key)
def v3_verrify():
    data = {
        'data':request.form,
        'verify':request.verify_response,
        'score':request.verify_response.get('score') if request.recaptcha_passed else 0
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run('localhost',5555,use_reloader=True)