-- uuid generates a unique identifier that is not sequential and is 128 bits long
-- good choice when you need to generate unique identifiers across multiple databases or systems
-- serial generates a unique integer value for each row added to a table.
-- a simple, sequential, and unique identifier for your rows
-- VARCHAR(MAX_LEN), MAX_LEN higher than max lenght of the value
-- e.g. name max len is 254, varchar(255)
-- NOT NULL: result in constrain validation error
-- ERROR: null value in column "name" violates not-null constraint
-- ALTER CONSTRAIN:
-- ALTER TABLE members ALTER COLUMN name DROP NOT NULL;
-- primary and foreign key is automatically indexed by default
-- CREATE DATABASE ecommerce;
CREATE TABLE members (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  mobile_no NUMERIC(8) Not NULL,
  address TEXT NULL
);

CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  manufacturer_name VARCHAR(255) NOT NULL,
  cost DECIMAL(10, 2) NOT NULL,
  weight_kg DECIMAL(10, 2) NOT NULL
);

-- REFERENCES, foreign key
CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  member_id INTEGER REFERENCES members(id) NOT NULL,
  item_id INTEGER REFERENCES items(id) NOT NULL,
  quantity INTEGER NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  weight_kg DECIMAL(10, 2) NOT NULL
);


-- [table_name]_[column_name]_seq is a system-generated sequence object that is created automatically when you define a column with the SERIAL data type.
-- ensure that each row in the table has a unique id value.