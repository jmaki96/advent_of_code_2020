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


def part_1(input_file_name, x_step, y_step):

    next_x = 0
    next_y = 0
    trees = 0

    with open(input_file_name, "r") as input_file:

        for y, line in enumerate(input_file.readlines()):
            # each line is increasing y, x across

            # if next_x is greater than length of the line it wraps around
            # for example, if it is 15 across, a next_x 14 == 14, next_x 15 == 0
            clean_line = line.strip()
            
            # check if we're at the right y
            if next_y == y:
                # check this point

                if clean_line[next_x] == "#":
                    trees += 1
                    clean_line = clean_line[:next_x] + "X" + clean_line[next_x+1:]
                else:
                    clean_line = clean_line[:next_x] + "O" + clean_line[next_x+1:]

                # increment to next point
                next_x += x_step
                next_y += y_step

                if next_x >= len(clean_line):
                    next_x -= len(clean_line)
        
            #_logger.debug(clean_line)

    return trees



if __name__ == "__main__":
    start_time = time.time()

    # Load arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', help='Example input')
    args = parser.parse_args()

    # ----------------- PART 1 -------------------------
    start_timestamp = time.time()

    trees = part_1(args.input, 3, 1)

    end_timestamp = time.time()
    _logger.info("part_1 took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("trees: {0}".format(trees))


    # ----------------- PART 2 -------------------------
    start_timestamp = time.time()

    tree_product = part_1(args.input, 1, 1)
    tree_product *= part_1(args.input, 3, 1)
    tree_product *= part_1(args.input, 5, 1)
    tree_product *= part_1(args.input, 7, 1)
    tree_product *= part_1(args.input, 1, 2)

    end_timestamp = time.time()
    _logger.info("part_2 took {0:.2f}s".format(end_timestamp-start_timestamp))

    _logger.info("tree_product: {0}".format(tree_product))

    end_time = time.time()
    _logger.info("Script finished in {0:.2f}s".format(end_time-start_time))
