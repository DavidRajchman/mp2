from flask import Flask, redirect, url_for, request, render_template, session 
from flask_bcrypt import Bcrypt
import json

from api_routes import temperature_api



app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ajkdhkajcocioauiodjkcjaxl" #session secret key

try:
    with open('users.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

app.register_blueprint(temperature_api, url_prefix='/api')


@app.route('/')
def home():
    if "username" in session:
        with open("temperatures.json", "r") as fp:
            temps = json.load(fp)
        return render_template('index.html', values=temps)
        
    else:
        print("no user logged in")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    errorx = request.args.get("errorx") #get message from url to display
    if request.method == 'POST':
        user = request.form["username"]
        password = request.form["password"]
        if user in users:
            if bcrypt.check_password_hash(users[user], password):
                session["username"] = user
                return redirect(url_for('home')) #correct login
            else:
                eror = "bad password,  please try again" 
                return redirect(url_for('login',errorx = eror))
        else:
            eror = "user does not exist, please register" 
            return redirect(url_for('login',errorx = eror))    
    else:
        return render_template('login.html', errorx = errorx)


@app.route('/register', methods=['GET', 'POST'])
def register():
    errorx = request.args.get("errorx") #get message from url to display
    if request.method == 'GET':
        return render_template("register.html", errorx = errorx)
    if request.method == 'POST':
        newuser = request.form["rusername"]
        password = request.form["rpassword"]
        if password == "":
            eror = "password cannot be blank"
            return redirect(url_for("register", errorx = eror ))

        if newuser in users: #check if the username is not already registered
            eror = "this username is already registered, choose a diferent username, or login"
            return redirect(url_for("register", errorx = eror )) 
        else: 
            # Hash and salt the password
            pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            
            users[newuser] = pw_hash
            print("user registered")
            with open('users.json', 'w') as f:
                json.dump(users, f)

            return redirect(url_for("home"))
    



if __name__ == '__main__':
    app.run(debug=True)
    