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
    config = parse_conf()
    venmo_requestor = VenmoRequestor(config)

    while True:
        new_transactions = venmo_requestor.get_new_transactions()

        for transaction in new_transactions:
            if venmo_requestor.check_transaction_in_db(transaction):
                print(transaction)
                venmo_requestor.insert_transaction(transaction)

        print()
        sleep(config["REQUEST_TIMER"])

    venmo_requestor.close()

if __name__ == "__main__":
    main()
