from flask import Flask,url_for,render_template,request,redirect,session,g
from dashboard import get_data
from werkzeug.security import generate_password_hash,check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_data(error):
    if hasattr(g, 'data_db'):
        g.data_db.close()

def current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_data()
        user_details = db.execute('select * from uses where name = ?',[user])
        user = user_details.fetchone()
    return user 

@app.route("/") 
def home():
    user = current_user()
    return render_template('home1.html',user = user)

@app.route("/login" ,methods=["GET","POST"])
def login():
    error = None
    db = get_data()
    
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        
        if not name or not password:
            error = "username or password should not be empty"
            return render_template('login.html',lo_error = error)
        user = db.execute('select * from uses where name = ?',[name])
        user = user.fetchone()

        if user:
            if check_password_hash(user['password'],password):
                session['user'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                error= "user name or password did not match"
        else:
            error= "user name or password did not match"
    return render_template('login.html',lo_error = error )

@app.route("/register",methods=["POST","GET"])
def register():
    user = current_user()
    db=get_data()
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        if not name or not password:
            error = "username and password should not be empty"
            return render_template('registration.html',ris_error = error)
        h_pass = generate_password_hash(password)
        check_user = db.execute('select * from uses where name = ?',[name])
        existing_user = check_user.fetchone()
        if existing_user:
            error = "username already in use"
            return render_template('registration.html',ris_error = error)

        db.execute('insert into uses (name , password) values (?,?)',[name,h_pass])
        db.commit()
        return redirect(url_for('home'))
    return render_template('registration.html',user = user)

@app.route("/dashboard")
def dashboard():
    user = current_user()
    db = get_data()
    details = db.execute('select * from emp')
    info = details.fetchall()
    return render_template('dashboard.html',user = user,info = info)

@app.route("/addnewemployee" , methods =['POST','GET'] )
def addnewemployee():
    user = current_user()
    db = get_data()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        
        if not name or not phone or not email or not address:
            error = "Fill all the fields "
            return render_template('addnewemployee.html',error = error)
        
        db.execute('insert into emp (name,phone,email,address) values (?,?,?,?)',[name,phone,email,address])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addnewemployee.html',user = user)

@app.route("/singleemployee/<int:eid>")
def singleemployee(eid):
    user = current_user()
    db=get_data()
    emp_details = db.execute('select * from emp where empid = ?',[eid])
    profile = emp_details.fetchone()
    return render_template('singleemployee.html',user = user,profile = profile)

@app.route('/fetchone/<int:eid>')
def fetchone(eid):
    user = current_user()
    db=get_data()
    emp_details = db.execute('select * from emp where empid = ?',[eid])
    profile = emp_details.fetchone()
    return render_template('update.html',user = user,profile = profile)

@app.route("/update" , methods = ["POST","GET"])
def update():
    user = current_user()
    db = get_data()
    if request.method == "POST":
        empid = request.form['empid']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']       
        db.execute('update emp set (name,phone,email,address) = (?,?,?,?) where empid = ? ',\
                   [name,phone,email,address,empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('update.html',user = user)

@app.route('/deleteemp/<int:eid>', methods = ["POST","GET"])
def delete(eid):
    user = current_user()
    db = get_data()
    if request.method == "GET":
        db.execute('delete from emp where empid = ?',[eid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user = user)

@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)