__doc__ = "Example template script format"

import logging, time, argparse

logging.basicConfig(format="%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s")
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


if __name__ == "__main__":
    start_time = time.time()

    # Load arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', help='Example input')
    args = parser.parse_args()

    end_time = time.time()
    _logger.info("Script finished in {0:.2f}s".format(end_time-start_time))
