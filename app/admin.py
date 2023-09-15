from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
import calendar
from app import app, check_permissions, get_cursor, title_list, region_list, city_list


@app.route('/member_list', methods=['GET', 'POST'])
def member_list():
    """
    Renders the member list management page, allowing admins to view, update, and register members.
    This function handles the following tasks:
    - Paginates member data for easier navigation.
    - Handles both member registration and updates.
    - Validates user input and checks for duplicate accounts.
    - Retrieves and displays member details.

    Returns:
        A rendered HTML template with member data, pagination, and registration/update functionality.
    """

    # Define a function to check if there are changes in member data
    def check_change(old, new):
        for i in range(len(new)):
            if old[i + 1] != new[i]:
                return True
        return False

    today = datetime.today().date()
    msg = ''
    # Check if the user is logged in
    if 'loggedIn' in session:
        if check_permissions() > 2:
            sql_data = get_cursor()
            sql = """SELECT count(*) FROM member WHERE state=1;"""
            sql_data.execute(sql)
            member_count = sql_data.fetchall()[0][0]
            member_count = math.ceil(member_count / 10)
            # Get the current page from the request or set it to the first page
            page = request.args.get('page')
            if not page:
                sql_page = 0
            else:
                page = int(page)
                sql_page = (page - 1) * 10
            # Handle POST requests (form submissions)
            if request.method == 'POST':
                # Extract data from the form
                first_name = request.form.get('first_name').capitalize()
                last_name = request.form.get('last_name').capitalize()
                title = int(request.form.get('title'))
                email = request.form.get('email')
                phone_number = request.form.get('phone_number')
                region = int(request.form.get('region'))
                city = int(request.form.get('city'))
                street_name = request.form.get('street_name')
                birth_date = request.form.get('birth_date')
                detailed_information = request.form.get('detailed_information')
                health_information = request.form.get('health_information')
                user_id = request.form.get('user_id')
                if user_id:
                    # If user_id is provided, update existing member information
                    sql = """SELECT m.user_id,m.first_name,m.last_name,m.title_id,u.email,m.phone_number,m.detailed_information FROM `member` AS m
                                LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                                WHERE m.user_id=%s;"""
                    sql_value = (user_id,)
                    sql_data.execute(sql, sql_value)
                    sql_instructor_list = sql_data.fetchall()[0]
                    new_data = (first_name, last_name, title, email, phone_number, detailed_information)
                    # Check if there are changes in member data
                    if check_change(sql_instructor_list, new_data):
                        sql = """UPDATE `member` SET first_name=%s,last_name=%s,birth_date=%s,title_id=%s,phone_number=%s,region_id=%s,city_id=%s,street_name=%s,
                                                    detailed_information=%s, health_information=%s 
                                                    WHERE user_id=%s;"""
                        sql_value = (first_name, last_name, birth_date, title, phone_number, region, city, street_name, detailed_information, health_information, user_id,)
                        sql_data.execute(sql, sql_value)
                        # check email
                        sql_data.execute("SELECT user_id, email FROM `user_account` WHERE user_id=%s;", (user_id,))
                        user_account_list = sql_data.fetchall()[0]
                        if email != user_account_list[1]:
                            sql_data.execute("SELECT user_id, email FROM `user_account` WHERE email=%s;", (email,))
                            if len(sql_data.fetchall()) > 0:
                                msg = "This email is already in use."
                            else:
                                sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
                    else:
                        msg = "No modification"
                else:
                    # Handle member registration
                    username = request.form.get('username')
                    password = request.form.get('password')
                    # Check if an account with the same email or username already exists
                    sql_data.execute('SELECT email, username FROM user_account WHERE email = %s OR username = %s', (email, username,))
                    existing_data = sql_data.fetchone()
                    if existing_data:
                        msg = 'An account with this email or username already exists!'
                    else:
                        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        sql_data.execute("""INSERT INTO user_account (username, password, email, is_member, register_date) 
                                                    VALUES (%s, %s, %s, 1, %s )""", (username, hashed, email, today))
                        sql_data.execute('SELECT user_id from user_account WHERE username = %s', (username,))
                        user_id = sql_data.fetchone()[0]
                        # Insert member data
                        sql = """INSERT INTO member (user_id, title_id, first_name, last_name, phone_number, 
                                    region_id, city_id, street_name, birth_date, state)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)"""
                        value = (user_id, title, first_name, last_name, phone_number, region, city, street_name, birth_date)
                        sql_data.execute(sql, value)
                        msg = "Registration success!"
            # Query to retrieve member data for the current page
            sql = """SELECT m.user_id,m.first_name,m.last_name,m.phone_number,t.title,u.username,u.email,m.title_id,
                        m.detailed_information,m.region_id,m.city_id,m.street_name,m.birth_date,m.health_information,m.state FROM member AS m
                        LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                        LEFT JOIN `title` AS t ON t.title_id=m.title_id
                        WHERE m.state = 1
                        LIMIT %s, 10;"""
            sql_data.execute(sql, (sql_page,))
            sql_member_list = sql_data.fetchall()
            for i in range(len(sql_member_list)):
                sql_member_list[i] = list(sql_member_list[i])
                sql_member_list[i][12] = str(sql_member_list[i][12])
            sql_data.close()
            today = str(today)
            return render_template("admin/member_list.html", member_count=member_count, member_list=sql_member_list, city_list=city_list, region_list=region_list,
                                   title_list=title_list, msg=msg, permissions=check_permissions(), today=today)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/instructor_list', methods=['GET', 'POST'])
