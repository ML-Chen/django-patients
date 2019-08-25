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
    payment varchar(255),
    additional_comments varchar(255)
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

-- Now, run excel2postgres.py

CREATE TABLE glasses_prescription_joined AS (
    SELECT patient.id AS patient, patient.last_name, patient.first_name, patient.dob, date, od, os, va_right, va_left, pd, conj, sclera, tears, cornea, iris, antc, lll, cc
    FROM public.glasses_prescription AS glasses_prescription LEFT JOIN public.patient AS patient
    ON REPLACE(patient.last_name, ' ', '') ILIKE CONCAT(REPLACE(glasses_prescription.last_name, ' ', ''), '%')
    AND REPLACE(patient.first_name, ' ', '') ILIKE CONCAT(REPLACE(glasses_prescription.first_name, ' ', ''), '%')
    AND patient.dob = glasses_prescription.dob
);
CREATE TABLE glasses_prescription_orphans AS (
    SELECT * FROM glasses_prescription_joined WHERE glasses_prescription_joined.patient IS NULL
);

CREATE TABLE glasses_joined AS (
    SELECT glasses_prescription.patient AS patient, glasses_prescription.id AS prescription, patient.last_name, patient.first_name, patient.dob, glasses.date, brand, model, color, frame, lens, contact_lens, additional_comments, payment -- omitting the 'recorded' column
    FROM public.glasses AS glasses LEFT JOIN public.glasses_prescription AS glasses_prescription
    ON REPLACE(patient.last_name, ' ', '') ILIKE CONCAT(REPLACE(glasses.last_name, ' ', ''), '%')
    AND REPLACE(patient.first_name, ' ', '') ILIKE CONCAT(REPLACE(glasses.first_name, ' ', ''), '%')
    AND glasses_prescription.dob = glasses.dob
    AND glasses_prescription.date = glasses.date
);
CREATE TABLE glasses_orphans AS (
    SELECT * FROM glasses_joined WHERE glasses_joined.patient IS NULL OR prescription IS NULL
);

CREATE TABLE insurance_joined AS (
    SELECT patient.id AS patient, patient.last_name, patient.first_name, patient.dob, insurance_id, insurance_id_2, can_call, called
    FROM public.insurance AS insurance LEFT JOIN public.patient AS patient
    ON lower(patient.last_name) = lower(insurance.last_name)
        AND lower(patient.first_name) = lower(insurance.first_name)
        AND patient.dob = insurance.dob
);
CREATE TABLE insurance_orphans AS (
    SELECT * FROM insurance_joined WHERE insurance_joined.patient IS NULL OR prescription IS NULL
);

ALTER TABLE glasses_prescription_joined DROP last_name, DROP first_name, DROP dob;
ALTER TABLE glasses_joined DROP last_name, DROP first_name, DROP dob;
ALTER TABLE insurance_joined DROP last_name, DROP first_name, DROP dob;

DROP TABLE glasses_prescription;
ALTER TABLE glasses_prescription_joined RENAME TO glasses_prescription;
DROP TABLE glasses;
ALTER TABLE glasses_joined RENAME TO glasses;
DROP TABLE insurance;
ALTER TABLE insurance_joined RENAME TO insurance;