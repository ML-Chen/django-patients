-- https://stackoverflow.com/a/57436699/5139284 for how to export Access databases to Postgres

ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Last Name" TO last_name;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "First Name" TO first_name;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Exam date" TO date;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "DOB" TO dob;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "OD" TO od;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "OS" TO os;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "VA right" TO va_right;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "VA left" TO va_left;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "PD" TO pd;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Conj" TO conj;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Sclera" TO sclera;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Tears" TO tears;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Cornea" TO cornea;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Iris" TO iris;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Antc" TO antc;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "CC" TO cc;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Lens/Lids/Lashes" TO lll;

ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Last Name" TO last_name;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "First Name" TO first_name;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Exam date" TO date;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "DOB" TO dob;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Brand" TO brand;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Model" TO model;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Color" TO color;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Frame" TO frame;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Lens" TO lens;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Contact Lens" TO contact_lens;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Additional Comments" TO additional_comments;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Price" TO price;
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Recorded" TO recorded;

ALTER TABLE postgres.public."Insurance" RENAME COLUMN "ID" TO id;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Last Name" TO last_name;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "First Name" TO first_name;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "DOB" TO dob;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Insurance ID" TO insurance_id;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Insurance ID 2" TO insurance_id_2;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Can Call" TO can_call;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Called" TO called;

ALTER TABLE postgres.public."Patient" RENAME COLUMN "ID" TO id;
ALTER TABLE postgres.public."Patient" RENAME COLUMN "Last Name" TO last_name;
ALTER TABLE postgres.public."Patient" RENAME COLUMN "First Name" TO first_name;
ALTER TABLE postgres.public."Patient" RENAME COLUMN "DOB" TO dob;
ALTER TABLE postgres.public."Patient" RENAME COLUMN "Telephone" TO phone;
ALTER TABLE postgres.public."Patient" RENAME COLUMN "Telephone 2" TO phone_2;
ALTER TABLE postgres.public."Patient" RENAME COLUMN "Address" TO address;
ALTER TABLE postgres.public."Patient" RENAME COLUMN "Gender" TO gender;
ALTER TABLE postgres.public."Patient" RENAME COLUMN "Downstairs?" TO downstairs;

ALTER TABLE postgres.public."Checkups" RENAME TO checkup;
ALTER TABLE postgres.public."Insurance" RENAME TO insurance;
ALTER TABLE postgres.public."Glasses" RENAME TO glasses;
ALTER TABLE postgres.public."Patient" RENAME TO patient;

ALTER TABLE patient ADD PRIMARY KEY (id);

CREATE TABLE checkup_ AS (
    SELECT patient.id AS patient, checkup.last_name, checkup.first_name, checkup.dob, date, od, os, va_right, va_left, pd, conj, sclera, tears, cornea, iris, antc, lll, cc
    FROM public.checkup AS checkup LEFT JOIN public.patient AS patient
    ON lower(patient.last_name) = lower(checkup.last_name)
    AND lower(patient.first_name) = lower(checkup.first_name)
    AND patient.dob = checkup.dob
);
ALTER TABLE checkup_ ADD CONSTRAINT fk_checkup_patient FOREIGN KEY (patient) REFERENCES patient (id);
ALTER TABLE checkup_ ADD id SERIAL PRIMARY KEY;
DROP TABLE checkup;
ALTER TABLE checkup_ RENAME TO checkup;

CREATE TABLE glasses_ AS (
    SELECT checkup.patient AS patient, checkup.id AS prescription, glasses.date, brand, model, color, frame, lens, contact_lens, additional_comments, price -- omitting the 'recorded' column
    FROM public.glasses AS glasses LEFT JOIN public.checkup AS checkup
    ON lower(checkup.last_name) = lower(glasses.last_name)
    AND lower(checkup.first_name) = lower(glasses.first_name)
    AND checkup.dob = glasses.dob
    AND checkup.exam_date = glasses.exam_date
);
ALTER TABLE glasses_ ADD CONSTRAINT fk_glasses_checkup FOREIGN KEY (prescription) REFERENCES checkup (id);
ALTER TABLE glasses_ ADD CONSTRAINT fk_glasses_patient FOREIGN KEY (patient) REFERENCES patient (id);
ALTER TABLE checkup DROP last_name, DROP first_name, DROP dob;
DROP TABLE glasses;
ALTER TABLE glasses_ RENAME TO glasses;

