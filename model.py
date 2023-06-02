from datetime import datetime
import mysql.connector
from flask import redirect, url_for, session, render_template
import json

class user_model():
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost", user="root", password="1234", database="newsx")
        self.conn.autocommit = True
        self.cur = self.conn.cursor(dictionary=True)
        print("success")
    def register(self, data):
        name = data['name']
        email = data['email']
        password = data['password']
        dob = (data['dob'])
        country = data['country']
        self.cur.execute("INSERT INTO userData (name, email, password, dob, country) VALUES (%s, %s, %s, %s, %s)", (name, email, password, dob, country))
        return redirect(url_for('select_interests'))

    def login(self, data):
        email = data['email']
        password = data['password']
        self.cur.execute("SELECT * FROM userData WHERE email = %s and password = %s", (email, password))
        user = self.cur.fetchone()

        if user:
            session['email'] = email
            return redirect(url_for('home'))
        else :
            return render_template("login.html", message="Invalid email or password")

    def select_interests(self, data):

        check = data.getlist('checkbox')
        dictionary = {
            "email": session['email'],
            "categories": check
        }

        with open("sample.json", 'r+') as file:
            userFound = False
            file_data = json.load(file)
            #check if email already exists in json file
            for i in range(len(file_data["userPreference"])):
                if file_data["userPreference"][i]['email'] == session['email']:
                    file_data["userPreference"][i]['categories'] = check
                    file.seek(0)
                    json.dump(file_data, file)
                    file.truncate()
                    userFound = True
                    break;
                
            if(userFound!=True):
                file_data["userPreference"].append(dictionary)
                file.seek(0)
                json.dump(file_data, file)
                file.truncate()
    
        return redirect(url_for('home'))

    def get_age(self):
        # get user's dob from database and calculate age
        self.cur.execute("SELECT dob FROM userData WHERE email = %s", (session['email'],))
        dob = self.cur.fetchone()
        #convert dob to string
        dob = dob['dob'].strftime('%Y-%m-%d')
        dob = datetime.strptime(dob, '%Y-%m-%d')
        dob = datetime.now() - dob
        dob = dob.days/365
        #make dob an integer
        dob = int(dob)
        return dob