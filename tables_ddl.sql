CREATE DATABASE education
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE TABLE institution(
	id text PRIMARY KEY,
	name text NOT NULL,
	city text NOT NULL
);

CREATE TABLE submission(
	submission_id text ,
	institution_id text NOT NULL,
	year smallint NOT NULL,
	staff_total smallint NOT NULL,
	subject_name text  NOT NULL,
	academic_papers smallint NOT NULL,
	students_total smallint NOT NULL,
	student_rating double precision NOT NULL,
	PRIMARY KEY (submission_id , subject_name),
	CONSTRAINT fk_institution_id FOREIGN KEY (institution_id) REFERENCES institution(id)
);