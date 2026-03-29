from .minesweeper_engine import generate_board,Cell,get_neibhours,count_of_mines,render_user_board,user_input,cascad_opening,render_board,check_win,reveal_cell
from dataclasses import dataclass
from collections import deque
from .solver import Solver
cell=Cell

""""функция игры"""
def main():
    opend_cells=0
    first_click=False
    rows=len(board)
    cols=len(board[0])
    all_coords=[]
    for r in range(rows):
        for c in range(cols):
            all_coords.append((r,c))
    safe_spots=rows*cols-count_of_mines
    alive=True
    checked=[]
    """создание исходной доски(пустой) с дэфолт знаениями"""
    grid = [[cell(False, False, False, 0) for a in range(cols)] for b in range(rows)]  
    render_user_board(grid)
    
    while alive and safe_spots>0:
        line=input("введите команду и координаты для хода:")  
        parsed_line=user_input(line,grid)
        if parsed_line is None:
            print("неправильный ввод нужно o y x")
            continue    
        command,r,c=parsed_line

        """генераия игровой доски(бэкэнд)(не видна юзеру) со всеми значенимями при первом клике(БЕЗОПАСНОМ!!!!)"""
        if not first_click:
            if command=="o" or command=="open":
                board=generate_board(rows,cols,count_of_mines,(r,c))
                first_click=True
                solve=Solver()
            else:
                print("введите корректно")
                render_user_board(board)
                continue
            
        cell_value=board[r][c]

        """открытие клеток и расстановка флагов + проверка после каждого открытия состояние клетки на мину"""
        if command in ["o","open"]:
            reveal_cell(board,r,c)
            # if not cell_value.is_revealed and not cell_value.is_flagged:
            #     cell_value.is_revealed=True
            #     if cell_value.adjacent_mines==0:
            #         cell_value.is_revealed=True
            #         cascad_opening(board,r,c)
            # elif cell_value.is_flagged:
            #     print("клетка под флагом")
            # else:
            #     print("клетка уже открыта")
            # render_user_board(board)

        if (cell_value.is_mine and not cell_value.is_flagged and cell_value.is_revealed):
            alive=False
            print("проигрышь")
            render_board(board)
            return None
        
        # if command in ["s","solver"]:
        #     render_board(board)
        #     safe,mines=solve.solve_step(board)
        #     if not safe and not mines:
        #         print("нет гарантированных ходов")
        #     else:
        #         print(safe,mines)


        if command in ["f","flag"]:
            if not cell_value.is_flagged and not cell_value.is_revealed:
                cell_value.is_flagged=True
                cell_value.is_revealed=False
            elif cell_value.is_revealed:
                print("нельзя тк клетка уже открыта")
            else:
                cell_value.is_flagged=False
                cell_value.is_revealed=False
            render_user_board(board)


        """проверка колличества оставшихся клеток тем самым проверка победы игрока если не откртых клеток столько же сколько и мин"""
        for r in range(rows):
            for c in range(cols):
                if (r,c) not in checked:
                    if board[r][c].is_revealed and not board[r][c].is_mine:
                        opend_cells+=1
                        checked.append((r,c))
                else:
                    continue

        if check_win(board,opend_cells)==True:
            print("ВЫ ПОБЕДИЛИ!!!!!")
            break
"""без этого тесты не работают ):"""
def display_board(board):
    return render_user_board(board)
def parse_input(board,line):
    return user_input(board,line)
        
if __name__ == "__main__":
    main()