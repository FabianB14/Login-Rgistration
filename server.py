from flask import Flask, render_template, redirect, request, session, flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')       
app = Flask(__name__)        
bcrypt = Bcrypt(app) 
app.secret_key = '173648436729' 
mysql = connectToMySQL('users_registration')

@app.route('/')
def index():
    
    all_users = mysql.query_db("SELECT * FROM users")
    print("All Users", all_users)
    return render_template('index.html', users = all_users )

@app.route('/createUser', methods=['POST'])
def create():
    mysql = connectToMySQL('users_registration')
    session['first_name']= request.form['first_name']
    session['last_name']= request.form['last_name']
    session['email']= request.form['email']
    
    
    if len(request.form['first_name']) < 1 and len(request.form['last_name'])<1:
        flash("Frist Name cannot be empty.")
        return redirect("/")
    if (request.form['first_name']).isalpha== False and (request.form['last_name']).isalpha == False:
        flash("Must be Alphabet")
        return redirect ("/")
    if request.form['password'] != request.form['password_confirmation']:
        flash("Passwords are not a match.")
        return redirect("/")
    if len(request.form['password']) <7:
        flash("Password cannot be less then 8 characters")
        return redirect("/")
    query = "SELECT email FROM users WHERE email = %(email)s;"
    data = {
            'email': request.form['email'],
            }
    if mysql.query_db(query,data) != ():
            flash("Email already exist.")
            return redirect('/')
    if not EMAIL_REGEX.match(request.form['email']):
        print("something")
        flash("Invalid Email Address!")
        return redirect('/')
    if len(request.form['email']) < 1: 
        flash("Email cannot be blank ")
        return redirect('/')
    
    
    # include some logic to validate user input before adding them to the database!
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])  
    print(pw_hash)  
    # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'
    # be sure you set up your database so it can store password hashes this long (60 characters)
    query = "INSERT INTO users (email, password, first_name, last_name) VALUES (%(email)s, %(password_hash)s,%(first_name)s,%(last_name)s);"
    # put the pw_hash in our data dictionary, NOT the password the user provided
    data = { "email" : request.form['email'],
            "password_hash" : pw_hash, 
            'first_name': request.form['first_name'],
            'last_name':  request.form['last_name']}
    mysql.query_db(query, data)
    # never render on a post, always redirect!
    mysql = connectToMySQL('users_registration')
    return render_template('index2.html')
@app.route("/log", methods = ['POST'])
def log():
    print("YOOOO")
    return render_template("index3.html")
@app.route("/in", methods = ['POST'])
def login():
    print("yooo")
    if len(request.form['password']) <1:
        flash("Password cannot be empty.")
        return render_template('index3.html')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) 
    print(pw_hash)
    query = "SELECT * FROM users_registration.users WHERE email = %(email)s;"
    data = {
            'email': request.form['email'],
            }
    result= mysql.query_db(query,data)
    if mysql.query_db(query,data) == ():
        flash("Please try again.")
        return render_template('index3.html')
    if bcrypt.check_password_hash(result[0]['password'],request.form['password']):
        if mysql.query_db(query,data) == ():
            flash("Please try again.")
            return render_template('index3.html')
        return render_template("index2.html")
    else:
        flash("Please try again")
        return redirect("/log")
if __name__=="__main__":
    app.run(debug=True)



