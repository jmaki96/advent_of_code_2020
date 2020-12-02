__doc__ = "Example template script format"

import logging, time, argparse, datetime, os

log_format = "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

datestamp = datetime.datetime.now().strftime("%m%d%Y_%H%M%S")

# file logging
file_logging = True
log_directory = ".\\logs"
if file_logging:
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)
    
    debug_log_handler = logging.FileHandler(os.path.join(log_directory, "debug_{0}.log".format(datestamp)))
    debug_log_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(log_format)
    debug_log_handler.setFormatter(formatter)
    _logger.addHandler(debug_log_handler)


if __name__ == "__main__":
    start_time = time.time()

    # Load arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', help='Example input')
    args = parser.parse_args()

    end_time = time.time()
    _logger.info("Script finished in {0:.2f}s".format(end_time-start_time))
