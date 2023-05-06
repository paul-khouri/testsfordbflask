
/* single table */
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

/* many tables */
drop table if exists match;
drop table if exists team;
drop table if exists match_team;

create table match(
    match_id integer primary key autoincrement ,
    match_date date not null ,
    location text not null
);

create table team(
    team_id integer primary key autoincrement ,
    team_name text not null unique
);

create table match_team(
    team_id integer not null ,
    match_id integer not null ,
    points integer,
    primary key (team_id, match_id)
);

insert into team(team_name)
values('Hot Shots 1');
insert into team(team_name)
values('Hot Shots 2');
insert into team(team_name)
values('Hot Shots 3');
insert into team(team_name)
values('St Marys 1');
insert into team(team_name)
values('St Marys 2');
insert into team(team_name)
values('Vic Uni 1');
insert into team(team_name)
values('WGC 1');
insert into team(team_name)
values('WGC 2');

insert into match(match_date, location)
values('2023-03-22 08:30', 'ASB');
insert into match(match_date, location)
values('2023-03-22 12:30', 'ASB');
insert into match(match_date, location)
values('2023-03-22 14:00', 'ASB');
insert into match(match_date, location)
values('2023-03-29 09:00', 'ASB');
insert into match(match_date, location)
values('2023-03-29 10:30', 'ASB');
insert into match(match_date, location)
values('2023-03-29 12:30', 'ASB');

insert into match_team(team_id,match_id)
values((select team_id from team where team_name = 'Hot Shots 3'),
       (select match_id from match where match_date = '2023-03-22 08:30'));
insert into match_team(team_id,match_id)
values((select team_id from team where team_name = 'St Marys 2'),
       (select match_id from match where match_date = '2023-03-22 08:30'));

insert into match_team(team_id,match_id)
values((select team_id from team where team_name = 'Hot Shots 1'),
       (select match_id from match where match_date = '2023-03-22 12:30'));
insert into match_team(team_id,match_id)
values((select team_id from team where team_name = 'Vic Uni 1'),
       (select match_id from match where match_date = '2023-03-22 12:30'));

/* -- */
drop table if exists draw;

create table draw
(
    draw_id   integer primary key autoincrement,
    draw_date date    not null,
    team_1    integer not null,
    score_1   integer,
    team_2    integer not null,
    score_2   integer,
    foreign key (team_1) references team (team_id),
    foreign key (team_2) references team (team_id),
    unique(draw_date,team_1,team_2)
);



