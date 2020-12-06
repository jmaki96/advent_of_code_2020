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


def part1(input_file_path):

    with open(input_file_path, "r") as input_file:
        responses = []
        response = set()
        for line in input_file.readlines():
            line = line.strip()  # remove newline characters etc...

            if line == "":
                # this is a new group
                responses.append(response)

                # _logger.debug("response from group {0}: {1}".format(len(responses), response))

                response = set()
            else:
                for character in line:
                    response.add(character)
        else:
            responses.append(response)

    return responses

def part2(input_file_path):

    with open(input_file_path, "r") as input_file:
        responses = []

        group_response = None
        response = set()
        for line in input_file.readlines():
            line = line.strip()  # remove newline characters etc...

            if line == "":
                # this is a new group
                responses.append(group_response)

                # _logger.debug("response from group {0}: {1}".format(len(responses), group_response))

                group_response = None
                
            else:
                for character in line:
                    response.add(character)

                if group_response is None:
                    group_response = response
                else:
                    group_response.intersection_update(response)

                response = set()
        else:
            responses.append(group_response)

    return responses

if __name__ == "__main__":
    start_time = time.time()

    # Load arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', help='Example input')
    args = parser.parse_args()

    # ----------------- PART 1 -------------------------
    start_timestamp = time.time()

    responses = part1(args.input)

    sum_count = sum([len(response) for response in responses])

    end_timestamp = time.time()
    _logger.info("part1 took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("responses: {0}".format(sum_count))

    # ----------------- PART 1 -------------------------
    start_timestamp = time.time()

    responses = part2(args.input)

    sum_count = sum([len(response) for response in responses])

    end_timestamp = time.time()
    _logger.info("part2 took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("responses: {0}".format(sum_count))

    end_time = time.time()
    _logger.info("Script finished in {0:.2f}s".format(end_time-start_time))
