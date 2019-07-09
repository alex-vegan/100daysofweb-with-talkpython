from program import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/100Days')
def p100days():
    return render_template('100Days.html')
