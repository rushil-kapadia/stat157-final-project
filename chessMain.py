from flask import Flask, render_template, request, url_for, flash, redirect, Markup
from questionGen import question_gen
from scoring import store_score, store_plots
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b4a5d0208a726a5d1c0fd37324feba25506'
mg = []
solution = [0]
fens = [0]

@app.route("/", methods=('GET', 'POST'))
def main():
    if request.method == 'POST':
        lower = request.form['lower']
        upper = request.form['upper']
        confidence = request.form['confidence']
        sol = solution[0]
        fen = fens[0]
        if not lower or len(lower) < 1:
            lower = 0
        if not upper or len(upper) < 1:
            upper = 0
        flash("Score: " + str(round(store_score(float(confidence), float(sol), float(lower), float(upper)), 2)))
        mg.append({'lower': lower, 'upper': upper, "confidence": int(float(confidence) *100), "solution": sol, "fen":fen, "fenUrl": "https://lichess.org/analysis/fromPosition/" + str(fen).replace(' ', '_')})
        return redirect(url_for('main'))
    solution.pop()
    fens.pop()
    soll, fen = question_gen()
    solution.append(soll)
    fens.append(fen)
    svg = open('data/game.svg').read
    drawing = svg2rlg("data/game.svg")
    renderPDF.drawToFile(drawing, "static/chessImg.pdf")
    return render_template('main.html', mg=mg, svg=Markup(svg))

@app.route("/data")
def data():
    store_plots()
    return render_template('data.html')

@app.route("/help")
def help():
    return render_template('help.html')