CREATE TABLE insurance_ AS (
    SELECT patient.id AS patient, insurance.last_name, insurance.first_name, insurance.dob, insurance_id, insurance_id_2, can_call, called
    FROM public.insurance AS insurance LEFT JOIN public.patient AS patient
    ON lower(patient.last_name) = lower(insurance.last_name)
    AND lower(patient.first_name) = lower(insurance.first_name)
    AND patient.dob = insurance.dob
);
ALTER TABLE insurance_ ADD CONSTRAINT fk_insurance_patient FOREIGN KEY (patient) REFERENCES patient (id);
ALTER TABLE insurance_ ADD id SERIAL PRIMARY KEY; -- y'know what it's okay if the id column is at the end
DROP TABLE insurance;
ALTER TABLE insurance_ RENAME TO insurance;

ALTER TABLE checkup RENAME TO glasses_prescription;

ALTER TABLE glasses RENAME TO glasses_;
ALTER TABLE glasses_prescription RENAME to glasses_prescription_;
ALTER TABLE insurance RENAME TO insurance_;
ALTER TABLE patient RENAME TO patient_;

UPDATE glasses_ SET brand = '' WHERE brand IS NULL;
UPDATE glasses_ SET model = '' WHERE model IS NULL;
UPDATE glasses_ SET color = '' WHERE color IS NULL;
UPDATE glasses_ SET frame = '' WHERE frame IS NULL;
UPDATE glasses_ SET lens = '' WHERE lens IS NULL;
UPDATE glasses_ SET contact_lens = '' WHERE contact_lens IS NULL;
UPDATE glasses_ SET additional_comments = '' WHERE additional_comments IS NULL;
UPDATE glasses_ SET price = '' WHERE price IS NULL;
UPDATE glasses_prescription_ SET od = '' WHERE od IS NULL;
UPDATE glasses_prescription_ SET os = '' WHERE os IS NULL;
UPDATE glasses_prescription_ SET va_right = '' WHERE va_right IS NULL;
UPDATE glasses_prescription_ SET va_left = '' WHERE va_left IS NULL;
UPDATE glasses_prescription_ SET va_left = '' WHERE va_left IS NULL;
UPDATE glasses_prescription_ SET va_left = '' WHERE va_left IS NULL;
UPDATE glasses_prescription_ SET conj = '' WHERE conj IS NULL;
UPDATE glasses_prescription_ SET sclera = '' WHERE sclera IS NULL;
UPDATE glasses_prescription_ SET tears = '' WHERE tears IS NULL;
UPDATE glasses_prescription_ SET cornea = '' WHERE cornea IS NULL;
UPDATE glasses_prescription_ SET va_left = '' WHERE va_left IS NULL;
UPDATE glasses_prescription_ SET iris = '' WHERE iris IS NULL;
UPDATE glasses_prescription_ SET antc = '' WHERE antc IS NULL;
UPDATE glasses_prescription_ SET cc = '' WHERE cc IS NULL;
UPDATE glasses_prescription_ SET lll = '' WHERE lll IS NULL;
UPDATE insurance_ SET insurance_id = '' WHERE insurance_id IS NULL;
UPDATE insurance_ SET insurance_id_2 = '' WHERE insurance_id_2 IS NULL;
UPDATE patient_ SET phone = '' WHERE phone IS NULL;
UPDATE patient_ SET phone_2 = '' WHERE phone_2 IS NULL;
UPDATE patient_ SET address = '' WHERE address IS NULL;
UPDATE patient_ SET gender = '' WHERE gender IS NULL;

UPDATE patient_ SET gender = 'f' WHERE gender = 'F';
UPDATE patient_ SET gender = 'm' WHERE gender = 'M';

-- Check for other genders.
SELECT * FROM patient_ WHERE gender != 'f' AND gender != 'm';

-- Manually fix invalid PDs.
SELECT * FROM glasses_prescription_ WHERE pd > 90;

-- After Django migration recreates tables, copy data over from existing tables

ALTER TABLE glasses ALTER size SET DEFAULT '';
ALTER TABLE glasses_prescription ALTER notes SET DEFAULT '';
ALTER TABLE glasses_prescription ALTER outside SET DEFAULT false;

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

DROP TABLE glasses_, glasses_prescription_, insurance_, patient_ CASCADE;


-- DROP TABLE auth_group, auth_group_permissions, auth_permission, auth_user, auth_user, auth_user_groups, auth_user_user_permissions, django_admin_log, django_content_type, django_migrations;

/*
ALTER TABLE patient ADD UNIQUE (
    REPLACE(REPLACE(last_name, ' ', ''), ',', ''),
    REPLACE(REPLACE(first_name, ' ', ''), ',', ''),
    dob
);
*/
