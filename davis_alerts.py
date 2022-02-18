import time

import mysql.connector

from config import logger, mysql_host, mysql_user, mysql_password, mysql_db
from helpers import db, Save_To_Purchase

db = db()
save_to_purchase = Save_To_Purchase()


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            db=mysql_db
        )
        return connection
    except Exception as e:
        logger.error('create_connection error: {}'.format(str(e)))
        raise


def fetch_customer_items(connection):
    try:
        # fetch user recorsd

        sql = """ SELECT * FROM customer_selected_items where payment_status = %s AND percentage_paid >= %s"""
        params = ('Partially_Paid', 0.75)
        items_list = db.retrieve_all_data(connection, sql, params)
        return items_list

    except Exception as e:
        logger.error('fetch_records error: {}'.format(str(e)))
        raise

