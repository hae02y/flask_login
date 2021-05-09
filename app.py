# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, session, request, redirect, url_for
from models import User, db
app = Flask(__name__)


@app.route('/')
def main():
    if 'userid' in session:
        userid = session['userid']
        return render_template('home.html',userid=userid)
    else:
        return render_template('error.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'userid' in session:
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('login.html')
        else:
            userid = User.query.filter_by(userid = request.form.get('userid')).first()
            password = User.query.filter_by(password = request.form.get('password')).first()

            if not userid:
                msg = "아이디 없음"
                return render_template('login.html' ,msg = msg)
            elif not password:
                msg = "비밀번호 틀림"
                return render_template('login.html' ,msg = msg)
            session['userid'] = request.form.get('userid')
            return redirect('/')

@app.route('/logout', methods = ['GET'])
def logout():    
    session.pop('userid', None)
    return redirect('/')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        username = request.form.get('username')
        repass = request.form.get('repass')

        if not (userid and password and username and repass):
            msg = "모두 입력하여주세요."
            return render_template('register.html', msg = msg)
        if password != repass:
            msg = "비밀번호가 다릅니다."
            return render_template('register.html', msg = msg)
        user = User()
        user.userid = userid
        user.username = username
        user.password = password

        db.session.add(user)
        db.session.commit()
        
        print(user.userid,user.username,user.password)

        return redirect('/')

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "adjsaldjlasjdlkasjdkl"
    db.init_app(app)
    db.app = app
    db.create_all()
    app.run(debug = True)