# COMP639_group_6_project1

### Title and description - Begin with a clear and concise title for your project. Provide a brief description or overview of the project's purpose and goals.

### Usage - describe how to use your project. Provide examples, code snippets, or screenshots to illustrate its functionality.

**In the guest.py all users can use these functions:**

@app.route('/') 
Template: index.html' 

This route renders the welcome page to all users, and this is where the user can login. This page shows pictures, the news feed, information about Waikirikiri Swim Centre, and the pricing for lessons and membership. There is also a footer with the contact information and the opening hours. 

@app.route('/login/', methods=['GET', 'POST']) 
Template: ‘login.html' 

This route lets the user type in their username and password to login or they can register an account here too.  

@app.route('/dashboard') 
Template: ‘dashboard.html' or URL: ‘instructor_timetable’ or URL: ‘index’ 

This route will render different templates depending on the type of user that has logged into the system. If the user is an instructor, it will redirect to the ‘instructor_timetable’ URL, ‘index’ URL for member or render the ‘dashboard.html’ template for admin. 

@app.route('/jump', methods=['GET', 'POST']) 
Template: ‘jump.html' 

This route will take the user to their logged in homepage by going through the URL for ‘dashboard.’ If the log in was unsuccessful then it will jump back to the log in page. 

@app.route('/logout') 
URL: 'index' 

After the user has logged out it will take them back to the welcome page. 

@app.route('/register', methods=['GET', 'POST']) 
Template: ‘register.html’ and ‘jump.html’ 

This route is where the user can fill out the registration form by creating a log in account and fill in their personal details. If the registration form has no errors, then it will redirect back to the welcome page (URL called ‘/’) where they can log in using their newly created account. 

@app.route('/change_password', methods=['GET', 'POST']) 
Template: ‘change_password.html’ 

This route renders the page to type in a new password and if the new password meets the requirements, then it will flash a message saying the password has been changed. 

**In member.py the user needs to log in as a member to access these functions:** 

@app.route('/member_change_information', methods=['GET', 'POST']) 
Template: ‘change_information.html' 

This route renders the page to allow members to change their personal details and update the database using a SQL query. 

@app.route('/view_class', methods=['GET', 'POST']) 
Template: ‘timetable.html’ 

This route renders the timetable page for the member to filter through the classes using the pool or instructor filter. The member can navigate the weeks by clicking on the arrow to go to next week or the previous week. The member can see more details or book the class by clicking on a class name. They can also check if the class is fully booked by looking at the number of spaces available under the class name. To book an individual lesson they click on an empty slot in the timetable. 

@app.route('/member_book_lesson', methods=['POST']) 
Template: ‘book_lesson.html’ 

This route renders the booking details for individual lessons after they have clicked on ‘Book individual lesson’ from the timetable. After they have filled out the form they can click on ‘Go to pay’ to be directed to the payment page.  

@app.route('/individual_payment', methods=['POST']) 
Template: ‘individual_payment.html' 

This route renders the booking confirmation page to show their selections from the previous page to allow them to double check the booking information entered. The member will click on their payment method and then they can click on ‘Confirm’ to complete their booking. 

@app.route('/pay_successful', methods=['POST']) 
Template: ‘jump.html’  

This route renders the jump page which tells the member that their payment was successful and redirects the member to a different URL page called ‘member_class_detail' to see their list of bookings. 

@app.route('/member_class_detail', methods=['GET']) 
Template: ‘class_detail.html’ 

This shows all the information about their booking, and they have the option to cancel the booking if they change their mind. 

@app.route('/delete_book_class', methods=['POST']) 
Template: ‘jump.html’ 

This route renders the jump page with the ‘Cancel Successfully’ message to let the member know the deletion of their class booking is complete before redirecting back to the list of bookings page (URL called '/member_class_detail').  

@app.route('/delete_book_lesson', methods=['POST']) 
Template: ‘jump.html’ 

