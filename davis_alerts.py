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


def update_customer_selected_prices(
        connection,
        quantity,
        unit_price_after,
        selection_id
):
    try:

        # update
        sql = """ UPDATE customer_selected_items SET unit_price_after = %s, total_price_after = %s where id = %s"""

        total_price_after = unit_price_after * quantity

        print("total_price_after is {}".format(total_price_after))

        val = (unit_price_after, total_price_after, selection_id)

        db.update_db(connection, sql, val)

        return True

    except Exception as e:
        logger.error('update_customer_selected_prices error: {}'.format(str(e)))
        raise

def fetch_customer_selected_items(connection):
    try:
        sql = """ SELECT * FROM customer_selected_items where payment_status != %s AND payment_status != %s and entity_user_id = 1"""
        params = ('Redeemed', 'defaulted')
        items_list = db.retrieve_all_data(connection, sql, params)
        return items_list

    except Exception as e:
        logger.error('fetch_customer_selected_items error: {}'.format(str(e)))
        raise

def check_product_prices(connection):
    try:
        # query products
        selected_list = fetch_customer_selected_items(connection)

        for selected_item in selected_list:
            sql = """ SELECT * FROM davis_products where product_id = %s"""
            params = (selected_item[2],)
            item = db.retrieve_all_data(connection, sql, params)

            # update selected products if prices differ
            for product in item:
                if float(product[10]) != float(selected_item[4]):
                    #update price

                    if selected_item[7] is None or selected_item[7] != float(product[10]):

                        update_customer_selected_prices(
                            connection,
                            quantity=selected_item[5],
                            unit_price_after=product[10],
                            selection_id=selected_item[0]
                        )

                        # notify customer
                        print ("notifies customer")
                        save_to_purchase.send_save_to_purchase_message(
                            phone_number="254718273753",
                            text="This is Notify you that the price of your selected "
                                 "product {} has changed from Ksh. {} to Ksh {}".format(selected_item[3],
                                                                                        selected_item[4],
                                                                                        product[10]
                                                                            )
                        )


        return True

    except Exception as e:
        logger.error('check_product_prices error: {}'.format(str(e)))
        logger.error(e, exc_info=True)
        raise


if __name__ == "__main__":
    session = None
    # while True:
    try:
        if not session:
            session = create_connection()
            print("establishing conncetion")
        fetched_customers = fetch_customer_selected_items(session)

        if len(fetched_customers):
            print("after fetching customers")
            check_product_prices(session)
        # update_sms_records(session)
        session.commit()
        session.close()
        session = None
        # time.sleep(5)
    except Exception as err:
        logger.error('Main error: {}'.format(str(err)))
        logger.error(err, exc_info=True)