
import logging

logger = logging.getLogger("SAVE_TO_PURCHASE_ENGINE")
logger.setLevel(logging.INFO)
hdlr = logging.FileHandler("save_to_purchase_engine.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s ')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)


mysql_host = "197.248.4.162"
mysql_user = "nilipie"
mysql_password = "ejX9bq!+WAuV2UK*"
mysql_db = "save_to_purchase"