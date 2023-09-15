from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, get_cursor, title_list, region_list, city_list


@app.route('/')
def index():
    """
    Render the index page, which serves as the main landing page of the web application.
    This function handles the following tasks:
    - Initializes a variable 'notice' to indicate whether there is a notice to be displayed.
    - Checks if the user is logged in by inspecting the 'loggedIn' key in the session data.
    - Retrieves the user's ID and permissions.
    - Queries the database for the latest 3 news items.
    - If the user has specific permissions (assumed '1' represents permission), checks for an active subscription.
    - Renders the 'guest/index.html' template with appropriate data, including any notices and news items.
    Returns:
        A rendered HTML template based on the user's status (logged in or guest) and permissions.
    """
    notice = False
    sql_data = get_cursor()
    sql_data.execute("""SELECT news_id,news,DATE_FORMAT(time,'%d %b %Y  %H:%i:%s') FROM news ORDER BY time DESC LIMIT 3;""")
    posted_news = sql_data.fetchall()
    # Check if the user is logged in
    if 'loggedIn' in session:
        user_id = session["user_id"]
        # Get user permissions
        permissions = check_permissions()
        # Check if the user has specific permissions (assuming 1 represents permission)
        if permissions == 1:
            sql = """SELECT member_id FROM member WHERE user_id=%s;"""
            sql_data.execute(sql, (user_id,))
            member_id = sql_data.fetchall()[0][0]
            sql = """SELECT start_date, end_date FROM payment_due WHERE member_id = %s AND end_date>=%s"""
            sql_data.execute(sql, (member_id, datetime.today().date()))
            subscription = sql_data.fetchall()
            sql_data.close()
            if not subscription:
                notice = True
        return render_template('guest/index.html', notice=notice, posted_news=posted_news, permissions=check_permissions())
    else:
        return render_template('guest/index.html', notice=notice, posted_news=posted_news)


# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Handle user login functionality.
    This function performs the following tasks:
    - Checks if the HTTP request is a POST request and if 'username' and 'password' were submitted in the form.
    - Validates the user's credentials by checking if the account exists in the database.
    - Compares the hashed password stored in the database with the provided password.
    - If the passwords match, logs the user in by setting session variables.
    - Redirects the user to the 'dashboard' page upon successful login.
    - Displays an error message if the provided credentials are incorrect.
    Returns:
        - If a GET request, renders the login form.
        - If a POST request, redirects to the dashboard or displays an error message on the login page.
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
        if account is not None:
            password_hash = account[3]
            # Check if the hashed password matches the one stored in the database
            if bcrypt.checkpw(user_password.encode('utf-8'), password_hash.encode('utf-8')):
                if account[4]:
                    cursor.execute("SELECT state FROM member WHERE user_id = %s", (account[0],))
                    state = cursor.fetchone()[0]
                elif account[5]:
                    cursor.execute("SELECT state FROM instructor WHERE user_id = %s", (account[0],))
                    state = cursor.fetchone()[0]
                else:
                    state = 1
                if state:
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
                    msg = "The account has been Inactivated, please get in touch with the staff."
            else:
                # Add a message to prompt the use
                msg = "Incorrect password!"
        else:
            # Account doesn't exist or username incorrect
            msg = 'Incorrect username!'
        cursor.close()
    # Show the login form with message (if any)
    return render_template('guest/login.html', msg=msg)


