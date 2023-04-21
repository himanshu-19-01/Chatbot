from flask import Flask, render_template, request, jsonify
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

# E:\chatbot-deployment-main\chatbot-deployment-main\model.py
import time

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os

test_list = [1, 2]

server = 'DESKTOP-SAAQPQ1'  # server name
database = 'Login_table'  # database name

# server = 'MBSDEVGGN65414' # server name
# database = 'URL_test' # database name


# conn=pyodbc.connect('DRIVER={SQL Server};'
# 'SERVER=DESKTOP-SAAQPQ1;'
# 'database=Login_table;'
# 'Trusted_Connection=yes;')
# cursor=conn.cursor()
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';trusted_connection=YES;''UID=sa;''PWD=914913;')
cursor = conn.cursor()

# Getting all the Mobile Numbers
# query ="select * from [URL_test].[dbo].[CustomerDetai] "

# df = pd.read_sql(query, conn)

# Mobile_No=df["MobileNo"]


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def login_page():
    msg = None
    if request.method == "POST":
        user = request.form["username"]
        pasword = request.form["password"]
        # query="select * from credentials where Username=%s and pasword=%s"
        cursor.execute("select * from credentials where credentials.Username= ? and credentials.pasword=?", user,
                       pasword)
        record = cursor.fetchone()
        if record:
            return render_template("base.html")
        else:
            msg = 'Invalid Username or Password !'
            return render_template("Login.html", error=msg)
    print("login")
    return render_template("Login.html")


@app.route('/chatbot', methods=["GET"])
def index_get():
    return render_template("base.html")


@app.route("/predict", methods=["POST"])
def predict():
    while True:
        # function for mail drafting
        def message(subject="SahiBnk Demo",
                    text="", img=None,
                    attachment=None):

            # build message contents
            msg = MIMEMultipart()

            # Add Subject
            msg['Subject'] = subject

            # Add text contents
            msg.attach(MIMEText(text))
            return msg

        text = request.get_json().get("message")  # customer response, datatype -string
        # TODO: checkif text is valid

        # deta=df[df["MobileNo"]==text]
        # if the value is YES the ask user to input the query and

        # checking if mobile no avaiable in dataframe or not
        # no = deta.empty

        # If data frame not empty (is mobile no is there) then:
        # if no != True:

        #     query ="select * from [URL_test].[dbo].[CustomerDetai] where MobileNo = ?"

        #     cursor.execute(query,[text])

        #     for row in cursor.fetchall():
        #         data=str(row)

        #     response=data
        #     message = {"answer":response}
        #     return jsonify(message)

        test_list.append(text)

        if test_list[-2] == "1":
            question1 = test_list[-1]
            smtp = smtplib.SMTP('manipalgroup.info')
            smtp.ehlo()
            smtp.starttls()
            smtp.login('mrinal.sharma', 'Mrna$8shm4')

            msg = message(subject="Sahibnk demo query", text=question1)

            # Make a list of emails, where you wanna send mail
            to = ["ankit.chauhan@manipalgroup.info", "rohan.shetty@manipalgroup.info",
                  "mrinal.sharma@manipalgroup.info"]

            # Provide some data to the sendmail function!dfs
            smtp.sendmail(from_addr='mrinal.sharma@manipalgroup.info',
                          to_addrs=to, msg=msg.as_string())

            time.sleep(10)

            response = "We have recived your Query we will reach out to you"
            message = {"answer": response}
            return jsonify(message)

        if test_list[-1] != "1":

            response = get_response(text)
            message = {"answer": response}
            return jsonify(message)

        else:
            response = "Please write your query in short"
            message = {"answer": response}
            return jsonify(message)


if __name__ == "__main__":
    app.run()



