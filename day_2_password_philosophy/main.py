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


def apply_rule_part1(rule, password):
    """ Takes in a rule and string and applies that rule to the string to determine if passed or failed. Returns result. """

    min_max_range, character = rule.split(" ")
    min_rate, max_rate = (int(x) for x in min_max_range.split("-"))
    # _logger.debug("Parsed rule of {0}-{1} for {2}".format(min_rate, max_rate, character))

    character_occurrences = 0

    for symbol in password:
        if symbol == character:
            character_occurrences += 1

    return character_occurrences <= max_rate and character_occurrences >= min_rate

def apply_rule_part2(rule, password):
    """ Takes in a rule and string and applies that rule to the string to determine if passed or failed. Returns result. """

    indexes, character = rule.split(" ")
    first_index, second_index = (int(x) - 1 for x in indexes.split("-"))  # subtract 1 because Toboggan Corporate Authority uses 1-based indexing
    
    return (password[first_index] == character) ^ (password[second_index] == character)


if __name__ == "__main__":
    start_time = time.time()

    # Load arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', help='Example input')
    args = parser.parse_args()

    with open(args.input, "r") as input_file_handle:
        total_passwords = 0
        valid_passwords = 0

        start_timestamp = time.time()
        for line in input_file_handle.readlines():
            total_passwords += 1
            rule, password = line.split(": ")


            
            passed = apply_rule_part2(rule, password)
           
            

            if passed:
                valid_passwords += 1

        end_timestamp = time.time()
        _logger.info("apply_rule_part1 took {0:.2f}s".format(end_timestamp-start_timestamp))

        _logger.info("Found {0} valid passwords out of {1}".format(valid_passwords, total_passwords))


    end_time = time.time()
    _logger.info("Script finished in {0:.2f}s".format(end_time-start_time))
