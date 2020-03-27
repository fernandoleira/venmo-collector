CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    payment_id character varying(255),
    target_username character varying(255),
    target_firstname character varying(255),
    target_lastname character varying(255),
    target_date_created date,
    author_username character varying(255),
    author_firstname character varying(255),
    author_lastname character varying(255),
    author_date_created date,
    story_id character varying(255),
    updated_time date
);

