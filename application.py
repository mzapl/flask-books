#FLASK
from flask import Flask, render_template, session, request
from flask_session import Session

#SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


#FLASK, SESSIONS CONFIGURATION
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

#SQL CONFIGURATION
engine = create_engine('postgresql://postgres:651596XY@localhost:5432/userdata')
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def main():
    if session.get('user_id') is None:
        return render_template("login.html")
    else:
        return render_template("index.html", user_name = session['user_data'].login)


@app.route("/login", methods=["POST"])
def login():
    user_login = request.form.get("login")
    user_password = request.form.get("password")
    try:
        session['user_data'] = db.execute("SELECT * FROM users WHERE login = :login", {"login": user_login.lower()}).fetchall()[0]
        if session['user_data'].password == user_password:
            session['user_id'] = session['user_data'].id
            return render_template('index.html', user_name = session['user_data'].login)
    except:
        return render_template( 'login.html', error = 'no_user')
    return render_template('login.html', error = 'wrong_password')


@app.route("/register", methods=["POST"])
def register():
    user_login = request.form.get("login")
    user_pass = request.form.get("password")
    if (db.execute("SELECT * FROM users WHERE login = :login", {"login": user_login.lower()}).fetchall()):
        return render_template( 'login.html', error = 'duplicate_user', user_login=user_login)
    else:
        db.execute("INSERT INTO users (login, password) VALUES (:login, :password)", {'login': user_login, 'password': user_pass})
        db.commit()
        return render_template("login.html", error=0)


@app.route("/logout")
def logout():
    session['user_id'] = None
    return main()

if __name__=="__main__":
    app.debug=1
    app.run()






