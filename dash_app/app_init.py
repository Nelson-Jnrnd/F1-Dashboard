from asyncio import current_task
from crypt import methods
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'secret' # Change this to a more secure key