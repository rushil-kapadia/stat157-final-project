from flask import Flask, render_template, request, url_for, flash, redirect, Markup
from questionGen import question_gen
from scoring import store_score, store_plots
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pdf2image import convert_from_path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b4a5d0208a726a5d1c0fd37324feba25506'
mg = []
solution = [0]
fens = [0]

@app.route("/", methods=('GET', 'POST'))
def main(name="bob"):
    if request.method == 'POST':
        print(request.form)
        lower = request.form['lower']
        upper = request.form['upper']
        confidence = request.form['confidence']
        sol = solution[0]
        fen = fens[0]
        flash("Previous score: " + str(store_score(float(confidence), float(sol), float(lower), float(upper))))
        if not lower:
            lower = 0
        elif not upper:
            upper = 0
        else:
            mg.append({'lower': lower, 'upper': upper, "alok meme level": confidence, "alok_non_meme":sol, "alok_is_such_a_fen":fen})
            return redirect(url_for('main'))
    solution.pop()
    fens.pop()
    soll, fen = question_gen()
    solution.append(soll)
    fens.append(fen)
    print(solution)
    svg = open('data/game.svg').read
    drawing = svg2rlg("data/game.svg")
    renderPDF.drawToFile(drawing, "static/chessImg.pdf")
    return render_template('main.html', mg=mg, svg=Markup(svg))

@app.route("/data")
def data(name="tom"):
    store_plots()
    return render_template('data.html', name=name)
