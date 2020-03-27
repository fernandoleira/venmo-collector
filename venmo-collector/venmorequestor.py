import json
import requests
import psycopg2

from queries import INSERT_QUERY, CHECK_QUERY

class VenmoRequestor:
    def __init__(self, conf):
        self._conf = conf

        self.conn = self._init_db_connection()
        self.cur = self.conn.cursor()

    def _init_db_connection(self):
        print("Connecting to database...")
        try:
            connection = psycopg2.connect(**self._conf["DB_CREDENTIALS"])
            print("Connected to database!")
            return connection
        except Exception as err:
            print('===== Cannot connect to the DB =====')
            print(err)
            exit()

    def close(self):
        self.cur.close()
        self.conn.close()

    def get_raw_transactions(self):
        req = requests.get(self._conf["URL"])
        res = req.text.replace("'", "\'")
        res = req.text.replace('"', "\"")

        # Parse to remove string
        parse = res.split('"')
        for i in range(len(parse)):
            if parse[i] == 'message':
                parse[i+2] = ""

        res = '"'.join(parse)
        raw_transactions = json.loads(res)["data"]

        return raw_transactions
    
    def parse_raw_transactions(self, raw_transaction):
        target_dict = dict(raw_transaction['transactions'][0]['target'])
        new_transaction = {
            'payment_id': str(raw_transaction['payment_id']),
            'target_username': target_dict['username'],
            'target_firstname': target_dict['firstname'],
            'target_lastname': target_dict['lastname'],
            'target_date_created': target_dict['date_created'],
            'author_username': raw_transaction['actor']['username'],
            'author_firstname': raw_transaction['actor']['firstname'],
            'author_lastname': raw_transaction['actor']['lastname'],
            'author_date_created': raw_transaction['actor']['date_created'],
            'story_id': raw_transaction['story_id'],
            'updated_time': raw_transaction['updated_time'],
        }

        return new_transaction

    def get_new_transactions(self):
        new_transactions = list()
        raw_transactions = self.get_raw_transactions()

        for raw_transaction in raw_transactions:
            new_transaction = self.parse_raw_transactions(raw_transaction)
            new_transactions.append(new_transaction)

        return new_transactions
    
    def check_transaction_in_db(self, transaction):

        if '' in transaction.values():
            return False

        check_query = CHECK_QUERY.format(
            column='payment_id', 
            value=transaction['payment_id']
        )

        self.cur.execute(check_query)
        check = self.cur.fetchone()

        return not check

    def insert_transaction(self, transaction):
        transaction_query = INSERT_QUERY.format(
            transaction['payment_id'],
            transaction['target_username'],
            transaction['target_firstname'],
            transaction['target_lastname'],
            transaction['target_date_created'],
            transaction['author_username'],
            transaction['author_firstname'],
            transaction['author_lastname'],
            transaction['author_date_created'],
            transaction['story_id'],
            transaction['updated_time']
        )

        try:
            ex = self.cur.execute(transaction_query)
            self.conn.commit()
            return 1

        except Exception as err:
            print(err)
            return 0
