assignments = []

### puzzle board Set-ups
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

cols = '123456789'
rows = 'ABCDEFGHI'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal1 = [a[0]+a[1] for a in zip(rows, cols)]
diagonal2 = [a[0]+a[1] for a in zip(rows, cols[::-1])]
dragonal_units= [diagonal1,diagonal2]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        for box in unit:
            repeats = [box2 for box2 in unit if values[box] == values[box2]]
            if len(repeats) > 1 and len(repeats) == len(values[box]):
                del_box = [box2 for box2 in unit if values[box] != values[box2]]
                for deleting in del_box:
                    for digit in values[box]:
                        if digit in values[deleting]:
                            assign_value(values, deleting, values[deleting].replace(digit, ''))

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
    """
    values = []
    for char in grid:
        if char == '.':
            values.append('123456789')
        else:
            values.append(char)
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    display code is copied from the lecture notes
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Deleting candidates that has been confirmed in other boxes
    Args:
        values: Sudoku board
    """
    changed = True
    while changed:

        changed = False
        for box in boxes:
            if len(values[box]) == 1:
                digit = values[box]
                for peer in peers[box]:
                    if digit in values[peer]:
                        assign_value(values, peer, values[peer].replace(digit, ''))
                        changed = True
    return values


def only_choice(values):
    """
    confirm digits that not a candidates in other boxes
    Args:
        values: sudoku board
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    iterate through eliminate, only_choice, and naked_twins techniques until no changed can be done.
    Args:
        values: sudoku board
    Returns:
        False: if contradiction appears
        values: reduce puzzle board

    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    changed = True
    while changed:
        changed = False
        while not stalled:
            solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

            values = eliminate(values)

            values = only_choice(values)
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            stalled = solved_values_before == solved_values_after
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
            values2 = naked_twins(values)
            if values != values2:
                values = values2
                changed = True
    return values

def search(values):
    """
    Perform a recurrence depth first search on a reduced puzzle
    Args:
        values: sudoku board
    Returns:
        False: failed attempts
        values: solved puzzle board

    """
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
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
    values = grid_values(grid)

    values = search(values)



    return values



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
