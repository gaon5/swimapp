-- 创建用于存储用户账户信息的表
CREATE TABLE IF NOT EXISTS user_account (
    user_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个用户的唯一标识符
    username VARCHAR(100) NOT NULL UNIQUE, -- 用户名，必须唯一且不能为空
    email VARCHAR(100) NOT NULL UNIQUE, -- 用户电子邮件地址，必须唯一且不能为空
    password VARCHAR(255) NOT NULL, -- 用户密码（已散列），不能为空
    is_member TINYINT(1) DEFAULT 0, -- 标志用户是否为会员
    is_instructor TINYINT(1) DEFAULT 0, -- 标志用户是否为讲师
    is_admin TINYINT(1) DEFAULT 0, -- 标志用户是否为管理员
    is_root TINYINT(1) DEFAULT 0, -- 标志用户是否为根用户（超级管理员）
    register_date DATE -- 用户注册日期
);

-- 创建用于存储新闻条目的表
CREATE TABLE IF NOT EXISTS news (
    news_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个新闻条目的唯一标识符
    news TEXT -- 新闻条目的内容
);

-- 创建用于存储称号（例如先生、女士、博士）的表
CREATE TABLE IF NOT EXISTS title (
    title_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个称号的唯一标识符
    title VARCHAR(255) -- 称号的名称
);

-- 创建用于存储城市信息的表
CREATE TABLE IF NOT EXISTS city (
    city_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个城市的唯一标识符
    city VARCHAR(255) -- 城市的名称
);

-- 创建用于存储城市内区域信息的表
CREATE TABLE IF NOT EXISTS region (
    region_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个区域的唯一标识符
    city_id INT, -- 外键，引用所属城市的标识符
    region VARCHAR(255), -- 区域的名称
    FOREIGN KEY (city_id) REFERENCES city(city_id) -- 建立外键关系
);

-- 创建用于存储管理员用户详细信息的表
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个管理员的唯一标识符
    user_id INT, -- 外键，引用关联的用户账户
    title_id INT, -- 外键，引用管理员的称号
    first_name VARCHAR(255), -- 管理员的名字
    last_name VARCHAR(255), -- 管理员的姓氏
    phone_number VARCHAR(255), -- 管理员的电话号码
    state TINYINT(1), -- 管理员的状态/状态
    FOREIGN KEY (user_id) REFERENCES user_account(user_id), -- 建立外键关系
    FOREIGN KEY (title_id) REFERENCES title(title_id) -- 建立外键关系
);

-- 创建用于存储讲师详细信息的表
CREATE TABLE IF NOT EXISTS instructor (
    instructor_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个讲师的唯一标识符
    user_id INT, -- 外键，引用关联的用户账户
    title_id INT, -- 外键，引用讲师的称号
    first_name VARCHAR(255), -- 讲师的名字
    last_name VARCHAR(255), -- 讲师的姓氏
    phone_number VARCHAR(255), -- 讲师的电话号码
    detailed_information TEXT, -- 讲师的详细信息
    state TINYINT(1), -- 讲师的状态/状态
    FOREIGN KEY (user_id) REFERENCES user_account(user_id), -- 建立外键关系
    FOREIGN KEY (title_id) REFERENCES title(title_id) -- 建立外键关系
);

-- 创建用于存储会员详细信息的表
CREATE TABLE IF NOT EXISTS member (
    member_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个会员的唯一标识符
    user_id INT, -- 外键，引用关联的用户账户
    title_id INT, -- 外键，引用会员的称号
    first_name VARCHAR(255), -- 会员的名字
    last_name VARCHAR(255), -- 会员的姓氏
    phone_number VARCHAR(255), -- 会员的电话号码
    detailed_information TEXT, -- 会员的详细信息
    city_id INT, -- 外键，引用会员所在城市
    region_id INT, -- 外键，引用会员在城市中的区域
    street_name VARCHAR(255), -- 会员的街道名/地址
    birth_date DATE, -- 会员的出生日期
    health_information TEXT, -- 会员的健康信息
    state TINYINT(1), -- 会员的状态/状态
    FOREIGN KEY (user_id) REFERENCES user_account(user_id), -- 建立外键关系
    FOREIGN KEY (title_id) REFERENCES title(title_id), -- 建立外键关系
    FOREIGN KEY (city_id) REFERENCES city(city_id), -- 建立外键关系
    FOREIGN KEY (region_id) REFERENCES region(region_id) -- 建立外键关系
);

