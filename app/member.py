from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, get_cursor, title_list, region_list, city_list


@app.route('/member_change_information', methods=['GET', 'POST'])
def member_change_information():
    """
    Webpage used for members to change their own information.
    This function performs the following tasks:
    - Checks if the user is logged in.
    - Validates user permissions (assuming 1 represents permission).
    - Handles member information change when the HTTP request method is POST.
    - Validates and updates the member's details in the database.
    - Checks if the provided email is already in use.
    - Redirects to the previous page or user list page based on the referrer URL.
    - Retrieves the member's details from the database and renders the 'change_information.html' template.
    Returns:
        - If the user is logged in and has permission, renders the 'change_information.html' template with member details.
        - If not logged in, redirects to the login page.
        - If not a member or lacking permission, redirects to the index page.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            user_id = session["user_id"]
            sql_data = get_cursor()
            msg = ""
            today = datetime.today().date()
            if request.method == 'POST':
                first_name = request.form.get('first_name').capitalize()
                last_name = request.form.get('last_name').capitalize()
                birth_date = request.form.get('birth_date')
                title = int(request.form.get('title'))
                email = request.form.get('email')
                phone_number = request.form.get('phone_number')
                region = int(request.form.get('region'))
                city = int(request.form.get('city'))
                street_name = request.form.get('street_name')
                detailed_information = request.form.get('detailed_information')
                health_information = request.form.get('health_information')
                user_id = request.form.get('user_id')
                sql = """UPDATE `member` SET first_name=%s,last_name=%s,birth_date=%s,title_id=%s,phone_number=%s,region_id=%s,city_id=%s,street_name=%s,
                            detailed_information=%s, health_information=%s 
                            WHERE user_id=%s;"""
                sql_value = (first_name, last_name, birth_date, title, phone_number, region, city, street_name, detailed_information, health_information,
                             user_id,)
                sql_data.execute(sql, sql_value)
                # check email
                sql_data.execute("SELECT user_id, email FROM `user_account` WHERE user_id=%s;", (user_id,))
                user_account_list = sql_data.fetchall()[0]
                if email != user_account_list[1]:
                    sql_data.execute("SELECT user_id, email FROM `user_account` WHERE email=%s;", (email,))
                    # Check if the new email is already in use
                    if len(sql_data.fetchall()) > 0:
                        msg = "This email is already in use."
                    else:
                        sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
                # Get the previous URL to determine redirection
                previous_url = str(request.referrer)
                urlList = [x for x in previous_url.split('/') if x != '']
                # If the user came from the 'user_list' page, redirect there
                if urlList[-1] == 'user_list':
                    return redirect(url_for('user_list'))
            sql = """SELECT m.user_id,m.title_id,m.first_name,m.last_name,m.phone_number,m.detailed_information,m.region_id,
                        m.city_id,m.street_name,m.birth_date,m.health_information,u.email FROM `member` AS m
                        LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                        WHERE m.user_id=%s;"""
            sql_value = (user_id,)
            sql_data.execute(sql, sql_value)
            member_detail = sql_data.fetchall()[0]
            sql_data.close()
            return render_template('member/change_information.html', member_detail=member_detail, msg=msg, title_list=title_list,
                                   region_list=region_list, city_list=city_list, permissions=check_permissions(), today=today)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/view_class', methods=['GET', 'POST'])
def view_class():
    """
    Display a timetable of classes for members.
    This route handles both GET and POST requests. It provides members with a timetable of classes for the current week
    or a selected date. It allows members to view class details, such as class name, instructor, pool, and available slots.
    :return: The 'timetable.html' template with class timetable data.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
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
            # Calculate the start of the week for the selected or current date
            start_of_week = today - timedelta(days=today.weekday())
            week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            week_list = [["", "", "Time/Day"]]
            # Generate the timetable header with dates and weekdays
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
                        WHERE (b.class_date BETWEEN %s AND %s) AND (i.state=1) AND (b.is_individual=0)
                        ORDER BY b.start_time"""
            sql_value = (week_list[1][0], week_list[-1][0])
            sql_data.execute(sql, sql_value)
            all_details_sql = sql_data.fetchall()
            sql_data.execute("""SELECT * FROM pool;""")
            pool_list = sql_data.fetchall()
            sql_data.execute("""SELECT * FROM instructor AS i LEFT JOIN title AS t ON i.title_id=t.title_id WHERE i.state=1;""")
            sql_instructor_list = sql_data.fetchall()
            sql = """SELECT class_id, COUNT(member_id) AS member_count
                        FROM book_list
                        GROUP BY class_id;"""
            sql_data.execute(sql)
            member_count = sql_data.fetchall()
            # Convert member_count data to a dictionary for easy access
            for i in range(len(member_count)):
                member_count[i] = list(member_count[i])
            member_count = {item[0]: item[1] for item in member_count}
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
            all_details = {item['id']: item for item in all_details}
            return render_template('member/timetable.html', week_list=week_list, all_details=all_details, today=today, pool_list=pool_list,
                                   member_count=member_count, instructor_list=sql_instructor_list, permissions=check_permissions(), before_day=before_day, before_time=before_time)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/member_book_lesson', methods=['POST'])
def member_book_lesson():
    """
    Handle member class booking.
    This route allows members to book classes based on instructor availability for a selected date and time.
    It also checks for active subscriptions and instructor availability.
    :return: The 'book_lesson.html' template with booking options.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            # Extract date and time information from the form data
            form_date = request.form.get('send_day')
            form_time = request.form.get('send_time')
            current_year = datetime.now().year
            # Parse the selected date and set it to the current year
            parsed_date = datetime.strptime(form_date, '%Y-%m-%d')
            complete_date = parsed_date.replace(year=current_year)
            complete_date_string = complete_date.strftime('%Y-%m-%d')
            # Parse the selected time and format it as 'HH:MM:SS'
            parsed_time = datetime.strptime(form_time, '%H:%M').time()
            start_time = parsed_time.replace(second=0).strftime('%H:%M:%S')
            # Calculate the end time, which is 30 minutes after the selected start time
            end_time = datetime.combine(datetime.min, parsed_time) + timedelta(minutes=30)
            sql_data = get_cursor()

            user_id = session['user_id']
            sql = """SELECT member_id From member WHERE user_id=%s;"""
            sql_data.execute(sql, (user_id,))
            member_id = sql_data.fetchall()[0][0]
            sql = """SELECT start_date, end_date FROM payment_due WHERE member_id = %s AND end_date>=%s"""
            sql_data.execute(sql, (member_id, datetime.today().date()))
            subscription = sql_data.fetchall()
            # If the member doesn't have an active subscription, redirect to the index page
            if not subscription:
                return redirect(url_for('index'))

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
            sql_data.execute(sql, value)
            sql_instructor_list = sql_data.fetchall()
            sql_data.execute("SELECT * FROM class_list;")
            class_list = sql_data.fetchall()
            sql_data.execute("""SELECT * FROM pool;""")
            pool_list = sql_data.fetchall()
            return render_template('member/book_lesson.html', instructor_list=sql_instructor_list, class_list=class_list, pool_list=pool_list, time=str(start_time), date=complete_date_string, edit=1, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/individual_payment', methods=['POST'])
def individual_payment():
    """
    Handle individual payment for booking a class.
    This route allows members to make individual payments for booking a class.
    It collects class details, instructor information, and payment options.
    :return: The 'individual_payment.html' template with payment options.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            # Retrieve form data for available date, start time, hour, instructor, and pool
            available_date = request.form.get('available_date')
            start_hour = request.form.get('start_hour')
            start_minute = request.form.get('start_minute')
            hour = request.form.get('hour')
            instructor = int(request.form.get('instructor'))
            pool = int(request.form.get('pool'))
            start_time = str(start_hour) + ":" + str(start_minute)
            parsed_time = datetime.strptime(start_time, '%H:%M').time()
            # Format start time and calculate end time based on class duration
            start_time = parsed_time.replace(second=0).strftime('%H:%M:%S')
            if int(hour) == 1:
                end_time = datetime.combine(datetime.min, parsed_time) + timedelta(minutes=30)
            else:
                end_time = datetime.combine(datetime.min, parsed_time) + timedelta(minutes=60)
            end_time = end_time.replace(second=0).strftime('%H:%M:%S')
            # Store relevant session data
            session['available_date'] = available_date
            session['start_time'] = start_time
            session['end_time'] = end_time
            session['instructor'] = instructor
            session['pool'] = pool
            session['hour'] = hour
            sql_data = get_cursor()
            sql_data.execute("""SELECT pool_name From pool WHERE pool_id = %s""", (pool,))
            pool_name = sql_data.fetchall()[0][0]
            sql = """SELECT CONCAT(t.title, " ", i.first_name, " ", i.last_name) as name From instructor AS i 
                        LEFT JOIN title AS t ON t.title_id=i.title_id WHERE i.user_id = %s"""
            sql_data.execute(sql, (instructor,))
            instructor_name = sql_data.fetchall()[0][0]
            return render_template('member/individual_payment.html', pool_name=pool_name, instructor_name=instructor_name, hour=hour, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/pay_successful', methods=['POST'])
def pay_successful():
    """
    Handle successful payment for booking a class.
    This route is used to process successful payments for class bookings.
    It calculates the price based on the class duration, records the payment,
    and updates the database with the booking information.
    :return: The 'jump.html' template with a success message and redirection link.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            # Retrieve session data and form data
            available_date = session['available_date']
            start_time = session['start_time']
            end_time = session['end_time']
            instructor = int(session['instructor'])
            pool = int(session['pool'])
            user_id = session['user_id']
            hour = int(session['hour'])
            payment_method = request.form.get('payment_method')
            if hour == 1:
                price = 44
            else:
                price = 80
            #     Remove session data to avoid duplication
            session.pop('available_date', None)
            session.pop('start_time', None)
            session.pop('end_time', None)
            session.pop('instructor', None)
            session.pop('pool', None)
            session.pop('hour', None)
            today = datetime.today().date()
            sql_data = get_cursor()
            sql = """SELECT member_id From member WHERE user_id=%s;"""
            sql_data.execute(sql, (user_id,))
            member_id = sql_data.fetchall()[0][0]
            sql = """SELECT instructor_id From instructor WHERE user_id=%s;"""
            sql_data.execute(sql, (instructor,))
            instructor_id = sql_data.fetchall()[0][0]
            sql = """INSERT INTO book_class_list (instructor_id, pool_id, class_id, class_date, start_time, end_time, is_individual) VALUES (%s,%s,1,%s,%s,%s,1);"""
            value = (instructor_id, pool, str(available_date), str(start_time), str(end_time))
            sql_data.execute(sql, value)
            sql_data.execute("""SET @book_class_id = LAST_INSERT_ID();""")
            sql = """INSERT INTO payment_list (member_id, price, payment_date, payment_type, payment_method) VALUES (%s,%s,%s,'Lesson',%s);"""
            value = (member_id, price, today, payment_method)
            sql_data.execute(sql, value)
            sql_data.execute("""SET @payment_id = LAST_INSERT_ID();""")
            sql = """INSERT INTO book_list (member_id, class_id, instructor_id, pool_id, payment_id) VALUES (%s,@book_class_id,%s,%s,@payment_id);"""
            value = (member_id, instructor_id, pool)
            sql_data.execute(sql, value)
            msg = "Payment was successful! Jump to my lesson."
            goUrl = '/member_class_detail'
            return render_template('guest/jump.html', msg=msg, goUrl=goUrl, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/member_class_detail', methods=['GET'])
def member_class_detail():
    """
    Display class details for a member.
    This route displays details of upcoming classes for a logged-in member.
    It retrieves class information from the database and renders it in the 'class_detail.html' template.
    :return: The 'class_detail.html' template with class details.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            today = datetime.today().date()
            user_id = int(session['user_id'])
            sql_data = get_cursor()
            sql = """SELECT DATE_FORMAT(bc.class_date,'%d %b %Y'),bc.start_time,bc.end_time, CONCAT(t.title, ' ', i.first_name, ' ', i.last_name) as instructor_name, i.phone_number, p.pool_name, bc.is_individual, bl.class_id
                        FROM book_list AS bl
                        LEFT JOIN book_class_list AS bc ON bc.book_class_id=bl.class_id
                        LEFT JOIN instructor AS i ON i.instructor_id=bl.instructor_id
                        LEFT JOIN title AS t ON t.title_id=i.title_id
                        LEFT JOIN pool AS p ON p.pool_id=bl.pool_id
                        LEFT JOIN member AS m ON m.member_id=bl.member_id
                        WHERE m.user_id=%s AND bc.class_date>=%s
                        order by bc.class_date;"""
            sql_data.execute(sql, (user_id, today,))
            detail_list = sql_data.fetchall()
            sql_data.close()
            # Prepare the data for rendering
            for i in range(len(detail_list)):
                detail_list[i] = list(detail_list[i])
                detail_list[i][0] = str(detail_list[i][0])
                detail_list[i][1] = str(detail_list[i][1])
                detail_list[i][2] = str(detail_list[i][2])
            return render_template('member/class_detail.html', detail_list=detail_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/class_detail', methods=['POST'])
def class_detail():
    """
    Display class details for an instructor.
    This route displays details of a specific class for instructors.
    It retrieves class information from the database and renders it in the 'class_details.html' template.
    :return: The 'class_details.html' template with class details.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            class_id = request.form.get('class_id')
            sql_data = get_cursor()
            sql = """SELECT b.book_class_id,p.pool_name,c.class_name,b.class_date,b.start_time,b.end_time,b.detailed_information,b.is_individual,
                        CONCAT(t.title, " ", i.first_name, " ", i.last_name) AS instructor_name,i.phone_number,i.detailed_information,i.state
                        FROM book_class_list AS b 
                        LEFT JOIN class_list AS c ON c.class_id=b.class_id
                        LEFT JOIN pool AS p ON b.pool_id=p.pool_id
                        LEFT JOIN instructor AS i ON b.instructor_id=i.instructor_id
                        LEFT JOIN title AS t ON i.title_id=t.title_id
                        WHERE b.book_class_id=%s AND i.state=1;"""
            sql_value = (class_id,)
            sql_data.execute(sql, sql_value)
            # Fetch the class information
            information = sql_data.fetchall()[0]
            information = list(information)
            information[4] = str(information[4])
            information[5] = str(information[5])
            sql = """SELECT class_id, COUNT(member_id) AS member_count
                            FROM book_list
                            WHERE class_id=%s;"""
            sql_value = (class_id,)
            sql_data.execute(sql, sql_value)
            member_count = sql_data.fetchall()[0]
            return render_template('instructor/class_details.html', information=information, member_count=member_count, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/member_book_class', methods=['POST'])
def member_book_class():
    """
    Allow members to book a class.
    This route allows members to book a specific class.
    It checks user permissions, class availability, and handles the booking process.
    :return: A confirmation message and redirection based on the booking result.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            user_id = session['user_id']
            class_id = request.form.get('class_id')
            sql_data = get_cursor()
            sql = """SELECT b.pool_id,b.instructor_id
                        FROM book_class_list AS b 
                        WHERE b.book_class_id=%s;"""
            sql_data.execute(sql, (class_id,))
            book_class_id = sql_data.fetchall()[0]
            sql = """SELECT member_id From member WHERE user_id=%s;"""
            sql_data.execute(sql, (user_id,))
            member_id = sql_data.fetchall()[0][0]

            sql = """SELECT start_date, end_date FROM payment_due WHERE member_id = %s AND end_date>=%s"""
            sql_data.execute(sql, (member_id, datetime.today().date()))
            subscription = sql_data.fetchall()
            # If there's no active subscription, redirect to the index page
            if not subscription:
                return redirect(url_for('index'))

            sql = """SELECT book_id From book_list WHERE class_id=%s AND member_id=%s;"""
            sql_data.execute(sql, (class_id, member_id,))
            # If the member hasn't booked the same class, proceed with the booking
            if not sql_data.fetchall():
                sql_data.execute("""SELECT count(book_id) From book_list WHERE class_id=%s AND member_id=%s;""", (class_id, member_id,))
                count = sql_data.fetchall()[0][0]
                if count < 30:
                    sql = """INSERT INTO book_list (member_id, class_id, instructor_id, pool_id) VALUES (%s,%s,%s,%s)"""
                    value = (member_id, class_id, book_class_id[1], book_class_id[0],)
                    sql_data.execute(sql, value)
                    msg = "Booking was successful! Jump to my class."
                    goUrl = '/member_class_detail'
                else:
                    msg = "There is no available slot for booking."
                    goUrl = '/view_class'
            else:
                msg = "You cannot book the same class twice! Jump to timetable."
                goUrl = '/view_class'
            return render_template('guest/jump.html', msg=msg, goUrl=goUrl, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/monthly_payment', methods=['GET', 'POST'])
def monthly_payment():
    """
    Handle monthly membership payments for members.
    This route allows members to choose a subscription duration, calculate the price, and process the payment.
    It also updates the membership due date based on the chosen subscription duration.
    :return: A confirmation message and redirection based on the payment result.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            msg = ''
            success_msg = None  # This will hold the success message
            user_id = session["user_id"]
            sql_data = get_cursor()
            sql = """SELECT member_id FROM member WHERE user_id=%s;"""
            sql_data.execute(sql, (user_id,))
            member_id = sql_data.fetchall()[0][0]
            sql = """SELECT member_id, start_date, end_date FROM payment_due
                                WHERE member_id=%s;"""
            sql_data.execute(sql, (member_id,))
            membership_due = sql_data.fetchall()
            due = ''
            # If there's an existing membership due record, get the end date
            if membership_due:
                due = membership_due[0][2]
            member_price = 70
            if request.method == 'GET':
                sql_data.close()
                return render_template('member/monthly_payment.html', msg=msg, membership_due=str(due), member_price=member_price, permissions=check_permissions())
            else:
                subscription_duration = int(request.form.get('subscription_duration'))
                payment_method = request.form.get('payment_method')
                # Calculate the price based on the selected duration
                if subscription_duration == 1:
                    month = 1
                    price = member_price
                elif subscription_duration == 2:
                    month = 3
                    price = member_price * 3 * 0.95
                elif subscription_duration == 3:
                    month = 6
                    price = member_price * 6 * 0.9
                elif subscription_duration == 4:
                    month = 12
                    price = member_price * 12 * 0.85
                else:
                    return redirect(url_for('index'))
                sql = """INSERT INTO payment_list (member_id, price, payment_date, payment_type, payment_method) 
                        VALUES (%s, %s, %s, 'Membership', %s)"""
                value = (member_id, price, datetime.today().date(), payment_method,)
                sql_data.execute(sql, value)
                # Update the membership due date based on the selected subscription duration
                if membership_due:
                    start_date = membership_due[0][2]
                    end_date = start_date + timedelta(days=30 * month)
                    due_sql = """UPDATE payment_due SET end_date=%s WHERE member_id=%s"""
                    sql_data.execute(due_sql, (end_date, member_id))
                else:
                    sql_data.execute("""SET @payment_id = LAST_INSERT_ID();""")
                    start_date = datetime.today().date()
                    end_date = start_date + timedelta(days=30 * month)
                    due_sql = """INSERT INTO payment_due (payment_id, member_id, start_date, end_date) VALUES (@payment_id,%s,%s,%s)"""
                    sql_data.execute(due_sql, (member_id, start_date, end_date))
                sql_data.close()
                success_msg = 'Thank you for your payment.'
                return render_template('guest/jump.html', goUrl='/', msg=success_msg, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/my_membership', methods=['GET'])
def my_membership():
    """
    Display the membership details of a logged-in member.
    This route retrieves and displays information about a member's current membership status,
    including the start and end dates of their subscription.
    :return: The 'my_membership.html' template with membership details.
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            user_id = session["user_id"]
            sql_data = get_cursor()
            sql = """SELECT member_id FROM member WHERE user_id=%s;"""
            sql_data.execute(sql, (user_id,))
            member_id = sql_data.fetchall()[0][0]
            sql = """SELECT start_date, end_date FROM payment_due WHERE member_id = %s"""
            sql_data.execute(sql, (member_id,))
            subscription = sql_data.fetchone()
            sql_data.close()
            # Determine the membership status and dates
            if subscription:
                start_date, end_date = subscription
                status = "Active" if end_date >= datetime.today().date() else "Expired"
                start_date = start_date.strftime('%d %b %Y')
                end_date = end_date.strftime('%d %b %Y')
            else:
                start_date, end_date = None, None
                status = "No Subscription"
            return render_template('member/my_membership.html', status=status, start_date=start_date, end_date=end_date, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/delete_book_class', methods=['POST'])
def delete_book_class():
    """
    Cancel scheduled class
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            user_id = session["user_id"]
            sql_data = get_cursor()
            sql = """SELECT member_id FROM member WHERE user_id=%s;"""
            sql_data.execute(sql, (user_id,))
            member_id = sql_data.fetchall()[0][0]
            class_id = request.form.get('class_id')
            sql = """DELETE FROM `book_list` WHERE class_id=%s AND member_id=%s;"""
            sql_data.execute(sql, (class_id, member_id,))
            msg = 'Cancel successfully.'
            return render_template('guest/jump.html', goUrl='/member_class_detail', msg=msg, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/delete_book_lesson', methods=['POST'])
def delete_book_lesson():
    """
    Cancel scheduled lesson
    """
    if 'loggedIn' in session:
        if check_permissions() == 1:
            user_id = session["user_id"]
            sql_data = get_cursor()
            sql = """SELECT member_id FROM member WHERE user_id=%s;"""
            sql_data.execute(sql, (user_id,))
            member_id = sql_data.fetchall()[0][0]
            class_id = request.form.get('class_id')
            sql = """SELECT class_id, payment_id FROM book_list WHERE class_id=%s AND member_id=%s;"""
            sql_data.execute(sql, (class_id, member_id,))
            book_class_id = sql_data.fetchall()[0][0]
            payment_id = sql_data.fetchall()[0][1]
            sql = """DELETE FROM `book_list` WHERE class_id=%s AND member_id=%s;"""
            sql_data.execute(sql, (class_id, member_id,))
            sql = """DELETE FROM `payment_list` WHERE payment_id=%s;"""
            sql_data.execute(sql, (payment_id,))
            sql = """DELETE FROM `book_class_list` WHERE book_class_id=%s;"""
            sql_data.execute(sql, (book_class_id,))
            msg = 'Cancel successfully.'
            return render_template('guest/jump.html', goUrl='/member_class_detail', msg=msg, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
