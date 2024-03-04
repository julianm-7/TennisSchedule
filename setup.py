import mysql.connector
#pip install mysql-connector or use pip3 if error occurs

def database():
    hostname = "petsitter-db.c1qoyei4uiho.us-east-2.rds.amazonaws.com"
    username = "pet_user"
    password = "petsitter"
    db = mysql.connector.connect(
        host = hostname, 
        user = username, 
        passwd = password,
        database = "tennis_tournaments"
    )
    return db

conn = database()
cur = conn.cursor()
if __name__ == '__main__':
    
    #cur.execute("DROP TABLE Players;")
    
    cur.execute("""CREATE TABLE Players(
        playerId INT AUTO_INCREMENT PRIMARY KEY,
        ranking INT NOT NULL,
        age INT NOT NULL, 
        gender VARCHAR(40) NOT NULL,
        Password VARCHAR(64) NOT NULL,
        FirstName VARCHAR(64) NOT NULL,
        LastName VARCHAR(64) NOT NULL,
        Birthdate DATE NOT NULL,
        EmailAddress VARCHAR(64) NOT NULL,
        originCountry VARCHAR(64) NOT NULL);""")
    
        
    conn.close()