This route renders the jump page with the ‘Cancel Successfully’ message to let the member know the deletion of their individual lesson booking is complete before redirecting back to the list of bookings page (URL called (URL called '/member_class_detail') 

@app.route('/class_detail', methods=['POST']) 
Template: ‘class_details.html' 

This renders the details for the selected aqua aerobics class from the timetable. It shows information like the instructor’s name, pool name, and times. 

@app.route('/member_book_class', methods=['POST']) 
Template: ‘jump.html' 

This route renders the jump page which tells the member that their booking for the class was successful and redirects the member to a different page to see their list of bookings URL called '/member_class_detail'. However, if the class is already fully booked then it will take the member to view the timetable (URL called '/view_class') so they can book a different class.  

@app.route('/monthly_payment', methods=['GET', 'POST']) 
Template: ‘jump.html' and ‘monthly_payment.html' 

This route renders the page to show the different subscription options (1-12months) with the price and payment method before they can click on ‘Pay Immediately.’ If the member chooses to pay then it will redirect them back to the home page (URL called ‘/’). 

@app.route('/my_membership', methods=['GET']) 
Template: ‘my_membership.html’ 

This route renders the page with the member’s subscription details showing the status, start and end of their membership. 

**In instructors.py the user needs to log in as an instructor to access the functions:**

@app.route('/instructor_change_information', methods=['GET', 'POST']) 
Template: ‘change_information.html' 

This route renders the page that lets the member change their personal details and update the database using a SQL query. 

@app.route('/instructor_timetable', methods=['GET', 'POST']) 
Template: ‘timetable.html' 

This route renders the timetable page for the instructor to filter through the classes using the pool or instructor filter.  The instructor can navigate the weeks by clicking on the arrow to go to next week or the previous week. By clicking on the individual lesson or on one of the aqua aerobics classes from the timetable they can do different functions: view class/lesson details and mark attendance for lessons. If the instructor wants to lock in a time to let the admin know when they can’t teach, it can be done by clicking on an empty slot. 

@app.route('/schedule_time', methods=['GET', 'POST']) 
Template: ‘schedule_time.html' 

This route renders the page for the instructor to choose the date, start and end time to before adding it to the list of unavailable time slots which is seen below. If the instructor wants to delete their unavailable time this can be done by clicking on ‘Delete’ too. 

@app.route('/lock_delete', methods=['POST']) 
URL: 'schedule_time' 

This route redirects the page back to the ‘schedule_time’ page after the instructor has deleted their unavailable time from the ‘My unavailable schedule for individual lessons’ table. 

@app.route('/instructor_class_details', methods=['GET', 'POST']) 
Template: ‘class_details.html' 

This route renders the selected aqua aerobics class from the timetable. It shows the pool name, class name, start and end time, who the instructor is along with their details and the members’ name and information who have booked the class. 

@app.route('/class_attendance', methods=['GET']) 
Template: ‘class_attendance.html' 

This page lets the instructor mark attendance of the members who have booked and showed up to the class. There is a tick box next to the members’ name which by default is coloured in red for not attended and it will change to green once the box has been ticked to show they have attended the class.   

@app.route('/attendance', methods=['POST']) 
URL: 'class_attendance' 

If the instructor did click on the tick box for attendance this route updates the database by removing the members from book_class_list and inserting the member into attendance_log.  If the instructor unclicks the tick box, then member will be removed from the attendance_log table. 

**In the admin.py only the admin can access these functions:**

@app.route('/member_list', methods=['GET', 'POST']) 
Template: ‘member_list.html’ 

This route renders the member list which contains all the users who have signed up as a member. The admin can add members, edit the members’ details or inactivate their accounts. If the admin does add members or edit their details, it will update the database using SQL queries. 

@app.route('/instructor_list', methods=['GET', 'POST']) 
Template: ‘instructor_list.html’ 

This route renders the instructor list which contains all the users who have signed up as an instructor. The admin can add instructors, edit the instructors’ details or inactivate their accounts. If the admin does add instructors or edit their details, it will update the database using SQL queries. 

@app.route('/delete_user', methods=['POST']) 
URL: ‘instructor_list’ 

If the admin clicked on the ‘Inactivate’ button in the member list the member will still have an account, but they can’t book a class or lesson as they need to repurchase a subscription. For instructors, they can no longer use their account. 

@app.route('/admin_change_information', methods=['GET', 'POST']) 
Template: ‘change_information.html’ 

This route renders the page with pre-filled fields of the admin’s current details which they can change and update. This also updates the database using SQL queries. 

@app.route('/admin_timetable', methods=['GET', 'POST']) 
Template: ‘timetable.html’ 

This route renders the page for the admin to see all the aqua aerobics classes and individual lessons in one timetable. The admin can filter by classes or lessons, pool name or instructor name so it is easier to find what they want. By clicking on an individual lesson or aqua aerobics class, a pop-up box with the class details will be shown. However, the aqua aerobics class details box will also have the function to edit or delete the class. If the admin wants to add a class, they can do this by clicking on an empty slot. 

@app.route('/admin_add_class', methods=['POST']) 
Template: ‘add_class.html’ 

This route renders the page for the admin to fill out the class details for the specific date and time so they can add it into the timetable. The admin can still choose a different date or time on this page. If the instructor has set a certain time where they aren’t available, it won’t show their name in the list of instructors to choose from. 

@app.route('/admin_edit_class', methods=['GET', 'POST']) 
Template: ' add_class.html’ and URL: ‘admin_timetable’ 

This route renders the same page for adding a class, but it will have the pre-filled with the current details for the class. Once the change has been made the admin will be redirected back to the timetable. 

@app.route('/admin_delete_class', methods=['POST']) 
URL: ‘admin_timetable’ 

This route will delete the selected class from the timetable and update the database using the SQL query. 

@app.route('/view_payments', methods=['GET']) 
Template: view_payments.html' 

This route renders a template that displays a table of payments made by members, including the date of payment, the amount, payment type (membership or lesson), payment method, and the members' usernames. 

@app.route('/subscriptions_due_date') 
Template: ‘subscriptions_due.html’ 

This route generates a template that provides an overview of the subscription status for all system members. Administrators can use it to identify users with no active subscription, those with expired subscriptions, individuals whose subscriptions are set to expire within 7 days, and those with currently active subscriptions. 

@app.route('/add_news', methods=['POST']) 
URL: ‘dashboard’ 

This lets the admin type news or updates and add it into the news feed which will be shown in the homepage for all users and welcome page for guests. It also shows the time and date of when the news/update was posted. Once the news has been posted into the news feed it will redirect back to the dashboard of the admin.   

@app.route('/delete_news', methods=['POST']) 
URL: ‘dashboard’ 

This route will delete the selected news post and redirect back to the admin’s dashboard. The post will be deleted from all the news feeds, so all users can't see it anymore. 

@app.route('/attendance_report', methods=['GET','POST']) 
Template: ‘attendance_report.html’ 

This route generates the report page, displaying a pie chart representing attendance statistics for aqua aerobics classes, individual lessons, and general pool usage. Additionally, it includes a table presenting details such as date, time, class name, the count of booked participants, attendees, and a corresponding attendance percentage. 

@app.route('/admin_financial_report', methods=['GET','POST']) 
Template: ‘financial_report.html’ 

This route generates a template that displays two revenue tables: one for Membership Subscriptions and another for individual lessons. These tables include member IDs, payment dates, amounts, and payment methods, providing insights into income sources from both memberships and lessons. Additionally, two pie charts are presented—one illustrating income distribution between memberships and lessons, and the other revealing payment method preferences for a more comprehensive financial overview. 

@app.route('/admin_popularity_report') 
Template: ‘popularity_report.html’ 

This route generates a template that presents a pie chart showcasing all aqua aerobics classes within the system, categorized by the quantity of bookings made by members for each class. Additionally, there's another pie chart depicting attendance for these aqua aerobics classes. This page provides a comprehensive report for all aqua aerobics classes. 

@app.route('/edit_pool', methods=['GET', 'POST']) 
Template: ‘edit_pool.html’ 

This route allows the admin to add a pool name into the system. The database will add the new pool name using the SQL query. 

@app.route('/edit_classes', methods=['GET', 'POST']) 
Template: ‘edit_class.html’ 

This route allows the admin to add an aqua aerobics class name into the system. The database will add the new aqua aerobics class name using the SQL query. 

### Login details - Put every user's username and password below

    root
    root/adminpassword
    
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
    ...
    member40/memberpassword

### Testing - Exaplin how to run tests (if applicable). Provide informatio on test coverage and test data

### Credit - acknowledge and give credit to individuals or organizations that have contributed to the project.

Leo played a major role in making sure the project codes functioned correctly. He is a team player who willingly assists other team members with their user stories and provides solutions on how to approach them. He has successfully completed all the user stories assigned to him in every sprint.

Nicholas has demonstrated exceptional leadership skills by ensuring that everyone stays on task and offering assistance to team members who need help with their code. His work ethic is impressive, and he consistently delivers results. Nicholas has completed all the user stories assigned to him for every sprint.

Silver is always eager to tackle new challenges and take on additional tasks. He recently worked on a PowerPoint presentation and sought feedback on it. Silver has consistently completed all the user stories assigned to him in every sprint.

Summer is enthusiastic about learning how to code new functions and remains focused on tasks. She has completed majority of  the user stories assigned to her in every sprint.

Jamin has been instrumental in ensuring the accuracy of spelling and grammar in the Waikirikiri Swim Centre. She successfully completed the majority of the user stories assigned to her in every sprint.

Everyone has actively participated in all meetings and discussions, maintaining open communication about the progress of the user stories.