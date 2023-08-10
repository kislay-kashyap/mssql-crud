-- Create a new database
CREATE DATABASE EmployeeDB;

-- Use the newly created database
USE EmployeeDB;

-- Create the employee table
CREATE TABLE Employee (id INT PRIMARY KEY,name VARCHAR(255),age INT,phone VARCHAR(15),experience INT);
