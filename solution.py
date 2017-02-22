from utils import *

#Array for storing moves for visualisation in pygame
assignments = []

def assign_value(values, box, value):
    """
    Assign an updated value to a box within the puzzle, while recording this
    assignment for later visualisation in pygame.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """
    Iterates over 9 box units within the puzzle, finding pairs of boxes within
    these units that share the same possible 2 values.
    These are then passed to another function to eliminate values from shared peers.
    """
    #First find twin boxes
    for unit in unit_list:
        #Finds pairs of boxes which share a unit and values
        pairs = [(box,pair) for box in unit for pair in unit if box!= pair if len(values[box]) == 2 if values[box] == values[pair]]
        #If pair exists pass to function to remove values from peers
        if len(pairs) > 0:
            values = eliminate_twins(values,pairs)
    return values
    
def eliminate_twins(values,pairs):
    """Eliminate values found using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        pairs: a list of pairs within a unit that form the twins to eliminate using

    Returns:
        the values dictionary with the naked twins eliminated from peers.
        
    Passed a set of pairs, from which shared peers are found which 
    cannot have the values shared by the pair.
    The values can then be crossed off from the peers.
    """
    for pair in pairs:
        #Creates a set of shared peers
        twin_peers = set(peers[pair[0]]) & set(peers[pair[1]])
        #For each of these peers remove the values from the twin boxes
        for peer in twin_peers:
            assign_value(values,peer,values[peer].replace(values[pair[0]][0],""))
            assign_value(values,peer,values[peer].replace(values[pair[0]][1],""))  
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    
    Asserts the whole grid is present before creating the dictionary of values.
    Unknown values are replaced with all possible digits for elimination later.
    """
    assert len(grid) == 81
    new_dict = dict(zip(boxes,grid)) 
    for i in new_dict:
        if new_dict[i] == ".":
            assign_value(new_dict,i,"123456789")
    return new_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in columns))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Find the values already solved within the puzzle, before iterating over
    these eliminating the solved value from the box's peers, as these cannot
    share the same value.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values,peer,values[peer].replace(digit,""))
    return values

def only_choice(values):
    """
    Iterate over units within the puzzle, searching for if a certain value can
    only appear in one box within the unit.
    Assign this box that value as it has to appear within the unit.
    """
    for i in unit_list:
        for digit in '123456789':
            dplaces = [box for box in i if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values,dplaces[0],digit)
    return values

def reduce_puzzle(values):
    """
    Repeat each strategy to reduce the possible values for each box of the puzzle,
    exiting if all boxes are solved, the solution stalls or if the puzzle 
    becomes unsolvable.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Reduce possible values in the puzzle, before checking if puzzle is still 
    viable or if it is solved, if so exit.
    If unsolved find an unsolved box with least choices, make a guess and run
    the reduction of possible values again. Recursion is used until the puzzle
    become unsolvable in which case another value is tried in the level above,
    until the puzzle is solved or all posibilities run out.
    """
    values = reduce_puzzle(values)
    if values == False:
        return False
    if len([box for box in values.keys() if len(values[box]) == 1]) == 81:
        return values
    n,s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)
    for i in values[s]:
        new_values = values.copy()
        assign_value(new_values,s,i)
        attempt = search(new_values) 
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.

    Create new grid dictionary and solve
    """
    new_grid = grid_values(grid)
    new_grid = search(new_grid)
    return new_grid

if __name__ == '__main__':
    #Puzzle to solve
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    #Call to solve
    (display(solve(diag_sudoku_grid)))

    #Visualise with pygame
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
