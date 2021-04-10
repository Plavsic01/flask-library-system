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


@app.route("/librarian")
def librarian():
    return render_template("librarian.html")


@app.route("/login-librarian",methods = ["POST","GET"])
def login_librarian():
    librarian_list = []

    # LIBRARIAN DATA

    sql_code_librarian = "SELECT * FROM librarian"
    db_cursor.execute(sql_code_librarian)
    result_librarian = db_cursor.fetchall()

    for res in result_librarian:
        lista = list(res)
        librarian_list.append(lista)

    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        if(len(librarian_list) == 0):
            print("nema bibliotekara u bazi")

        elif(len(librarian_list) > 0):

           for i in range(len(librarian_list)):
                if(user == librarian_list[i][1] and password == librarian_list[i][2]):
                    print("bibliotekar konektovan")
                    session["user"] = user
                    is_librarian = True
                    is_admin = False
                    return redirect(url_for("librarian"))

    elif request.method == "GET":
        if("user" in session):
            user = session["user"]
            print("user u sessionu je librarian:" + session["user"])
            return redirect(url_for("librarian"))

        else:
            print("user nije u sessionu")
    return render_template("index_login.html")




@app.route("/login/admin",methods = ["POST","GET"])
def login_admin():

    user = None
    admin_list = []
    
    # ADMIN DATA
    sql_code_admin = "SELECT * FROM admins"
    db_cursor.execute(sql_code_admin)
    result_admin = db_cursor.fetchall()

    for res in result_admin:
        admin_list = list(res)
    

    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        

    # ZA ADMINA 
    
        if(len(admin_list) == 0):
            print("nema admina u bazi")

        elif(user == admin_list[1] and password == admin_list[2]):
            print("admin konektovan")
            session["user"] = user
            return redirect(url_for("index"))


                    
    elif request.method == "GET":
        if("user" in session):
            user = session["user"]
            print("user u sessionu je admin:" + session["user"])
            return redirect(url_for("admin"))

        else:
            print("user nije u sessionu")
        return render_template("index_login.html")

    


@app.route("/logout-admin")
def logout_admin():
    if("user" in session):
        session.pop("user",None)
        print("user admin vise nije u sessionu")
       
    return redirect(url_for("login_admin"))


@app.route("/logout-librarian")
def logout_librarian():
    if("user" in session):
        session.pop("user",None)
        print("user librarian vise nije u sessionu")
       
    return redirect(url_for("login_librarian"))