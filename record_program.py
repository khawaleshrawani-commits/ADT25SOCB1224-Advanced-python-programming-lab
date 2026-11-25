
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Program execution
logging.debug("Program started")
logging.info("Application is running")

try:
    a = 10
    b = 0
    result = a / b

except ZeroDivisionError:
    logging.exception("Error occurred: Division by zero")

logging.warning("Program completed with warning")
logging.critical("Application ended")
