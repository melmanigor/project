from flask import Flask,render_template,request,redirect,url_for,abort,flash,send_from_directory,session
import webbrowser
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash
from threading import Timer
from src.dal.show_table import Show_table
from test2.test_db_connect_config import host,dbname,user,password
from test2.test_db_connect import Test_db_connect

app=Flask(__name__,template_folder='../../ui/templates')

@app.route("/vacations")
def show_vacation():
    db=Test_db_connect(host=host,dbname=dbname,user=user,password=password)
    dal=Show_table(db)
    rows=dal.get_table("vacations")
    db.close()
    vacations=[]
    for row in rows:
        vacations.append({
            'id':row[0],
            'country_id':row[1],
            'description':row[2],
            'start_date':row[3].isoformat(),
            'end_date':row[4].isoformat(),
            'file_img':row[5],
            'price':row[6]
        })
    return render_template("vacation.html",vacations=vacations)
if __name__=='__main__':
    app.run(debug=True)