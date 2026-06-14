# step 1 create database:
- vedant

# step 2 run below Queries on postgresql

- create table galary(id serial Primary key,users text, image text, comm text null)
- create table galary(id serial Primary key,users text, image text, comm text null)
- create table users(id serial Primary key,uname text, pwd text)
- create table user_detail(id serial primary key,user_id int references users(id), description text, dp text)

## this is sample insert query
- insert into galary (users,image) values('amit','baseimage.jpg')



## sample data example
[(1, 1, 'vedant', '/images/system/user.jpg')(asdfasdf,afa,asdfasfd)]

[] == list → 0 index tuple
() == tuple → 3 image

data[0][3] 
data[1][2]


## current bugs 
profile descripton sanitation



## 18-jan-2026 -- Comment Section DB Query
create table comment (id serial Primary key,image_id int references galary(id), user_id int references users(id),cmts text)
#drop table comment   
select * from comment


## reference query
select * from user_detail

select * from users as u inner join user_detail as d on u.id=d.user_id where u.uname ='harsh'

select * from galary

----- comment section---

create table comment (id serial Primary key,image_id int references galary(id), user_id int references users(id),cmts text)

drop table comment

select * from galary
select * from users

insert into comment(image_id,user_id,cmts) values(2,2,'nice')

select * from users as u inner join galary as g on g.users=u.uname inner join comment as c on u.id=c.user_id

select * from comment

select * from user_detail

select u.uname,c.cmts,ud.dp from users as u inner join comment as c on u.id=c.user_id inner join user_detail as ud on u.id=ud.user_id

select u.uname,c.cmts,ud.dp,c.image_id from users as u inner join comment as c on u.id=c.user_id inner join user_detail as ud on u.id=ud.user_id where c.image_id={image_id} order by c.id

## current problems
- hard coded comments  // solved
- hardcoded username is galay need to replace it with user id // solved
- make image comments dynemic // solved
- All comments are visible on all images // solved
----------------
- Comment Refresh issue
- Search Dashboard Page change after submitting comment

==========14-06-2026============
- like is hardcoded
- unique views
- email login - to make it unique
- Ai Integration (comment polish / chat polish)
- email on comment