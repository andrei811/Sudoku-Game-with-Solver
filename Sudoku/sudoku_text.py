
def valid(x, y, value, matrix):

    for i in range(9):
        if (matrix[x][i] == value or matrix[i][y] == value) and i != x and i != y:
            return False
    
    p_x = ((x // 3) * 3) 
    p_y = ((y // 3) * 3) 
    
    for i in range(p_x, p_x + 3):
        for j in range(p_y, p_y + 3):
            if matrix[i][j] == value and (i != x or j != y):
                return False
    
    return True

def SudokuSolver(pos, R, lenR, matrix):
    
    if (pos >= lenR):
        return True
    
    x = R[pos][0]
    y = R[pos][1]
    
    for i in range(1, 10):
        if valid(x, y, i, matrix):
            
            matrix[x][y] = i
            
            if (SudokuSolver(pos + 1, R, lenR, matrix)):
                return True
            
            matrix[x][y] = 0
    
    return False


def is_solvable_and_valid(x, y, value, new_matrix):
    
    if not valid(x, y, value, new_matrix):
        return False
    
    R = []
    
    for i in range(9):
        for j in range(9):
            if new_matrix[i][j] == 0:
                R.append([i, j])
    
    to_return = SudokuSolver(0, R, len(R), new_matrix)
    
    
    
    for p in R:
        if p[0] != x or p[1] != y:
                new_matrix[p[0]][p[1]] = 0
    
    if not to_return:
        new_matrix[x][y] = 0
    
    return to_return

