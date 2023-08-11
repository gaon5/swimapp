from flask import Flask, url_for, request, redirect, render_template, session
from datetime import datetime
import mysql.connector
import config
import math
import bcrypt
import re



# When you gonna start, pip install -r requirements.txt


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = 'aHn6Zb7MstRxC8vEoF2zG3B9wQjKl5YD'


db_conn = None
connection = None


def get_cursor():
    global db_conn
    global connection
    connection = mysql.connector.connect(user=config.dbuser,
                                         password=config.dbpass,
                                         host=config.dbhost,
                                         database=config.dbname,
                                         autocommit=True)
    db_conn = connection.cursor()
    return db_conn


@app.route('/sample', methods=['GET', 'POST'])
def sample():
    sample_value = 1
    sql_data = get_cursor()
    sql = """SELECT * FROM sample_database WHERE sample_id=%s;"""
    sql_value = (sample_value,)
    sql_data.execute(sql, sql_value)
    sample_list = sql_data.fetchall()
    sql_data.close()

    return render_template('sample.html', sample_list=sample_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration:
    1. Validate POST data and ensure all necessary fields are present.
    2. Check the database to ensure no existing accounts share the same email or username.
    3. Validate email, password, and username formats using regex.
    4. If everything checks out, hash the password and insert the user into the database.
    5. Also insert the member's additional information (like first name, last name, phone number).
    
    """
    msg = ''

    if request.method == 'POST':
        # Ensure necessary fields are present
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number']
        if not all(field in request.form for field in fields):
            return render_template('register.html', msg="Please fill out the form!")

        username, password, email, first_name, last_name, phone_number= (request.form[field] for field in fields)

        # Check criteria
        with get_cursor() as cursor:
            cursor.execute('SELECT email, username FROM user_account WHERE email = %s OR username = %s', (email, username))
            existing_data = cursor.fetchone()
           
            if existing_data:
                existing_email, existing_username = existing_data
                if existing_email == email:
                    msg = 'An account with this email already exists!'
                if existing_username == username:
                    msg += ' An account with this username already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
                msg = 'Password must contain at least 8 characters, one letter and one number!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            else:
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

                cursor.execute('INSERT INTO user_account (username, password, email, is_member) VALUES (%s, %s, %s, 1)', (username, hashed, email))
                cursor.execute('SELECT user_id from user_account WHERE username = %s', (username,))
                user_id = cursor.fetchone()[0]

                cursor.execute('INSERT INTO member (user_id, first_name, last_name, phone_number) VALUES (%s, %s, %s, %s)', (user_id, first_name, last_name, phone_number))
                cursor.close()

                msg = 'You have successfully registered!'

    return render_template('register.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
