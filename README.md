# COMP639 Group 6 Project1

### Title and description 

The **Waikirikiri Swim Centre Management System** is a comprehensive software solution designed to modernize and streamline the operations of the Waikirikiri Swim Centre. With approximately 1000 members and a team of 10 swim instructors, this system aims to automate and enhance the management of crucial aspects of the swim centre's activities. 

### Project Objectives 

The primary goals of this system are: 

1. **Member Management:** Simplify member registration, enable profile updates, and provide a convenient platform for members to access essential information. Members can easily view their subscription details, booked lessons, and class schedules. 

2. **Payment Tracking:** Empower administrators to efficiently track member payments. The system offers financial reporting capabilities, sends payment reminders, and ensures seamless payment processing. 

3. **Class Scheduling:** Enable members to book aqua aerobics classes while allowing instructors to manage their class schedules effectively. Instructors can also view and update their availability. 
 
4. **Swimming Lessons:** Facilitate the booking of individual swimming lessons by members. Instructors can manage their availability, access swim trainee information, and efficiently deliver specialized swimming instruction. 

5. **Attendance Tracking:** The system records member attendance across various activities, including pool usage, individual lessons, and class participation. This feature enhances operational efficiency and member engagement. 

6. **Pool Management:** The Waikirikiri Swim Centre boasts multiple pools, each with its purpose. Aqua aerobics classes and individual lessons can be scheduled in different pools based on specific requirements, providing flexibility and convenience. 
 
7. **Financial Reports:** Administrators and managers have access to comprehensive financial reports. These reports include revenue breakdowns by subscription fees and lesson charges, helping track overall revenue and financial performance. 

8. **Communication:** Admins and managers can communicate with members through on-screen reminders and updates, ensuring effective and timely information dissemination. 

### User Roles 

The system accommodates three primary user roles: 

1. **Admin/Manager:** This role involves managing member profiles, monitoring payments, generating reports, and updating their own profiles. 

2. **Member:** Members can view and update their profiles, book swimming lessons and classes, manage subscriptions, and make payments, providing a seamless experience.

3. **Instructors:** Instructors can manage their profiles, schedule classes, and access information related to individual lesson bookings. 

### Core Functionality 

The system's core functionality revolves around the efficient tracking of member attendance. When members arrive at the Swim Centre and scan their membership cards, the system intelligently categorizes their activities (pool usage, individual lessons, or class attendance). 

The Waikirikiri Swim Centre Management System aims to simplify the registration process, offer a user-friendly experience for members, and provide comprehensive tools for administrators and instructors to enhance operational efficiency. 

### Usage

**In the guest.py all users can use these functions:**

| Route                            | Method    | Template or URL            | Description                                                                                                                      |
|----------------------------------|-----------|----------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| `@app.route('/')`                | -         | `index.html`               | This route renders the welcome page to all users. Displays pictures, news feed, etc. Footer with contact info and opening hours. |
| `@app.route('/login/')`          | GET, POST | `login.html`               | User can type in their username and password to login or register an account.                                                    |
| `@app.route('/dashboard')`       | -         | Varies                     | Renders different templates based on user type: `dashboard.html` for admin, URLs for member and instructor.                      |
| `@app.route('/jump')`            | GET, POST | `jump.html`                | Takes user to logged-in homepage via `dashboard` URL. Redirects to login page if login was unsuccessful.                         |
| `@app.route('/logout')`          | -         | index                      | After logout, redirects to welcome page.                                                                                         |
| `@app.route('/register')`        | GET, POST | `register.html, jump.html` | User can fill out registration form. If successful, redirects to welcome page for login.                                         |
| `@app.route('/change_password')` | GET, POST | `change_password.html`     | Page to type in new password. If successful, flashes message that password has been changed.                                     |

**In member.py the user needs to log in as a member to access these functions:**

