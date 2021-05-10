#  Copyright (c) 2021 by Ole Christian Astrup. All rights reserved.  Licensed under MIT
#   license.  See LICENSE in the project root for license information.
#
import os
import logging
from logging.config import dictConfig
from ariadne import QueryType

#from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

from nlp.nlp import LanguageProcessor
from wolfram.wolframalpha import WolframAlpha
# debug settings
debug = eval(os.environ.get("DEBUG", "False"))

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers':{
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        "console": {
            "level": "DEBUG" if debug else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "DEBUG" if debug else "INFO",
        "handlers": ["console"] if debug else ["wsgi"],
    }
})

# Create the app
app = Flask(__name__, static_folder="static/", template_folder="static/")
app.debug = True
app.config["LOG_TYPE"] = "CSV"
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
toolbar = DebugToolbarExtension(app)
# The domain classes
nlp = LanguageProcessor(app.logger)
wolfram = WolframAlpha(app.logger)


#app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/any.db" # ToDo: Implement database store
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db = SQLAlchemy(app)

query = QueryType()


@app.route('/', methods=["GET", "POST"])
def hello():
    return 'A REST-ful GraphQL Server!' # ToDo: Create a welcome page

@app.route('/logs', methods=["GET", "POST"])
def root():
    """index page"""
    return render_template("index.html")

