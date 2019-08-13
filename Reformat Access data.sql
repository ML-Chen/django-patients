ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Last Name" TO last_name;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "First Name" TO first_name;
ALTER TABLE postgres.public."Checkups" RENAME COLUMN "Exam date" TO exam_date;
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
ALTER TABLE postgres.public."Glasses" RENAME COLUMN "Exam date" TO exam_date;
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

ALTER TABLE postgres.public."Insurance" RENAME COLUMN "ID" TO pk;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Last Name" TO last_name;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "First Name" TO first_name;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "DOB" TO dob;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Insurance ID" TO insurance_id;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Insurance ID 2" TO insurance_id_2;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Can Call" TO can_call;
ALTER TABLE postgres.public."Insurance" RENAME COLUMN "Called" TO called;

ALTER TABLE postgres.public."Patient" RENAME COLUMN "ID" TO pk;
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

ALTER TABLE patient ADD PRIMARY KEY (pk);

CREATE TABLE checkup_ AS (
    SELECT patient.pk AS patient, checkup.last_name, checkup.first_name, checkup.dob, exam_date, od, os, va_right, va_left, pd, conj, sclera, tears, cornea, iris, antc, lll, cc
    FROM public.checkup AS checkup LEFT JOIN public.patient AS patient
    ON patient.last_name = checkup.last_name
    AND patient.first_name = checkup.first_name
    AND patient.dob = checkup.dob
);
ALTER TABLE checkup_ ADD CONSTRAINT fk_checkup_patient FOREIGN KEY (patient) REFERENCES patient (pk);
ALTER TABLE checkup_ ADD pk SERIAL PRIMARY KEY;
DROP TABLE checkup;
-- Recreate table with columns rearranged
CREATE TABLE checkup AS (
    SELECT pk, patient, last_name, first_name, dob, exam_date, od, os, va_right, va_left, pd, conj, sclera, tears, cornea, iris, antc, cc, lll
    FROM public.checkup_
);
ALTER TABLE checkup ADD PRIMARY KEY (pk);
DROP TABLE checkup_;

CREATE TABLE glasses_ AS (
    SELECT checkup.patient AS patient, checkup.pk AS prescription, glasses.exam_date, brand, model, color, frame, lens, contact_lens, additional_comments, price -- omitting the 'recorded' column
    FROM public.glasses AS glasses LEFT JOIN public.checkup AS checkup
    ON checkup.last_name = glasses.last_name
    AND checkup.first_name = glasses.first_name
    AND checkup.dob = glasses.dob
);
ALTER TABLE glasses_ ADD CONSTRAINT fk_glasses_checkup FOREIGN KEY (prescription) REFERENCES checkup (pk);
ALTER TABLE glasses_ ADD CONSTRAINT fk_glasses_patient FOREIGN KEY (patient) REFERENCES patient (pk);
ALTER TABLE checkup DROP last_name, DROP first_name, DROP dob;
DROP TABLE glasses;
ALTER TABLE glasses_ RENAME TO glasses;

CREATE TABLE insurance_ AS (
    SELECT patient.pk AS patient, insurance.last_name, insurance.first_name, insurance.dob, insurance_id, insurance_id_2, can_call, called
    FROM public.insurance AS insurance LEFT JOIN public.patient AS patient
    ON patient.last_name = insurance.last_name
    AND patient.first_name = insurance.first_name
    AND patient.dob = insurance.dob
);
ALTER TABLE insurance_ ADD CONSTRAINT fk_insurance_patient FOREIGN KEY (patient) REFERENCES patient (pk);
ALTER TABLE insurance_ ADD pk SERIAL PRIMARY KEY; -- y'know what it's okay if the pk column is at the end
DROP TABLE insurance;
ALTER TABLE insurance_ RENAME TO insurance;

ALTER TABLE checkup RENAME TO glasses_prescription;
ALTER TABLE public.glasses RENAME COLUMN exam_date TO date;