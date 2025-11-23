create database if not exists bd_crud;
use bd_crud;

create table if not exists review(
id   int auto_increment primary key,
nota int check(nota between 0 and 5),
comentario varchar(500)
);