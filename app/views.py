from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('public/index.html')

@app.route('/cv')
def cv():
    return 'cv'

@app.route('/projects')
def projects():
    return 'projects'
