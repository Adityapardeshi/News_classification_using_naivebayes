from datetime import datetime
import mysql.connector
from flask import redirect, url_for

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
        return redirect(url_for('register'))

    def login(self, data):
        email = data['email']
        password = data['password']
        self.cur.execute("SELECT * FROM userData WHERE email = %s and password = %s", (email, password))
        user = self.cur.fetchone()
        if user:
            return redirect(url_for('home'))
        else :
            return "Invalid email or password"
