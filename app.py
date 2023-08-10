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


@app.route('/selfInformation', methods=['GET', 'POST'])
def self_information():
    # if 'loggedIn' in session:
    if 1:
        # user_id = session["user_id"]
        user_id = 3
        sql_data = get_cursor()
        if request.method == 'GET':
            sql = """SELECT * FROM `admin` AS a
                        LEFT JOIN `user_account` AS u ON a.user_id=u.user_id
                        WHERE a.user_id=%s;"""
            sql_value = (user_id,)
            sql_data.execute(sql, sql_value)
            admin_list = sql_data.fetchall()
            sql_data.close()
            return render_template('adminInformation.html', admin_list=admin_list)
        else:
            title = request.form.get('title')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            user_id = request.form.get('user_id')
            # 检查email

            return redirect(url_for('self_information'))
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True)
