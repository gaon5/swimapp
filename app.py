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

    # if "loggedin" in session:
    if 1:
        # user_id = session['id']
        user_id = 4

        sql_data = get_cursor()
        get_role_sql = """SELECT * from user_account WHERE user_id = %s;"""
        sql_data.execute(get_role_sql,(user_id,))
        result = sql_data.fetchone()

        if result[4]:
            role = "member"
<<<<<<< Updated upstream
            profile_detail_sql = """SELECT member.member_id,member.user_id,member.first_name,member.last_name,member.phone_number,
                                    member.detailed_information,member.street_name,member.birth_date,member.health_information,
                                    title.title,city.city,region.region 
                                    FROM member 
                                    LEFT JOIN title ON member.title_id = title.title_id
                                    LEFT JOIN city ON member.city_id = city.city_id
                                    LEFT JOIN region ON member.region_id = region.region_id
                                    WHERE user_id = %s;"""
            sql_data.execute(profile_detail_sql,(user_id,))
            profile_details = sql_data.fetchone()
            title = profile_details[9]


        elif result[5]:
            role = "instructor"
            profile_detail_sql = """SELECT instructor.instructor_id,instructor.user_id,instructor.first_name,instructor.last_name,
                                    instructor.phone_number, instructor.detailed_information,
                                    title.title
                                    FROM instructor 
                                    LEFT JOIN title ON instructor.title_id = title.title_id 
                                    WHERE user_id = %s;"""
            sql_data.execute(profile_detail_sql,(user_id,))
            profile_details = sql_data.fetchone()
            title = profile_details[-1]

        elif result[6]:
            role = "admin"
            profile_detail_sql = """SELECT admin.admin_id,admin.user_id,admin.first_name,admin.last_name,
                                    admin.phone_number, title.title
                                    FROM admin
                                    LEFT JOIN title ON admin.title_id = title.title_id 
                                    WHERE user_id = %s;"""
            sql_data.execute(profile_detail_sql,(user_id,))
            profile_details = sql_data.fetchone()
            title = profile_details[-1]
        elif result[7]:
            role = "root"
    
        return render_template("profile.html", role = role, profile_details = profile_details,title = title,)

=======
            profile_detail_sql = """SELECT m.member_id,m.user_id,m.first_name,m.last_name,m.phone_number,
                                    m.detailed_information,m.street_name,m.birth_date,m.health_information,t.title,c.city,r.region
                                    from member
                                    inner join title on member.title_id = title.title_id
                                    inner join city on member.city_id = city.city_id
                                    inner join region on member.region_id = region.region_id
                                    WHERE user_id = %s;"""
            sql_data.execute(profile_detail_sql,user_id)
            profile_details = sql_data.fetchone()
        
        elif result[5]:
            role = "instructor"
            profile_detail_sql = """SELECT i.instructor_id,i.user_id,i.first_name,i.last_name,i.phone_number, 
                                    i.detailed_information, t.title
                                    from instructor
                                    inner join title on instructor.title_id = title.title_id 
                                    WHERE user_id = %s;"""
            sql_data.execute(profile_detail_sql,user_id)
            profile_details = sql_data.fetchone()
            
        elif result[6]:
            role = "admin"
            profile_detail_sql = """SELECT a.admin_id,a.user_id,a.first_name,a.last_name,a.phone_number,t.title 
                                     from admin 
                                     inner join title on instructor.title_id = title.title_id 
                                     WHERE user_id = %s;"""
            sql_data.execute(profile_detail_sql,user_id)
            profile_details = sql_data.fetchone()
            
        elif result[7]:
            role = "root"
    
        return render_template("profile.html", 
                               role = role, profile_details = profile_details)
>>>>>>> Stashed changes
    else:
        return "Please Log In"

@app.route('/member_list', methods=['GET'])
def member_list():
    sql_data = get_cursor()

    # user_id = session['id']
    user_id = 4

    get_role_sql = """SELECT * FROM user_account WHERE user_id = %s;"""
    sql_data.execute(get_role_sql,(user_id,))
    result = sql_data.fetchone()
    if result[6]:
        role = "admin"
        member_list_sql = """SELECT member.member_id,member.user_id,member.first_name,member.last_name,member.phone_number,
                            member.detailed_information,member.street_name,member.birth_date,member.health_information,
                            title.title,city.city,region.region 
                            FROM member 
                            LEFT JOIN title ON member.title_id = title.title_id
                            LEFT JOIN city ON member.city_id = city.city_id
                            LEFT JOIN region ON member.region_id = region.region_id
                            ORDER BY member_id;"""
        sql_data.execute(member_list_sql,)
        member_list_result = sql_data.fetchall()
        print(member_list_result)
        return render_template("member_list.html",role = role,member_list_result = member_list_result,)

    else:
        return "You could not approach member list"



if __name__ == '__main__':
    app.run(debug=True)
