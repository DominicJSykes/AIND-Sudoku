assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unit_list:
        pairs = [(box,pair) for box in unit for pair in unit if box!= pair if len(values[box]) == 2 if values[box] == values[pair]]
        if len(pairs) > 0:
            for pair in pairs:
                twin_peers = set(peers[pair[0]]) & set(peers[pair[1]])
                for peer in twin_peers:
                    assign_value(values,peer,values[peer].replace(values[pair[0]][0],""))
                    assign_value(values,peer,values[peer].replace(values[pair[0]][1],""))  
    return values
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def single_cross(A, B):
    "Cross product of elements in A and elements in B."
    return [A[i]+B[i] for i in range(len(A))]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
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
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values,peer,values[peer].replace(digit,""))
    return values

def only_choice(values):
    for i in unit_list:
        for digit in '123456789':
            dplaces = [box for box in i if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values,dplaces[0],digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        stalled = True
    return values

def search(values):
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
    """
    new_grid = grid_values(grid)
    new_grid = search(new_grid)
    return new_grid

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    #Create the rows and columns where rows are named A-I and columns named 1-9.
    rows = "ABCDEFGHI"
    columns = "123456789"
    boxes = cross(rows,columns)
    
    row_units = [cross(r,columns) for r in rows]
    column_units = [cross(rows,c) for c in columns]
    square_units = [cross(rs,cs) for rs in ["ABC","DEF","GHI"] for cs in ["123","456","789"]]
    reverse_rows = rows[::-1]
    diag_one = [single_cross(rows,columns)]
    diag_two = [single_cross(reverse_rows,columns)]
    unit_list = row_units + column_units + square_units + diag_one + diag_two
    units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    (display(solve(diag_sudoku_grid)))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