def instructor_list():
    """
    Renders the instructor list management page, allowing admins to view, update, and register instructors.
    This function handles the following tasks:
    - Paginates instructor data for easier navigation.
    - Handles both instructor registration and updates.
    - Validates user input and checks for duplicate email addresses or usernames.
    - Retrieves and displays instructor details.
    Returns:
        A rendered HTML template with instructor data, pagination, and registration/update functionality.
    """

    # Define a function to check if there are changes in instructor data
    def check_change(old, new):
        for i in range(len(new)):
            if old[i + 1] != new[i]:
                return True
        return False

    today = datetime.today().date()
    msg = ''
    # Check if the user is logged in
    if 'loggedIn' in session:
        if check_permissions() > 2:
            sql_data = get_cursor()
            # Query to get the total count of active instructors
            sql = """SELECT count(*) FROM instructor WHERE state=1;"""
            sql_data.execute(sql)
            instructor_count = sql_data.fetchall()[0][0]
            instructor_count = math.ceil(instructor_count / 10)
            # Get the current page from the request or set it to the first page
            page = request.args.get('page')
            if not page:
                sql_page = 0
            else:
                page = int(page)
                sql_page = (page - 1) * 10
            # Handle POST requests (form submissions)
            if request.method == 'POST':
                # Extract data from the form
                first_name = request.form.get('first_name').capitalize()
                last_name = request.form.get('last_name').capitalize()
                title = int(request.form.get('title'))
                email = request.form.get('email')
                phone_number = request.form.get('phone_number')
                detailed_information = request.form.get('detailed_information')
                user_id = request.form.get('user_id')
                if user_id:
                    # If user_id is provided, update existing instructor information
                    sql = """SELECT i.user_id,i.first_name,i.last_name,i.title_id,u.email,i.phone_number,i.detailed_information FROM `instructor` AS i
                                LEFT JOIN `user_account` AS u ON i.user_id=u.user_id
                                WHERE i.user_id=%s;"""
                    sql_value = (user_id,)
                    sql_data.execute(sql, sql_value)
                    sql_instructor_list = sql_data.fetchall()[0]
                    new_data = (first_name, last_name, title, email, phone_number, detailed_information)
                    # Check if there are changes in instructor data
                    if check_change(sql_instructor_list, new_data):
                        sql = """UPDATE `instructor` SET first_name=%s,last_name=%s,title_id=%s,phone_number=%s,detailed_information=%s WHERE user_id=%s;"""
                        sql_value = (first_name, last_name, title, phone_number, detailed_information, user_id,)
                        sql_data.execute(sql, sql_value)
                        # check email
                        sql_data.execute("SELECT user_id, email FROM `user_account` WHERE user_id=%s;", (user_id,))
                        user_account_list = sql_data.fetchall()[0]
                        if email != user_account_list[1]:
                            sql_data.execute("SELECT user_id, email FROM `user_account` WHERE email=%s;", (email,))
                            if len(sql_data.fetchall()) > 0:
                                msg = "This email is already in use."
                            else:
                                sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
                    else:
                        msg = "No modification"
                else:
                    # Handle instructor registration
                    username = request.form.get('username')
                    password = request.form.get('password')
                    # Check if an account with the same email or username already exists
                    sql_data.execute('SELECT email, username FROM user_account WHERE email = %s OR username = %s', (email, username,))
                    existing_data = sql_data.fetchone()
                    if existing_data:
                        msg = 'An account with this email or username already exists!'
                    else:
                        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        sql_data.execute("""INSERT INTO user_account (username, password, email, is_instructor, register_date) 
                                                    VALUES (%s, %s, %s, 1, %s )""", (username, hashed, email, today))
                        sql_data.execute('SELECT user_id from user_account WHERE username = %s', (username,))
                        user_id = sql_data.fetchone()[0]
                        sql = """INSERT INTO instructor (user_id, title_id, first_name, last_name, phone_number, state) 
                                    VALUES (%s,%s,%s,%s,%s,1)"""
                        value = (user_id, title, first_name, last_name, phone_number)
                        sql_data.execute(sql, value)
                        msg = "Registration success!"
            sql = """SELECT i.user_id,i.first_name,i.last_name,i.phone_number,t.title,u.username,u.email,i.title_id,i.detailed_information,i.state FROM instructor AS i
                                                LEFT JOIN `user_account` AS u ON u.user_id=i.user_id
                                                LEFT JOIN `title` AS t ON t.title_id=i.title_id
                                                WHERE i.state = 1
                                                LIMIT %s, 10;"""
            sql_data.execute(sql, (sql_page,))
            sql_instructor_list = sql_data.fetchall()
            sql_data.close()
            return render_template("admin/instructor_list.html", instructor_count=instructor_count, instructor_list=sql_instructor_list, title_list=title_list, msg=msg, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/delete_user', methods=['POST'])
def delete_user():
    """
    Deactivates (soft deletes) a user account, either a member or an instructor, based on the provided parameters.
    This function handles the following tasks:
    - Checks if the user is logged in and has sufficient permissions (admin-level).
    - Retrieves the user ID and user type (member or instructor) from the request.
    - Updates the corresponding user's state to mark it as deactivated (soft delete).
    Returns:
        A redirection to the member_list or instructor_list route based on the user type.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            is_member = request.form.get('is_member')
            user_id = request.form.get('user_id')
            sql_data = get_cursor()
            if is_member == '1':
                sql = """UPDATE member SET state=0 Where user_id=%s"""
                sql_data.execute(sql, (user_id,))
                sql_data.close()
                return redirect(url_for('member_list'))
            else:
                sql = """UPDATE instructor SET state=0 Where user_id=%s"""
                sql_data.execute(sql, (user_id,))
                sql_data.close()
                return redirect(url_for('instructor_list'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_change_information', methods=['GET', 'POST'])
def admin_change_information():
    """
    Allows an admin user to update their own information.
    This function handles the following tasks:
    - Checks if the user is logged in and has admin-level permissions.
    - Retrieves the admin's user ID and existing information.
    - Processes a POST request to update the admin's information, including email.
    - Performs checks to detect changes and update the database accordingly.
    - Renders the 'admin/change_information.html' template with updated or existing information.
    Returns:
        A rendered HTML template for updating admin information.
    """

    def check_change(old, new):
        for i in range(len(new)):
            if old[i + 1] != new[i]:
                return True
        return False

    if 'loggedIn' in session:
        if check_permissions() > 2:
            user_id = session["user_id"]
            sql_data = get_cursor()
            msg = ""
            # Handle POST request for updating admin information
            if request.method == 'POST':
                title = int(request.form.get('title'))
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                email = request.form.get('email')
                phone_number = request.form.get('phone_number')
                user_id = request.form.get('user_id')
                sql = """SELECT a.user_id,a.title_id,a.first_name,a.last_name,a.phone_number,u.email FROM `admin` AS a
                            LEFT JOIN `user_account` AS u ON a.user_id=u.user_id
                            WHERE a.user_id=%s;"""
                sql_value = (user_id,)
                sql_data.execute(sql, sql_value)
                admin_list = sql_data.fetchall()[0]
                new_data = (title, first_name, last_name, phone_number, email)
                # check change
                if check_change(admin_list, new_data):
                    sql = """UPDATE `admin` SET title_id=%s,first_name=%s,last_name=%s,phone_number=%s WHERE user_id=%s;"""
                    value = (title, first_name, last_name, phone_number, user_id,)
                    sql_data.execute(sql, value)
                    # check email
                    sql_data.execute("SELECT user_id, email FROM `user_account` WHERE user_id=%s;", (user_id,))
                    user_account_list = sql_data.fetchall()[0]
                    if email != user_account_list[1]:
                        sql_data.execute("SELECT user_id, email FROM `user_account` WHERE email=%s;", (email,))
                        if len(sql_data.fetchall()) > 0:
                            msg = "This email is already in use."
                        else:
                            sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
                else:
                    msg = "No modification"
            # Query to retrieve the admin's information
            sql = """SELECT a.user_id,a.title_id,a.first_name,a.last_name,a.phone_number,u.email FROM `admin` AS a
                        LEFT JOIN `user_account` AS u ON a.user_id=u.user_id
                        WHERE a.user_id=%s;"""
            sql_value = (user_id,)
            print(sql % sql_value)
            sql_data.execute(sql, sql_value)
            admin_list = sql_data.fetchall()[0]
            sql_data.close()
            return render_template('admin/change_information.html', admin_list=admin_list, msg=msg, title_list=title_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_timetable', methods=['GET', 'POST'])
def admin_timetable():
    """
    Display and manage the admin's class timetable.
    This function handles the following tasks:
    - Checks if the user is logged in with admin-level permissions.
    - Retrieves the admin's user ID and the current date.
    - Processes a POST request to change the selected date (if applicable).
    - Generates a weekly timetable view starting from the current date.
    - Queries the database to retrieve class details within the selected week.
    - Retrieves pool information, instructor details, and member counts for classes.
    - Renders the 'admin/timetable.html' template with timetable data.
    Returns:
        A rendered HTML template displaying the admin's class timetable.
    """
    # Check if the user is logged in with admin-level permissions
    if 'loggedIn' in session:
        if check_permissions() > 2:
            user_id = session["user_id"]
            if request.method == 'POST':
                today = datetime.strptime(request.form.get('day'), '%Y-%m-%d').date()
            else:
                today = date.today()
            real_day = date.today()
            if real_day == today:
                before_day = today.weekday() + 1
                real_time = datetime.now().time().strftime('%H')
                before_time = int((int(real_time) - 5) * 2) - 1
            elif real_day < today:
                before_day = 0
                before_time = 0
            else:
                before_day = 9
                before_time = 30
            # Calculate the start of the week based on the selected date
            start_of_week = today - timedelta(days=today.weekday())
            week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            week_list = [["", "", "Time/Day"]]
            # Generate the weekly timetable view
            for i in range(7):
                x = (start_of_week + timedelta(days=i)).strftime('%d %b %Y')
                temp_list = [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d'), week[i], str(x)]
                week_list.append(temp_list)
            sql_data = get_cursor()
            sql = """SELECT b.book_class_id, b.instructor_id, b.pool_id, p.pool_name, b.is_individual, c.class_name, 
                        CONCAT(t.title, " ", i.first_name, " ", i.last_name) AS instructor_name, i.phone_number,
                        i.state, b.class_date, b.start_time, b.end_time
                        FROM book_class_list AS b 
                        LEFT JOIN class_list AS c ON c.class_id=b.class_id
                        LEFT JOIN pool AS p ON b.pool_id=p.pool_id
                        LEFT JOIN instructor AS i ON b.instructor_id=i.instructor_id
                        LEFT JOIN title AS t ON i.title_id=t.title_id
                        WHERE (b.class_date BETWEEN %s AND %s) AND (i.state=1)
                        ORDER BY b.start_time"""
            sql_value = (week_list[1][0], week_list[-1][0])
            sql_data.execute(sql, sql_value)
            all_details_sql = sql_data.fetchall()
            sql_data.execute("""SELECT * FROM pool;""")
            pool_list = sql_data.fetchall()
            sql = """SELECT class_id, COUNT(member_id) AS member_count
                        FROM book_list
                        GROUP BY class_id;"""
            sql_data.execute(sql)
            member_count = sql_data.fetchall()
            sql_data.execute("SELECT * FROM instructor AS i LEFT JOIN title AS t ON i.title_id=t.title_id WHERE i.state=1;")
            sql_instructor_list = sql_data.fetchall()
            for i in range(1, len(week_list), 1):
                week_list[i][0] = week_list[i][0][5:]
            # Prepare class details for rendering in the timetable
            all_details = []
            for item in all_details_sql:
                time = int(((item[10].total_seconds() / 3600) - 5) * 2)
                continuance = int(((item[11] - item[10]).total_seconds() / 3600) * 2)
                all_details.append({
                    "x": str(item[9].weekday() + 1),
                    "y": str(time - 1),
                    "continuance": continuance,
                    "id": str(item[0]),
                    "instructor_id": item[1],
                    "pool_id": item[2],
                    "is_individual": item[4],
                    "pool_name": item[3],
                    "class_name": item[5],
                    "instructor_name": item[6],
                    "instructor_phone": item[7]
                })
            # Organize data into dictionaries for easy access
            all_details = {item['id']: item for item in all_details}
            for i in range(len(member_count)):
                member_count[i] = list(member_count[i])
            member_count = {item[0]: item[1] for item in member_count}
            return render_template('admin/timetable.html', week_list=week_list, pool_list=pool_list, today=today, instructor_list=sql_instructor_list,
                                   all_details=all_details, member_count=member_count, link=url_for('admin_timetable'), permissions=check_permissions(), before_day=before_day, before_time=before_time)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_add_class', methods=['POST'])
def admin_add_class():
    """
    Handle the addition of a new class by an admin.
    This function handles the following tasks:
    - Checks if the user is logged in with admin-level permissions.
    - Parses and validates the form input for class date and time.
    - Constructs a complete datetime object from the input.
    - Queries the database to retrieve available instructors for the specified date and time.
    - Retrieves class and pool information from the database.
    - Renders the 'admin/add_class.html' template with instructor, class, and pool options.
    Returns:
        A rendered HTML template for adding a new class.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            form_date = request.form.get('send_day')
            form_time = request.form.get('send_time')
            current_year = datetime.now().year
            parsed_date = datetime.strptime(form_date, '%m-%d')
            complete_date = parsed_date.replace(year=current_year)
            complete_date_string = complete_date.strftime('%Y-%m-%d')
            parsed_time = datetime.strptime(form_time, '%H:%M').time()
            start_time = parsed_time.replace(second=0).strftime('%H:%M:%S')
            end_time = datetime.combine(datetime.min, parsed_time) + timedelta(minutes=30)
            sql_data = get_cursor()
            # Query to retrieve available instructors for the specified date and time
            sql = """SELECT DISTINCT i.user_id, i.first_name, i.last_name, t.title
                        FROM instructor AS i
                        LEFT JOIN available_time AS a ON i.user_id = a.user_id
                        LEFT JOIN title AS t ON t.title_id=i.title_id
                        WHERE NOT EXISTS (
                            SELECT 1
                            FROM book_class_list AS b
                            LEFT JOIN instructor AS ins ON ins.instructor_id=b.instructor_id
                            WHERE ins.user_id = i.user_id
                            AND b.class_date = %s
                            AND b.start_time <= %s
                            AND b.end_time >= %s
                            AND ins.state = 1
                        ) AND NOT EXISTS (
                            SELECT 1
                            FROM available_time AS a2
                            WHERE a2.user_id = i.user_id
                            AND a2.date = %s
                            AND a2.start_time <= %s
                            AND a2.end_time >= %s
                        );"""
            value = (complete_date_string, start_time, end_time, complete_date_string, start_time, end_time)
            print(sql % value)
            sql_data.execute(sql, value)
            sql_instructor_list = sql_data.fetchall()
            # Retrieve class and pool information from the database
            sql_data.execute("SELECT * FROM class_list;")
            class_list = sql_data.fetchall()
            sql_data.execute("""SELECT * FROM pool;""")
            pool_list = sql_data.fetchall()
            return render_template('admin/add_class.html', instructor_list=sql_instructor_list, class_list=class_list, pool_list=pool_list,
                                   time=str(start_time), date=complete_date_string, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_edit_class', methods=['GET', 'POST'])
def admin_edit_class():
    """
    Handle the editing of a class by an admin.
    This function handles the following tasks:
    - Checks if the user is logged in with admin-level permissions.
    - If the request is GET, retrieves class details for editing.
    - Parses and validates form input for class date and time.
    - Constructs a complete datetime object from the input.
    - Queries the database to retrieve available instructors for the specified date and time.
    - Retrieves class and pool information from the database.
    - If the request is POST, updates or inserts a new class entry in the database.
    Returns:
        A rendered HTML template for editing a class or redirects to the admin timetable page.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            if request.method == 'GET':
                # Handle GET request to retrieve class details for editing
                class_id = request.args.get('class_id')
                if not class_id:
                    return redirect(url_for('admin_timetable'))
                sql_data = get_cursor()
                sql = """SELECT i.user_id,b.pool_id,b.class_id,b.class_date,b.detailed_information,b.start_time,b.end_time
                            FROM book_class_list AS b
                            LEFT JOIN instructor AS i on b.instructor_id = i.instructor_id 
                            WHERE book_class_id=%s"""
                value = (class_id,)
                sql_data.execute(sql, value)
                class_detail = list(sql_data.fetchall()[0])
                if int(((class_detail[6] - class_detail[5]).total_seconds() / 3600)) == 1:
                    class_detail.append(2)
                else:
                    class_detail.append(1)
                class_detail.append(class_id)
                class_detail[5], class_detail[6] = str(class_detail[5]).split(':')[0], str(class_detail[5]).split(':')[1]
                sql_data.execute("SELECT * FROM class_list;")
                class_list = sql_data.fetchall()
                sql_data.execute("""SELECT * FROM pool;""")
                pool_list = sql_data.fetchall()
                sql_data.execute("""SELECT i.user_id, i.first_name, i.last_name, t.title 
                                        FROM instructor AS i
                                        LEFT JOIN title AS t ON t.title_id=i.title_id
                                        WHERE i.state = 1;""")
                sql_instructor_list = sql_data.fetchall()
                sql_data.close()
                return render_template('admin/add_class.html', instructor_list=sql_instructor_list, class_list=class_list, pool_list=pool_list,
                                       class_detail=class_detail, permissions=check_permissions(), edit=1)
            else:
                # Handle POST request to update or insert a new class entry in the database
                form_date = request.form.get('send_day')
                form_time = request.form.get('send_time')
                class_id = request.form.get('class_id')
                if form_date:
                    current_year = datetime.now().year
                    parsed_date = datetime.strptime(form_date, '%m-%d')
                    complete_date = parsed_date.replace(year=current_year)
                    complete_date_string = complete_date.strftime('%Y-%m-%d')
                    parsed_time = datetime.strptime(form_time, '%H:%M').time()
                    start_time = parsed_time.replace(second=0).strftime('%H:%M:%S')
                    end_time = datetime.combine(datetime.min, parsed_time) + timedelta(minutes=30)
                    sql_data = get_cursor()
                    # Query to retrieve available instructors for the specified date and time
                    sql = """SELECT i.user_id, i.first_name, i.last_name, t.title
                                            FROM instructor AS i
                                            LEFT JOIN available_time AS a ON i.user_id = a.user_id
                                            LEFT JOIN title AS t ON t.title_id=i.title_id
                                            WHERE NOT EXISTS (
                                                SELECT 1
                                                FROM book_class_list AS b
                                                LEFT JOIN instructor AS ins ON ins.instructor_id=b.instructor_id
                                                WHERE ins.user_id = i.user_id
                                                AND b.class_date = %s
                                                AND b.start_time <= %s
                                                AND b.end_time >= %s
                                                AND ins.state = 1
                                            ) AND NOT EXISTS (
                                                SELECT 1
                                                FROM available_time AS a2
                                                WHERE a2.user_id = i.user_id
                                                AND a2.date = %s
                                                AND a2.start_time <= %s
                                                AND a2.end_time >= %s
                                            ) group by a.user_id;"""
                    value = (complete_date_string, start_time, end_time, complete_date_string, start_time, end_time)
                    sql_data.execute(sql, value)
                    sql_instructor_list = sql_data.fetchall()
                    sql_data.execute("SELECT * FROM class_list;")
                    class_list = sql_data.fetchall()
                    sql_data.execute("""SELECT * FROM pool;""")
                    pool_list = sql_data.fetchall()
                    sql_data.close()
                    return render_template('admin/add_class.html', instructor_list=sql_instructor_list, class_list=class_list, pool_list=pool_list,
                                           time=str(start_time), date=complete_date_string, permissions=check_permissions(), edit=1, class_id=class_id)
                else:
                    # Handle form submission to update or insert class details
                    available_date = request.form.get('available_date')
                    start_hour = request.form.get('start_hour')
                    start_minute = request.form.get('start_minute')
                    hour = request.form.get('hour')
                    class_name = int(request.form.get('class_name'))
                    instructor = int(request.form.get('instructor'))
                    pool = int(request.form.get('pool'))
                    detailed_information = str(request.form.get('detailed_information'))
                    start_time = str(start_hour) + ":" + str(start_minute)
                    parsed_time = datetime.strptime(start_time, '%H:%M').time()
                    start_time = parsed_time.replace(second=0).strftime('%H:%M:%S')
                    if int(hour) == 1:
                        end_time = datetime.combine(datetime.min, parsed_time) + timedelta(minutes=30)
                    else:
                        end_time = datetime.combine(datetime.min, parsed_time) + timedelta(minutes=60)
                    end_time = end_time.replace(second=0).strftime('%H:%M:%S')
                    sql_data = get_cursor()
                    sql_data.execute("""SELECT instructor_id,user_id FROM instructor WHERE user_id=%s""", (instructor,))
                    instructor_id = sql_data.fetchall()[0][0]
                    if class_id:
                        # Update existing class entry in the database
                        sql = """UPDATE book_class_list SET instructor_id=%s,pool_id=%s,class_id=%s,class_date=%s,start_time=%s,end_time=%s,detailed_information=%s WHERE book_class_id=%s;"""
                        value = (instructor_id, pool, class_name, available_date, start_time, str(end_time)[-8:], detailed_information, int(class_id))
                    else:
                        sql = """INSERT INTO book_class_list(instructor_id, pool_id, class_id, class_date, start_time, end_time, detailed_information) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s);"""
                        value = (instructor_id, pool, class_name, available_date, start_time, str(end_time)[-8:], detailed_information)
                    sql_data.execute(sql, value)
                    sql_data.close()
                    return redirect(url_for('admin_timetable'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_delete_class', methods=['POST'])
def admin_delete_class():
    """
    Handle the deletion of a class by an admin.
    This function checks if the user is logged in with admin-level permissions,
    and if so, deletes the specified class entry from the database.
    Returns:
        Redirects to the admin timetable page after deletion.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            class_id = request.form.get('class_id')
            sql_data = get_cursor()
            sql_data.execute("""DELETE FROM `book_class_list` WHERE book_class_id=%s;""", (class_id,))
            sql_data.close()
            return redirect(url_for('admin_timetable'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/view_payments', methods=['GET'])
def view_payments():
    """
    Display payment details for admin view.
    This function checks if the user is logged in with admin-level permissions
    and retrieves payment details from the database for display.
    Returns:
        A rendered HTML template displaying payment details.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            cursor = get_cursor()
            # Query the database for payment details
            sql = """SELECT p.payment_id,DATE_FORMAT(p.payment_date,'%d %b %Y'),p.price,p.payment_type,p.payment_method,ua.username FROM payment_list p
                        LEFT JOIN member m on p.member_id = m.member_id
                        LEFT JOIN user_account ua on m.user_id = ua.user_id
                        ORDER BY payment_date DESC;"""
            cursor.execute(sql)
            payments = cursor.fetchall()
            cursor.close()
            return render_template('admin/view_payments.html', payments=payments, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/subscriptions_due_date')
def subscriptions_due_date():
    """
    Display lists of members with subscriptions due, about to due, and active subscriptions.
    This function checks if the user is logged in with admin-level permissions
    and retrieves member subscription details from the database for display.
    Returns:
        A rendered HTML template displaying subscription details.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            msg = ''
            sql_data = get_cursor()
            today = datetime.today().date()
            sql_data.execute("""SELECT m.first_name,m.last_name,m.phone_number, u.email, DATE_FORMAT(u.register_date,'%d %b %Y')
                        FROM member AS m
                        LEFT JOIN payment_due AS pa on m.member_id = pa.member_id
                        INNER JOIN user_account AS u on m.user_id = u.user_id
                        WHERE pa.start_date IS NULL AND pa.end_date IS NULL
                        ORDER BY u.register_date;""")
            No_List = sql_data.fetchall()
            sql = """SELECT m.first_name,m.last_name, DATE_FORMAT(p.payment_date,'%d %b %Y'), DATE_FORMAT(pa.start_date,'%d %b %Y'),DATE_FORMAT(pa.end_date,'%d %b %Y'),m.phone_number, u.email, m.member_id
                        FROM member AS m
                        INNER JOIN payment_list AS p on m.member_id = p.member_id
                        INNER JOIN payment_due AS pa on p.payment_id = pa.payment_id
                        INNER JOIN user_account AS u on m.user_id = u.user_id
                        WHERE pa.end_date < %s AND m.state=1;"""
            value = (today,)
            sql_data.execute(sql, value)
            Due_List = sql_data.fetchall()
            sql = """SELECT m.first_name,m.last_name, DATE_FORMAT(p.payment_date,'%d %b %Y'), DATE_FORMAT(pa.start_date,'%d %b %Y'),DATE_FORMAT(pa.end_date,'%d %b %Y'),m.phone_number, u.email 
                        FROM member AS m
                        INNER JOIN payment_list AS p on m.member_id = p.member_id
                        INNER JOIN payment_due AS pa on p.payment_id = pa.payment_id
                        INNER JOIN user_account AS u on m.user_id = u.user_id
                        WHERE (%s <= pa.end_date) AND (pa.end_date <= DATE_ADD( %s, INTERVAL 7 DAY)) AND m.state=1;"""
            value = (today, today,)
            sql_data.execute(sql, value)
            About_to_due_list = sql_data.fetchall()
            sql = """SELECT m.first_name,m.last_name, DATE_FORMAT(p.payment_date,'%d %b %Y'), DATE_FORMAT(pa.start_date,'%d %b %Y'),DATE_FORMAT(pa.end_date,'%d %b %Y'),m.phone_number, u.email 
                        FROM member AS m
                        INNER JOIN payment_list AS p on m.member_id = p.member_id
                        INNER JOIN payment_due AS pa on p.payment_id = pa.payment_id
                        INNER JOIN user_account AS u on m.user_id = u.user_id
                        WHERE pa.end_date > %s AND m.state=1;"""
            value = (today,)
            sql_data.execute(sql, value)
            Active_List = sql_data.fetchall()
            sql_data.close()
            return render_template('admin/subscriptions_due.html', permissions=check_permissions(), No_List=No_List, Due_List=Due_List, About_to_due_list=About_to_due_list,
                                   Active_List=Active_List, msg=msg)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_delete_member', methods=['POST'])
def admin_delete_member():
    """
    Handle the deletion of a member by an admin.
    This function checks if the user is logged in with admin-level permissions
    and deletes the specified member's entry from the database.
    Returns:
        A rendered HTML template indicating successful deletion.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            member_id = request.form['member_id']
            # Query the database to update the member's state to '0' (inactive)
            sql_data = get_cursor()
            sql = """UPDATE member SET state=0 Where member_id=%s"""
            value = (member_id,)
            sql_data.execute(sql, value)
            msg = 'Delete Successfully'
            sql_data.close()
            return render_template('guest/jump.html', permissions=check_permissions(), goUrl='/subscriptions_due_date', msg=msg)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/add_news', methods=['POST'])
def add_news():
    """
    Add news to the system.
    This function checks if the user is logged in with admin-level permissions
    and inserts news with the current timestamp into the database.
    Returns:
        Redirects to the dashboard after adding news.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            now = datetime.now()
            news = request.form['news']
            sql_data = get_cursor()
            sql = """INSERT INTO news (news,time) VALUE (%s,%s);"""
            sql_value = (news, now,)
            sql_data.execute(sql, sql_value)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index'))


@app.route('/delete_news', methods=['POST'])
def delete_news():
    """
    Delete news by its ID.
    This function checks if the user is logged in with admin-level permissions
    and deletes a specific news item from the database.
    Args:
        news_id (int): The ID of the news item to delete.
    Returns:
        Redirects to the dashboard after deleting the news item.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            news_id = request.form['news_id']
            sql_data = get_cursor()
            sql_data.execute("""DELETE FROM news WHERE news_id=%s""", (news_id,))
            sql_data.close()
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/attendance_report', methods=['GET','POST'])
def attendance_report():
    """
    Generate an attendance report for classes.
    This function checks if the user is logged in with admin-level permissions
    and retrieves attendance data for classes from the database.
    Returns:
        A rendered HTML template displaying the attendance report.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            sql_data = get_cursor()
            total = 0
            total_list = [0, 0, 0]
            today = datetime.today().date()
            # Query the database to retrieve class attendance data
            sql = """SELECT log_id, attendance_date, is_individual FROM attendance_log
                            LEFT JOIN book_class_list ON book_class_list.book_class_id = attendance_log.class_id
                            WHERE attendance_date >= DATE_SUB(%s, INTERVAL 30 DAY) AND attendance_date <= %s;"""
            sql_value = (today, today)
            sql_data.execute(sql, sql_value)
            sql_list = sql_data.fetchall()
            for sql in sql_list:
                if sql[-1] == 0:
                    total_list[0] += 1
                elif sql[-1] == 1:
                    total_list[1] += 1
                else:
                    total_list[2] += 1
                total += 1
            today = datetime.today().date()
            sql = """SELECT  a.class_id,DATE_FORMAT(a.class_date,'%d %b %Y'),a.start_time,a.end_time,a.class_name,a.group_count,IFNULL(b.attendance_count, 0) AS attendance_count
                                    FROM 
                                        (SELECT bcl.book_class_id AS class_id, bcl.class_date, bcl.start_time, bcl.end_time, cl.class_name,
                                        (SELECT COUNT(*) FROM book_list AS bl WHERE bl.class_id = bcl.book_class_id) AS group_count
                                        FROM book_class_list AS bcl
                                        LEFT JOIN class_list AS cl ON cl.class_id = bcl.class_id
                                        WHERE bcl.class_id != 1
                                        GROUP BY CONCAT(bcl.class_date, bcl.start_time, bcl.end_time, cl.class_name)) AS a
                                    LEFT JOIN
                                        (SELECT class_id,COUNT(*) AS attendance_count
                                        FROM attendance_log
                                        GROUP BY class_id) AS b
                                    ON a.class_id = b.class_id
                                    WHERE a.class_date<=%s
                                    ORDER BY a.class_date DESC;"""
            sql_data.execute(sql, (today,))
            attendance = sql_data.fetchall()
            for i in range(len(attendance)):
                attendance[i] = list(attendance[i])
                if attendance[i][5]:
                    attendance[i].append(int(attendance[i][6]) / int(attendance[i][5]) * 100)
                    attendance[i][7] = round(attendance[i][7], 1)
                else:
                    attendance[i].append(0.0)
            sql_data.close()
            return render_template('admin/attendance_report.html', total=total, total_list=total_list, attendance=attendance, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_financial_report', methods=['GET','POST'])
def admin_financial_report():
    """
    Generate financial reports based on user selection.
    This function checks if the user is logged in with admin-level permissions
    and generates financial reports based on user selections, including monthly,
    yearly, and last 30 days reports.
    Returns:
        A rendered HTML template displaying the financial report.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            sql_data = get_cursor()
            title = 'Financial activity of last 30 days'
            year_list = []
            payment_list = []
            method_list = ['Paypal','Master Card','Credit']
            count_list = []
            income_list = []
            month_list = False
            month_flag = False
            year_flag = False
            lesson = 0
            membership = 0
            lesson_float = 0.0
            membership_float = 0.0
            total_float = 0.0
            # if the user wants to choose a report type
            if request.form.get('report_type'):
                report_type = request.form.get('report_type')
                if report_type == 'month':
                    month_flag = True
                else:
                    year_flag = True
                    for i in range(2015,2025):
                        year_list.append(i)
                return render_template('admin/financial_report.html', title=title, month_flag=month_flag, year_flag=year_flag, year_list=year_list, payment_list=payment_list, lesson_float=lesson_float, membership_float=membership_float, total_float=total_float, method_list=method_list, count_list=count_list, month_list=month_list, income_list=income_list, permissions=check_permissions())
            # if the user chooses monthly report
            elif request.form.get('month'):
                start_date = request.form.get('month') + '-01'
                sql = """SELECT * FROM payment_list
                        WHERE payment_date >= %s
                        AND payment_date < DATE_ADD(%s, INTERVAL 1 MONTH)
                        ORDER BY payment_date;"""
                sql_value = (start_date,start_date)
                month_num = int(request.form.get('month')[5:])
                year_num = request.form.get('month')[:4]
                title = 'Monthly report on {} {}'.format(calendar.month_name[month_num],year_num)
            # if the user chooses annual report
            elif request.form.get('year'):
                financial_date = request.form.get('year') + '-03-31'
                sql = """SELECT * FROM payment_list
                        WHERE payment_date > DATE_SUB(%s, INTERVAL 1 YEAR)
                        AND payment_date <= %s
                        ORDER BY payment_date;"""
                sql_value = (financial_date,financial_date)
                title = 'Annual report between 01/04/{} and 31/03/{}'.format(int(request.form.get('year'))-1,request.form.get('year'))
                month_list = ['04','05','06','07','08','09','10','11','12','01','02','03']
            # default report shows activity of last 30 days
            else:
                today_date = date.today()
                sql = """SELECT * FROM payment_list
                        WHERE payment_date >= DATE_SUB(%s, INTERVAL 30 DAY)
                        AND payment_date <= %s
                        ORDER BY payment_date;"""
                sql_value = (today_date, today_date)
            sql_data.execute(sql, sql_value)
            sql_list = sql_data.fetchall()
            # Organise sql_list and append them into payment_list
            for sql in sql_list:
                temp_list = list(sql)
                temp_list[2] = format(temp_list[2], '.2f')
                temp_list[3] = sql[3].strftime("%d %b %Y")
                payment_list.append(temp_list)
            # Calculate membership subscription and individual lesson total revenue
            for payment in payment_list:
                if payment[4] == 'Membership':
                    membership += float(payment[2])
                elif payment[4] == 'Lesson':
                    lesson += float(payment[2])
            # Calculate number of each payment method in the payment list
            for method in method_list:
                count = 0
                for payment in payment_list:
                    if payment[-1] == method:
                        count += 1
                count_list.append(count)
            # If produce an annual report, calculate revenue for each month
            if month_list:
                for month in month_list:
                    count = 0
                    for payment in payment_list:
                        if payment[3][3:6] == calendar.month_name[int(month)][:3]:
                            count += float(payment[2])
                    income_list.append(count)
                # Reconstruct month_list
                month_list = []
                for i in range(4,13,1):
                    string = ''
                    string = calendar.month_name[i] + ' ' + str(int(request.form.get('year'))-1)
                    month_list.append(string)
                for i in range(1,4,1):
                    string = ''
                    string = calendar.month_name[i] + ' ' + request.form.get('year')
                    month_list.append(string)
            total = lesson + membership
            lesson_float = format(lesson, '.2f')
            membership_float = format(membership, '.2f')
            total_float = format(total, '.2f')
            sql_data.close()
            return render_template('admin/financial_report.html', title=title, month_flag=month_flag, year_flag=year_flag, year_list=year_list, payment_list=payment_list, lesson_float=lesson_float, membership_float=membership_float, total_float=total_float, method_list=method_list, count_list=count_list, month_list=month_list, income_list=income_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_popularity_report')
def admin_popularity_report():
    """
    Generate a popularity report for classes based on bookings and attendance.
    This function checks if the user is logged in with admin-level permissions
    and generates a popularity report for classes within the last 30 days. The report
    includes class details, the number of bookings, and the number of attendances.
    Returns:
        A rendered HTML template displaying the popularity report.
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            today = date.today()
            booking_list = []
            booking_numbers = []
            booking_total = 0
            attendance_list = []
            attendance_numbers = []
            attendance_total = 0
            sql_data = get_cursor()
            # Fetch a list of class details within the last 30 days
            sql_data.execute("""SELECT book_class_id, class_name FROM book_class_list 
                                INNER JOIN class_list ON class_list.class_id = book_class_list.class_id
                                WHERE (is_individual) = 0 AND (class_date >= DATE_SUB(%s, INTERVAL 30 DAY) AND class_date <= %s);
                                """, (today, today))
            sql_list = sql_data.fetchall()
            # build up booking_list
            for sql in sql_list:
                if sql[1] not in booking_list:
                    booking_list.append(sql[1])
                    booking_numbers.append(0)
                booking_total += 1
            # build up booking numbers
            for i in range(0, len(booking_list), 1):
                for sql in sql_list:
                    if sql[1] == booking_list[i]:
                        booking_numbers[i] += 1
            # Fetch a list of recent attendances
            sql_data.execute("""SELECT log_id, class_name FROM attendance_log
                                    INNER JOIN book_class_list ON attendance_log.class_id = book_class_list.book_class_id
                                    INNER JOIN class_list ON class_list.class_id = book_class_list.class_id
                                    WHERE (is_individual) = 0 AND (attendance_date >= DATE_SUB(%s, INTERVAL 30 DAY) AND attendance_date <= %s);""", (today, today))
            sql_list = sql_data.fetchall()
            # build up attendance_list
            for sql in sql_list:
                if sql[1] not in attendance_list:
                    attendance_list.append(sql[1])
                    attendance_numbers.append(0)
                attendance_total += 1
            # build up attendance numbers
            for i in range(0, len(attendance_list), 1):
                for sql in sql_list:
                    if sql[1] == attendance_list[i]:
                        attendance_numbers[i] += 1
            sql_data.close()
            return render_template('admin/popularity_report.html', booking_list=booking_list, booking_numbers=booking_numbers, booking_total=booking_total,
                                   attendance_list=attendance_list, attendance_numbers=attendance_numbers, attendance_total=attendance_total,
                                   permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/edit_pool', methods=['GET', 'POST'])
def edit_pool():
    """
    Add swimming pool
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            sql_data = get_cursor()
            if request.method == 'POST':
                pool_id = request.form.get('pool_id')
                if pool_id:
                    sql_data.execute("""DELETE FROM pool WHERE pool_id=%s;""", (pool_id,))
                else:
                    pool_name = request.form.get('pool_name').capitalize()
                    sql_data.execute("""INSERT INTO pool (pool_name) VALUE (%s);""", (pool_name,))
            sql_data.execute("""SELECT * FROM pool;""")
            pool_list = sql_data.fetchall()
            return render_template('admin/edit_pool.html', pool_list=pool_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/edit_classes', methods=['GET', 'POST'])
def edit_classes():
    """
    Add class
    """
    if 'loggedIn' in session:
        if check_permissions() > 2:
            sql_data = get_cursor()
            if request.method == 'POST':
                classes_id = request.form.get('class_id')
                if classes_id:
                    sql_data.execute("""DELETE FROM class_list WHERE class_id=%s;""", (classes_id,))
                else:
                    classes_name = request.form.get('class_name').capitalize()
                    sql_data.execute("""INSERT INTO class_list (class_name) VALUE (%s);""", (classes_name,))
            sql_data.execute("""SELECT * FROM class_list;""")
            class_list = sql_data.fetchall()
            return render_template('admin/edit_class.html', class_list=class_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
