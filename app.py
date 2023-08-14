from flask import Flask, url_for, request, redirect, render_template, session
from datetime import datetime
import mysql.connector
import config
import math
import bcrypt

# When you gonna start, pip install -r requirements.txt


app = Flask(__name__)
app.config.from_object(config)

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


# @app.route('/sample', methods=['GET', 'POST'])
# def sample():
#     sample_value = 1
#     sql_data = get_cursor()
#     sql = """SELECT * FROM sample_database WHERE sample_id=%s;"""
#     sql_value = (sample_value,)
#     sql_data.execute(sql, sql_value)
#     sample_list = sql_data.fetchall()
#     sql_data.close()

#     return render_template('sample.html', sample_list=sample_list)


@app.route('/user_list', methods=['GET'])
def user_list():
    # if "loggedin" in session:
    if 1:
        # if session['admin'] == 1 or session['root'] == 1:
        if 1:
            sql_data = get_cursor()
            sql = """SELECT m.user_id,m.first_name,m.last_name,m.phone_number,t.title,u.username,u.email,m.state FROM member AS m
                        LEFT JOIN `user_account` AS u ON m.user_id=u.user_id
                        LEFT JOIN `title` AS t ON t.title_id=m.title_id
                        WHERE m.state = 1;"""
            sql_data.execute(sql)
            member_list = sql_data.fetchall()
            sql = """SELECT i.user_id,i.first_name,i.last_name,i.phone_number,t.title,u.username,u.email,i.state FROM instructor AS i
                        LEFT JOIN `user_account` AS u ON u.user_id=i.user_id
                        LEFT JOIN `title` AS t ON t.title_id=i.title_id
                        WHERE i.state = 1;"""
            sql_data.execute(sql)
            instructor_list = sql_data.fetchall()
            sql_data.close()
            return render_template("user_list.html", member_list=member_list, instructor_list=instructor_list)
        else:
            return url_for("/")
    else:
        return url_for("/login/")


if __name__ == '__main__':
    app.run(debug=True)