| Route                                      | Method    | Template or URL                     | Description                                                                                                                                                                                                                              |
|--------------------------------------------|-----------|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `@app.route('/member_change_information')` | GET, POST | `change_information.html`           | This route renders the page to allow members to change their personal details and update the database using a SQL query.                                                                                                                 |
| `@app.route('/view_class')`                | GET, POST | `timetable.html`                    | This route renders the timetable page for the member to filter through the classes using the pool or instructor filter. The member can navigate the weeks by clicking on the arrow to go to next week or the previous week...            |
| `@app.route('/member_book_lesson')`        | POST      | `book_lesson.html`                  | This route renders the booking details for individual lessons after they have clicked on ‘Book individual lesson’ from the timetable. After they have filled out the form they can click on ‘Go to pay’ to be directed to...             |
| `@app.route('/individual_payment')`        | POST      | `individual_payment.html`           | This route renders the booking confirmation page to show their selections from the previous page to allow them to double check the booking information entered. The member will click on their payment method and then...                |
| `@app.route('/pay_successful')`            | POST      | `jump.html`                         | This route renders the jump page which tells the member that their payment was successful and redirects the member to a different URL page called ‘member_class_detail' to see their list of bookings.                                   |
| `@app.route('/member_class_detail')`       | GET       | `class_detail.html`                 | This shows all the information about their booking, and they have the option to cancel the booking if they change their mind.                                                                                                            |
| `@app.route('/delete_book_class')`         | POST      | `jump.html`                         | This route renders the jump page with the ‘Cancel Successfully’ message to let the member know the deletion of their class booking is complete before redirecting back to the list of bookings page (URL called '/member_class_detail'). |
| `@app.route('/delete_book_lesson')`        | POST      | `jump.html`                         | This route renders the jump page with the ‘Cancel Successfully’ message to let the member know the deletion of their individual lesson booking is complete before redirecting back to the list of bookings page...                       |
| `@app.route('/class_detail')`              | POST      | `class_details.html`                | This renders the details for the selected aqua aerobics class from the timetable. It shows information like the instructor’s name, pool name, and times.                                                                                 |
| `@app.route('/member_book_class')`         | POST      | `jump.html`                         | This route renders the jump page which tells the member that their booking for the class was successful and redirects the member to a different page to see their list of bookings URL called '/member_class_detail'. However,...        |
| `@app.route('/monthly_payment')`           | GET, POST | `jump.html`, `monthly_payment.html` | This route renders the page to show the different subscription options (1-12months) with the price and payment method before they can click on ‘Pay Immediately.’ If the member chooses to pay then it will redirect them...             |
| `@app.route('/my_membership')`             | GET       | `my_membership.html`                | This route renders the page with the member’s subscription details showing the status, start and end of their membership.                                                                                                                |

**In instructors.py the user needs to log in as an instructor to access the functions:**

| Route                                          | Method    | Template or URL           | Description                                                                                                                                                                                                                                    |
|------------------------------------------------|-----------|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `@app.route('/instructor_change_information')` | GET, POST | `change_information.html` | This route renders the page that lets the member change their personal details and update the database using a SQL query.                                                                                                                      |
| `@app.route('/instructor_timetable')`          | GET, POST | `timetable.html`          | This route renders the timetable page for the instructor to filter through the classes using the pool or instructor filter. The instructor can navigate the weeks, view class/lesson details, mark attendance, and indicate unavailable slots. |
| `@app.route('/schedule_time')`                 | GET, POST | `schedule_time.html`      | This route renders the page for the instructor to choose the date, start and end time for their unavailability. Instructors can also delete their unavailable times.                                                                           |
| `@app.route('/lock_delete')`                   | POST      | schedule_time             | This route redirects the page back to the ‘schedule_time’ page after the instructor has deleted their unavailable time from the list.                                                                                                          |
| `@app.route('/instructor_class_details')`      | GET, POST | `class_details.html`      | This route renders the selected aqua aerobics class from the timetable. It showcases the class details, instructor's info, and member's info who booked the class.                                                                             |
| `@app.route('/class_attendance')`              | GET       | `class_attendance.html`   | This page lets the instructor mark attendance of the members. Attendance is indicated by tick boxes, which by default show as red for not attended and turn green when ticked to indicate attendance.                                          |
| `@app.route('/attendance')`                    | POST      | `class_attendance`        | This route updates the database based on attendance marking. If the instructor ticks the attendance box, the member is moved from the book_class_list to the attendance_log. If unticked, the member is removed from the attendance_log.       |

**In the admin.py only the admin can access these functions:**

