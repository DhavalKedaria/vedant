# step 1 create database:
- vedant

# step 2 run below Queries on postgresql

- create table galary(id serial Primary key,users text, image text, comm text null)
- create table galary(id serial Primary key,users text, image text, comm text null)
- create table users(id serial Primary key,uname text, pwd text)
- create table user_detail(id serial primary key,user_id int references users(id), description text, dp text)

## this is sample insert query
- insert into galary (users,image) values('amit','baseimage.jpg')



## sample data
[(1, 1, 'vedant', '/images/system/user.jpg')(asdfasdf,afa,asdfasfd)]

[] == list → 0 index tuple
() == tuple → 3 image

data[0][3] 
data[1][2]