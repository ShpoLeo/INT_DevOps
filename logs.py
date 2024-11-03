import logging
import sys
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s:%(filename)s:%(lineno)d,%(funcName)s - %(message)s',
                    handlers=[logging.FileHandler("system_info.log"),
                              logging.StreamHandler()])

logger = logging.getLogger(__file__)