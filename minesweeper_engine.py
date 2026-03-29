import random
from dataclasses import dataclass
from collections import deque
count_of_mines=8

def get_neibhours(coord,all_coords):
    """ функци нахождения соседей. принимает [координату] или массив координат возвращает массив соседей"""
    neibhours=[]
    coords=all_coords
    for pare in coord:      
        for i in [-1,1]:
            pare1=(pare[0]+i,pare[1])
            pare2=(pare[0],pare[1]+i)
            pare3=(pare[0]+i,pare[1]+i)
            pare4=(pare[0]+i,pare[1]-i)

            neibhours.append(pare1) if pare1 in coords else None 
            neibhours.append(pare2) if pare2 in coords else None
            neibhours.append(pare3) if pare3 in coords else None
            neibhours.append(pare4) if pare4 in coords else None
    return neibhours
"""класс с синтаксическим сахаром датакласс(встроенные функции с __func__) отвечает за параметр клетки """
@dataclass
class Cell:
    is_mine: bool=False
    is_revealed: bool=False
    is_flagged: bool=False
    adjacent_mines: int=0
cell=Cell

def generate_board(rows, cols, num_mines, first_click_coords):
    """функция генерации доски 
    внури генерируется доска по колличеству рядов и колонок
    рандомно создаются координаты для мин без первого клика
    потом по всем этим данным заполняется доска"""
    board_coords=[]
    test_board=[]
    if rows <= 0 or cols <= 0:
        raise ValueError("неверные данные")
    [[board_coords.append((r,c)) for r in range(rows)] for c in range(cols)]

    cords_for_mine_places=board_coords.copy()
    cords_for_mine_places.remove(first_click_coords)

    grid=[[cell() for r in range(rows)] for c in range(cols)]

    mine_places=sorted(random.sample(cords_for_mine_places,num_mines))
    mines_neibhors=sorted(get_neibhours(mine_places,board_coords))

    for r in range(rows):
            for c in range(cols):
                if (r,c) in mine_places:
                    grid[r][c].is_mine=True
                if (r,c) in mines_neibhors and (r,c) not in mine_places:
                    grid[r][c].is_mine=False
                    grid[r][c].adjacent_mines+=mines_neibhors.count((r,c))
                if (r,c) not in mine_places and (r,c) not in mines_neibhors:
                    grid[r][c].is_mine=False
    return grid
def check_win(board,opend_cells):
    """функция проверки победы игрока 
    если количество мин равно количеству всех клеток - открытые клетки -> победа"""
    rows=len(board)
    cols=len(board[0])
    if count_of_mines==(rows*cols)-opend_cells:
            render_board(board)
            return True
    return False


def render_board(grid,rows,cols):
    """функция рендера доски с заданными элементами(мины поля с цифрами)"""
    board=[]
    # rows=len(grid)
    # cols=len(grid[0])
    for r in range(rows):
            row=[]
            for c in range(cols):
                if grid[r][c].is_mine:
                    row.append("*")
                else:   
                    row.append(grid[r][c].adjacent_mines)
            board.append(row)
    print("x/y ",*[x for x in range(cols)])
    for index in range(len(grid)):
        print("  ",index,*board[index])


def render_user_board(board):
    """рендерит доску для юзера для игры,"""
    rows=len(board)
    cols=len(board[0])
    print("x/y",*[x for x in range(cols)])
    for r in range(rows):
        row=[]
        for c in range(cols):
            cl=board[r][c]
            if cl.is_revealed==True:
                row.append(cl.adjacent_mines)
            elif cl.is_flagged==True:
                row.append("F")
            else:
                row.append("#")
        print(r," ",*row)

def user_input(board,line):
    """функция обработки ввода юзера
    пока ввод не будет нужным будет запрашивать заново"""
    rows=len(board)
    cols=len(board[0])
    all_coords=[]

    """обрабатывает инпут от юзера"""
    line=line.strip().split()
    if len(line)!=3:
        return None
    comand=line[0].lower()
    if comand not in ["open","o","flag","f"]:
        return None
    
    try:
        r,c=int(line[1]),int(line[2])
    except ValueError:
        return None
    
    if 0<=r<rows and 0<=c<cols:
        return comand,r,c
    else:
        return None
    
def cascad_opening(board,r,c):
    """функция каскадного расскрытия 0
    проходится по соседям соседей соседей и так далее
    ищет нули и расскрывает их
    не нули просто расскрывает делая их границами каскада"""
    que =deque([(r,c)])
    visited=[]
    rows=len(board)
    cols=len(board[0])
    all_coords=[]
    for r in range(rows):
        for c in range(cols):
            all_coords.append((r,c))
    while len(que)>0:
        cur_cord=que.popleft()
        if cur_cord in visited:
            continue

        else:
            visited.append(cur_cord)
        c_x,c_y=cur_cord
        cur_cell=board[c_x][c_y]

        if cur_cell.is_mine or cur_cell.is_flagged:
            continue
        if not cur_cell.is_revealed:
            cur_cell.is_revealed=True

        if cur_cell.adjacent_mines==0:
            for nb_x, nb_y in get_neibhours([cur_cord],all_coords):
                nb_cell=board[nb_x][nb_y]
                if nb_cell.is_mine or nb_cell.is_flagged or nb_cell in visited:
                    continue

                if nb_cell.adjacent_mines>0:
                    if not nb_cell.is_revealed:
                        nb_cell.is_revealed=True

                else:
                    que.append((nb_x,nb_y))

def reveal_cell(board,r,c):
    """функция раскрытия клетки"""
    cell_value=board[r][c]
    if not cell_value.is_revealed and not cell_value.is_flagged:
        cell_value.is_revealed=True
        if cell_value.adjacent_mines==0:
            cell_value.is_revealed=True
            cascad_opening(board,r,c)
        elif cell_value.is_flagged:
            return "клетка под флагом"
        else:
            return("клетка уже открыта")
        return render_user_board(board)

