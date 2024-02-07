# docker run --name lesson-db -p 5432:5432 -e POSTGRES_PASSWORD=admin -d postgres
DROP TABLE IF EXISTS students;
-- Table: students
CREATE TABLE students (
    id INT PRIMARY KEY AUTOINCREMENT,
    name VARCHAR (30),
    group_id INT,
    FOREIGN KEY (group_id) REFERENCES groups (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS groups;
-- Table: students
CREATE TABLE groups (
    id INT PRIMARY KEY AUTOINCREMENT,
    name VARCHAR (30),
);

DROP TABLE IF EXISTS lecturers;
-- Table: students
CREATE TABLE lecturers (
    id INT PRIMARY KEY AUTOINCREMENT,
    name VARCHAR (30),
);

DROP TABLE IF EXISTS subjects;
-- Table: students
CREATE TABLE subjects (
    id INT PRIMARY KEY,
    name VARCHAR (30),
    lecturer_id INT,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS assessments;
-- Table: assessments
CREATE TABLE assessments (
    id INT PRIMARY KEY,
    name VARCHAR (30),
    student_id INT,
    subject_id INT,
    created_at DATETIME
    FOREIGN KEY (student_id) REFERENCES students (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
);