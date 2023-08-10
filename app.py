from flask import Flask, url_for, request, redirect, render_template, session
from datetime import datetime
import mysql.connector
import config
import math
import bcrypt



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

# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests   
@app.route('/login/', methods=['GET', 'POST'])
def login():
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']

        # Check if account exists
        cursor = get_cursor()
        cursor.execute("SELECT * FROM user_account WHERE username = %s", (username,))
        account = cursor.fetchone()

        if account is not None:
            password_hash = account[3]

            # Check if the hashed password matches the one stored in the database
            if bcrypt.checkpw(user_password.encode('utf-8'), password_hash.encode('utf-8')):
                # If the passwords match, log the user in
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['is_member'] = account[4]
                session['is_instructor'] = account[5]
                session['is_admin'] = account[6]
                session['is_root'] = account[7]

                if session['is_member'] == 1:
                # Redirect to home page
                    return redirect(url_for('home'))
                elif session['is_instructor'] == 1:
                    return redirect(url_for('staff_dashboard'))
                elif session['is_admin'] == 1:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('sample'))
            else:
                # Add a message to prompt the use
                return 'Incorrect password!'
        else:
            # Account doesn't exist or username incorrect
            return 'Incorrect username!'

    # Show the login form with message (if any)
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # Add a flash message to prompt the user
    return "'You have been logged out.', 'success'"

   


if __name__ == '__main__':
    app.run(debug=True)
