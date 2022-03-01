import time

import MySQLdb
import mysql.connector

from config import logger, mysql_host, mysql_user, mysql_password, mysql_db
from helpers import db, Save_To_Purchase

db = db()
save_to_purchase = Save_To_Purchase()


def create_connection():
    try:
        connection = MySQLdb.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            db=mysql_db
        )
        return connection
    except Exception as e:
        logger.error('create_connection error: {}'.format(str(e)))
        raise


def fetch_records(connection):
    try:
        # fetch user recorsd

        sql = """ SELECT * FROM davis_sub_categories where active_status = %s"""
        params = ('active',)
        category_list = db.retrieve_all_data(connection, sql, params)
        return category_list

    except Exception as e:
        logger.error('fetch_records error: {}'.format(str(e)))
        logger.error(e, exc_info=True)
        raise


def get_davis_products(connection):
    try:
        category_list = fetch_records(connection)

        if not category_list:
            return True

        for category in category_list:

            products_response = save_to_purchase.get_products_for_db(category[2])

            if len(products_response):
                for x in products_response:

                    if x['controller']['quantity'] > 0:
                        product_status = "in_stock"
                    else:
                        product_status = "sold_out"

                    # update query
                    print(x['product_id'])

                    sql = """ UPDATE davis_products SET 
                   image = %s,
                   name = %s,
                   price = %s,
                   currency = %s,
                   amount = %s,
                   sku = %s,
                   price2 = %s,
                   price_noformat = %s,
                   quantity = %s,
                   image2 = %s,
                   currency2 = %s,
                   special = %s,
                   special_noformat = %s,
                   special_discount = %s,
                   active_status = %s,
                   product_status = %s
                   where product_id = %s"""

                    val = (
                        x['image'], x['name'], x['price'], x['currency'], x['amount'], x['sku'],
                        x['controller']['price'], float(x['controller']['price_noformat']),
                        x['controller']['quantity'], x['controller']['image'],
                        x['controller']['currency'], x['controller']['special'],
                        x['controller']['special_noformat'],
                        x['controller']['special_discount'],
                        "active",
                        product_status,
                        x['product_id']
                    )
                    print("updating products")

                    db.update_db(connection, sql, val)
        return True

    except Exception as e:
        logger.error('get_davis_products error: {}'.format(str(e)))
        raise


# def update_sms_records(connection):
#     try:
#
#         # update
#
#         sql = """ UPDATE previous_nilipie_users SET status = %s where status = %s"""
#
#         val = ("active", "inactive")
#
#         db.update_db(connection, sql, val)
#
#         return True
#
#     except Exception as e:
#         logger.error('update_sms_records error: {}'.format(str(e)))
#         raise


if __name__ == "__main__":
    session = None
    # while True:
    try:
        if not session:
            session = create_connection()
            print("establishing conncetion")
        deposit_list = fetch_records(session)

        print("after fetch_records {}".format(len(deposit_list)))
        get_davis_products(session)
        # update_sms_records(session)
        # session.commit()
        session.close()
        session = None
        # time.sleep(5)
    except Exception as err:
        logger.error('Main error: {}'.format(str(err)))
        logger.error(err, exc_info=True)
        # if session:
        #     session.rollback()
