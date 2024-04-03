from setup import database
from flask import Flask, render_template, request
import sqlite3 as sql
from Format import FormatDate
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', path = '/')
 
@app.route('/players', methods = ['GET', 'POST'])
def players():
    rows = ''
    if request.method == 'GET':
        con = database()
        con.row_factory = sql.Row
        cur = con.cursor(dictionary=True)
        cur.execute('''SELECT * FROM Player''')
        rows = cur.fetchall()
        con.close()
        
    elif request.method == 'POST':
        try:
            con = database()
            cur = con.cursor(dictionary=True)

            name = request.form['name']
            ranking = request.form['ranking']
            age = request.form['age']
            gender = request.form['gender']
            country = request.form['country']
                        
            cur.execute('INSERT INTO Player(name, ranking, age, gender, originCountry)\
                VALUES(%s,%s,%s,%s,%s)', (name, ranking, age, gender, country))
            con.commit()
            
            
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        finally:
            con.row_factory = sql.Row
            cur.execute('''SELECT * FROM Player''')
            rows = cur.fetchall()
            con.close()
            
    return render_template("players.html", rows = rows, path = '/players')
        
@app.route('/tournaments', methods = ['GET', 'POST'])
def tournaments():
    rows = ''
    if request.method == 'GET':
        con = database()
        con.row_factory = sql.Row
        cur = con.cursor(dictionary=True)
        
        cur.execute('''SELECT * FROM Tournament''') 
        rows = cur.fetchall()
        con.close()
        
        for row in rows:
            row['registrationDate'] = FormatDate(row['registrationDate'])
            row['deadlineDate'] = FormatDate(row['deadlineDate'])
            
    elif request.method == 'POST':
        try:
            con = database()
            con.row_factory = sql.Row
            cur = con.cursor(dictionary=True)
            
            name = request.form['name']
            opens = request.form['opens']
            closes = request.form['closes']
            cost = request.form['cost']
            country = request.form['country']
                        
            cur.execute('INSERT INTO Tournament(tournamentName, registrationDate, deadlineDate, cost, country)\
                VALUES(%s,%s,%s,%s,%s)', (name, opens, closes, cost, country))
            con.commit()
            
            
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        finally:
            con.row_factory = sql.Row
            cur.execute('''SELECT * FROM Tournament''')
            rows = cur.fetchall()
            con.close()
            for row in rows:
                row['registrationDate'] = FormatDate(row['registrationDate'])
                row['deadlineDate'] = FormatDate(row['deadlineDate'])
    
    return render_template("tournaments.html", rows = rows, path = '/tournaments')

@app.route('/stadiums', methods = ["GET", "POST"])
def stadiums():
    if request.method == "GET":
        con = database()
        con.row_factory = sql.Row
        cur = con.cursor(dictionary=True)
        cur.execute('''SELECT * FROM Stadium''')
        rows = cur.fetchall()
        con.close()
    elif request.method == 'POST':
        try:
            con = database()
            cur = con.cursor(dictionary=True)

            name = request.form['name']
            surface = request.form['surface']
            occupancy = request.form['occupancy']
                        
            cur.execute('INSERT INTO Stadium(stadiumName, surface, occupancy)\
                VALUES(%s,%s,%s)', (name, surface, occupancy))
            con.commit()
            
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        finally:
            con.row_factory = sql.Row
            cur.execute('''SELECT * FROM Stadium''')
            rows = cur.fetchall()
            con.close()
    
    return render_template("stadiums.html", rows = rows, path = '/stadiums')

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
    cur.execute('''SELECT name, playerId FROM Player''')
    players = cur.fetchall()
    cur.execute('''SELECT tournamentName FROM Tournament''')
    tournaments = cur.fetchall()
    cur.execute('''SELECT stadiumName FROM Stadium''')
    stadiums = cur.fetchall()

    con.close()
    return render_template('other.html', playsAt = playsAt, hostedAt = hostedAt, competesIn = competesIn, 
                           players = players, tournaments = tournaments, stadiums = stadiums, path = '/other')

if __name__ == '__main__':
    app.run(debug = True)