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

def binary_search(direction, min_val, max_val):
    """ tbd"""

    if len(direction) == 0:
        if min_val != max_val:
            _logger.error("Did not resolve to a single value! min {0} max {1}".format(min_val, max_val))
        else:
            #_logger.debug("min {0} = max {1}".format(min_val, max_val))
            return min_val
    else:
        if direction[0] == "F" or direction[0] == "L":   # lower half
            mid_point = int((max_val - min_val - 1) / 2) + min_val
            #_logger.debug("down - max {0} mid {1} min {2}".format(max_val, mid_point, min_val))
            return binary_search(direction[1:], min_val, mid_point)

        elif direction[0] == "B" or direction[0] == "R":
            mid_point = int((max_val - min_val + 1) / 2) + min_val
            #_logger.debug("up - max {0} mid {1} min {2}".format(max_val, mid_point, min_val))
            return binary_search(direction[1:], mid_point, max_val)

def part1(boarding_pass_path):

    with open(boarding_pass_path, "r") as boarding_passes:

        max_seat_id = 0

        for line in boarding_passes.readlines():
            row_direction = line[0:7]
            col_direction = line[7:10]

            row = binary_search(row_direction, min_row, max_row)
            #_logger.debug("found row {0}".format(row))

            col = binary_search(col_direction, min_col, max_col)
            #_logger.debug("found col {0}".format(col))

            seat_id = (row * 8) + col 

            if seat_id > max_seat_id:
                max_seat_id = seat_id
    
    return max_seat_id

def part2(boarding_pass_path):

    with open(boarding_pass_path, "r") as boarding_passes:

        seat_ids = []

        for line in boarding_passes.readlines():
            row_direction = line[0:7]
            col_direction = line[7:10]

            row = binary_search(row_direction, min_row, max_row)
            #_logger.debug("found row {0}".format(row))

            col = binary_search(col_direction, min_col, max_col)
            #_logger.debug("found col {0}".format(col))

            seat_id = (row * 8) + col 

            seat_ids.append(seat_id)
    
    # found all the seat_ids on the plane, so now sort and iterate until there's a missing one
    sorted_seat_ids = sorted(seat_ids)
    _logger.debug(sorted_seat_ids)
    prev_id = -1

    for seat_id in sorted_seat_ids:
        if prev_id == -1:
            prev_id = seat_id
        else:
            if seat_id != prev_id + 1:
                return seat_id - 1
            else:
                prev_id = seat_id
    

if __name__ == "__main__":
    start_time = time.time()

    # Load arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', help='Example input')
    args = parser.parse_args()

    # plane constants
    max_row = 127
    min_row = 0

    max_col = 7
    min_col = 0

    # ----------------- PART 1 -------------------------
    start_timestamp = time.time()

    max_seat_id = part1(args.input)

    end_timestamp = time.time()
    _logger.info("part1 took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("max_seat_id: {0}".format(max_seat_id))

    # ----------------- PART 2 -------------------------
    start_timestamp = time.time()

    your_seat_id = part2(args.input)

    end_timestamp = time.time()
    _logger.info("part2 took {0:.2f}s".format(end_timestamp-start_timestamp))
    _logger.info("your_seat_id: {0}".format(your_seat_id))

    end_time = time.time()
    _logger.info("Script finished in {0:.2f}s".format(end_time-start_time))
