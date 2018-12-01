
from flask import Flask, jsonify, url_for, json, render_template, redirect, request, session, make_response
import sqlite3 as sql
import os
import math
app = Flask(__name__)


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    error = None
    if request == 'POST':
        ticker = request.form['username']
        validate = validate_ticker(ticker)

        if validate == False:
            error = 'Invalid credentials. Please try again'

        else:

            return render_template('/analysis.html/?ticker=ticker')
    else:
        print "DEBUG: save() GET method was called"
    return render_template('home.html', error=error)


def validate_ticker(ticker):
    con = sql.connect('stock.db')
    validate = False

    with con:
        cur = con.cursor()
        cur.execute('select value from store')
        rows = cur.fetchall()
        for row in rows:
            tick = row[0]

            if(tick == ticker):
                validate = True
    return validate


@app.route("/analysis", methods=['GET', 'POST'])
def analysis():
    ticker = request.args.get('ticker')
    con = sql.connect('stock.db')
    with con:
        cur = con.cursor()
        cur.execute("select * from analysis where ticker=(?)", (ticker,))
        rows = cur.fetchone()
        con.commit()
    return (render_template('/analysis.html', rows=rows))


if __name__ == '__main__':
    app.run(debug=True)
