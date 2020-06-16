import STcpClient
import random
import numpy as np

'''
    輪到此程式移動棋子
    board : 棋盤狀態(list of list), board[i][j] = i row, j column 棋盤狀態(i, j 從 0 開始)
            0 = 空、1 = 黑、2 = 白、-1 = 四個角落
    is_black : True 表示本程式是黑子、False 表示為白子

    return Step
    Step : single touple, Step = (r, c)
            r, c 表示要下棋子的座標位置 (row, column) (zero-base)
'''


def eval_func(state):
    # 粘捷負責
    simple_diff = (state==MY_COLOR).sum()-(state==ENEMY_COLOR).sum() # a baseline
    eval_val = simple_diff
    return eval_val

def getwalkables(state):
    indices = np.argwhere(state==0)
    return [tuple(row) for row in indices]

def testidx(idx, state, THIS_COLOR):
    #彥淳負責
    x = idx[0]
    y = idx[1]
    next_state = np.copy(state)
    flip_num = 0

    # check if it flips 

    # x to negative 
    for k in range(x-1, -1, -1): 
        if state[(k,y)] == THIS_COLOR:
            for j in range(k+1,x):
                next_state[(j,y)] = THIS_COLOR
                flip_num +=1
            break
        elif state[(k,y)] == BLANK:
            break

    # x to positive
    for k in range(x+1, 8): 
        if state[(k,y)] == THIS_COLOR:
            for j in range(k-1, x, -1):
                next_state[(j,y)] = THIS_COLOR
                flip_num +=1
            break
        elif state[(k,y)] == BLANK:
            break

    # y to negative 
    for k in range(y-1, -1, -1): 
        if state[(x,k)] == THIS_COLOR:
            for j in range(k+1,y):
                next_state[(x,j)] = THIS_COLOR
                flip_num +=1
            break
        elif state[(x,k)] == BLANK:
            break

    # y to positive
    for k in range(y+1, 8): 
        if state[(x,k)] == THIS_COLOR:
            for j in range(k-1, y, -1):
                next_state[(x,j)] = THIS_COLOR
                flip_num +=1
            break
        elif state[(x,k)] == BLANK:
            break

    # x=y line to negative
    for k in zip(range(x-1,-1,-1),range(y-1,-1,-1)):
        if state[k] == THIS_COLOR:
            for j in zip(range(k[0]+1, x), range(k[1]+1, y)):
                next_state[j] = THIS_COLOR
                flip_num +=1
            break
        elif state[k] == BLANK:
            break
    
    # x=y line to positive
    for k in zip(range(x+1,8),range(y+1,8)):
        if state[k] == THIS_COLOR:
            for j in zip(range(k[0]-1, x, -1), range(k[1]-1, y, -1)):
                next_state[j] = THIS_COLOR
                flip_num +=1
            break
        elif state[k] == BLANK:
            break
    
    # x+y=p line to negative
    for k in zip(range(x-1,-1,-1),range(y+1,8)):
        if state[k] == THIS_COLOR:
            for j in zip(range(k[0]+1, x), range(k[1]-1, y, -1)):
                next_state[j] = THIS_COLOR
                flip_num +=1
            break
        elif state[k] == BLANK:
            break
    
    # x+y=p line to positive
    for k in zip(range(x+1,8),range(y-1,-1,-1)):
        if state[k] == THIS_COLOR:
            for j in zip(range(k[0]-1, x, -1), range(k[1]+1, y)):
                next_state[j] = THIS_COLOR
                flip_num +=1
            break
        elif state[k] == BLANK:
            break
    
    if flip_num != 0:
        next_state[idx] = THIS_COLOR
        return flip_num, True, next_state
    
    # check if it is in 6*6
    if 1<=x<=6 and 1<=y<=6:
        next_state[idx] = THIS_COLOR
        return flip_num, True, next_state
    else:
        return flip_num, False, next_state
    
    

def minmax(state, depth, maxplayer, is_black, alpha, beta):
    next_states = []
    next_placement = []

    THIS_COLOR = 1 if is_black else 2

    walkables = getwalkables(state)
    for w in walkables:
        flip_num, is_legal, s = testidx(w, state, THIS_COLOR)
        if is_legal:
            next_states.append(s)
            next_placement.append(w)
    
    if depth==0 or len(next_states)==0:
        # depth-cut or no legal move
        if depth == DEPTH:
            return (0,0) # input state has no legal move --> return illegal move
        else:
            return eval_func(state)

    i = -1 #the index of the instance of lists
    if maxplayer:
        v = -np.inf
        for s in next_states:
            i +=1
            v = max(v, minmax(s, depth-1, False, not is_black, alpha, beta))
            if v>=beta:
                if depth == DEPTH:
                    return next_placement[i]
                else:
                    return v
            alpha = max(alpha, v)

        if depth == DEPTH:
            return next_placement[i]
        else:
            return v
    else:
        v = np.inf
        for s in next_states:
            i+=1
            v = min(v, minmax(s, depth-1, True, not is_black, alpha, beta))
            if v<=alpha:
                if depth == DEPTH:
                    return next_placement[i]
                else:
                    return v
            beta = min(beta, v)

        if depth == DEPTH:
            return next_placement[i]
        else:
            return v


DEPTH = 4
BLANK = 0
MY_COLOR = 1 # just an init
ENEMY_COLOR = 2 # just an init

def GetStep(board, is_black):

    # make the board a ndarray
    board = np.array(board, dtype='int32')

    # do the minmax process
    depth = DEPTH
    alpha = -np.inf
    beta = np.inf
    MY_COLOR = 1 if is_black else 2
    ENEMY_COLOR = 2 if is_black else 1
    #print("A2")
    #return (0,0)
    return minmax(board, depth, True, is_black, alpha, beta)


while(True):
    print("A1!")
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break
    
    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)
