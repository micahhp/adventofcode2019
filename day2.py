# Import packages
import os
import itertools


# Define functions
def read_input(filename):
    """
    Takes a file, opens and reads it, and turns contents into a list of integers
    :param filename: name of file containing data to read
    :return: list of integers read out of the file
    """
    # Define path to filename
    dir_path = os.getcwd()
    data_path = os.path.join(dir_path, "data", filename)
    # Open file and read to lines
    with open(data_path) as f:
        texty = f.readlines()
    # Convert each value in lines to integer
    items = texty[0].split(",")
    input_data = [int(item) for item in items]
    # return the list of integers read from the file
    return input_data


def run_program(program_values, target_pos, noun, verb):
    """
    Takes a list of integers that make-up 'memory' or collection of commands. It changes
    the values of the pos-1 and pos-2 commands to the noun and verb, respectively. Then
    it runs until the stop condition is met and reports the value stored in memory at the
    target position (target_pos)
    :param program_values: list of integers that make-up commands, aka 'memory'
    :param target_pos: the 0-based index of the target position to find the value of interest
    :param noun: replacement value of element at pos-1
    :param verb: replacement value of element at pos-2
    :return: the value in memory at the target position, usually position-0
    """
    # Overwrite memory with noun, verb values at pos-1, pos-2, respectively
    program_values[1] = noun
    program_values[2] = verb
    # Initialize flag, start position for looping
    flag = "go"
    intcode_start = 0
    # While the flag isn't 'stop', loop through the groups of Intcodes & follow instructions
    while flag != "stop":
        # Slice input_data into Intcode of focus for this loop, from (start pos.) to (start + 4)
        intcode = program_values[intcode_start:intcode_start + 4]
        # print(len(intcode))
        # Test first position for 99 (stop), 1 (add), or 2 (multiply)
        if (intcode[0] == 99) | (len(intcode) < 4):  # Stop the program
            flag = "stop"
        elif intcode[0] == 1:  # Add pos-1 to pos-2 & store at pos-3
            program_values[intcode[3]] = program_values[intcode[1]] + program_values[intcode[2]]
        elif intcode[0] == 2:  # Multiply pos-1 & pos-2 & store at pos-3
            program_values[intcode[3]] = program_values[intcode[1]] * program_values[intcode[2]]
        # Increment start pos by 4 to go to next set of Intcode instructions
        intcode_start += 4
        # Check position of intcode_start to ensure it's within the list of integers; if not, break loop
        if intcode_start > len(program_values):
            break
    # Return the value in memory at the target position, usually 0th item
    return program_values[target_pos]


def intcode_program(filename, target_pos, noun=0, verb=0, stop_value=0):
    """
    Takes the input data stored at filename, and processes it as an Intcode Program until the
    stop condition is met after changing the pos-1 and pos-2 values to the value of noun and verb,
    respectively. Returns the value stored in memory at the target position (usually position-0) after
    the stop condition has been met and the Intcode Program is finished running
    :param filename: name of file holding the input data stored in the 'data' directory
    :param target_pos: 0-based index of the memory of utmost interest
    :param noun: replacement value of item at pos-1 in memory
    :param verb: replacement value of item at pos-2 in memory
    :param stop_value: value of memory at target position after Intcode Program completes that satisfies condition
    :return: mix of print statements depending on the type of problem.  If (noun, verb) are defined, it returns
    the value stored in memory at the target position after the Program has finished. If (noun, verb) are not
    defined, it will return the values of (noun, verb) that achieve the desired stop_value at the target position
    of the memory upon completion of the Intcode Program.
    """
    # Determine the case: either (noun, verb) are fixed or variable
    if (noun > 0) & (verb > 0):  # Fixed values for (noun, verb)
        # Get the data that makes-up the Intcode Program
        input_data = read_input(filename)
        # Run the Intcode Program; return value in memory at target_pos (usually 0th item)
        res = run_program(input_data, target_pos, noun, verb)
        print("Defined: (noun, verb) = ({}, {})".format(noun, verb))
        print("Program result at position-{}: {}\n".format(target_pos, res))
    else:  # Find correct values for (noun, verb) to result in stop_value
        # Generate set of all permutations of integers from 0-99, inclusive
        l_combos = itertools.permutations(range(0, 100), 2)
        # Test each combination of integers until the stop_value is achieved
        for combo in l_combos:
            # Reset memory, aka re-read the test data
            input_data = read_input(filename)
            # Grab values of noun, verb for this iteration
            (noun, verb) = combo
            # Run the Intcode Program; return value in memory at target_pos
            step_res = run_program(input_data, target_pos, noun, verb)
            # Test result of program for stop_value condition; break if it's matched
            if step_res == stop_value:
                # Calculate the resultant for this successful (noun, verb) combo
                res = 100 * noun + verb
                print("Undefined (noun, verb) -- Stop Condition: Program = {} at position-{}".format(stop_value,
                                                                                                     target_pos))
                print("Result: (noun, verb) = ({}, {})".format(noun, verb))
                print("100 * n + verb = {}\n".format(res))
                break


# Call the main function
if __name__ == '__main__':
    # Part #1: If (noun, verb) = (12, 2), what is the value in memory at position-0?
    intcode_program("day2.txt", 0, noun=12, verb=2)
    # Part #2: If Program results in 1969072 at position-0, what are (noun, verb)?
    intcode_program("day2.txt", 0, stop_value=19690720)
