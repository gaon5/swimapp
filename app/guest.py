from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, get_cursor, title_list, region_list, city_list


@app.route('/')
def index():
    # Select news from database, and display.
    if 'loggedIn' in session:
        return render_template('guest/index.html', permissions=check_permissions())
    else:
        return render_template('guest/index.html')


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
    msg = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists
        cursor = get_cursor()
        cursor.execute("SELECT * FROM user_account WHERE username = %s", (username,))
        account = cursor.fetchone()
        cursor.close()
        if account is not None:
            password_hash = account[3]
            # Check if the hashed password matches the one stored in the database
            if bcrypt.checkpw(user_password.encode('utf-8'), password_hash.encode('utf-8')):
                # If the passwords match, log the user in
                session['loggedIn'] = True
                session['user_id'] = account[0]
                session['username'] = account[1]
                session['is_member'] = account[4]
                session['is_instructor'] = account[5]
                session['is_admin'] = account[6]
                session['is_root'] = account[7]
                # Redirect to home page
                return redirect(url_for('dashboard'))
            else:
                # Add a message to prompt the use
                msg = "Incorrect password!"
        else:
            # Account doesn't exist or username incorrect
            msg = 'Incorrect username!'
    # Show the login form with message (if any)
    return render_template('guest/login.html', msg=msg)


@app.route('/dashboard')
def dashboard():
    sql_data = get_cursor()
    sql = """SELECT COUNT(instructor_id) FROM instructor;"""
    sql_data.execute(sql)
    instructor_count = sql_data.fetchall()
    sql = """SELECT COUNT(member_id) FROM member"""
    sql_data.execute(sql)
    member_count = sql_data.fetchall()
    sql = """SELECT COUNT(user_id) FROM user_account;"""
    sql_data.execute(sql)
    user_count = sql_data.fetchall()
    sql = """SELECT COUNT(pool_id) FROM pool;"""
    sql_data.execute(sql)
    pool_count = sql_data.fetchall()
    sql = """SELECT COUNT(DISTINCT class_id) FROM book_class_list;"""
    sql_data.execute(sql)
    class_count = sql_data.fetchall()
    sql_data.close()
    if 'loggedIn' in session:
        if session['is_instructor'] == 1:
            return render_template('instructor/dashboard.html', instructor_count=instructor_count, member_count=member_count,
                                   user_count=user_count,
                                   pool_count=pool_count, class_count=class_count, permissions=check_permissions())
        elif session['is_admin'] == 1:
            return render_template('admin/dashboard.html', instructor_count=instructor_count, member_count=member_count, user_count=user_count,
                                   pool_count=pool_count, class_count=class_count, permissions=check_permissions())
        elif session['is_root'] == 1:
            return render_template('root/dashboard.html', instructor_count=instructor_count, member_count=member_count, user_count=user_count,
                                   pool_count=pool_count, class_count=class_count, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/jump', methods=['GET', 'POST'])
def jump():
    msg = ""
    previous_url = str(request.referrer)
    urlList = [x for x in previous_url.split('/') if x != '']
    if urlList[-1] == 'login':
        return render_template('guest/jump.html', goUrl='/dashboard', msg=msg)
    else:
        return render_template('guest/jump.html', goUrl='/login/', msg=msg)


@app.route('/logout')
def logout():
    """
    Handle user logout:
    1. Remove user-specific data from the session to log the user out.
    2. Redirect or inform the user that they have successfully logged out.
    """
    # Remove session data, this will log the user out
    session.pop('loggedIn', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_member', None)
    session.pop('is_admin', None)
    session.pop('is_instructor', None)
    session.pop('is_root', None)
    # Add a flash message to prompt the user
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    1. Setup: Establishes the /register route for GET and POST requests.
    2. Feedback Init: Initializes an empty feedback message with msg = ''.
    3. GET Handling: On GET, retrieves titles, cities, and citys; returns the registration form.
    4. POST Handling: On POST, extracts and processes submitted form data.
    5. Validation: Checks for duplicate accounts, validates email, password, username, and birthdate formats.
    6. Data Storage: If valid, hashes password, stores user data in the database, retrieves the user's ID, and saves detailed info.
    7. Feedback Setup: Sets a feedback message based on the registration outcome.
    8. Response: Renders the register.html template with the feedback message.
    """
    # Initial message to display to the user
    msg = ''
    today = datetime.today().date()
    if request.method == 'POST':
        # Define the required and optional fields for registration
        required_fields = [
            'username', 'password', 'email', 'title_id', 'first_name', 'last_name',
            'phone_number', 'region_id', 'city_id', 'street_name', 'birth_date'
        ]
        optional_fields = ['detailed_information', 'health_information']

        # Ensure all necessary fields are present in the submitted form
        if not all(request.form.get(field) for field in required_fields):
            msg = "Please fill out all required fields!"
            return render_template('guest/register.html', msg=msg)

        # Extract form values
        values = {field: request.form[field] for field in required_fields}
        for field in optional_fields:
            values[field] = request.form.get(field, None)

        # Process basic details
        username = values['username'].capitalize()
        password = values['password']
        email = values['email']
        first_name = values['first_name'].capitalize()
        last_name = values['last_name'].capitalize()

        with get_cursor() as cursor:
            # Check if provided email or username already exists in the database
            cursor.execute('SELECT email, username FROM user_account WHERE email = %s OR username = %s', (email, username,))
            existing_data = cursor.fetchone()
            # If there's a match, notify the user
            if existing_data:
                existing_email, existing_username = existing_data
                if existing_email == email:
                    msg = 'An account with this email already exists!'
                if existing_username == username:
                    msg += 'An account with this username already exists!'
            else:
                # Generate password hash and get current registration date
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                # Insert the user's basic details into user_account
                cursor.execute("""INSERT INTO user_account (username, password, email, is_member, register_date) 
                            VALUES (%s, %s, %s, 1, %s )""", (username, hashed, email, today))
                # Get the generated user_id for the above insert
                cursor.execute('SELECT user_id from user_account WHERE username = %s', (username,))
                user_id = cursor.fetchone()[0]
                # Insert the user's detailed information into the member table
                sql = """INSERT INTO member (user_id, title_id, first_name, last_name, phone_number, 
                            region_id, city_id, street_name, birth_date, state)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 0)"""
                value = (user_id, values['title_id'], first_name, last_name, values['phone_number'], values['region_id'],
                         values['city_id'], values['street_name'], values['birth_date'])
                cursor.execute(sql, value)
                cursor.close()
                return redirect(url_for('payment'))
        # Return the registration template with the appropriate message
    return render_template('guest/register.html', msg=msg, titles=title_list, cities=region_list, citys=city_list, today=today)


@app.route('/monthly_payment', methods=['GET', 'POST'])
def monthly_payment():
    return render_template('guest/monthly_payment.html')
