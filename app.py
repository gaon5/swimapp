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


@app.route('/', methods=['GET'])
def home():
    return render_template("base.html")



@app.route('/profile', methods=['GET'])
def profiles():
    if "loggedin" in session:

        sql_data = get_cursor()
        user_id = session['id']
        get_role_sql = """SELECT * from user_account WHERE user_id = %s;"""
        sql_data.execute(get_role_sql,user_id)
        result = sql_data.fetchone()
        if result[4]:
            role = "member"
        elif result[5]:
            role = "instructor"
        elif result[6]:
            role = "admin"
        elif result[7]:
            role = "root"
    
        if role =="member":
            profile_detail_sql = """SELECT * from member WHERE user_id = %s;"""
        elif role == "instructor":
            profile_detail_sql = """SELECT * from instructor WHERE user_id = %s;"""
        elif role == "admin":
            profile_detail_sql = """SELECT * from admin WHERE user_id = %s;"""
    
        sql_data.execute(profile_detail_sql,user_id)
        profile_details = sql_data.fetchone()

        if role =="member":
            member_id = profile_details[0]
            title_id = profile_details[2]
            first_name = profile_details[3]
            last_name = profile_details[4]
            phone_number = profile_details[5]
        elif role == "instructor":
            instructor_id = profile_details[0]
            title_id = profile_details[2]
            first_name = profile_details[3]
            last_name = profile_details[4]
            phone_number = profile_details[5]
            detailed_information  = profile_details[6]
        elif role == "admin":
            admin_id = profile_details[0]
            title_id = profile_details[2]
            first_name = profile_details[3]
            last_name = profile_details[4]
            phone_number = profile_details[5]

        title_sql = """SELECT * from title WHERE title_id = %s;"""
        sql_data.execute(title_sql,title_id)
        title = sql_data.fetchone()[0]


        return render_template("profile.html", 
                               member_id = member_id, title = title, first_name = first_name, last_name = last_name,
                               phone_number = phone_number,instructor_id = instructor_id, detailed_information = detailed_information, 
                               admin_id = admin_id,role = role)

    else:
        return "Please Log In"

@app.route('/member_list', methods=['GET'])
def member_list():
    sql_data = get_cursor()
    user_id = session['id']
    get_role_sql = """SELECT * from user_account WHERE user_id = %s;"""
    sql_data.execute(get_role_sql,user_id)
    result = sql_data.fetchone()
    if result[4]:
        role = "member"
    elif result[5]:
        role = "instructor"
    elif result[6]:
        role = "admin"
    elif result[7]:
        role = "root"

    member_list_sql = """SELECT * from member ;"""
    sql_data.execute(member_list_sql,)
    member_list_result = sql_data.fetchall()

    title_sql = """SELECT * from title WHERE title_id = %s;"""
    sql_data.execute(title_sql,member_list_result['title_id'])
    title = sql_data.fetchone()[0]

    if role == "admin":
        return render_template("member_list.html",role = role,member_list_result = member_list_result,title = title)
    else:
        return "You could not read this page"

@app.route('/member_details', methods=['GET'])
def member_details():
    UserID = request.args.get('UserID')
    sql_data = get_cursor()
    user_id = session['id']
    get_role_sql = """SELECT * from user_account WHERE user_id = %s;"""
    sql_data.execute(get_role_sql,user_id)
    result = sql_data.fetchone()
    if result[4]:
        role = "member"
    elif result[5]:
        role = "instructor"
    elif result[6]:
        role = "admin"
    elif result[7]:
        role = "root"

    if role == "admin":
        profile_detail_sql = """SELECT * from member WHERE user_id = %s;"""
        sql_data.execute(profile_detail_sql,UserID)
        profile_details = sql_data.fetchone()
        member_id = profile_details[0]
        title_id = profile_details[2]
        first_name = profile_details[3]
        last_name = profile_details[4]
        phone_number = profile_details[5]
        title_sql = """SELECT * from title WHERE title_id = %s;"""
        sql_data.execute(title_sql,title_id)
        title = sql_data.fetchone()[0]

        return render_template("profile.html", 
                               member_id = member_id, title = title, first_name = first_name, last_name = last_name,
                               phone_number = phone_number, role = "member")



if __name__ == '__main__':
    app.run(debug=True)
