from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, get_cursor, title_list, city_list, region_list


@app.route('/member_change_information', methods=['GET', 'POST'])
def member_change_information():
    """
    The webpage used to give the member change his own information
    :return: member_change_information.html
    """
    if 'loggedIn' in session:
        if check_permissions():
            user_id = session["user_id"]
            sql_data = get_cursor()
            msg = ""
            if request.method == 'POST':
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                birth_date = request.form.get('birth_date')
                title = int(request.form.get('title'))
                email = request.form.get('email')
                phone_number = request.form.get('phone_number')
                city = int(request.form.get('city'))
                region = int(request.form.get('region'))
                street_name = request.form.get('street_name')
                detailed_information = request.form.get('detailed_information')
                health_information = request.form.get('health_information')
                user_id = request.form.get('user_id')
                sql = """UPDATE `member` SET first_name=%s,last_name=%s,birth_date=%s,title_id=%s,phone_number=%s,city_id=%s,region_id=%s,street_name=%s,
                            detailed_information=%s, health_information=%s 
                            WHERE user_id=%s;"""
                sql_value = (first_name, last_name, birth_date, title, phone_number, city, region, street_name, detailed_information, health_information,
                             user_id,)
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
                previous_url = str(request.referrer)
                urlList = [x for x in previous_url.split('/') if x != '']
                if urlList[-1] == 'user_list':
                    return redirect(url_for('user_list'))
            sql = """SELECT m.user_id,m.title_id,m.first_name,m.last_name,m.phone_number,m.detailed_information,m.city_id,
                        m.region_id,m.street_name,m.birth_date,m.health_information,u.email FROM `member` AS m
                        LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                        WHERE m.user_id=%s;"""
            sql_value = (user_id,)
            sql_data.execute(sql, sql_value)
            member_detail = sql_data.fetchall()[0]
            sql_data.close()
            return render_template('member/member_change_information.html', member_detail=member_detail, msg=msg, title_list=title_list,
                                   city_list=city_list, region_list=region_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/display_class/<class_id>')
def display_class(class_id):
    sample_value = class_id
    sql_data = get_cursor()
    sql = """SELECT class_id, class_name, class_date, start_time, end_time, class_list.detailed_information, first_name, last_name, pool.pool_name 
                FROM swimming_pool.class_list 
                INNER JOIN instructor ON class_list.instructor_id=instructor.instructor_id 
                INNER JOIN pool ON class_list.pool_id=pool.pool_id 
                WHERE class_id=%s;"""
    sql_value = (sample_value,)
    sql_data.execute(sql, sql_value)
    detail_list = sql_data.fetchone()
    sql_data.close()
    return render_template('member/display_class.html', detail_list=detail_list, permissions=check_permissions())


@app.route('/view_class', methods=['GET', 'POST'])
def view_class():
    if 'loggedIn' in session:
        if check_permissions():
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
                        WHERE (c.class_date BETWEEN %s AND %s) AND (i.state=1)
                        ORDER BY c.start_time"""
            sql_value = (week_list[1][0], week_list[-1][0])
            sql_data.execute(sql, sql_value)
            all_details_sql = sql_data.fetchall()
            sql_data.execute("""SELECT * FROM pool;""")
            pool_list = sql_data.fetchall()
            sql_data.execute("""SELECT * FROM instructor AS i LEFT JOIN title AS t ON i.title_id=t.title_id WHERE i.state=1;""")
            instructor_list = sql_data.fetchall()
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
            return render_template('instructor/instructor_timetable.html', week_list=week_list, all_details=all_details, today=today, pool_list=pool_list,
                                   instructor_list=instructor_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
