__doc__ = "Day 1 challenge for 2020: https://adventofcode.com/2020/day/1"

import logging, time, argparse, math

logging.basicConfig(format="%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s")
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

def lazy_search(vals, expected_sum):
    """ Does a lazy double loop of a set of integers, finds a pair of integers that adds to expected sum and returns the product."""

    for i, first_val in enumerate(vals):

        for second_val in vals[0:i] + vals[i+1:]:  # don't iterate over the current first val
            if second_val + first_val == expected_sum:
                _logger.info("Found match first val {0} second val {1}".format(first_val, second_val))
                return second_val * first_val
    
    _logger.info("Didn't find a match that satisfied sum!")
    
    return None

def arbitrary_search(vals, expected_sum, combination_length):
    """ Does an optimized search of a set of integers and tries to find an arbitrarily sized set of integers that add up to the expected sum."""

    combinations = recursive_search(vals, [], combination_length)

    for combination in combinations:
        if sum(combination) == expected_sum:
            _logger.info("Found match")
            for i, val in enumerate(combination):
                _logger.info("{0}: {1}".format(i, val))
            return math.prod(combination)
    
    _logger.info("Didn't find a match that satisfied sum!")
    
    return None


def recursive_search(vals, current_combination, combination_length):
    """ Recursively peels values out of vals and reduces sum count to return all unique combinations."""

    #_logger.debug("len vals {0}".format(len(vals)))
    #_logger.debug("len current combination {0}".format(len(current_combination)))

    rtn = []

    additional_vals_needed = combination_length - len(current_combination) 

    if len(vals) < additional_vals_needed:
        # If there aren't enough values left to build a new set to sum, this is a dead branch of the tree
        return rtn  # return an empty list, there are no potential sets down this branch
    else:
        # If there's only one more value needed in this combination, build and return the list.

        if additional_vals_needed == 1:
            for val in vals:
                combination = list(current_combination)  # Copy current list
                combination.append(val)
                rtn.append(combination)
            
        else:
            for i, val in enumerate(vals):  # more than 1 remaining, recurse
                combination = list(current_combination)  # Copy current list
                combination.append(val)
                rtn += recursive_search(vals[0:i] + vals[i+1:], combination, combination_length)
            
        return rtn
            

if __name__ == "__main__":
    start_time = time.time()

    # Load arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', help='')
    parser.add_argument('-v', '--value', help='')
    
    args = parser.parse_args()

    with open(args.input, "r") as input_file_handle:

        vals = []

        for line in input_file_handle.readlines():
            vals.append(int(line))
        
        result = lazy_search(vals, int(args.value))

        if result is None:
            raise ValueError("Failed to find match!")
        else:
            _logger.info("Part 1 - Found answer: {0}".format(result))

        result = arbitrary_search(vals, int(args.value), 3)

        if result is None:
            raise ValueError("Failed to find match!")
        else:
            _logger.info("Part 2 - Found answer: {0}".format(result))


    end_time = time.time()
    _logger.info("Script finished in {0:.2f}s".format(end_time-start_time))