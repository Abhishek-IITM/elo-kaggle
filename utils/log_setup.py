import logging
import datetime as dt
from config import path
logging.basicConfig(format='%(asctime)s,%(msecs)d [%(filename)s:%(lineno)d] %(levelname)-8s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO,
                    handlers=[
                        logging.FileHandler("{}/{}_{}.log".format(path.log_path, "log_file",
                                               dt.datetime.strftime(dt.datetime.now().date(), "%Y_%m_%d"))),
                        logging.StreamHandler()
                    ])
_log = logging.getLogger()