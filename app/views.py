from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('public/index.html')

@app.route('/cv')
def cv():
    return render_template('public/cv.html') 

@app.route('/blog')
def blog():
    return render_template('public/blog.html') 

@app.route('/websynth')
def websynth():
    return render_template('public/websynth.html') 
