create table lan (
   id int primary key not null,
   lankod char (2) not null unique,
   namn varchar(30) not null unique
);

create index lan_namn_idx on lan ( namn );

insert into lan values (01, '01', 'Stockholm');
insert into lan values (03, '03', 'Uppsala');
insert into lan values (04, '04', 'Södermanland');
insert into lan values (05, '05', 'Östergötland');
insert into lan values (06, '06', 'Jönköping');
insert into lan values (07, '07', 'Kronoberg');
insert into lan values (08, '08', 'Kalmar');
insert into lan values (09, '09', 'Gotland');
insert into lan values (10, '10', 'Blekinge');
insert into lan values (12, '12', 'Skåne');
insert into lan values (13, '13', 'Halland');
insert into lan values (14, '14', 'Västra Götaland');
insert into lan values (17, '17', 'Värmland');
insert into lan values (18, '18', 'Örebro');
insert into lan values (19, '19', 'Västmanland');
insert into lan values (20, '20', 'Dalarna');
insert into lan values (21, '21', 'Gävleborg');
insert into lan values (22, '22', 'Västernorrland');
insert into lan values (23, '23', 'Jämtland');
insert into lan values (24, '24', 'Västerbotten');
insert into lan values (25, '25', 'Norrbotten');

