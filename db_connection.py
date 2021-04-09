import mysql.connector


# function that connects to mySQL database

def connect_db(host,user,password,database):
    try:
        my_db = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
        )

        isConnected = my_db.is_connected()

        if(isConnected):
            print("Established database connection")
        
        return my_db
    
    except:
        print("not connected")




