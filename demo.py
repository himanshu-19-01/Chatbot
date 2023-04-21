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
chat_response=[1,2]
username=""



server = 'DESKTOP-SAAQPQ1'  # server name
database = 'Login_table'# database name
# server = 'MBSDEVGGN65414' # server name````````````````
# database = 'URL_test' # database name



# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';trusted_connection=YES;')
# cursor = conn.cursor()
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';trusted_connection=YES;''UID=sa;''PWD=914913;')
cursor = conn.cursor()

# Getting all the Mobile Numbers
# query ="select * from [URL_test].[dbo].[CustomerDetai]"

# df = pd.read_sql(query, conn)

#Mobile_No=df["MobileNo"]    


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
            return render_template("index.html", error=msg)
    return render_template("index.html")
@app.route('/', methods=["GET"])
def index_get():
    return render_template("base.html")

@app.route("/predict", methods=["POST"])
def predict():
    
    while True:
                #function for mail drafting
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

         
        text=request.get_json().get("message")   #customer response, datatype -string 
        # TODO: checkif text is valid

        #deta=df[df["MobileNo"]==text]
        # if the value is YES the ask user to input the query and 
        
        #checking if mobile no avaiable in dataframe or not
        #no = deta.empty

        # If data frame not empty (is mobile no is there) then:
        #if no != True:

            # query ="select * from [URL_test].[dbo].[CustomerDetai] where MobileNo = ?"
        
            # cursor.execute(query,[text])

            # for row in cursor.fetchall():
            #     data=str(row)

            # response=data
            # message = {"answer":response}
            # return jsonify(message)

        

        test_list.append(text)
        response = get_response(text) 
        chat_response.append(response) # handling chat bot response
        data = request.json
        message = data['message']
        print("hello")
        print(data)
        payload = request.json
        sendmail = payload.get('sendmail',False)
        hindibtn=payload.get('hindi',False)
        if hindibtn:
            response = " नमस्ते मैं आपकी कैसे सहायता कर सकती हूँ?"
            message={"answer":response}
            return jsonify(message)
        print(sendmail)
        if sendmail:
            # question1=test_list[-1]
            # smtp = smtplib.SMTP('manipalgroup.info')
            # smtp.ehlo()
            # smtp.starttls()
            # smtp.login('mrinal.sharma', 'Mrna$8shm4')
                
            # msg = message(subject="Sahibnk demo query", text =question1 )

            # # Make a list of emails, where you wanna send mail
            # to = ["ankit.chauhan@manipalgroup.info","rohan.shetty@manipalgroup.info","mrinal.sharma@manipalgroup.info","himanshumanral2003@gmail.com"]

            # # Provide some data to the sendmail function!dfs
            # smtp.sendmail(from_addr='mrinal.sharma@manipalgroup.info',
            #                 to_addrs=to, msg=msg.as_string())

            # time.sleep(10)                

            response = "We have recived your Query we will reach out to you"
            message={"answer":response}
            return jsonify(message)
            # return jsonify(message)
        # if response=="I do not understand If you need any further assist you can just write down your query or contact our customer support team on #9623461271 or if you want to send mail just TYPE 'YES'..."
        if  test_list[-1]!="YES":
            
            response = get_response(text) 
            message={"answer":response}
            return jsonify(message)       
        # else:
        #     #Please write your query in short
        #     response = "Please write your query in short"
        #     message={"answer":response}
        #     return jsonify(message)
 

        
        


if __name__ =="__main__":
    app.run(debug=True)



  