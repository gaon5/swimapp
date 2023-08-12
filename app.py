from flask import Flask, url_for, request, redirect, render_template, session
from datetime import date, datetime, timedelta
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

@app.route('/')
def home():
    return redirect('sample')

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

# Function to display aqua aerobics class timetable
@app.route('/view_class')
def view_class():
    # Generate a list of dates for the week
    start_date = date(2023,8,7)
    end_date = date(2023,8,13)
    delta = timedelta(days=1)
    sql_data = get_cursor()
    # Select data of every aqua aerobic class within a week
    sql = """SELECT class_id, class_name, class_date, start_time FROM class_list WHERE (is_individual=0) AND (class_date BETWEEN %s AND %s);"""
    sql_value = (start_date,end_date)
    sql_data.execute(sql,sql_value)
    sql_list = sql_data.fetchall()
    date_list = []
    while start_date <= end_date:
        date_list.append(start_date.isoformat()[5:])
        start_date += delta
    class_list = []
    # Check the weekday number of each date and append them.
    for item in sql_list:
        temp_list = list(item) # Convert tuple into list
        weekday_number = item[2].weekday() + 1
        time = str(item[3]) # Convert time into string
        temp_list[3] = time[:-3] # Remove seconds from the time and replace timedelta with string
        temp_list.append(weekday_number)
        class_list.append(temp_list)
    # Create time_list and row_list to display time and slots for the timetables
    time_list = ['6:00','7:00','8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00']
    row_list = []
    for time in time_list:
        temp_list = []
        temp_list.append(time)
        for i in range(7):
            temp_list.append('')
        row_list.append(temp_list)
    # Compare class_list with time_list. Change the empty value to a dictionary of class_id (key) and class_name (value) if there is a class at that time
    for item in class_list:
        for row in row_list:
            if item[3] == row[0]:
                row[item[-1]] = {item[0]:item[1]}
    sql_data.close()
    return render_template('view_class.html', class_list=class_list, date_list=date_list, row_list=row_list)

# Function to display details of a class
@app.route('/display_class/<class_id>')
def displayclass(class_id):
    sample_value = class_id
    sql_data = get_cursor()
    sql = """SELECT class_id, class_name, class_date, start_time, end_time, class_list.detailed_information, book_number, first_name, last_name, pool.pool_name  FROM swimming_pool.class_list INNER JOIN instructor ON class_list.instructor_id=instructor.instructor_id INNER JOIN pool ON class_list.pool_id=pool.pool_id WHERE class_id=%s;"""
    sql_value = (sample_value,)
    sql_data.execute(sql, sql_value)
    detail_list = sql_data.fetchone()
    sql_data.close()
    return render_template('display_class.html', detail_list=detail_list)

if __name__ == '__main__':
    app.run(debug=True)
