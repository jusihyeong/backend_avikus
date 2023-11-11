create database avikus;


create table avikus.task
(
    id       int unsigned auto_increment primary key,
    name     varchar(255) not null,
    `create` datetime     not null,
    content  longtext     null
);