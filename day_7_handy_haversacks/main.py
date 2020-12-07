__doc__ = "Example template script format"

import logging, time, argparse, datetime, os, re

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

# patterns

CONTAINER_PATTERN = re.compile(r"([a-z]*) ([a-z]*) bags contain")
SUB_BAGS_PATTERN = re.compile(r"(\d+) ([a-z]*) ([a-z]*) bag")


def load_rules(rule_file_path):
    """ rules are a dict of dicts like this:
    
            {"bag type": # contains
                {"bag_type": 3, # qty of this bag ...
                }
            }
    """
    
    rules = {}

    with open(rule_file_path, "r") as rule_file:
        
        for line in rule_file.readlines():

            container = CONTAINER_PATTERN.match(line)
            sub_bags = SUB_BAGS_PATTERN.findall(line)

            container_label = " ".join(container.groups())

            if container_label in rules:
                _logger.error("duplicate label in input!")
                return None

            rules[container_label] = {}

            for bag in sub_bags:
                qty = int(bag[0])
                sub_bag_label = "{0} {1}".format(bag[1], bag[2])

                rules[container_label][sub_bag_label] = qty
    
    return rules
            
def part1(rules, search_label, current_label):
    """ Searches rules for a given label and return how many bags contain this label (recursively)"""

    if len(rules[current_label]) == 0:
        return 0

    if search_label in rules[current_label]:
        return 1

    for label in rules[current_label]:
        if part1(rules, search_label, label) == 1:
            return 1
    
    return 0

def part2(rules, current_label):
    """ Counts bags recursively"""

    rtn = 0 

    if len(rules[current_label]) != 0:
        for label in rules[current_label]:
            rtn += (rules[current_label][label] * part2(rules, label))
    
    _logger.debug("{0} contains {1} bags".format(current_label, rtn))

    rtn += 1  # add one bag for itself

    return rtn

if __name__ == "__main__":
    start_time = time.time()

    # Load arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', help='Example input')
    args = parser.parse_args()

    # ----------------- INTRODUCTION: LOAD RULES -------------------------
    start_timestamp = time.time()

    rules = load_rules(args.input)

    end_timestamp = time.time()
    _logger.info("load_rules took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("num rules: {0}".format(len(rules)))

    # ----------------- PART 1 -------------------------
    start_timestamp = time.time()

    running_total = 0
    for label in rules:
        running_total += part1(rules, "shiny gold", label)

    end_timestamp = time.time()
    _logger.info("part1 took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("total bags: {0}".format(running_total))

    # ----------------- PART 2 -------------------------
    start_timestamp = time.time()

    bags_in_shiny_gold = part2(rules, "shiny gold")

    end_timestamp = time.time()
    _logger.info("part2 took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("bags in shiny gold: {0}".format(bags_in_shiny_gold))

    end_time = time.time()
    _logger.info("Script finished in {0:.2f}s".format(end_time-start_time))