@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page with various statistics and information.
    This function performs the following tasks:
    - Acquires a database cursor for SQL operations.
    - Retrieves and counts various statistics from the database, including:
      - The count of instructors
      - The count of members
      - The count of user accounts
      - The count of pools
      - The count of distinct class IDs
      - The latest 3 news items sorted by time
      - The class list
      - Attendance information (complex SQL query)
      - Visit statistics (complex SQL query)
    - Closes the database cursor after data retrieval.
    - Checks if the user is logged in and their role (instructor, admin, root), then renders the appropriate dashboard template.
    Returns:
        - Rendered HTML templates for instructor, admin, root, or redirects to the index page for non-logged-in users.
    """
    sql_data = get_cursor()
    sql_data.execute("""SELECT COUNT(instructor_id) FROM instructor WHERE state = 1;""")
    instructor_count = sql_data.fetchall()
    sql_data.execute("""SELECT COUNT(member_id) FROM member WHERE state = 1;""")
    member_count = sql_data.fetchall()
    sql_data.execute("""SELECT COUNT(user_id) FROM user_account;""")
    user_count = sql_data.fetchall()
    sql_data.execute("""SELECT COUNT(pool_id) FROM pool;""")
    pool_count = sql_data.fetchall()
    sql_data.execute("""SELECT COUNT(DISTINCT class_id)-1 FROM class_list;""")
    class_count = sql_data.fetchall()
    sql_data.execute("""SELECT news_id,news,DATE_FORMAT(time,'%d %b %Y  %H:%i:%s') FROM news ORDER BY time DESC LIMIT 3;""")
    posted_news = sql_data.fetchall()
    sql_data.execute("""SELECT * FROM class_list;""")
    class_list = sql_data.fetchall()
    # Complex SQL query to fetch attendance information
    sql = """SELECT a.log_id, a.attendance_date, CONCAT(m.first_name, ' ', m.last_name) AS name, cl.class_name, p.pool_name
                FROM attendance_log AS a
                INNER JOIN member AS m ON m.member_id = a.member_id
                INNER JOIN pool AS p ON p.pool_id = a.pool_id
                LEFT JOIN book_class_list AS bc ON bc.book_class_id = a.class_id
                LEFT JOIN class_list AS cl ON cl.class_id = bc.class_id
                ORDER BY class_name;"""
    sql_data.execute(sql)
    attendance = sql_data.fetchall()
    # Complex SQL query to fetch visit statistics
    sql = """SELECT m.member_id, CONCAT(m.first_name, ' ', m.last_name) AS name, DATE_FORMAT(a.attendance_date, '%Y-%m') AS Month, 
                COUNT(*) AS Monthly_Count, week(a.attendance_date, 1) AS Week, COUNT(*) AS Weekly_Count
                FROM member AS m
                INNER JOIN attendance_log AS a ON m.member_id = a.member_id
                GROUP BY m.member_id, Month, Week ORDER BY name;"""
    sql_data.execute(sql)
    visit = sql_data.fetchall()
    sql_data.close()
    if 'loggedIn' in session:
        if session['is_instructor'] == 1:
            return redirect(url_for('instructor_timetable'))
        elif session['is_admin'] == 1:
            return render_template('admin/dashboard.html', instructor_count=instructor_count, member_count=member_count, user_count=user_count,
                                   pool_count=pool_count, class_count=class_count, permissions=check_permissions(), attendance=attendance, posted_news=posted_news, visit=visit, class_list=class_list)
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
    Handle user logout functionality.
    This function performs the following tasks:
    - Removes session data, effectively logging the user out by clearing session variables.
    - Removes the following session variables:
      - 'loggedIn': Indicates whether the user is logged in.
      - 'user_id': Stores the user's ID.
      - 'username': Stores the user's username.
      - 'is_member': Indicates if the user is a member.
      - 'is_admin': Indicates if the user is an admin.
      - 'is_instructor': Indicates if the user is an instructor.
      - 'is_root': Indicates if the user has root-level access.
    - Redirects the user to the index page after logout.
    Returns:
        - A redirection to the index page.
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
    This function performs the following tasks:
    - Initializes an empty message variable 'msg'.
    - Retrieves the current date.
    - Processes user registration when the HTTP request method is POST.
    - Validates the presence of required fields in the submitted form.
    - Extracts form values for both required and optional fields.
    - Checks if the provided email or username already exists in the database.
    - If not, generates a password hash, inserts the user's basic and detailed information into the database,
      and logs the user in by setting session variables.
    - If registration is successful, redirects the user to the index page.
    - Renders the registration form with appropriate messages and options when the HTTP request method is GET.
    Returns:
        - If a POST request is successful, redirects to the index page.
        - If a POST request fails, renders the registration form with error messages.
        - If a GET request, renders the registration form with initial options.
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
        username = values['username']
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
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)"""
                value = (user_id, values['title_id'], first_name, last_name, values['phone_number'], values['region_id'],
                         values['city_id'], values['street_name'], values['birth_date'])
                cursor.execute(sql, value)
                cursor.execute("SELECT * FROM user_account WHERE user_id = %s", (user_id,))
                account = cursor.fetchone()
                cursor.close()
                session['loggedIn'] = True
                session['user_id'] = account[0]
                session['username'] = account[1]
                session['is_member'] = account[4]
                session['is_instructor'] = account[5]
                session['is_admin'] = account[6]
                session['is_root'] = account[7]
                msg = "Registration success!"
                return render_template('guest/jump.html', goUrl='/', msg=msg, permissions=check_permissions())
        # Return the registration template with the appropriate message
    return render_template('guest/register.html', msg=msg, titles=title_list, regions=region_list, cities=city_list, today=today)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    sql_data = get_cursor()
    msg = ''
    # get password from the user
    sql = """SELECT password FROM user_account WHERE user_id=%s"""
    sql_value = (session["user_id"],)
    sql_data.execute(sql,sql_value)
    sql_list = sql_data.fetchone()
    old_password = sql_list[0].encode('utf-8')
    # if the user submits new passwords
    if request.method == 'POST':
        new_password = request.form.get('newpw')
        confirm_password = request.form.get('confirmpw')
        # convert confirm password to bytes
        byte_password = confirm_password.encode('utf-8')
        # check whether the passwords are the same
        if new_password != confirm_password:
            msg = "Passwords do not match. Please try again."
        elif bcrypt.checkpw(byte_password, old_password):
            msg = "New password cannot be the same as previous password"
        # update hashed password if validated
        else:
            hashed_password = bcrypt.hashpw(confirm_password.encode('utf-8'), bcrypt.gensalt())
            sql = "UPDATE user_account SET password=%s WHERE user_id=%s"
            sql_value = (hashed_password,session["user_id"])
            sql_data.execute(sql,sql_value)
            msg = "Password changed."
    return render_template('change_password.html',permissions=check_permissions(), old_password=old_password, msg=msg)


@app.errorhandler(Exception)
def handle_error(error):
    """
    Receive all unexpected errors
    :param error:
    :return: error.html
    """
    print(error)
    return render_template('guest/error.html', permissions=check_permissions())
