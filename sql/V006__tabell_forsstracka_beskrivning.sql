create table forsstracka_beskrivning (
    forsstracka_id int primary key not null references forsstracka(id),
    beskrivning text not null,
    uppdaterad timestamp without time zone not null,
    uppdaterad_av varchar(40) not null
);
