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


def parse_passports(batch_file_path):
    """ Takes a file path, opens it, and parses it into a list of dictionaries (passports)"""

    with open(batch_file_path, "r") as batch_file:

        passports = []
        passport = {}

        for line in batch_file.readlines():

            if line.strip() == "":
                # end of current passport
                passports.append(passport)
                passport = {}
            else:
                key_value_pairs = [x.strip() for x in line.split(" ") if x.strip() != ""]

                for key_value_pair in key_value_pairs:
                    #_logger.debug("kvp {0}".format(key_value_pair))
                    key, value = key_value_pair.split(":")
                    passport[key] = value

    return passports


def apply_part1_rule(passports, required_keys):

    valid_passports = 0

    for passport in passports:
        for key in required_keys:
            if not key in passport:
                break
        else:
            valid_passports += 1

    return valid_passports


# part 2 helpers

def _check_year(value, min_year, max_year):

    if len(value) != 4:
        return False

    try:
        int_value = int(value)
    except ValueError as e:
        return False
    
    return int_value <= max_year and int_value >= min_year

def _check_height(value):

    # expect the last two characters to be units
    units = value[-2:]

    if units == "cm":
        min_val = 150
        max_val = 193
    elif units == "in":
        min_val = 59
        max_val = 76
    else:
        return False

    try:
        int_value = int(value[:-2])
    except ValueError as e:
        return False
    
    return int_value <= max_val and int_value >= min_val 

def _check_hair_color(value):

    if len(value) != 7:
        return False

    if value[0] != "#":
        return False
    
    return value[1:].isalnum()

def _check_eye_color(value):
    valid_colors = {"brn", "amb", "blu", "gry", "hzl", "grn", "oth"}

    return value in valid_colors

def _check_pid(value):

    if len(value) != 9:
        return False
    
    return value.isnumeric()

def apply_part2_rule(passports, required_keys):

    valid_passports = 0

    for passport in passports:
        for key in required_keys:
            if not key in passport:
                break
            else:
                value = passport[key]
                # Validate data
                if key == "byr":
                    if not _check_year(value, 1920, 2002):
                        _logger.debug("{0} failed validation with {1}".format(key, value))
                        break
                elif key == "iyr":
                    if not _check_year(value, 2010, 2020):
                        _logger.debug("{0} failed validation with {1}".format(key, value))
                        break
                elif key == "eyr":
                    if not _check_year(value, 2020, 2030):
                        _logger.debug("{0} failed validation with {1}".format(key, value))
                        break
                elif key == "hgt":
                    if not _check_height(value):
                        _logger.debug("{0} failed validation with {1}".format(key, value))
                        break
                elif key == "hcl":
                    if not _check_hair_color(value):
                        _logger.debug("{0} failed validation with {1}".format(key, value))
                        break
                elif key == "ecl":
                    if not _check_eye_color(value):
                        _logger.debug("{0} failed validation with {1}".format(key, value))
                        break
                elif key == "pid":
                    if not _check_pid(value):
                        _logger.debug("{0} failed validation with {1}".format(key, value))
                        break
                
        else:
            valid_passports += 1

    return valid_passports


if __name__ == "__main__":
    start_time = time.time()

    # Load arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', help='Example input')
    args = parser.parse_args()

    # ----------------- INTRODUCTION: PARSE PASSPORTS -------------------------
    start_timestamp = time.time()

    passports = parse_passports(args.input)

    end_timestamp = time.time()
    _logger.info("parse_passports took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("num passports: {0}".format(len(passports)))


    # ----------------- PART 1 -------------------------
    start_timestamp = time.time()

    valid_passports = apply_part1_rule(passports, ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])

    end_timestamp = time.time()
    _logger.info("apply_part1_rule took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("valid_passports: {0}".format(valid_passports))

    # ----------------- PART 2 -------------------------
    start_timestamp = time.time()

    valid_passports = apply_part2_rule(passports, ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])

    end_timestamp = time.time()
    _logger.info("apply_part2_rule took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("valid_passports: {0}".format(valid_passports))


    end_time = time.time()
    _logger.info("Script finished in {0:.2f}s".format(end_time-start_time))
