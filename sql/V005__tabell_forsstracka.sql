create type klass as enum ('1', '2', '3-', '3', '3+', '4-', '4', '4+', '5-', '5', '5+', '6');

create table forsstracka (
    id serial primary key,
    namn varchar(30) not null,
    langd int not null,
    fallhojd int not null,
    gradering_klass klass not null,
    gradering_lyft klass[] not null,
    koord_lat float not null,
    koord_long float not null,
    flode_smhipunkt int not null,
    flode_minimum int not null,
    flode_optimal int not null,
    flode_maximum int not null
);

create index forsstracka_namn_idx on forsstracka ( namn );

create table forsstracka_lan (
    forsstracka_id int not null references forsstracka(id),
    lan_id int not null references lan(id),
    constraint forsstracka_lan_unique unique (forsstracka_id, lan_id)
);

create table forsstracka_vattendrag (
    forsstracka_id int not null references forsstracka(id),
    vattendrag_id int not null references vattendrag(id),
    constraint forsstracka_vattendrag_unique unique (forsstracka_id, vattendrag_id)
);

insert into forsstracka values (1, 'Brännsågen-Åbyggeby', 6000, 28, '2', '{}', 60.75627, 17.03825, 12020, 20, 30, 100);
insert into forsstracka_vattendrag values (1,1);
insert into forsstracka_lan values (1,21);

insert into forsstracka values (2, 'Forsby', 250, 4, '2', '{}', 60.71786, 17.14122, 12020, 30, 50, 100);
insert into forsstracka_vattendrag values (2,1);
insert into forsstracka_lan values (2,21);

insert into forsstracka values (3, 'Vavaren', 350, 12, '3+', '{}', 60.69801, 17.15803, 12020, 20, 25, 40);
insert into forsstracka_vattendrag values (3,1);
insert into forsstracka_lan values (3,21);

insert into forsstracka values (4, 'Konserthuset', 1000, 5, '2', '{"5","4+"}', 60.67298, 17.13364, 11802, 30, 60, 100);
insert into forsstracka_vattendrag values (4,2);
insert into forsstracka_lan values (4,21);


select setval(pg_get_serial_sequence('forsstracka', 'id'), (select max(id) from forsstracka)+1);
