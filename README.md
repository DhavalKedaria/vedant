# step 1 create database:
- vedant

# step 2 run below Queries on postgresql

- create table galary(id serial Primary key,users text, image text, comm text null)
- create table galary(id serial Primary key,users text, image text, comm text null)
- create table users(id serial Primary key,uname text, pwd text)
- create table user_detail(id serial primary key,user_id int references users(id), description text, dp text)

## this is sample insert query
- insert into galary (users,image) values('amit','baseimage.jpg')
