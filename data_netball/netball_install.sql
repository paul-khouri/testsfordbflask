


/* many tables */


drop table if exists team;

create table team(
    team_id integer primary key autoincrement ,
    team_name text not null unique
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

drop table if exists member;
create table member
(
    member_id integer primary key autoincrement ,
    member_name text not null,
    member_type text,
    team_id integer,
    email text not null,
    dob date,
    password text not null,
    authorisation inetger not null,
    foreign key (team_id) references team (team_id)
);

drop table if exists class;
create table class
(
    class_id integer primary key autoincrement ,
    class_name text not null,
    elevator_pitch text not null,
    content text not null,
    start_date date,
    frequency integer,
    duration integer
);

insert into class(class_name, elevator_pitch, content, start_date, frequency, duration)
values(
'Dynamic Warm up',
'Prepare the body, heart and mind for the upcoming activity',
'Due to the nature of the game - explosive, powerful movements, repeated '||
'Anterior cruciate ligament injuries are devastating'||
'knee injuries that occur in sports such as Netball.'||
'This injury will put an athlete out of sport and Netball'||
'for up to a year.' ||char(10) ||
 'The Netball Dynamic Warm-Up helps prevent'||
'both of these common Netball injuries.',
'14/07/2023',
7,
4
);

insert into class(class_name, elevator_pitch, content, start_date, frequency, duration)
values(
'Landing Skills',
'The focus is on the skill of the landing movement rather than the height of the jump',
'Landing Skill sessions should be short in duration and '||
'focused on quality. The focus is on the skill of the landing'||
'movement rather than the height of the jump.'|| char(10) ||
'Once a player has developed the skill and quality of the'||
'landing movement they can progress onto plyometric' ||
 'activity or harder balance, proprioception tasks.',
'18/07/2023',
7,
6
);















