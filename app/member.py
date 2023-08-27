from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
import math
import bcrypt
import re
from app import app, check_permissions, get_cursor, title_list, region_list, city_list


@app.route('/member_change_information', methods=['GET', 'POST'])
def member_change_information():
    """
    The webpage used to give the member change his own information
    :return: change_information.html
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
                    if len(sql_data.fetchall()) > 0:
                        msg = "This email already be used."
                    else:
                        sql_data.execute("UPDATE `user_account` SET email=%s WHERE user_id=%s;", (email, user_id,))
                previous_url = str(request.referrer)
                urlList = [x for x in previous_url.split('/') if x != '']
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
                                   region_list=region_list, city_list=city_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


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
            instructor_list = sql_data.fetchall()
            sql = """SELECT class_id, COUNT(member_id) AS member_count
                        FROM book_list
                        GROUP BY class_id;"""
            sql_data.execute(sql)
            member_count = sql_data.fetchall()
            for i in range(len(member_count)):
                member_count[i] = list(member_count[i])
            member_count = {item[0]: item[1] for item in member_count}
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
            return render_template('member/timetable.html', week_list=week_list, all_details=all_details, today=today, pool_list=pool_list,
                                   member_count=member_count, instructor_list=instructor_list, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/member_book_lesson', methods=['POST'])
def member_book_lesson():
    if 'loggedIn' in session:
        if check_permissions():
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
            return render_template('member/book_lesson.html', instructor_list=instructor_list, class_list=class_list, pool_list=pool_list, time=str(start_time), date=complete_date_string, edit=1, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/individual_payment', methods=['POST'])
def individual_payment():
    available_date = request.form.get('available_date')
    start_hour = request.form.get('start_hour')
    start_minute = request.form.get('start_minute')
    hour = request.form.get('hour')
    instructor = int(request.form.get('instructor'))
    pool = int(request.form.get('pool'))
    start_time = str(start_hour) + ":" + str(start_minute)
    parsed_time = datetime.strptime(start_time, '%H:%M').time()
    start_time = parsed_time.replace(second=0).strftime('%H:%M:%S')
    if int(hour) == 1:
        end_time = datetime.combine(datetime.min, parsed_time) + timedelta(minutes=30)
    else:
        end_time = datetime.combine(datetime.min, parsed_time) + timedelta(minutes=60)
    end_time = end_time.replace(second=0).strftime('%H:%M:%S')
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
                LEFT JOIN title AS t ON t.title_id=i.title_id WHERE i.instructor_id = %s"""
    sql_data.execute(sql, (pool,))
    instructor_name = sql_data.fetchall()[0][0]
    return render_template('member/individual_payment.html', pool_name=pool_name, instructor_name=instructor_name, hour=hour, permissions=check_permissions())


@app.route('/pay_successful', methods=['POST'])
def pay_successful():
    available_date = session['available_date']
    start_time = session['start_time']
    end_time = session['end_time']
    instructor = int(session['instructor'])
    pool = int(session['pool'])
    user_id = session['user_id']
    hour = int(session['hour'])
    if hour == 1:
        price = 44
    else:
        price = 80
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
    sql = """INSERT INTO payment_list (member_id, price, payment_date) VALUES (%s,%s,%s);"""
    value = (member_id, price, today)
    sql_data.execute(sql, value)
    sql_data.execute("""SET @payment_id = LAST_INSERT_ID();""")
    sql = """INSERT INTO book_list (member_id, class_id, instructor_id, pool_id, payment_id) VALUES (%s,@book_class_id,%s,%s,@payment_id);"""
    value = (member_id, instructor_id, pool)
    sql_data.execute(sql, value)
    msg = "Pay successful! Jump to my lesson."
    goUrl = '/member_class_detail'
    return render_template('guest/jump.html', msg=msg, goUrl=goUrl, permissions=check_permissions())


@app.route('/member_class_detail', methods=['GET'])
def member_class_detail():
    today = datetime.today().date()
    user_id = int(session['user_id'])
    sql_data = get_cursor()
    sql = """SELECT bc.class_date,bc.start_time,bc.end_time, CONCAT(t.title, ' ', i.first_name, ' ', i.last_name) as instructor_name, i.phone_number, p.pool_name, bc.is_individual 
                FROM book_list AS bl
                LEFT JOIN book_class_list AS bc ON bc.book_class_id=bl.class_id
                LEFT JOIN instructor AS i ON i.instructor_id=bl.instructor_id
                LEFT JOIN title AS t ON t.title_id=i.title_id
                LEFT JOIN pool AS p ON p.pool_id=bl.pool_id
                LEFT JOIN member AS m ON m.member_id=bl.member_id
                WHERE m.user_id=%s AND bc.class_date>%s
                order by bc.class_date;"""
    sql_data.execute(sql, (user_id, today,))
    detail_list = sql_data.fetchall()
    sql_data.close()
    for i in range(len(detail_list)):
        detail_list[i] = list(detail_list[i])
        detail_list[i][0] = str(detail_list[i][0])
        detail_list[i][1] = str(detail_list[i][1])
        detail_list[i][2] = str(detail_list[i][2])
    return render_template('member/class_detail.html', detail_list=detail_list, permissions=check_permissions())


@app.route('/class_detail', methods=['POST'])
def class_detail():
    if 'loggedIn' in session:
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
            sql = """SELECT book_id From book_list WHERE class_id=%s AND member_id=%s;"""
            sql_data.execute(sql, (class_id, member_id,))
            if not sql_data.fetchall():
                sql = """INSERT INTO book_list (member_id, class_id, instructor_id, pool_id) VALUES (%s,%s,%s,%s)"""
                value = (member_id, class_id, book_class_id[1], book_class_id[0],)
                sql_data.execute(sql, value)
                msg = "Book successful! Jump to my class."
                goUrl = '/member_class_detail'
            else:
                msg = "You cannot book the same class twice! Jump to timetable."
                goUrl = '/view_class'
            return render_template('guest/jump.html', msg=msg, goUrl=goUrl, permissions=check_permissions())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
