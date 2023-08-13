from flask import Flask, url_for, request, redirect, render_template, session
from datetime import datetime, date
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

# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests   
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Handle user login:
    
    1. Check if "username" and "password" POST data exist (i.e., the form has been submitted).
    2. Create variables for the username and password for easy access.
    3. Check if the username exists in the database.
    4. If the username exists, validate the hashed password against the submitted password.
    5. If passwords match, create session data for the logged-in user.
    6. Redirect the user to the appropriate dashboard based on their role.
    7. If the username or password is incorrect, inform the user.
    8. If the request is a GET request or the form hasn't been submitted, show the login form.

    """
   
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
                session['user_id'] = account[0]
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
                    return redirect(url_for('dashboard'))
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

    """
    Handle user logout:
    
    1. Remove user-specific data from the session to log the user out.
    2. Redirect or inform the user that they have successfully logged out.
    """
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_member', None)
    session.pop('is_admin', None)
    session.pop('is_instructor', None)
    session.pop('is_root', None)

    # Add a flash message to prompt the user
    return "'You have been logged out.', 'success'"

   
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""

    msg = ''

    if request.method == 'GET':
        with get_cursor() as cursor:
            cursor.execute('SELECT * FROM title')
            titles = cursor.fetchall()

            cursor.execute('SELECT * FROM city')
            cities = cursor.fetchall()
            
            cursor.execute('SELECT * FROM region')
            regions = cursor.fetchall()

        return render_template('register.html', msg=msg, titles=titles, cities=cities, regions=regions)

    if request.method == 'POST':
        required_fields = [
            'username', 'password', 'email', 'title_id', 'first_name', 'last_name', 
            'phone_number', 'city_id', 'region_id', 'street_name', 'birth_date'
        ]
        optional_fields = ['detailed_information', 'health_information']

        # Ensure all necessary fields are present
        if not all(request.form.get(field) for field in required_fields):
            msg = "Please fill out all required fields!"
            return render_template('register.html', msg=msg)

        values = {field: request.form[field] for field in required_fields}
        for field in optional_fields:
            values[field] = request.form.get(field, None)

        username = values['username'].capitalize()
        password = values['password']
        email = values['email']
        first_name = values['first_name'].capitalize()
        last_name = values['last_name'].capitalize()

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
            elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', username):
                msg = 'Username must be at least 8 characters long and contain both characters and numbers!'
            elif not first_name.isalpha() or not last_name.isalpha():
                msg = 'First name and Last name must only contain letters!'
            elif not re.match(r'^\d{4}-\d{2}-\d{2}$', values['birth_date']):
                msg = 'Birth date must be in the format YYYY-MM-DD!'
            else:
                # Validate that the provided birth date is in the past
                input_date = datetime.strptime(values['birth_date'], '%Y-%m-%d').date()
                if input_date > datetime.today().date():
                    msg = 'Please provide a valid birth date. The date cannot be in the future.'
                else:
                    # Calculate the date in Python
                    register_date = datetime.today().date()
                    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute('INSERT INTO user_account (username, password, email, is_member, register_date) VALUES (%s, %s, %s, 1, %s )', (username, hashed, email, register_date))
                    cursor.execute('SELECT user_id from user_account WHERE username = %s', (username,))
                    user_id = cursor.fetchone()[0]
                    cursor.execute('INSERT INTO member (user_id, title_id, first_name, last_name, phone_number, detailed_information, city_id, region_id, street_name, birth_date, health_information, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                ( user_id, values['title_id'], values['first_name'], values['last_name'],
                values['phone_number'], values['detailed_information'], values['city_id'], 
                values['region_id'], values['street_name'], values['birth_date'], values['health_information'], 1))
                    msg = 'You have successfully registered!'

        return render_template('register.html', msg=msg)



if __name__ == '__main__':
    app.run(debug=True)
