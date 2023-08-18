CREATE DATABASE example;
USE example; CREATE TABLE student(id int NOT NULL AUTO_INCREMENT, first_name varchar(50), last_name varchar(50), city varchar(50), semester int, PRIMARY KEY(id)); INSERT INTO student(first_name, last_name, city, semester) VALUES ('Juan', 'Perez', 'Cochabamba', 3),('Carlos', 'Lopez', 'La Paz',5);
CREATE USER 'example_user'@'%' IDENTIFIED BY 'mysql';
GRANT ALL ON example.* TO 'example_user'@'%';
