from setup import database
from flask import Flask, render_template, request
import sqlite3 as sql
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/players', methods = ['GET'])
def players():
    con = database()
    con.row_factory = sql.Row
    cur = con.cursor(dictionary=True)
        
    cur.execute('''SELECT * FROM Player''')
        
    rows = cur.fetchall()
    con.close()
    return render_template("players.html", rows = rows)

@app.route('/tournaments')
def tournaments():
    con = database()
    con.row_factory = sql.Row
    cur = con.cursor(dictionary=True)
        
    cur.execute('''SELECT * FROM Tournament''')
        
    rows = cur.fetchall()
    con.close()
    return render_template("tournaments.html", rows = rows)

@app.route('/stadiums')
def stadiums():
    con = database()
    con.row_factory = sql.Row
    cur = con.cursor(dictionary=True)
        
    cur.execute('''SELECT * FROM Stadium''')
    rows = cur.fetchall()
    con.close()
    return render_template("stadiums.html", rows = rows)

@app.route('/other')
def other():
    con = database()
    con.row_factory = sql.Row
    cur = con.cursor(dictionary=True)
        
    cur.execute('''SELECT name, stadiumName FROM PlaysAt,Player WHERE PlaysAt.playerID = Player.playerID''')
    playsAt = cur.fetchall()
    cur.execute('''SELECT tournamentName, stadiumName FROM HostedAt''')
    hostedAt = cur.fetchall()
    cur.execute('''SELECT name, tournamentName FROM CompetesIn, Player WHERE CompetesIn.playerID = Player.playerID''')
    competesIn = cur.fetchall()
    con.close()
    return render_template('other.html', playsAt = playsAt, hostedAt = hostedAt, competesIn = competesIn)

if __name__ == '__main__':
    app.run(debug = True)