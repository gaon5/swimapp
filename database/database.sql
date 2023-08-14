-- Create a table to store user account information
CREATE TABLE IF NOT EXISTS user_account (
    user_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each user
    username VARCHAR(100) NOT NULL UNIQUE, -- User's username, must be unique
    email VARCHAR(100) NOT NULL UNIQUE, -- User's email address, must be unique
    password VARCHAR(255) NOT NULL, -- User's password (hashed), cannot be null
    is_member TINYINT(1) DEFAULT 0, -- Flag indicating if the user is a member
    is_instructor TINYINT(1) DEFAULT 0, -- Flag indicating if the user is an instructor
    is_admin TINYINT(1) DEFAULT 0, -- Flag indicating if the user is an admin
    is_root TINYINT(1) DEFAULT 0, -- Flag indicating if the user is a root user (super admin)
    register_date DATE -- Date when the user registered
);

-- Create a table to store news entries
CREATE TABLE IF NOT EXISTS news (
    news_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each news entry
    news TEXT -- Content of the news entry
);

-- Create a table to store titles (e.g., Mr., Mrs., Dr.)
CREATE TABLE IF NOT EXISTS title (
    title_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each title
    title VARCHAR(255) -- The title's name
);

-- Create a table to store city information
CREATE TABLE IF NOT EXISTS city (
    city_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each city
    city VARCHAR(255) -- Name of the city
);

-- Create a table to store region information within cities
CREATE TABLE IF NOT EXISTS region (
    region_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each region
    city_id INT, -- Foreign key referencing the city this region belongs to
    region VARCHAR(255), -- Name of the region
    FOREIGN KEY (city_id) REFERENCES city(city_id) -- Establishing a foreign key relationship
);

-- Create a table to store admin user details
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each admin
    user_id INT, -- Foreign key referencing the associated user account
    title_id INT, -- Foreign key referencing the admin's title
    first_name VARCHAR(255), -- Admin's first name
    last_name VARCHAR(255), -- Admin's last name
    phone_number VARCHAR(255), -- Admin's phone number
    state TINYINT(1), -- Admin's state/status
    FOREIGN KEY (user_id) REFERENCES user_account(user_id), -- Establishing a foreign key relationship
    FOREIGN KEY (title_id) REFERENCES title(title_id) -- Establishing a foreign key relationship
);

-- Create a table to store instructor details
CREATE TABLE IF NOT EXISTS instructor (
    instructor_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each instructor
    user_id INT, -- Foreign key referencing the associated user account
    title_id INT, -- Foreign key referencing the instructor's title
    first_name VARCHAR(255), -- Instructor's first name
    last_name VARCHAR(255), -- Instructor's last name
    phone_number VARCHAR(255), -- Instructor's phone number
    detailed_information TEXT, -- Additional detailed information about the instructor
    state TINYINT(1), -- Instructor's state/status
    FOREIGN KEY (user_id) REFERENCES user_account(user_id), -- Establishing a foreign key relationship
    FOREIGN KEY (title_id) REFERENCES title(title_id) -- Establishing a foreign key relationship
);

-- Create a table to store member details
CREATE TABLE IF NOT EXISTS member (
    member_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each member
    user_id INT, -- Foreign key referencing the associated user account
    title_id INT, -- Foreign key referencing the member's title
    first_name VARCHAR(255), -- Member's first name
    last_name VARCHAR(255), -- Member's last name
    phone_number VARCHAR(255), -- Member's phone number
    detailed_information TEXT, -- Additional detailed information about the member
    city_id INT, -- Foreign key referencing the member's city
    region_id INT, -- Foreign key referencing the member's region within the city
    street_name VARCHAR(255), -- Member's street name/address
    birth_date DATE, -- Member's birth date
    health_information TEXT, -- Information about member's health
    state TINYINT(1), -- Member's state/status
    FOREIGN KEY (user_id) REFERENCES user_account(user_id), -- Establishing a foreign key relationship
    FOREIGN KEY (title_id) REFERENCES title(title_id), -- Establishing a foreign key relationship
    FOREIGN KEY (city_id) REFERENCES city(city_id), -- Establishing a foreign key relationship
    FOREIGN KEY (region_id) REFERENCES region(region_id) -- Establishing a foreign key relationship
);

-- Create a table to store pool information
CREATE TABLE IF NOT EXISTS pool (
    pool_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each pool
    pool_name VARCHAR(255) -- Name of the pool
);

-- Create a table to store payment information for members
CREATE TABLE IF NOT EXISTS payment_list (
    payment_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each payment
    member_id INT, -- Foreign key referencing the associated member
    price FLOAT, -- Payment amount/price
    payment_date DATE, -- Date of the payment
    FOREIGN KEY (member_id) REFERENCES member(member_id) -- Establishing a foreign key relationship
);

-- Create a table to store class information
CREATE TABLE IF NOT EXISTS class_list (
    class_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each class
    instructor_id INT, -- Foreign key referencing the associated instructor
    pool_id INT, -- Foreign key referencing the associated pool
    class_name VARCHAR(255), -- Name of the class
    class_date DATE, -- Date of the class
    start_time TIME, -- Start time of the class
    end_time TIME, -- End time of the class
    detailed_information TEXT, -- Additional detailed information about the class
    is_individual TINYINT(1), -- Flag indicating if the class is individual
    maximum_number INT, -- Maximum number of people
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id), -- Establishing a foreign key relationship
    FOREIGN KEY (pool_id) REFERENCES pool(pool_id) -- Establishing a foreign key relationship
);

-- Create a table to store attendance logs
CREATE TABLE IF NOT EXISTS attendance_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each attendance log entry
    member_id INT, -- Foreign key referencing the associated member
    class_id INT, -- Foreign key referencing the associated class
    attendance_date DATE, -- Date of the attendance
    FOREIGN KEY (member_id) REFERENCES member(member_id), -- Establishing a foreign key relationship
    FOREIGN KEY (class_id) REFERENCES class_list(class_id) -- Establishing a foreign key relationship
);

-- Create a table to store book information
CREATE TABLE IF NOT EXISTS book_list (
    book_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each booking
    member_id INT, -- Foreign key referencing the associated member
    class_id INT, -- Foreign key referencing the associated class
    instructor_id INT, -- Foreign key referencing the associated instructor
    pool_id INT, -- Foreign key referencing the associated pool
    payment_id INT, -- Foreign key referencing the associated payment
    FOREIGN KEY (member_id) REFERENCES member(member_id), -- Establishing a foreign key relationship
    FOREIGN KEY (class_id) REFERENCES class_list(class_id), -- Establishing a foreign key relationship
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id), -- Establishing a foreign key relationship
    FOREIGN KEY (pool_id) REFERENCES pool(pool_id), -- Establishing a foreign key relationship
    FOREIGN KEY (payment_id) REFERENCES payment_list(payment_id) -- Establishing a foreign key relationship
);

-- Create a table to store payment due dates
CREATE TABLE IF NOT EXISTS payment_due (
    due_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each due date
    payment_id INT, -- Foreign key referencing the associated payment
    start_date DATE, -- Start date of the due period
    end_date DATE, -- End date of the due period
    FOREIGN KEY (payment_id) REFERENCES payment_list(payment_id) -- Establishing a foreign key relationship
);

-- Insert a root user into the user_account table
INSERT INTO user_account (username, email, password, is_root, register_date)
    VALUES('admin', 'admin@admin.com', '$2b$12$rZ/oMfPkT9q16IWgGJ9n6.e5xynS7f9elfPmPiR.TbEBo2yTkc2Dq', 1, "2023-08-08");
-- admin/adminpassword
