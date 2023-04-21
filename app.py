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
#from six.moves import urllib


#Mail monitoring Libraries

# mail sending lib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os


#function for mail drafting
def message(subject="Sahipay health Notification", 
            text="", img=None,
            attachment=None):
    
    # build message contents
    msg = MIMEMultipart()
      
    # Add Subject
    msg['Subject'] = subject  
      
    # Add text contents
    msg.attach(MIMEText(text))  
  
    # Check if we have anything
    # given in the img parameter
       
    return msg


server = 'MBSDEVGGN65414' # server name
database = 'URL_test' # database name



conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';trusted_connection=YES;')
cursor = conn.cursor()

# Getting all the Mobile Numbers
query ="select * from [URL_test].[dbo].[CustomerDetai] "

df = pd.read_sql(query, conn)

Mobile_No=df["MobileNo"]





app=Flask(__name__)

@app.route('/', methods=["GET"])
def index_get():
    return render_template("base.html")


@app.route("/predict", methods=["POST"])
def predict():
    text=request.get_json().get("message")   #custmer response
    # TODO: checkif text is valid

    deta=df[df["MobileNo"]==text]
    # if the value is YES the ask user to input the query and 
    
    #checking if mobile no avaiable in dataframe or not
    no = deta.empty
    
    

    # Mobile no +Aadhaar card last 4 digit 

    #Name first 4 characters + DOB(DD/MM/YY)
    
    # If data frame not empty (is mobile no is there) then:
    if no != True:

        query ="select * from [URL_test].[dbo].[CustomerDetai] where MobileNo = ?"
    
        cursor.execute(query,[text])

        for row in cursor.fetchall():
            data=str(row)

        response=data
        message = {"answer":response}
        return jsonify(message)


    #for mail part
    test_list = []      
    test_list.append(text)

    if test_list[-2]=='YES':
        mail=text
        print(mail)
        smtp = smtplib.SMTP('manipalgroup.info')
        smtp.ehlo()
        smtp.starttls()
        smtp.login('mrinal.sharma', 'mr!nLs#rm$414')
            
        msg = message(subject="Sahibnk demo query", text = mail)

        # Make a list of emails, where you wanna send mail
        #ankit.chauhan@manipalgroup.info","rohan.shetty@manipalgroup.info
        to = ["ankit.chauhan@manipalgroup.info","rohan.shetty@manipalgroup.info" ]

        # Provide some data to the sendmail function!dfs
        smtp.sendmail(from_addr='mrinal.sharma@manipalgroup.info',
                        to_addrs=to, msg=msg.as_string())

         # Finally, don't forget to close the connection
                        

        response ="Done!, your query has been mailed to our customer support they will get back to you soon"
        message={"answer":response}

        return jsonify(message)

    
    response = get_response(text)
    message={"answer":response}
    return jsonify(message)


if __name__ =="__main__":
    app.run()


  