-- steve.clients definition

-- Drop table

-- DROP TABLE steve.clients;

CREATE TABLE steve.clients (
	nom varchar(50) NULL,
	mail varchar(50) NOT NULL,
	datedenaissance date NULL,
	sexe varchar(1) NULL,
	adresse varchar(200) NULL,
	CONSTRAINT clients_pk PRIMARY KEY (mail)
);


-- steve.factures definition

-- Drop table

-- DROP TABLE steve.factures;

CREATE TABLE steve.factures (
	numerofact varchar(14) NOT NULL,
	creationdate timestamp NULL,
	total float8 NULL,
	mail varchar(50) NULL,
	CONSTRAINT factures_pk PRIMARY KEY (numerofact),
	CONSTRAINT factures_clients_fk FOREIGN KEY (mail) REFERENCES steve.clients(mail)
);