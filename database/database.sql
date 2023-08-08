CREATE TABLE IF NOT EXISTS user_account (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_member TINYINT(1) DEFAULT 0,
    is_instructor TINYINT(1) DEFAULT 0,
    is_admin TINYINT(1) DEFAULT 0,
    is_root TINYINT(1) DEFAULT 0,
    register_date DATE
);

CREATE TABLE IF NOT EXISTS title (
    title_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS city (
    city_id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS region (
    region_id INT PRIMARY KEY AUTO_INCREMENT,
    city_id INT,
    region VARCHAR(255),
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);

CREATE TABLE IF NOT EXISTS admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title_id INT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES user_account(user_id),
    FOREIGN KEY (title_id) REFERENCES title(title_id)
);

CREATE TABLE IF NOT EXISTS instructor (
    instructor_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title_id INT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(255),
    detailed_information TEXT,
    FOREIGN KEY (user_id) REFERENCES user_account(user_id),
    FOREIGN KEY (title_id) REFERENCES title(title_id)
);

CREATE TABLE IF NOT EXISTS member (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title_id INT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(255),
    detailed_information TEXT,
    city_id INT,
    region_id INT,
    street_name VARCHAR(255),
    birth_date DATE,
    health_information TEXT,
    FOREIGN KEY (user_id) REFERENCES user_account(user_id),
    FOREIGN KEY (title_id) REFERENCES title(title_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);

CREATE TABLE IF NOT EXISTS pool (
    pool_id INT PRIMARY KEY AUTO_INCREMENT,
    pool_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS payment_list (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    price FLOAT,
    payment_date DATE,
    FOREIGN KEY (member_id) REFERENCES member(member_id)
);

CREATE TABLE IF NOT EXISTS class_list (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    instructor_id INT,
    pool_id INT,
    class_name VARCHAR(255),
    class_date DATE,
    start_time TIME,
    end_time TIME,
    detailed_information TEXT,
    is_individual TINYINT(1),
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id),
    FOREIGN KEY (pool_id) REFERENCES pool(pool_id)
);

CREATE TABLE IF NOT EXISTS attendance_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    class_id INT,
    attendance_date DATE,
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    FOREIGN KEY (class_id) REFERENCES class_list(class_id)
);

CREATE TABLE IF NOT EXISTS book_list (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    class_id INT,
    instructor_id INT,
    pool_id INT,
    payment_id INT,
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    FOREIGN KEY (class_id) REFERENCES class_list(class_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id),
    FOREIGN KEY (pool_id) REFERENCES pool(pool_id),
    FOREIGN KEY (payment_id) REFERENCES payment_list(payment_id)
);

INSERT INTO user_account (username, email, password, is_root, register_date)
    VALUES('admin', 'admin@admin.com', '$2b$12$rZ/oMfPkT9q16IWgGJ9n6.e5xynS7f9elfPmPiR.TbEBo2yTkc2Dq', 1, "2023-08-08");
-- admin/adminpassword