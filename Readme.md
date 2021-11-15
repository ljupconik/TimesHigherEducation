```buildoutcfg
sudo docker build -t pg_image .
sudo docker run -p 5432:5432 --name pg_container -d pg_image
```

Once the docker Postgres contaier is up and running connect to it with any DB UI like Pgadmin4.
Then first create the database "education"
```
CREATE DATABASE education
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
```

Then inside of the database "education" create the 2 tables :
```buildoutcfg
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
```

Or alternatively if you have an existing running Postgres database , just alter the parameters of :
```buildoutcfg
conn = jdbc.connect("org.postgresql.Driver", "jdbc:postgresql://localhost:5432/education" , ['postgres', ''], jars="driver/postgresql-42.2.5.jar")
```