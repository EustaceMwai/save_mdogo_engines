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
            cursor = db_connection.cursor(dictionary=True)
            cursor.execute(sql, params)
        except mysql.connector.Error as e:
            logger.error(e)
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




