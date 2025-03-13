-- "Steve".invoice definition

-- Drop table

-- DROP TABLE "Steve".invoice;

CREATE TABLE "Steve".invoice (
	numerofact varchar(14) NOT NULL,
	creationdate timestamp NULL,
	CONSTRAINT invoice_pk PRIMARY KEY (numerofact)
);