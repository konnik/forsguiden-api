create table vattendrag (
   id serial primary key,
   namn varchar(30) not null,
   beskrivning varchar(500)
);

create index vattendrag_namn_idx on vattendrag ( namn );

create table vattendrag_lan (
    vattendrag_id int not null references vattendrag(id),
    lan_id int not null references lan(id)
);

insert into vattendrag values (1, 'Testeboån', 'Ån rinner genom ett flackt skogs- och myrlandskap mellan Ockelbo och Gävle. Testeboån var tidigare flottled och spår efter detta finns kvar på sina håll.');
insert into vattendrag_lan values (1,21);

insert into vattendrag values (2, 'Gavleån', 'Hela Gavleån är ca 2 mil lång och rinner från Storsjön till havet i Gävlebukten. Det finns 8 kraftverk på sträckan och den enda del som är intressant ur forspaddlingssynpunkt är nedströms det sista kraftverket i Boulognerskogen i centrala Gävle.');
insert into vattendrag_lan values (2,21);

insert into vattendrag values (3, 'Vålån', 'Vålån är en fantastisk sträcka för de som gillar brutal utförspaddling. Sträckan är 7 km med en fallhöjd av 80 m. Grad 1 - 5. Den innehåller sex svåra passager.');
insert into vattendrag_lan values (3,23);

SELECT setval(pg_get_serial_sequence('vattendrag', 'id'), (SELECT MAX(id) FROM vattendrag)+1);
