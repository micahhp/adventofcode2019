# Import packages
import os


# Define functions
def read_input(filename):
    """
    Takes a file, opens and reads it, and turns contents into a list of instructions/coords
    :param filename: name of file containing data to read
    :return: list of integers read out of the file
    """
    # Define path to filename
    dir_path = os.getcwd()
    data_path = os.path.join(dir_path, "data", filename)
    # Open file and read to lines
    with open(data_path) as f:
        texty = f.readlines()
    # Loop through lines and split into individual instructions/coords
    input_data = []
    for item in texty:
        this_item = item.replace("\n", "").split(",")
        input_data.append(this_item)
    # return the list of instructions/coords read from the file
    return input_data


def trace_wires(filename, metric):
    """
    Takes a list of two wire direction maps, calculates intersections, and returns either
    optimal Manhattan Distance -or- most efficient route to intersection
    :param filename: name of file that contains the wire path maps
    :param metric: solution option: 'distance' = optimal Manhattan Distance to intersection;
    'route' = optimal intersection by fewest turns
    :return: returns either optimal Manhattan Distance or fewest number of moves depending
    on the value of 'metric' parameter
    """
    # Convert input file into usable input
    input_data = read_input(filename)
    # Instantiate final list of coordinates covered by the two wires
    l_results = []
    # Loop through each wire in group of two wires
    for wire_map in input_data:
        # Instantiate list of coordinates, and cursor coordinates (origin; 0,0) for this wire
        l_coords = []
        cursor_x = 0
        cursor_y = 0
        # Loop through each instruction to traverse grid and record location in l_results
        for instruction in wire_map:
            # Split instruction into parts; pick math operation based on 'direction'
            (direction, quant) = (instruction[0], int(instruction[1:]))
            # Create a list of coordinates marked by this step alone; add to overall list in l_results
            l_this_step = []
            # Record coords of each step in this quantity of steps
            for ind in range(quant):
                if direction == 'R':  # Cursor moves to Right
                    cursor_x += 1
                elif direction == 'L':  # Cursor moves to Left
                    cursor_x -= 1
                elif direction == 'U':  # Cursor moves Up
                    cursor_y += 1
                elif direction == 'D':  # Cursor moves Down
                    cursor_y -= 1
                else:  # Cursor direction doesn't match expected types
                    print("Bad Instruction: {}".format(instruction))
                    continue
                # Add this step to the internal list of coords for this step
                l_this_step.append((cursor_x, cursor_y))
            # Add coords from this instruction to list of coords for this wire
            l_coords += l_this_step
        # Add collection of all coords for this wire to the resultant list
        l_results.append(l_coords)
    # Find list of all intersections between the two wires
    intersections = list(set(l_results[0]) & set(l_results[1]))
    # Set min_distance, min_moves to really high numbers so that they can be overwritten by best fit
    # Need to create spots to save the coordinates of the "best fit" intersection for each method
    min_dist = 1000000
    min_dist_pair = ()
    min_moves = 1000000
    min_moves_pair = ()
    # Loop through list of intersections and calculate Manhattan Distance, number of moves for each
    for xx in intersections:
        dist = abs(xx[0]) + abs(xx[1])
        move_1 = l_results[0].index(xx) + 1
        move_2 = l_results[1].index(xx) + 1
        move_sum = move_1 + move_2
        # Test Manhattan Distance for this intersection against global min_dist
        if dist < min_dist:
            min_dist = dist
            min_dist_pair = xx
        # Test number of moves required to reach this intersection against global min_moves
        if move_sum < min_moves:
            min_moves = move_sum
            min_moves_pair = xx
    # Output results for these two wires depending on output parameter passed to function
    if metric == 'distance':
        print("\nIntersection with lowest Manhattan Distance ({}, {}) - Distance: {}".format(
            min_dist_pair[0], min_dist_pair[1], min_dist))
    elif metric == 'route':
        print("\nIntersection with shortest route ({}, {}) - Moves: {}".format(
            min_moves_pair[0], min_moves_pair[1], min_moves))


# Call the main function
if __name__ == '__main__':
    # Part #1: What is the minimum Manhattan Distance intersection for these two wires?
    trace_wires('day3.txt', 'distance')
    # Part #2: What intersection is reached using the fewest number of moves for these two wires?
    trace_wires('day3.txt', 'route')
