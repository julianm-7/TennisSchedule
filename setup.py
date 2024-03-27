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
    
    '''
    
    cur.execute("""CREATE TABLE Player(
        playerID INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR (140),
        ranking INT,
        age INT NOT NULL, 
        gender CHAR(6) NOT NULL,
        originCountry VARCHAR(64) NOT NULL);""")
        
    cur.execute("""CREATE TABLE Tournament(
        tournamentName VARCHAR(64) PRIMARY KEY,
        registrationDate DATE NOT NULL,
        deadlineDate DATE NOT NULL, 
        cost INT NOT NULL,
        country VARCHAR(64) NOT NULL);""")
        
    cur.execute("""CREATE TABLE Stadium(
        stadiumName VARCHAR(64) PRIMARY KEY,
        surface CHAR(5) NOT NULL,
        occupancy INT NOT NULL);""")
        
    cur.execute("""CREATE TABLE CompetesIn(
        playerID INT,
        tournamentName VARCHAR(64),
        wins INT,
        losses INT,
        date DATE,
        PRIMARY KEY (playerID, tournamentName),
        FOREIGN KEY (playerID) REFERENCES Player(playerID),
        FOREIGN KEY (tournamentName) REFERENCES Tournament(tournamentName));""")
        
    cur.execute("""CREATE TABLE PlaysAt(
        playerID INT,
        stadiumName VARCHAR(64),
        wins INT,
        losses INT,
        PRIMARY KEY (playerID, stadiumName),
        FOREIGN KEY (playerID) REFERENCES Player(playerID),
        FOREIGN KEY (stadiumName) REFERENCES Stadium(stadiumName));""")
        
    cur.execute("""CREATE TABLE HostedAt(
        tournamentName VARCHAR(64),
        stadiumName VARCHAR(64),
        PRIMARY KEY (tournamentName, stadiumName),
        FOREIGN KEY (tournamentName) REFERENCES Tournament(tournamentName),
        FOREIGN KEY (stadiumName) REFERENCES Stadium(stadiumName));""")
    '''    
    conn.close()


## establishing connection with MySQL server
    """
    using mysql.connector.connect
    """