from flask import Flask,render_template, request,jsonify
from flask_cors import CORS
from chat import get_response

# PYODBC libraries

import pyodbc
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, MetaData, Table, select
import sqlalchemy
import urllib
from six.moves import urllib
import webbrowser


import time

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os


test_list = [1,2] 

server = 'MBSDEVGGN65414' # server name````````````````
database = 'URL_test' # database name



conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';trusted_connection=YES;')
cursor = conn.cursor()


app=Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def login_page():
    msg = None
    if request.method == "POST": 
        user = request.form["username"]
        pasword = request.form["password"]
        # query="select * from credentials where Username=%s and pasword=%s"
        cursor.execute("select * from credentials where credentials.Username= ? and credentials.pasword=?", user,pasword)
        record = cursor.fetchone()
        if record: 
            return render_template("base.html",username=user)
        else:
            msg = 'Invalid Username or Password !'
            return render_template("Login.html", error=msg)
    return render_template("Login.html")
@app.route('/', methods=["GET"])
def index_get():
    return render_template("base.html")

@app.route("/predict", methods=["POST"])
def predict():
    while True:
        text=request.get_json().get("message") 
        test_list.append(text)

        if  test_list[-1]!="Please write your query in short.":
            response = get_response(text) 
            message={"answer":response}
            return jsonify(message)       
        if test_list[-1]=="Please write your query in short.":
            #Please write your query in short
            response = "Mail Sent!"
            message={"answer":response}
            return jsonify(message)

if __name__ =="__main__":
    app.run(debug=True)