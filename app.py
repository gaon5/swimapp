from flask import Flask, url_for, request, redirect, render_template, session
from datetime import datetime
import mysql.connector
import config
import math
import bcrypt



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


@app.route('/member_change_information', methods=['GET', 'POST'])
def member_change_information():
    def check_change(old, new):
        for i in range(len(new)):
            if old[i + 1] != new[i]:
                return True
        return False

    # if 'loggedIn' in session:
    if 1:
        # user_id = session["user_id"]
        user_id = 2
        sql_data = get_cursor()
        msg = ""
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            birth_date = request.form.get('birth_date')
            title = int(request.form.get('title'))
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            city = request.form.get('city')
            region = request.form.get('region')
            street_name = request.form.get('street_name')
            detailed_information = request.form.get('detailed_information')
            health_information = request.form.get('health_information')
            user_id = request.form.get('user_id')
            sql = """SELECT m.user_id,m.first_name,m.last_name,m.birth_date,m.title_id,u.email,m.phone_number,m.city_id,m.region_id,m.street_name 
                        FROM `member` AS m
                        LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                        WHERE m.user_id=%s;"""
            sql_value = (user_id,)
            sql_data.execute(sql, sql_value)
            member_list = sql_data.fetchall()[0]
            new_data = (first_name, last_name, birth_date, title, email, phone_number, city, region, street_name)
            if check_change(member_list, new_data):
                sql = """UPDATE `member` SET first_name=%s,last_name=%s,birth_date=%s,title_id=%s,phone_number=%s,city_id=%s,region_id=%s,street_name=%s,
                            detailed_information=%s, health_information=%s 
                            WHERE user_id=%s;"""
                sql_value = (first_name, last_name, birth_date, title, phone_number, city, region, street_name, detailed_information,
                             health_information, user_id,)
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
        sql = """SELECT m.user_id,m.title_id,m.first_name,m.last_name,m.phone_number,m.detailed_information,m.city_id,
                    m.region_id,m.street_name,m.birth_date,m.health_information,u.email FROM `member` AS m
                    LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                    WHERE m.user_id=%s;"""
        sql_value = (user_id,)
        sql_data.execute(sql, sql_value)
        member_detail = sql_data.fetchall()[0]
        sql_data.close()
        return render_template('member_change_information.html', member_detail=member_detail, msg=msg)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
