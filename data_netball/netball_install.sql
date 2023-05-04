drop table if exists game;


create table game(
    game_id integer primary key autoincrement ,
    game_date datetime not null unique ,
    team_1 text not null,
    score_1 integer not null,
    team_2 text not null,
    score_2 integer not null
);

insert into game(game_date, team_1, score_1, team_2, score_2)
values('2023-03-22 08:30','Hot Shots 3',	28,	'St Marys 2',30);
insert into game(game_date, team_1, score_1, team_2, score_2)
values('2023-03-22 12:30','Vic Uni 1',10,'Hot Shots 1',25);
insert into game(game_date, team_1, score_1, team_2, score_2)
values('2023-03-22 14:00', 'WGC'	, 28, 'Hot Shots 2',39);
insert into game(game_date, team_1, score_1, team_2, score_2)
values('2023-03-29 09:00','Hot Shots 3',13,'St Marys 2',28);
insert into game(game_date, team_1, score_1, team_2, score_2)
values('2023-03-29 10:30', 'Vic Uni 1',	39, 'Hot Shots 1',40);
insert into game(game_date, team_1, score_1, team_2, score_2)
values('2023-03-29 12:30','WGC',15, 'Hot Shots 2',23);
