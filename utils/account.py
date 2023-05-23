import json
import env
import requests
import data_storage.models as models

from utils import logger
from utils.utils import DbAccess


class Account:
    @staticmethod
    def login():
        return ""
        logger.info("Auth: Logging in...")
        email=env.email
        password=env.password
        accountModel = models.Account()
        db = DbAccess()
        account_exists = False
        logger.info("Checking user account ...")
        account = db.select("accounts",[],{'email':email,"password":password})
        if account :
            logger.info("Account already exists")
            if account[0]['auth_token']:
                logger.info("Auth tokem already exists")
                return account[0]['auth_token']
            account_exists = True
        
        logger.info("Making API call to get auth token ")
        url = env.api_base_url + "/client/auth/login"
        # print(url)
        # return
        data = {
            "email": email,
            "password": password
        }
        logger.info("Initiating POST request")
        req = requests.post(url, json=data, headers={
                            "X-Requested-With": "XMLHttpRequest"})
        logger.info("Request sent!")
        data = json.loads(req.content.decode())
        logger.info("Response data")
        logger.info(data)
        response = data['response']
        message = data['message']
        if response != "success":
           logger.error(f"Failed to login: MSG {message}")
           return False 
       
        # user = data['user']
        # name = user['name']
        # # email = user['email']
        # phone_number = user['phone_number']
        # is_suspended = user["is_suspended"]
        # baby_id = user["baby_id"]
        # # baby = user['baby']
        # baby_name = baby["name"]
        # baby_dob = baby["dob"]
        # baby_gender = baby["gender"]
        # baby_weight =baby["weight"]
        # baby_length = baby["length"]
        # baby_medical_conditions = baby["medical_conditions"]
        
        logger.info("Getting auth token from data")
        auth_token = data["authToken"]
        logger.info("Saving user credentials ")
        if account_exists :
            db.update("accounts",{"auth_token":auth_token,"is_active":1},{"email":email})
        else:
            accountModel.create({"email":email,"password":password, "is_active":1,"auth_token":auth_token})
        
        logger.info("Credentials saved")
        return auth_token

    @staticmethod
    def logout():
        pass

    @staticmethod
    def get_auth_token():
        db = DbAccess()
        accounts = db.select("accounts",[],{"is_active":1})
        if accounts :
            account = accounts[0]
            return account['auth_token']
        return Account.login()