from flask import render_template
from bookapp import app

@app.route('/')
def index():
    return render_template('index.html', value='Hello World!')
