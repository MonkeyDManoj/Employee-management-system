create table uses(id INTEGER PRIMARY KEY AUTOINCREMENT, name text not null, password text not null, admin boolean
default '0');

create table emp(empid INTEGER PRIMARY KEY AUTOINCREMENT, name text not null,email text , phone INT,
address text, joining_date TIMESTAMP default CURRENT_TIMESTAMP, total_projects_handled integer default 1, total_test_cases
 integer default 1, total_defects integer default 1,total_defects_pending integer default 1);