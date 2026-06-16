# Repository.py

import json
import constants


# ---------- Verification Database ----------

def load_verification_db():
    
    try:
        with open(constants.VERIFICATION_DB, "r+") as file: 
            content = file.read().strip()
    except (FileNotFoundError, FileExistsError):
        with open(constants.VERIFICATION_DB, "w+") as file:
            content = file.read().strip()

    if content == "":
        verification_database = {}
    else:
        verification_database = json.loads(content)

    return verification_database


def save_verification_db(verification_database):
    with open(constants.VERIFICATION_DB, "w") as file:
        json.dump(verification_database, file, indent=2)



