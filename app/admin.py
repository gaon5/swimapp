from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, get_cursor, title_list, region_list, city_list


@app.route('/user_list', methods=['GET'])
def user_list():
    if 'loggedIn' in session:
        if check_permissions() > 2:
            sql_data = get_cursor()
            sql = """SELECT m.user_id,m.first_name,m.last_name,m.phone_number,t.title,u.username,u.email,m.title_id,
                        m.detailed_information,m.region_id,m.city_id,m.street_name,m.birth_date,m.health_information,m.state FROM member AS m
                        LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                        LEFT JOIN `title` AS t ON t.title_id=m.title_id
                        WHERE m.state = 1;"""
            sql_data.execute(sql)
            member_list = sql_data.fetchall()
            sql = """SELECT i.user_id,i.first_name,i.last_name,i.phone_number,t.title,u.username,u.email,i.title_id,i.detailed_information,i.state FROM instructor AS i
                        LEFT JOIN `user_account` AS u ON u.user_id=i.user_id
                        LEFT JOIN `title` AS t ON t.title_id=i.title_id
                        WHERE i.state = 1;"""
            sql_data.execute(sql)
            instructor_list = sql_data.fetchall()
            sql_data.close()
            for i in range(len(member_list)):
                member_list[i] = list(member_list[i])
                member_list[i][12] = str(member_list[i][12])
            today = datetime.today().date()
            return render_template("admin/user_list.html", member_list=member_list, instructor_list=instructor_list, title_list=title_list,
                                   region_list=region_list, city_list=city_list, today=today, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_change_information', methods=['GET', 'POST'])
def admin_change_information():
    """
    The webpage used to give the admin change his own information
    :return: change_information.html
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
                            msg = "This email already be used."
                        else:
                            sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
                else:
                    msg = "No modification"
            sql = """SELECT a.user_id,a.title_id,a.first_name,a.last_name,a.phone_number,u.email FROM `admin` AS a
                        LEFT JOIN `user_account` AS u ON a.user_id=u.user_id
                        WHERE a.user_id=%s;"""
            sql_value = (user_id,)
            sql_data.execute(sql, sql_value)
            admin_list = sql_data.fetchall()[0]
            sql_data.close()
            return render_template('admin/change_information.html', admin_list=admin_list, msg=msg, title_list=title_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/delete_user')
def delete_user():
    if 'loggedIn' in session:
        if check_permissions() > 2:
            is_member = request.args.get('is_member')
            user_id = request.args.get('user_id')
            sql_data = get_cursor()
            if is_member == '1':
                sql = """UPDATE member SET state=0 Where user_id=%s"""
                sql_data.execute(sql, (user_id,))
            else:
                sql = """UPDATE instructor SET state=0 Where user_id=%s"""
                sql_data.execute(sql, (user_id,))
            sql_data.close()
            return redirect(url_for('user_list'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_timetable', methods=['GET', 'POST'])
def admin_timetable():
    if 'loggedIn' in session:
        if check_permissions() > 2:
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
            instructor_list = sql_data.fetchall()
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
            return render_template('admin/timetable.html', week_list=week_list, pool_list=pool_list, today=today, instructor_list=instructor_list,
                                   all_details=all_details, member_count=member_count, link=url_for('admin_timetable'), permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_add_class', methods=['POST'])
def admin_add_class():
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
            instructor_list = sql_data.fetchall()
            sql_data.execute("SELECT * FROM class_list;")
            class_list = sql_data.fetchall()
            sql_data.execute("""SELECT * FROM pool;""")
            pool_list = sql_data.fetchall()
            return render_template('admin/add_class.html', instructor_list=instructor_list, class_list=class_list, pool_list=pool_list,
                                   time=str(start_time), date=complete_date_string, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_edit_class', methods=['GET', 'POST'])
def admin_edit_class():
    if 'loggedIn' in session:
        if check_permissions() > 2:
            if request.method == 'GET':
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
                                        LEFT JOIN title AS t ON t.title_id=i.title_id;""")
                instructor_list = sql_data.fetchall()
                sql_data.close()
                return render_template('admin/add_class.html', instructor_list=instructor_list, class_list=class_list, pool_list=pool_list,
                                       class_detail=class_detail, permissions=check_permissions(), edit=1)
            else:
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
                    instructor_list = sql_data.fetchall()
                    sql_data.execute("SELECT * FROM class_list;")
                    class_list = sql_data.fetchall()
                    sql_data.execute("""SELECT * FROM pool;""")
                    pool_list = sql_data.fetchall()
                    sql_data.close()
                    return render_template('admin/add_class.html', instructor_list=instructor_list, class_list=class_list, pool_list=pool_list,
                                           time=str(start_time), date=complete_date_string, permissions=check_permissions(), edit=1, class_id=class_id)
                else:
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
    if 'loggedIn' in session:
        if check_permissions() > 2:
            class_id = request.form.get('class_id')
            sql_data = get_cursor()
            sql_data.execute("""DELETE FROM `book_class_list` WHERE book_class_id=%s""", (class_id,))
            sql_data.close()
            return redirect(url_for('admin_timetable'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