-- 创建用于存储泳池信息的表
CREATE TABLE IF NOT EXISTS pool (
    pool_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个泳池的唯一标识符
    pool_name VARCHAR(255) -- 泳池的名称
);

-- 创建用于存储会员支付信息的表
CREATE TABLE IF NOT EXISTS payment_list (
    payment_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个支付的唯一标识符
    member_id INT, -- 外键，引用关联的会员
    price FLOAT, -- 支付金额/价格
    payment_date DATE, -- 支付日期
    FOREIGN KEY (member_id) REFERENCES member(member_id) -- 建立外键关系
);

-- 创建用于存储课程信息的表
CREATE TABLE IF NOT EXISTS class_list (
    class_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个课程的唯一标识符
    instructor_id INT, -- 外键，引用关联的讲师
    pool_id INT, -- 外键，引用关联的泳池
    class_name VARCHAR(255), -- 课程的名称
    class_date DATE, -- 课程的日期
    start_time TIME, -- 课程的开始时间
    end_time TIME, -- 课程的结束时间
    detailed_information TEXT, -- 课程的详细信息
    is_individual TINYINT(1), -- 标志课程是否为个别课程
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id), -- 建立外键关系
    FOREIGN KEY (pool_id) REFERENCES pool(pool_id) -- 建立外键关系
);

-- 创建用于存储出勤日志的表
CREATE TABLE IF NOT EXISTS attendance_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个出勤日志条目的唯一标识符
    member_id INT, -- 外键，引用关联的会员
    class_id INT, -- 外键，引用关联的课程
    attendance_date DATE, -- 出勤日期
    FOREIGN KEY (member_id) REFERENCES member(member_id), -- 建立外键关系
    FOREIGN KEY (class_id) REFERENCES class_list(class_id) -- 建立外键关系
);

-- 创建用于存储预订信息的表
CREATE TABLE IF NOT EXISTS book_list (
    book_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个预订的唯一标识符
    member_id INT, -- 外键，引用关联的会员
    class_id INT, -- 外键，引用关联的课程
    instructor_id INT, -- 外键，引用关联的讲师
    pool_id INT, -- 外键，引用关联的泳池
    payment_id INT, -- 外键，引用关联的支付
    FOREIGN KEY (member_id) REFERENCES member(member_id), -- 建立外键关系
    FOREIGN KEY (class_id) REFERENCES class_list(class_id), -- 建立外键关系
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id), -- 建立外键关系
    FOREIGN KEY (pool_id) REFERENCES pool(pool_id), -- 建立外键关系
    FOREIGN KEY (payment_id) REFERENCES payment_list(payment_id) -- 建立外键关系
);

-- 创建用于存储付款到期日的表
CREATE TABLE IF NOT EXISTS payment_due (
    due_id INT PRIMARY KEY AUTO_INCREMENT, -- 每个付款到期日的唯一标识符
    payment_id INT, -- 外键，引用关联的支付
    start_date DATE, -- 到期期间的开始日期
    end_date DATE, -- 到期期间的结束日期
    FOREIGN KEY (payment_id) REFERENCES payment_list(payment_id) -- 建立外键关系
);

-- 将一个根用户插入到user_account表中
INSERT INTO user_account (username, email, password, is_root, register_date)
    VALUES('admin', 'admin@admin.com', '$2b$12$rZ/oMfPkT9q16IWgGJ9n6.e5xynS7f9elfPmPiR.TbEBo2yTkc2Dq', 1, "2023-08-08");