| Route                                     | Method    | Template or URL           | Description                                                                                                                                                                                              |
|-------------------------------------------|-----------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `@app.route('/member_list')`              | GET, POST | `member_list.html`        | Admin views and manages member details. They can add, edit, or inactivate member accounts. Changes result in database updates.                                                                           |
| `@app.route('/instructor_list')`          | GET, POST | `instructor_list.html`    | Admin views and manages instructor details. They can add, edit, or inactivate instructor accounts. Changes result in database updates.                                                                   |
| `@app.route('/delete_user')`              | POST      | instructor_list           | Handles the 'Inactivate' button action for members and instructors. Members remain but cannot book; instructors cannot use their account.                                                                |
| `@app.route('/admin_change_information')` | GET, POST | `change_information.html` | Admin can view and modify their own details. The database is updated accordingly.                                                                                                                        |
| `@app.route('/admin_timetable')`          | GET, POST | `timetable.html`          | Admin can view a comprehensive timetable and interact with class details through a pop-up. They can also add or delete classes.                                                                          |
| `@app.route('/admin_add_class')`          | POST      | `add_class.html`          | Admin provides details for a new class. The interface respects instructor availability.                                                                                                                  |
| `@app.route('/admin_edit_class')`         | GET, POST | `add_class.html`          | Admin modifies existing class details, with pre-filled class information. After updates, redirection happens to the timetable.                                                                           |
| `@app.route('/admin_delete_class')`       | POST      | admin_timetable           | Admin can delete a specific class from the timetable. The database reflects this deletion.                                                                                                               |
| `@app.route('/view_payments')`            | GET       | `view_payments.html`      | Admin views a comprehensive list of payments made by members, with details like payment date, amount, type, method, and username.                                                                        |
| `@app.route('/subscriptions_due_date')`   | -         | `subscriptions_due.html`  | Overview of subscription statuses for all members: active, expiring soon, expired, or no subscription.                                                                                                   |
| `@app.route('/add_news')`                 | POST      | dashboard                 | Admin can post news updates, which will be reflected on the homepage for all users and a welcome page for guests. After posting, a redirect to the admin dashboard occurs.                               |
| `@app.route('/delete_news')`              | POST      | dashboard                 | Admin can remove a specific news post. This deletion is reflected across all news feeds for users.                                                                                                       |
| `@app.route('/attendance_report')`        | GET, POST | `attendance_report.html`  | Detailed attendance report: a pie chart for attendance across different activities and a detailed table with date, time, class name, bookings, attendees, and attendance percentage.                     |
| `@app.route('/admin_financial_report')`   | GET, POST | `financial_report.html`   | Revenue reports for memberships and individual lessons. Tables present member IDs, payment dates, amounts, and methods. Pie charts provide an overview of income sources and payment method preferences. |
| `@app.route('/admin_popularity_report')`  | -         | `popularity_report.html`  | Pie charts representing popularity metrics for aqua aerobics classes, both in terms of bookings and actual attendance.                                                                                   |
| `@app.route('/edit_pool')`                | GET, POST | `edit_pool.html`          | Admin can add a new pool name to the system. This addition is reflected in the database.                                                                                                                 |
| `@app.route('/edit_classes')`             | GET, POST | `edit_class.html`         | Admin can add a new aqua aerobics class name to the system. This addition is reflected in the database.                                                                                                  |

### Login details

    admin
    admin1/adminpassword
    
    instructor
    instructor1/instructorpassword
    instructor2/instructorpassword
    ...
    instructor10/instructorpassword
    
    member
    member1/memberpassword
    member2/memberpassword
    member3/memberpassword
    ...
    member40/memberpassword

### Testing

#### Overview 

Testing is a crucial part of ensuring the reliability and functionality of the Waikirikiri Swim Centre Management System. This section provides information on test coverage, and details about the test data used. 

#### Test Coverage 
 
Test coverage measures how much of the codebase is exercised by our tests. It helps identify areas that may need more testing to ensure robustness. The Waikirikiri Swim Centre Management System aims for comprehensive test coverage, targeting critical areas such as: 

- Member registration and profile management 

- Payment processing and subscription tracking 

- Class scheduling and booking 

- Individual swimming lesson management 

- Attendance tracking and pool usage 

- Financial reporting and revenue calculations 

- User roles and permissions 

#### Test Data 

Test data is essential for evaluating system behavior and ensuring that the application handles various scenarios effectively. The testing process involves the use of both real and synthetic data to validate different functionalities.
 
- **Member Registration:** Test data includes sample member profiles with various input values for registration, ensuring that the system processes registrations correctly. 

- **Class Scheduling:** Test data covers class schedules, instructor availability, and member bookings to validate class management features. 

- **Individual Swimming Lessons:** Data for individual lessons includes instructor availability, member bookings, and lesson details to assess lesson booking functionality. 

- **Attendance Tracking:** Test data models member attendance across pool usage, class participation, and individual lessons, ensuring accurate attendance recording. 

- **Financial Reports:** Synthetic financial data helps validate financial reporting features, including revenue calculations and breakdowns. 

The combination of real and synthetic data ensures comprehensive testing of the Waikirikiri Swim Centre Management System, providing confidence in its performance and reliability.

### Credit

Leo played a major role in making sure the project codes functioned correctly. He is a team player who willingly assists other team members with their user stories and provides solutions on how to approach them. He has successfully completed all the user stories assigned to him in every sprint.

Nicholas has demonstrated exceptional leadership skills by ensuring that everyone stays on task and offering assistance to team members who need help with their code. His work ethic is impressive, and he consistently delivers results. Nicholas has completed all the user stories assigned to him for every sprint.

Silver is always eager to tackle new challenges and take on additional tasks. He recently worked on a PowerPoint presentation and sought feedback on it. Silver has consistently completed all the user stories assigned to him in every sprint.

Summer is enthusiastic about learning how to code new functions and remains focused on tasks. She has completed majority of  the user stories assigned to her in every sprint.

Jamin has been instrumental in ensuring the accuracy of spelling and grammar in the Waikirikiri Swim Centre. She successfully completed the majority of the user stories assigned to her in every sprint.

Everyone has actively participated in all meetings and discussions, maintaining open communication about the progress of the user stories.
