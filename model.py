from datetime import datetime
import mysql.connector
from flask import redirect, url_for, session
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
            return "Invalid email or password"


    def select_interests(self, data):

        check = data.getlist('checkbox')
        dictionary = {
            "email": "adityaopardeshi@gmail.com",
            "categories": check
        }

        with open("sample.json", 'r+') as file:
            file_data = json.load(file)
            file_data["userPreference"].append(dictionary)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    
        #print(check)
        return redirect(url_for('home'))