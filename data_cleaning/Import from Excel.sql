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
    cc varchar(255),
    conj varchar(255),
    sclera varchar(255),
    tears varchar(255),
    cornea varchar(255),
    iris varchar(255),
    antc varchar(255),
    lll varchar(255),
    CONSTRAINT glasses_prescription_pkey PRIMARY KEY (id)
);

CREATE TABLE glasses (
    last_name varchar(255) NOT NULL,
    first_name varchar(255) NOT NULL,
    dob date NOT NULL,
    date date NOT NULL,
    brand varchar(255),
    model varchar(255),
    color varchar(255),
    frame varchar(255),
    lens varchar(255),
    contact_lens varchar(255),
    additional_comments varchar(255),
    payment varchar(255)
); -- don't import recorded column

CREATE TABLE insurance (
   last_name varchar(255) NOT NULL,
   first_name varchar(255) NOT NULL,
   dob date NOT NULL,
   insurance_id varchar(255),
   insurance_id_2 varchar(255),
   can_call bool,
   called bool
);

/*
INSERT INTO patient (id, last_name, first_name, dob, phone, phone_2, address, gender, downstairs)
SELECT id, last_name, first_name, dob, phone, phone_2, address, gender, downstairs
FROM patient_;

INSERT INTO glasses_prescription (id, patient_id, date, od, os, va_right, va_left, pd, cc, conj, sclera, tears, cornea, iris, antc, lll)
SELECT id, patient, date, od, os, va_right, va_left, pd, cc, conj, sclera, tears, cornea, iris, antc, lll
FROM glasses_prescription_;

INSERT INTO glasses (patient_id, prescription_id, date, brand, model, color, frame, lens, contact_lens, price, additional_comments)
SELECT patient, prescription, date, brand, model, color, frame, lens, contact_lens, price, additional_comments
FROM glasses_;

INSERT INTO insurance (id, patient_id, insurance_id, insurance_id_2)
SELECT id, patient, insurance_id, insurance_id_2
FROM insurance_;
 */

-- somehow get tables from Excel??

-- COPY patient FROM 'C:/Users/micha/Google Drive/Patients 8-16-19/Patient.txt' WITH DELIMITER '\t' CSV HEADER;

CREATE TABLE checkup_joined AS (
    SELECT patient.id AS patient, checkup.last_name, checkup.first_name, checkup.dob, date, od, os, va_right, va_left, pd, conj, sclera, tears, cornea, iris, antc, lll, cc
    FROM public.checkup AS checkup LEFT JOIN public.patient AS patient
    ON lower(patient.last_name) = lower(checkup.last_name)
    AND lower(patient.first_name) = lower(checkup.first_name)
    AND patient.dob = checkup.dob
);
CREATE TABLE checkup_orphans AS (
    SELECT * FROM checkup_joined WHERE checkup_joined.patient IS NULL
);

CREATE TABLE glasses_joined AS (
    SELECT checkup.patient AS patient, checkup.id AS prescription, glasses.date, brand, model, color, frame, lens, contact_lens, additional_comments, price -- omitting the 'recorded' column
    FROM public.glasses AS glasses LEFT JOIN public.checkup AS checkup
     ON lower(checkup.last_name) = lower(glasses.last_name)
         AND lower(checkup.first_name) = lower(glasses.first_name)
         AND checkup.dob = glasses.dob
         AND checkup.exam_date = glasses.exam_date
);
CREATE TABLE glasses_orphans AS (
    SELECT * FROM glasses_joined WHERE glasses_joined.patient IS NULL OR prescription IS NULL
);

CREATE TABLE insurance_joined AS (
    SELECT patient.id AS patient, insurance.last_name, insurance.first_name, insurance.dob, insurance_id, insurance_id_2, can_call, called
    FROM public.insurance AS insurance LEFT JOIN public.patient AS patient
    ON lower(patient.last_name) = lower(insurance.last_name)
        AND lower(patient.first_name) = lower(insurance.first_name)
        AND patient.dob = insurance.dob
);
CREATE TABLE insurance_orphans AS (
    SELECT * FROM insurance_joined WHERE insurance_joined.patient IS NULL OR prescription IS NULL
);
