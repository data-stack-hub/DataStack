

# importing module
import logging

# Create and configure logger
logging.basicConfig(format='%(asctime)s %(levelname) -7s " "%(name)s: %(message)s')

# Creating an object
logger = logging.getLogger('ds')

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
