import os
import json
from time import sleep

from venmorequestor import VenmoRequestor

# Function to parse a .json cofig file into a dictionary
def parse_conf():
    conf_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
    with open(conf_path, 'r+') as fn:
        conf = json.loads(fn.read())

    return conf

# Main function    
def main(): 
    venmo_requestor = VenmoRequestor(parse_conf())

    while True:
        new_transactions = venmo_requestor.get_new_transactions()
        print(new_transactions)

        for transaction in new_transactions:
            if venmo_requestor.check_transaction_in_db(transaction):
                venmo_requestor.insert_transaction(transaction)

        sleep(60)

    venmo_requestor.close()

if __name__ == "__main__":
    main()
