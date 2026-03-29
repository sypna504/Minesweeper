from .minesweeper_engine import generate_board,Cell,get_neibhours

class Solver:
    
    def __init__(self):
        pass
    
    def solve_step(self,board):
        rows=len(board)
        cols=len(board[0])
        all_coords=[]
        for r in range(rows):
            for c in range(cols):
                all_coords.append((r,c))
        constr=set()
        all_cords=all_coords
        """метод для решения 1 шага"""
        safe_open=set()
        mines=set()
        f=1
        count=0
        while f==1:
            f=0
            count+=1
            for r in range(rows):
                for c in range(cols):
                    popoln=0
                    value=board[r][c]
                    if not value.is_revealed:
                        continue
                    N=value.adjacent_mines
                    neibhours=get_neibhours([(r,c)],all_cords)

                    """поиск открытых соседей"""
                    neib_opend=set()
                    for x,y in neibhours:
                        if board[x][y].is_revealed:
                            neib_opend.add((x,y))
                    """поиск флагов рядом"""
                    neib_flags=set()
                    for x,y in neibhours:
                        if (x,y) in mines:
                            neib_flags.add((x,y))

                    """поиск соседей не попавших никуда"""
                    neib_anonym=set()
                    for x,y in neibhours:
                        if  not board[x][y].is_revealed and not board[x][y].is_flagged and (x,y) not in mines:
                            neib_anonym.add((x,y))

                    """первое правило"""
                    if N==len(neib_anonym)+len(neib_flags):
                        for i in neib_anonym:
                            if i not in neib_flags and i not in mines:
                                mines.add(i)
                                f+=1
                                
                    
                    """второе правило"""
                    
                    if len(neib_flags)==N:
                        for i in neib_anonym:
                            if i not in neib_opend and i not in safe_open:
                                safe_open.add(i)
                                f=1
            if count>10000:
                break

        """второй решатель"""

        """функция упрощения
        пока есть изменения находит новые ограниячения либо упрощает их либо сразу говорит что ограничение не валидно и это мина или сэйф клетка"""
        def _symplify(mass_of_frozenset):
            mass_of_frozensets=list(mass_of_frozenset)
            f=True
            
            while f:
                mass_of_new_frozensets=set()
                f=False
                
                for s,k in mass_of_frozensets:

                    s1=s-safe_open
                    mines_intercec=s1&mines
                    s2=s1-mines_intercec
                    k_new=k-len(mines_intercec)

                    if k_new==0:
                        if s2:
                            safe_open.update(s2)
                            f=True
                        continue

                    if len(s2)==0:
                        continue

                    if k_new==len(s2):
                        mines.update(s2)
                        f=True
                        continue

                    if (s2!=s) or (k_new!=k):
                        f=True
                    mass_of_new_frozensets.add((frozenset(s2),k_new))

                mass_of_frozensets=mass_of_new_frozensets  
            return list(mass_of_frozensets)
        """функция генерации ограничений
        проходит по соседям клетки и определяет их по группам(множествам)"""
        def _generate_constraints(board):
            mass_of_frozensets=[]
            rows=len(board)
            cols=len(board[0])

            for r in range(rows):
                for c in range(cols):
                    cl=board[r][c]
                    if cl.is_revealed:

                        cl_neib=get_neibhours([(r,c)],all_cords)
                        N=cl.adjacent_mines
                                
                        already_mines=set() #колличество УЖЕ найденных мин
                        for x,y in cl_neib:
                            if (x,y) in mines:
                                already_mines.add((x,y))

                        cl_annon_neib=set()
                        for x,y in cl_neib:
                            if not board[x][y].is_revealed and (x,y) not in mines:
                                cl_annon_neib.add((x,y))
                        
                        count_of_mines_nearby=N-len(already_mines)
                        
                        mass_of_frozensets.append((frozenset(cl_annon_neib),count_of_mines_nearby))
            return _symplify(mass_of_frozensets)
        """функция применения правила подмножеств
        пока происходят изменения 
        создается новая пара ограничений и колличества мин по разности 
        базовя проверка на мины и безопасного хода
        после проверки ограничение добавляется в список с новыми ограничениями
        """
        def _apply_subset_rule(mass_of_frozensets):
                mass_of_frozensets=mass_of_frozensets
                flag=True
                

                while flag:
                    new_limits=[]
                    flag=False

                    for s1,k1 in mass_of_frozensets:
                        for s2,k2 in mass_of_frozensets:

                            if s2!=s1 and s1<s2:
                                new_s=s2-s1
                                new_k=k2-k1

                                if new_k==0:
                                    safe_open.update(new_s)
                                    flag=True
                                    continue

                                if new_k==len(new_s):
                                    mines.update(new_s)
                                    flag=True
                                    continue

                                new_f=(frozenset(new_s),new_k)
                                if  new_f not in mass_of_frozensets  and new_f not in new_limits and len(new_s)!=0:
                                    flag=True
                                    new_limits.append(new_f)
                                    
                                if 0<=new_k<=len(new_s) or new_k<0 or len(new_s)==0:
                                    continue
            
                    if len(new_limits)!=0:
                        mass_of_frozensets=_symplify(list(set(mass_of_frozensets)|set(new_limits)))
                        flag=True
                    mass_of_frozensets=_symplify(mass_of_frozensets)

                return mass_of_frozensets
        a=_generate_constraints(board)
        b=_apply_subset_rule(_symplify(a))
        
        return safe_open,mines