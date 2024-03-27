'''
Due: 02/21/2024 Frank Marino, fmm20a. The program in this file
is the individual work of Frank Marino
'''

from flask import Flask, render_template, request
from datetime import datetime
import sqlite3 as sql
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/listAll')
def list_genre():
    return render_template('getReviews.html')

@app.route('/top5')
def top5():
    return render_template('getYear.html')

@app.route('/enternew')
def new_review():
    return render_template('addReview.html')

@app.route('/addrec', methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            title = request.form['Title']
            director = request.form['Director']
            year = request.form['Year']
            genre = request.form['Genre']
            
            username = request.form['Username']
            review = request.form['Review']
            rating = request.form['Rating']
            
            rating = float(rating)
            current_datetime = datetime.now()
            movieid = title[:6] + str(year)
            
            with sql.connect("movieData.db") as con:
                cur = con.cursor()
                
                cur.execute("SELECT MovieID FROM Movies WHERE MovieID = ?", (movieid,))
                existing_movie = cur.fetchone()
                
                if existing_movie:
                    print("MovieID already exists")
                else:
                    cur.execute("INSERT INTO Movies (MovieID, Title, Director, Genre, Year) VALUES (?,?,?,?,?)",
                                (movieid, title, director, genre,  year))
                
                cur.execute("INSERT INTO Reviews (Username, MovieID, ReviewTime, Rating, Review) VALUES (?,?,?,?,?)",
                            (username, movieid, current_datetime, rating, review))
                con.commit()
                
        except sql.Error as e:
            con.rollback()
            print("SQL error:", e)
        except Exception as e:
            con.rollback()
            print("Error:", e)
            print("Not added")
        
        finally:
            return render_template("index.html")
            con.close()
        
@app.route('/getGenre', methods = ['GET'])
def getGenre():   
    genre = request.args.get('Genre')
    with sql.connect("movieData.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
            
        cur.execute('''SELECT Movies.Title, Movies.Director, Reviews.Review, Reviews.Rating 
                    FROM Reviews
                    INNER JOIN Movies on Reviews.MovieID = Movies.MovieID
                    WHERE Genre = ?''', (genre,))
            
        rows = cur.fetchall()
        return render_template("listByGenre.html", rows = rows)
        con.close()
    
@app.route('/getYear', methods = ['GET'])
def getYear():   
    year = request.args.get('Year')
    with sql.connect("movieData.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
            
        cur.execute('''SELECT Movies.Title, Movies.Genre, AVG(Reviews.Rating) AS avg_Rating
                    FROM Movies
                    INNER JOIN Reviews ON Movies.MovieID = Reviews.MovieID
                    WHERE Year = ?
                    GROUP BY Movies.Title
                    ORDER BY avg_Rating DESC
                    LIMIT 5''', (year,))
            
        rows = cur.fetchall()
        return render_template("bestInYear.html", rows = rows) 
        con.close()
    
if __name__ == '__main__':
    app.run(debug = True)