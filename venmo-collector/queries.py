# Insert query to the database with available formating
INSERT_QUERY = """
INSERT INTO transactions (
    payment_id,
    target_username,
    target_firstname,
    target_lastname,
    target_date_created,
    author_username,
    author_firstname,
    author_lastname,
    author_date_created,
    story_id,
    updated_time
)
VALUES (
	'{}',
	'{}',
	'{}',
	'{}',
	'{}',
	'{}',
	'{}',
	'{}',
	'{}',
	'{}',
	'{}'
);
"""

# Query to check for a transaction duplicate
CHECK_QUERY = """
SELECT * FROM transactions WHERE {column} = '{value}';
"""