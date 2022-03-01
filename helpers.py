import json

import mysql.connector
import requests

from config import logger


class db:
    def retrieve_all_data(self, db_connection, sql, params):
        results = None
        try:
            cursor = db_connection.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()
        except mysql.connector.Error as e:
            logger.error("retrieve_all_data error {}".format(e))
            logger.error(e, exc_info=True)
            raise
        return results

    def update_db(self, db_connection, sql, params):
        results = None
        try:
            print(sql)
            print(params)
            cursor = db_connection.cursor()
            cursor.execute(sql, params)
            print("has successfully update items")
        except mysql.connector.Error as e:
            logger.error(e)
            logger.error(e, exc_info=True)
            raise
        return results


class Save_To_Purchase:

    def update_products(self, ):

        try:
            pass

        except Exception as e:
            pass

    @staticmethod
    def get_products_for_db(category_id):
        try:
            logger.info("get_products_for_db request {}".format(category_id))
            # headers = {'User-Agent': 'Mozilla/5.0'}
            endpoint = "https://www.davisandshirtliff.com/shop/index.php?route=product/category/getcategoryproducts"

            session = requests.Session()

            payload = {'category_id': category_id}
            params = {'route': "product/category/getcategoryproducts"}

            response_data = session.post(
                endpoint, params=params,
                data=payload)

            logger.info("response is {}".format(response_data.text))

            products = response_data.json()

            return products

        except Exception as e:
            logger.error("get_products error {}".format(e))
            logger.error(e, exc_info=True)
            raise

    @staticmethod
    def send_save_to_purchase_message(phone_number, text):
        url = "https://api.onfonmedia.co.ke/v1/sms/SendBulkSMS"

        payload = {
            "SenderId": "OnfonInfo",
            "MessageParameters": [
                {
                    "Number": phone_number,
                    "Text": text,
                }
            ],
            "ApiKey": "80oGEibQEFzf37KcXRqKt36jtg2K7WgaGlZgc/sCxIQ=",
            "ClientId": "811a6c43-7f28-4c27-8fc6-f1b5c54d3a3e"
        }

        headers = {
            'Content-Type': "application/json",
            'AccessKey': "SW9ibWmBMNzJ6r4oZRr5GgyvhGpxkAnY",
        }
        # logging.info(json.dumps(payload))
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=True)

        return response




