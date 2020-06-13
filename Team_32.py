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
    pass

def getwalkables(state):
    indices = np.argwhere(state==0)
    return [tuple(row) for row in indices]

def testidx(idx, state, is_black):
    #彥淳負責
    pass

def minmax(state, depth, maxplayer, is_black, alpha, beta):
    next_states = []
    next_placement = []

    walkables = getwalkables(state)
    for w in walkables:
        flipnum, is_legal, s = testidx(w, state, is_black)
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
            v = max(v, minmax(s, depth-1, False, is_black, alpha, beta))
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
            v = min(v, minmax(s, depth-1, True, is_black, alpha, beta))
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

def GetStep(board, is_black):

    # make the board a ndarray
    board = np.array(board, dtype='int32')

    # do the minmax process
    depth = DEPTH
    alpha = -np.inf
    beta = np.inf
    return minmax(board, depth, True, is_black, alpha, beta)


while(True):
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break
    
    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)
