from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, get_cursor, title_list


@app.route('/instructor_change_information', methods=['GET', 'POST'])
def instructor_change_information():
    """
    The webpage used to give the instructor change his own information
    :return: change_information.html
    """

    def check_change(old, new):
        for i in range(len(new)):
            if old[i + 1] != new[i]:
                return True
        return False

    if 'loggedIn' in session:
        if check_permissions() > 1:
            user_id = session["user_id"]
            sql_data = get_cursor()
            msg = ""
            if request.method == 'POST':
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                title = int(request.form.get('title'))
                email = request.form.get('email')
                phone_number = request.form.get('phone_number')
                detailed_information = request.form.get('detailed_information')
                user_id = request.form.get('user_id')
                sql = """SELECT i.user_id,i.first_name,i.last_name,i.title_id,u.email,i.phone_number,i.detailed_information FROM `instructor` AS i
                            LEFT JOIN `user_account` AS u ON i.user_id=u.user_id
                            WHERE i.user_id=%s;"""
                sql_value = (user_id,)
                sql_data.execute(sql, sql_value)
                instructor_list = sql_data.fetchall()[0]
                new_data = (first_name, last_name, title, email, phone_number, detailed_information)
                if check_change(instructor_list, new_data):
                    sql = """UPDATE `instructor` SET first_name=%s,last_name=%s,title_id=%s,phone_number=%s,detailed_information=%s WHERE user_id=%s;"""
                    sql_value = (first_name, last_name, title, phone_number, detailed_information, user_id,)
                    sql_data.execute(sql, sql_value)
                    # check email
                    sql_data.execute("SELECT user_id, email FROM `user_account` WHERE user_id=%s;", (user_id,))
                    user_account_list = sql_data.fetchall()[0]
                    if email != user_account_list[1]:
                        sql_data.execute("SELECT user_id, email FROM `user_account` WHERE email=%s;", (email,))
                        if len(sql_data.fetchall()) > 0:
                            msg = "This email already be used."
                        else:
                            sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
                else:
                    msg = "no modification"
                previous_url = str(request.referrer)
                urlList = [x for x in previous_url.split('/') if x != '']
                if urlList[-1] == 'user_list':
                    return redirect(url_for('user_list'))
            sql = """SELECT i.user_id,i.title_id,i.first_name,i.last_name,i.phone_number,i.detailed_information,u.email FROM `instructor` AS i
                        LEFT JOIN `user_account` AS u ON i.user_id=u.user_id
                        WHERE i.user_id=%s;"""
            sql_value = (user_id,)
            sql_data.execute(sql, sql_value)
            instructor_detail = sql_data.fetchall()[0]
            sql_data.close()
            return render_template('instructor/change_information.html', instructor_detail=instructor_detail, msg=msg, title_list=title_list,
                                   permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/instructor_timetable', methods=['GET', 'POST'])
def instructor_timetable():
    if 'loggedIn' in session:
        if check_permissions() > 1:
            user_id = session["user_id"]
            if request.method == 'POST':
                today = datetime.strptime(request.form.get('day'), '%Y-%m-%d').date()
            else:
                today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            week_list = [["Time/Day", '']]
            for i in range(7):
                temp_list = [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d'), week[i]]
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
                        WHERE (b.class_date BETWEEN %s AND %s) AND (i.state=1) AND (i.user_id=%s)
                        ORDER BY b.start_time"""
            sql_value = (week_list[1][0], week_list[-1][0], user_id)
            sql_data.execute(sql, sql_value)
            all_details_sql = sql_data.fetchall()
            sql_data.execute("""SELECT * FROM pool;""")
            pool_list = sql_data.fetchall()
            sql = """SELECT class_id, COUNT(member_id) AS member_count
                        FROM book_list
                        GROUP BY class_id;"""
            sql_data.execute(sql)
            member_count = sql_data.fetchall()
            sql = """SELECT user_id,instructor_id FROM instructor WHERE user_id=%s"""
            sql_data.execute(sql, (user_id,))
            instructor_id = sql_data.fetchall()[0][1]
            sql_data.execute("SELECT user_id, date, start_time, end_time FROM available_time WHERE (date BETWEEN %s AND %s) AND (user_id=%s);",
                             (week_list[1][0], week_list[-1][0], user_id,))
            lock_list = sql_data.fetchall()
            for i in range(len(lock_list)):
                time = int(((lock_list[i][2].total_seconds() / 3600) - 5) * 2)
                continuance = int(((lock_list[i][3] - lock_list[i][2]).total_seconds() / 3600) * 2)
                lock_list[i] = list(lock_list[i])
                lock_list[i][1] = str(lock_list[i][1].weekday() + 1)
                lock_list[i][2] = time - 1
                lock_list[i][3] = continuance
            for i in range(1, len(week_list), 1):
                week_list[i][0] = week_list[i][0][5:]
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
            for i in range(len(member_count)):
                member_count[i] = list(member_count[i])
            member_count = {item[0]: item[1] for item in member_count}
            return render_template('instructor/timetable.html', week_list=week_list, pool_list=pool_list, today=today, instructor_id=instructor_id,
                                   all_details=all_details, member_count=member_count, lock_list=lock_list, link=url_for('instructor_timetable'),
                                   permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/schedule_time', methods=['GET', 'POST'])
def schedule_time():
    if 'loggedIn' in session:
        if check_permissions():
            sql_data = get_cursor()
            user_id = session["user_id"]
            error_msg = ""
            success_msg = ""
            today = date.today() + timedelta(days=1)
            if request.method == 'POST':
                available_date = datetime.strptime(request.form.get('available_date'), '%Y-%m-%d').date()
                start_time = datetime.strptime(request.form.get('start_time'), '%H:%M:%S')
                total_sec = start_time.hour * 3600 + start_time.minute * 60 + start_time.second
                start_time = timedelta(seconds=total_sec)
                end_time = datetime.strptime(request.form.get('end_time'), '%H:%M:%S')
                total_sec = end_time.hour * 3600 + end_time.minute * 60 + end_time.second
                end_time = timedelta(seconds=total_sec)
                sql = """SELECT date, start_time, end_time FROM available_time WHERE user_id=%s;"""
                sql_value = (user_id,)
                sql_data.execute(sql, sql_value)
                check_list = sql_data.fetchall()
                if start_time >= end_time:
                    error_msg = "End time cannot be earlier or equal to start time"
                    return render_template('instructor/schedule_time.html', success_msg=success_msg, error_msg=error_msg, date_list=check_list,
                                           today=today, permissions=check_permissions())
                for check in check_list:
                    if check[0] == available_date and start_time >= check[1] and start_time < check[2]:
                        error_msg = "Invalid start time or end time"
                        return render_template('instructor/schedule_time.html', success_msg=success_msg, error_msg=error_msg, date_list=check_list,
                                               today=today, permissions=check_permissions())
                    elif check[0] == available_date and end_time > check[1] and end_time <= check[2]:
                        error_msg = "Invalid start time or end time"
                        return render_template('instructor/schedule_time.html', success_msg=success_msg, error_msg=error_msg, date_list=check_list,
                                               today=today, permissions=check_permissions())
                sql = """INSERT INTO available_time VALUES (NULL,%s,%s,%s,%s);"""
                sql_value = (user_id, available_date, start_time, end_time)
                sql_data.execute(sql, sql_value)
                success_msg = "Schedule added successfully"
            sql = """SELECT date, start_time, end_time FROM available_time WHERE user_id=%s;"""
            sql_value = (user_id,)
            sql_data.execute(sql, sql_value)
            date_list = sql_data.fetchall()
            sql_data.close()
            return render_template('instructor/schedule_time.html', success_msg=success_msg, error_msg=error_msg, date_list=date_list, today=today,
                                   permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/instructor_class_details', methods=['GET', 'POST'])
def instructor_class_details():
    if 'loggedIn' in session:
        if request.method == 'POST':
            if check_permissions():
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
                class_detail = sql_data.fetchall()[0]
                information = list(class_detail)
                information[4] = str(information[4])
                information[5] = str(information[5])
                sql = """SELECT class_id, COUNT(member_id) AS member_count
                            FROM book_list
                            WHERE class_id=%s;"""
                sql_value = (class_id,)
                sql_data.execute(sql, sql_value)
                member_count = sql_data.fetchall()[0]
                member_list = []
                if member_count[1]:
                    sql = """SELECT t.title,m.first_name,m.last_name,m.phone_number,m.detailed_information,m.health_information FROM book_list AS b
                                RIGHT JOIN member AS m ON m.member_id=b.member_id
                                LEFT JOIN title AS t ON m.title_id=t.title_id
                                where b.class_id=%s;"""
                    sql_value = (class_id,)
                    sql_data.execute(sql, sql_value)
                    member_list = sql_data.fetchall()
                return render_template('instructor/class_details.html', information=information, member_count=member_count, member_list=member_list,
                                       permissions=check_permissions())
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
