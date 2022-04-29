from flask import Flask, render_template, request, url_for, flash, redirect
from questionGen import question_gen
from scoring import compute_score

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b4a5d0208a726a5d1c0fd37324feba25506'
solution = -1

mg = []

@app.route("/", methods=('GET', 'POST'))
def main(name="bob"):
    if request.method == 'POST':
        print(request.form)
        lower = request.form['lower']
        upper = request.form['upper']
        confidence = request.form['confidence']

        if not lower:
            flash('lower is required!')
        elif not upper:
            flash('upper is required!')
        else:
            mg.append({'lower': lower, 'upper': upper, "alok meme level": confidence})
            return redirect(url_for('main'))
    solution = question_gen()
    return render_template('main.html', mg=mg)

@app.route("/data")
def data(name="tom"):
    return render_template('data.html', name=name)

# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']

#         if not title:
#             flash('Title is required!')
#         elif not content:
#             flash('Content is required!')
#         else:
#             messages.append({'title': title, 'content': content})
#             return redirect(url_for('index'))

#     return render_template('create.html')