from flask import render_template, request, redirect, url_for,\
        abort, send_from_directory, flash
from {[ name ]} import app
from models import db, MyModel

@app.route('/')
def index():
    return render_template('index.html')
