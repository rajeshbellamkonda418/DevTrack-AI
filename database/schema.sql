CREATE DATABASE IF NOT EXISTS devtrack_ai;
USE devtrack_ai;
CREATE TABLE IF NOT EXISTS applications (

    id INT AUTO_INCREMENT PRIMARY KEY,

    company VARCHAR(120) NOT NULL,

    role VARCHAR(120) NOT NULL,

    status ENUM(
        'Applied',
        'Interview',
        'Selected',
        'Rejected'
    ) NOT NULL DEFAULT 'Applied',

    skills TEXT,

    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);