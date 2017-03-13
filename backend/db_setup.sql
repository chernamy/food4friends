CREATE DATABASE IF NOT EXISTS test;
CREATE DATABASE IF NOT EXISTS prod;
use prod;
CREATE TABLE IF NOT EXISTS USER(userid VARCHAR(20) NOT NULL, role ENUM('none', 'buyer', 'seller') NOT NULL, location VARCHAR(255), PRIMARY KEY(userid));
CREATE TABLE IF NOT EXISTS ITEM(userid VARCHAR(40) NOT NULL, photo VARCHAR(40) NOT NULL, servings INT NOT NULL, end INT NOT NULL,price DECIMAL(5, 2) NOT NULL, address VARCHAR(255) NOT NULL, description TEXT, PRIMARY KEY(userid));
CREATE TABLE IF NOT EXISTS TRANSACTION(sellerid VARCHAR(40) NOT NULL, buyerid VARCHAR(40) NOT NULL, servings INT NOT NULL);
CREATE TABLE IF NOT EXISTS COMMUNITY(communityid int NOT NULL AUTO_INCREMENT, communityname varchar(255) NOT NULL, PRIMARY KEY(communityid));
CREATE TABLE IF NOT EXISTS MEMBERSHIP(userid varchar(20) NOT NULL, communityid int NOT NULL, status ENUM('pending', 'joined') NOT NULL);
CREATE TABLE IF NOT EXISTS RATING(sellerid varchar(20) NOT NULL, buyerid varchar(20) NOT NULL, rating ENUM('1', '2', '3', '4', '5') NOT NULL, description varchar(255));
