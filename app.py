from setup import database
from flask import Flask, render_template, request, redirect, jsonify
import sqlite3 as sql
from Format import FormatDate
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', path = '/')
 
@app.route('/players', methods = ['GET', 'POST', 'PUT'])
def players():
    rows = ''
    if request.method == 'GET':
        con = database()
        con.row_factory = sql.Row
        cur = con.cursor(dictionary=True)
        cur.execute("""SELECT Player.playerID, name, ranking, age, gender, originCountry, COALESCE(SUM(CompetesIn.wins), 0) AS totalWins
            FROM Player LEFT JOIN CompetesIn ON Player.playerID = CompetesIn.playerID 
            GROUP BY Player.playerID;""")
        rows = cur.fetchall()
        con.close()
        return render_template("players.html", rows = rows, path = '/players')
   
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
            con.close()
            return redirect('/players')
            
    elif request.method == 'PUT':
        try:
            data = request.json
            con = database()
            cur = con.cursor(dictionary=True)
            player = data.get('playerID')
            name = data.get("name")
            ranking = data.get("ranking")
            age = data.get("age")
            gender = data.get("gender")
            country = data.get("originCountry")
            cur.execute('UPDATE Player SET name = %s, ranking=%s, age=%s,gender=%s,OriginCountry=%s \
                WHERE playerID=%s', (name, ranking, age, gender, country, player))
            con.commit()
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        finally:
            con.close()
            


@app.route('/delete-player/<playerID>')
def deletePlayer(playerID):
    if request.method =='GET':
        try:
            con = database()
            cur = con.cursor()
            cur.execute('DELETE FROM Player WHERE playerID = %s', (playerID,))
            con.commit()
            
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        
        finally:
            con.close()
            
    return redirect('/players')
        
@app.route('/tournaments', methods = ['GET', 'POST','PUT'])
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
        return render_template("tournaments.html", rows = rows, path = '/tournaments')
            
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
                
    elif request.method == 'PUT':
        try:
            data = request.json
            print(data)
            con = database()
            cur = con.cursor(dictionary=True)
            tournament = data.get('tournamentName')
            print(tournament)
            opens = data.get('opens')
            closes = data.get('closes')
            print(closes)
            cost = data.get('cost')
            cost = cost[1:]
            country = data.get('country')
            print(country)
            
            
            cur.execute('UPDATE Tournament SET registrationDate = %s, deadlineDate=%s, cost=%s, country=%s\
                WHERE tournamentName=%s', (opens, closes, cost, country, tournament))
            con.commit()
            return jsonify({'success': True}), 200
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            con.close()


@app.route('/delete-tournament/<tournamentName>')
def deleteTournament(tournamentName):
    if request.method =='GET':
        try:
            con = database()
            cur = con.cursor()
            cur.execute('DELETE FROM Tournament WHERE tournamentName = %s', (tournamentName,))
            con.commit()
            
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        
        finally:
            con.close()
            
    return redirect('/tournaments')

@app.route('/stadiums', methods = ["GET", "POST", "PUT"])
def stadiums():
    if request.method == "GET":
        con = database()
        con.row_factory = sql.Row
        cur = con.cursor(dictionary=True)
        cur.execute('''SELECT * FROM Stadium''')
        rows = cur.fetchall()
        con.close()
        return render_template("stadiums.html", rows = rows, path = '/stadiums')
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
    elif request.method == 'PUT':
        try:
            data = request.json
            con = database()
            cur = con.cursor(dictionary=True)
            stadium = data.get('stadiumName')
            surface = data.get("surface")
            occupancy = data.get("occupancy")
            
            cur.execute('UPDATE Stadium SET surface = %s, occupancy=%s\
                WHERE stadiumName=%s', (surface, occupancy, stadium))
            con.commit()
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        finally:
            con.close()
    


@app.route('/delete-stadium/<stadiumName>')
def deleteStadium(stadiumName):
    if request.method =='GET':
        try:
            con = database()
            cur = con.cursor()
            cur.execute('DELETE FROM Stadium WHERE stadiumName = %s', (stadiumName,))
            con.commit()
            
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        
        finally:
            con.close()
            
    return redirect('/stadiums')

