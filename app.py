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
            pass
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
