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
    :return: instructor_change_information.html
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
            return render_template('instructor/instructor_change_information.html', instructor_detail=instructor_detail, msg=msg, title_list=title_list, permissions=check_permissions())
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
            sql = """SELECT c.class_id, c.instructor_id, c.pool_id, p.pool_name, c.is_individual, c.class_name, 
                        CONCAT(t.title, " ", i.first_name, " ", i.last_name) AS instructor_name, i.phone_number,
                        i.state, c.class_date, c.start_time, c.end_time
                        FROM class_list AS c
                        LEFT JOIN pool AS p ON c.pool_id=p.pool_id
                        LEFT JOIN instructor AS i ON c.instructor_id=i.instructor_id
                        LEFT JOIN title AS t ON i.title_id=t.title_id
                        WHERE (c.class_date BETWEEN %s AND %s) AND (i.state=1) AND (i.user_id=%s)
                        ORDER BY c.start_time"""
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
            for i in range(1, len(week_list), 1):
                week_list[i][0] = week_list[i][0][5:]
            all_details = []
            for item in all_details_sql:
                time = int(((item[10].total_seconds() / 3600) - 9) * 2)
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
            return render_template('instructor/instructor_timetable.html', week_list=week_list, pool_list=pool_list, today=today, instructor_id=instructor_id,
                                   all_details=all_details, member_count=member_count, link=url_for('instructor_timetable'), permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
