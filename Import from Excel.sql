DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

CREATE TABLE patient (
    id serial NOT NULL,
    last_name varchar(255) NOT NULL,
    first_name varchar(255) NOT NULL,
    dob date NOT NULL,
    phone varchar(20),
    phone_2 varchar(20),
    address varchar(255),
    gender varchar(1),
    downstairs boolean,
    CONSTRAINT patient_pkey PRIMARY KEY (id)
);

CREATE TABLE glasses_prescription (
    id serial NOT NULL,
    last_name varchar(255) NOT NULL,
    first_name varchar(255) NOT NULL,
    dob date NOT NULL,
    date date NOT NULL,
    od varchar(255),
    os varchar(255),
    va_right varchar(255),
    va_left varchar(255),
    pd varchar(255),
    cc varchar(255)
    conj varchar(255),
    sclera varchar(255),
    tears varchar(255),
    cornea varchar(255),
    iris varchar(255),
    antc varchar(255),
    lll varchar(255),
    CONSTRAINT glasses_prescription_pkey PRIMARY KEY (id)
)