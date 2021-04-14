from flask import *
import db_connection
import os

def select_all(prazna_lista):
        sql_code_librarian = "SELECT * FROM librarian"
        db_cursor.execute(sql_code_librarian)
        result_librarian = db_cursor.fetchall()

        for res in result_librarian:
            lista = list(res)
            prazna_lista.append(lista)

        return prazna_lista

def select_books(prazna_lista):
        sql_code_librarian = "SELECT * FROM books"
        db_cursor.execute(sql_code_librarian)
        result_librarian = db_cursor.fetchall()

        for res in result_librarian:
            lista = list(res)
            prazna_lista.append(lista)

        return prazna_lista

def select_admin(prazna_lista):
        sql_code_librarian = "SELECT * FROM admins"
        db_cursor.execute(sql_code_librarian)
        result_librarian = db_cursor.fetchall()

        for res in result_librarian:
            lista = list(res)
            prazna_lista.append(lista)

        return prazna_lista


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
    lista_admin = []
    admin_list = select_admin(lista_admin)

    if("user" in session):
        user = session["user"]

        if(user != admin_list[0][1]):
            session.pop("user",None)
            return redirect(url_for("login_admin"))

        return render_template("admin.html",ulogovan = user)
    else:
        return redirect(url_for("login_admin"))


@app.route("/librarian")
def librarian():
    user = session["user"]

    lista_admin = []

    admin_list = select_admin(lista_admin)

    if(user == admin_list[0][1]):
        session.pop("user",None)
        return redirect(url_for("login_librarian"))


    if("user" not in session):
        return redirect(url_for("login_librarian"))

    else:
        return render_template("librarian.html",ulogovan = user)


@app.route("/librarian/login",methods = ["POST","GET"])
def login_librarian():
    librarian_list = []

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
                    return redirect(url_for("librarian"))

    elif request.method == "GET":
        if("user" in session):
            user = session["user"]
            print("user u sessionu je librarian:" + session["user"])
            return redirect(url_for("librarian"))

        else:
            print("user nije u sessionu")
    return render_template("index_login.html")


# librarian functions come here

@app.route("/librarian/add",methods=["POST","GET"])
def add_books():
    if request.method == "POST":
        name = request.form["name"]
        author = request.form["author"]

        sql_code = "INSERT INTO books (bookname,bookauthor) VALUES ('{}','{}')".format(name,author)
        db_cursor.execute(sql_code)
        db.commit()

    return render_template("librarian_add_books.html")


@app.route("/librarian/view")
def view_books():

    if("user" in session):
        lista_knjiga = []
        lista = select_books(lista_knjiga)

        return render_template("librarian_view_books.html",lista_knjiga = lista)

    else:
        return redirect(url_for("login_librarian"))


# ovo treba zavrsiti
@app.route("/librarian/issue/book")
def issue_books():
    return render_template("librarian_issue_books.html")



@app.route("/admin/login",methods = ["POST","GET"])
def login_admin():

    user = None
    admin_list = []

    sql_code_admin = "SELECT * FROM admins"
    db_cursor.execute(sql_code_admin)
    result_admin = db_cursor.fetchall()

    for res in result_admin:
        admin_list = list(res)

    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if(user == admin_list[1] and password == admin_list[2]):
            print("admin konektovan")
            session["user"] = user
            return redirect(url_for("admin"))

      
    elif request.method == "GET":
        if("user" in session):
            user = session["user"]
            print("user u sessionu je admin:" + session["user"])
            return redirect(url_for("admin"))


        else:
            print("user nije u sessionu")
            return render_template("index_login.html")

    return render_template("index_login.html")

    


@app.route("/admin/add",methods=["GET","POST"])
def admin_add():
    user = session["user"]

    if(request.method=="POST"):

        username = request.form["username"]
        password = request.form["password"]
        
        is_true = True

        sql_code = "INSERT INTO librarian (librarianName,librarianPassword) VALUES ('{}','{}')".format(username,password)

        db_cursor.execute(sql_code)
        db.commit()

        return render_template("admin_add_librarian.html",ulogovan = user,name = username,is_name = is_true)

    

    return render_template("admin_add_librarian.html",ulogovan = user)

@app.route("/admin/view")
def admin_view():
    if("user" in session):
        librarian_list = []
        lista = select_all(librarian_list)

        return render_template("admin_view_librarian.html",lista_librarian = lista)

    else:
        return redirect(url_for("login_admin"))



@app.route("/admin/delete",methods=["GET","POST"])
def admin_delete():

    if("user" in session):
        librarian_list = []
        lista = select_all(librarian_list)

        if(request.method=="POST"):
            library_id = request.form["id"]
            library_id = int(library_id)
            
            for i in range(len(lista)):
                if(library_id == lista[i][0]):
                    sql_code = "DELETE FROM librarian WHERE idlibrarian = {}".format(library_id)
                    db_cursor.execute(sql_code)
                    db.commit()
                    return(render_template("admin_delete_librarian.html",msg = True,id=library_id)) 
                    

        return render_template("admin_delete_librarian.html")

    else:

        return redirect(url_for("login_admin"))

# LOGOUT ADMIN
@app.route("/logout/admin")
def logout_admin():
    if("user" in session):
        session.pop("user",None)
        print("user admin vise nije u sessionu")

    return redirect(url_for("login_admin"))

# LOGOUT LIBRARIAN
@app.route("/logout/librarian")
def logout_librarian():
    if("user" in session):
        session.pop("user",None)
        print("user librarian vise nije u sessionu")
       
    return redirect(url_for("login_librarian"))


# todo: add issue books, add view issued books and return books 
