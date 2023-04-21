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
  

       
    return msg



def predict():

    test_list = [1,2]   

    while True:
        text=input("Type user input: ")  #custmer response
        # TODO: checkif text is vali
        test_list.append(text)
        if test_list[-2]=='YES':
            question1=test_list[-1]
            print(question1)
            smtp = smtplib.SMTP('smtp.gmail.com',port=587 )
            smtp.ehlo()
            smtp.starttls()
            smtp.login('himanshumanral2003@gmail.com', '12345@Manral')
                
            msg = message(subject="Sahibnk demo query", text =question1 )

            # Make a list of emails, where you wanna send mail
            to = ["ankit.chauhan@manipalgroup.info","rohan.shetty@manipalgroup.info"]

            # Provide some data to the sendmail function!dfs
            smtp.sendmail(from_addr='himanshumanral20032gmail.com',
                            to_addrs=to, msg=msg.as_string())

            response = "We have recived your Query we will reach out to you"
            predict()

            
            
        
        if text != "YES":
        
            response = get_response(text)
        else:
            response = "Please write your query in short"
        


        # test_list.append(text)

        # if test_list[-2]=='YES':
        #     mail=text
        #     smtp = smtplib.SMTP('manipalgroup.info')
        #     smtp.ehlo()
        #     smtp.starttls()
        #     smtp.login('mrinal.sharma', 'mr!nLs#rm$414')
                
        #     msg = message(subject="Sahibnk demo query", text = mail)

        #     # Make a list of emails, where you wanna send mail
        #     to = ["ankit.chauhan@manipalgroup.info","rohan.shetty@manipalgroup.info"]

        #     # Provide some data to the sendmail function!dfs
        #     smtp.sendmail(from_addr='mrinal.sharma@manipalgroup.info',
        #                     to_addrs=to, msg=msg.as_string())

        #      # Finally, don't forget to close the connection
                            

        #     response ="Done!, your query has been mailed to our customer support they will get back to you soon"
        #     message={"answer":response}

        #     return jsonify(message)

        
        
        print(response)

        print(test_list)

predict()




  