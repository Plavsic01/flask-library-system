from flask import *
import db_connection
import os



# Creating Flask App instance

app = Flask(__name__)

app.secret_key = os.urandom(16)

# Connecting to database

db = db_connection.connect_db("localhost","root","najbolji3","libraryDB")
db_cursor = db.cursor()


# Creating route endpoints


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/login",methods = ["POST","GET"])
def adminLogin():

    user = None
    admin_list = []

    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        session["user"] = user
        print(user + " " + password)
        
    # I WILL ADD THIS LATER

        sql_code = "SELECT * FROM admin WHERE adminName = '{}'AND adminPassword = '{}'".format(user,password)

        db_cursor.execute(sql_code)
        result = db_cursor.fetchall()

        for res in result:
            admin_list = list(res)


        return render_template("admin.html",username = user)
    
    else:
        if("user" in session):
            user = session["user"]
            print("user u sessionu je:" + session["user"])
            return redirect(url_for("admin"))

        return render_template("index_admin_login.html")

    


@app.route("/admin/logout")
def adminLogout():
    if("user" in session):
        session.pop("user",None)
        print("user vise nije u sessionu")
       
    return redirect(url_for("adminLogin"))