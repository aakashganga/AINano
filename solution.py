from utils import *

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return ([s+t for s in A for t in B])
	#pass

# assignments = []
# rows = 'ABCDEFGHI'
# cols = '123456789'
# boxes = cross(rows, cols)
# row_units = [cross(r, cols) for r in rows]
# col_units = [cross(rows, c) for c in cols]
# square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# unitlist = row_units + col_units + square_units
# units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
# diagonal1 = sum([cross(rows[i], cols[i]) for i in range(len(rows))], [])
# diagonal2 = sum([cross(rows[i], cols[8 - i]) for i in range(len(rows))], [])


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

# def naked_twins(grid):
#     """Eliminate values using the naked twins strategy.
#     Args:
#         values(dict): a dictionary of the form {'box_name': '123456789', ...}
#
#     Returns:
#         the values dictionary with the naked twins eliminated from peers.
#     """
#     newgrid = grid.copy()
#     for i in range(27):
#         unitvalues = [grid[box] for box in unitlist[i]]
#         dictlist = {value:unitvalues.count(value) for value in unitvalues}
#         twindict = dict((k, v) for k, v in dictlist.items() if v >= 2)
#         if twindict:
#             for twinkey, twinvalue in twindict.items():
#                 unitvalues = [unit.replace(twinkey,"") if unit != twinkey else unit for unit in unitvalues]
#         tempdict = dict(zip(unitlist[i], unitvalues))
#         for box,value in tempdict.items():
#             if grid[box]!= tempdict[box]:
#                 newgrid[box] = tempdict[box]
#     return newgrid


def naked_twins(grid):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    newgrid = grid.copy() # first copy the grid to make sure that we don't lose values

    # In the loop below, we go through each item of each list present in the unitlist
    # and identify naked twins. Once naked twins are identified, we remove each digit
    # one by one only when the naked twin is 2 digit long and length of item in the list
    #  of the unitlist is larger than the twin identified.


    for i in range(27): # because we have 27 lists in the unitlist variable
        unitvalues = [grid[box] for box in unitlist[i]]
        dictlist = {value: unitvalues.count(value) for value in unitvalues}
        twindict = dict((k, v) for k, v in dictlist.items() if v >= 2)
        if twindict:
            for twinkey, twinvalue in twindict.items():
                tempvals = []
                for unit in unitvalues:
                    if unit != twinkey and len(twinkey)== 2 and len(unit) > len(twinkey):
                        for digit in twinkey:
                            # print ("digit", digit)
                            # print ('unit before replacement:',unit)
                            unit = unit.replace(digit, "")
                            # print ('unit after replacement:',unit)
                    else:
                        unit = unit
                    tempvals.append(unit)
                unitvalues = tempvals
                # unitvalues = [unit.replace(twinkey,"") if unit != twinkey else unit for unit in unitvalues]
        tempdict = dict(zip(unitlist[i], unitvalues))
        for box, value in tempdict.items():
            if grid[box] != tempdict[box]:
                newgrid[box] = tempdict[box]
    return newgrid





    

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


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
    #pass
    
    sdgrid = {}
    for i in range(len(boxes)):
        if grid[i] == '.':
            sdgrid[boxes[i]] = cols
        else:
            sdgrid[boxes[i]] = grid[i]            
    return (sdgrid)
    
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    #pass
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(grid):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for key, value in grid.items():
        if len(value) == 1:
            catchvalue = value
            for peer in peers[key]:
                grid[peer] = grid[peer].replace(catchvalue,"")             
    return (grid)
    

def only_choice(grid):
    for unit in unitlist:
        for digit in cols:
            dbox = [box for box in unit if digit in grid[box]]
            #print ("dbox is:", dbox)
            if len(dbox)==1:
                grid[dbox[0]] = digit
    return (grid)
    
    
def reduce_puzzle(grid):
    stalled = False
    while not stalled:
        # check how many boxes have a determinate value
        solved_values_before = len([box for box in grid.keys() if len(grid[box])==1])
        
        # do a round of eliminate strategy
        grid = eliminate(grid)
        
        # do a round of only choice strategy
        grid = only_choice(grid)
        
        # check how many boxes have been determined
        solved_values_after = len([box for box in grid.keys() if len(grid[box])==1])
        #print ('solved_values_after', solved_values_after)
        
        stalled = solved_values_after == solved_values_before
        #print ('stalled flag is:',stalled)
        
        # sanity check. Return false if there is a box with zero available values
        if len([box for box in grid.keys() if len(grid[box])==0]):
            return False
    return (grid)        
    
    
def search(grid):
    sudoku_solved = False
    #minlen = 9
    #while not sudoku_solved:
    grid = reduce_puzzle(grid)
    #print ('boxes',boxes)
    #solved_values_after = len([box for box in grid.keys() if len(grid[box])==1])
    if grid is False:
        return False ## Failed earlier
    if all(len(grid[s]) == 1 for s in boxes): 
        #print ('solved_values_after',solved_values_after)
        return grid ## Solved!
#         for box, value in grid.items():
#             if len(value) > 1:
#                 minlen = min(minlen,len(value))
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(grid[s]), s) for s in boxes if len(grid[s]) > 1)
    #print ("n is", n)
    #print ("s is", s)
    
    for value in grid[s]:
        new_grid = grid.copy()
        new_grid[s] = value
        attempt = search(new_grid)
        if attempt:
            return (attempt)


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    grid = naked_twins(search(grid_values(grid)))
    if grid is False:
        return False  ## Failed earlier
    if all(len(grid[s]) == 1 for s in boxes):
        # print ('solved_values_after',solved_values_after)
        return grid  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(grid[s]), s) for s in boxes if len(grid[s]) > 1)
    # print ("n is", n)
    # print ("s is", s)

    for value in grid[s]:
        new_grid = grid.copy()
        new_grid[s] = value
        attempt = solve(new_grid)
        if attempt:
            return (attempt)

if __name__ == '__main__':


    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
