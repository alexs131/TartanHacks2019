drop table patient_data;
create table patient_data (
    id integer primary key autoincrement,
    name text not null,
    color text not null,
    shape text not null,
    writing text not null,
    identified_pill text not null,
    date current_date
);