@app.route('/other')
def other():
    con = database()
    con.row_factory = sql.Row
    cur = con.cursor(dictionary=True)
        
    cur.execute('''SELECT PlaysAt.playerID, name, stadiumName FROM PlaysAt,Player WHERE PlaysAt.playerID = Player.playerID''')
    playsAt = cur.fetchall()
    cur.execute('''SELECT tournamentName, stadiumName FROM HostedAt''')
    hostedAt = cur.fetchall()
    cur.execute('''SELECT CompetesIn.playerID, name, tournamentName, wins FROM CompetesIn, Player WHERE CompetesIn.playerID = Player.playerID''')
    competesIn = cur.fetchall()
    cur.execute('''SELECT name, playerID FROM Player''')
    players = cur.fetchall()
    cur.execute('''SELECT tournamentName FROM Tournament''')
    tournaments = cur.fetchall()
    cur.execute('''SELECT stadiumName FROM Stadium''')
    stadiums = cur.fetchall()

    con.close()
    return render_template('other.html', playsAt = playsAt, hostedAt = hostedAt, competesIn = competesIn, 
                           players = players, tournaments = tournaments, stadiums = stadiums, path = '/other')
    
@app.route('/addPlaysAt', methods = ['GET', 'POST'])
def addPlaysAt():
    if request.method == 'POST':
        try:
            con = database()
            cur = con.cursor()
            
            player = request.form['player']
            stadium = request.form['stadium']
            
            cur.execute('INSERT INTO PlaysAt (playerID, stadiumName)\
                VALUES (%s , %s)', (player, stadium))
            
            con.commit()
            
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        
        finally:
            con.close()
        
    return redirect('/other')
     
@app.route('/deletePlaysAt/<playerID>-<stadiumName>')
def deletePlaysAt(playerID, stadiumName):
    try:
        con = database()
        cur = con.cursor()
        
        cur.execute('DELETE FROM PlaysAt WHERE playerID = %s AND stadiumName = %s', (playerID, stadiumName))
        con.commit()
         
    except Exception as e:
        con.rollback()
        # For debugging purposes, print or log the traceback
        print("Exception occurred:", e)
        traceback.print_exc()
        print('exception')
        
    finally:
        con.close()
            
    return redirect('/other') 

@app.route('/addHostedAt', methods = ['POST'])
def addHostedAt():
    if request.method == 'POST':
        try:
            con = database()
            cur = con.cursor()
            
            tournament = request.form['tournament']
            stadium = request.form['stadium']
            
            cur.execute('INSERT INTO HostedAt (tournamentName, stadiumName)\
                VALUES (%s , %s)', (tournament, stadium))
            
            con.commit()
            
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        
        finally:
            con.close()
        
    return redirect('/other')

@app.route('/deleteHostedAt/<tournamentName>-<stadiumName>')
def deleteHostedAt(tournamentName, stadiumName):
    try:
        con = database()
        cur = con.cursor()
        
        cur.execute('DELETE FROM HostedAt WHERE tournamentName = %s AND stadiumName = %s', (tournamentName, stadiumName))
        con.commit()
         
    except Exception as e:
        con.rollback()
        # For debugging purposes, print or log the traceback
        print("Exception occurred:", e)
        traceback.print_exc()
        print('exception')
        
    finally:
        con.close()
            
    return redirect('/other') 

@app.route('/addCompetesIn', methods = ['POST'])
def addCompetesIn():
    if request.method == 'POST':
        try:
            con = database()
            cur = con.cursor()
            
            player = request.form['player']
            tournament = request.form['tournament']
            wins = request.form['wins']
            
            cur.execute('INSERT INTO CompetesIn (playerID, tournamentName, wins)\
                VALUES (%s , %s, %s)', (player, tournament, wins))
            con.commit()
            
        except Exception as e:
            con.rollback()
            # For debugging purposes, print or log the traceback
            print("Exception occurred:", e)
            traceback.print_exc()
            print('exception')
        
        finally:
            con.close()
        
    return redirect('/other')

@app.route('/deleteCompetesIn/<playerID>-<tournamentName>')
def deleteCompetesIn(playerID, tournamentName):
    try:
        con = database()
        cur = con.cursor()
        
        cur.execute('DELETE FROM CompetesIn WHERE playerID = %s AND tournamentName = %s', (playerID, tournamentName))
        con.commit()
         
    except Exception as e:
        con.rollback()
        # For debugging purposes, print or log the traceback
        print("Exception occurred:", e)
        traceback.print_exc()
        print('exception')
        
    finally:
        con.close()
            
    return redirect('/other') 
if __name__ == '__main__':
    app.run(debug = True)