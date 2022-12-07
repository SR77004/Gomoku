
import numpy as np
import regex as re


UTILITY = {'Quintet': [20000000, ['xxxxx']],
           'Quartet_2Opens': [400000, ['exxxxe']],
           'Quartet_1Open': [50000, ['nxxxxe', 'exxxxn']],
           'Triplet_2Opens': [30000, ['exxxe']],
           'Triplet_1Open': [15000, ['nxxxee', 'eexxxn']],
           'ProbQuartet_2Opens': [7000, ['exexxe', 'exxexe']],
           'ProbQuartet_1Open': [3000, ['nxexxe',
                                                'nxxexe', 'exxexn', 'exexxn']],
           'Double_2Opens': [500, ['eexxe', 'exxee']],
           'Double_1Open': [400, ['nxxeee', 'eeexxn']],
           'nProbTriplet_2Opens': [100, ['exexe']],
           'ProbTriplet_1Open': [40, ['nxexee', 'eexexn']]}

FINISHED = {'Quintet': [200000, ['xxxxx']]}

HEURISTIC = [[0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0, 0, 0],
             [0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0],
             [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0]]


def hasWinnerSeq(board, lastPlayer, winnerSeq='xxxxx'):

    newBoard = board.copy()
    a = np.asarray([[2 for i in range(15)]]).T
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=1)),
                              axis=1).copy()
    a = np.asarray([[2 for i in range(17)]])
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=0)),
                              axis=0).copy()
    count = 0
    count += searchInList(makeDig(newBoard, lastPlayer), winnerSeq)
    count += searchInList(makeCol(newBoard, lastPlayer), winnerSeq)
    count += searchInList(makeLin(newBoard, lastPlayer), winnerSeq)
    if count > 0:
        return True
    else:
        return False



def calculateHeuristic(board,
                       player,
                       heuristicValues=UTILITY,
                       positionValuesHeuristic=HEURISTIC):

    sequenceHeuristic = 0
    positionHeuristic = 0
    newBoard = board.copy()
    a = np.asarray([[2 for i in range(15)]]).T
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=1)),
                              axis=1).copy()
    a = np.asarray([[2 for i in range(17)]])
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=0)),
                              axis=0).copy()
    for values in heuristicValues.keys():
        ValueSequence = heuristicValues[values][0]
        count = 0
        sequence = heuristicValues[values][1]
        for seq in sequence:
            count += searchInList(makeDig(newBoard, player), seq)
            count += searchInList(makeCol(newBoard, player), seq)
            count += searchInList(makeLin(newBoard, player), seq)
        sequenceHeuristic += count*ValueSequence
    newBoard = board.copy()
    if(player == 1):
        np.place(newBoard, newBoard == -1, 0)
        positionHeuristic = np.sum(np.multiply(newBoard,
                                               positionValuesHeuristic))
    else:
        np.place(newBoard, newBoard == 1, 0)
        positionHeuristic = -np.sum(np.multiply(newBoard,
                                                positionValuesHeuristic))
    HeuristicValue = positionHeuristic + sequenceHeuristic

    total = HeuristicValue





    player = -1*player
    sequenceHeuristic = 0
    positionHeuristic = 0
    newBoard = board.copy()
    a = np.asarray([[2 for i in range(15)]]).T
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=1)),
                              axis=1).copy()
    a = np.asarray([[2 for i in range(17)]])
    newBoard = np.concatenate((a, np.concatenate((newBoard, a), axis=0)),
                              axis=0).copy()
    for values in heuristicValues.keys():
        ValueSequence = heuristicValues[values][0]
        count = 0
        sequence = heuristicValues[values][1]
        for seq in sequence:
            count += searchInList(makeDig(newBoard, player), seq)
            count += searchInList(makeCol(newBoard, player), seq)
            count += searchInList(makeLin(newBoard, player), seq)
        sequenceHeuristic += count*ValueSequence
    newBoard = board.copy()
    if(player == 1):
        np.place(newBoard, newBoard == -1, 0)
        positionHeuristic = np.sum(np.multiply(newBoard,
                                               positionValuesHeuristic))
    else:
        np.place(newBoard, newBoard == 1, 0)
        positionHeuristic = -np.sum(np.multiply(newBoard,
                                                positionValuesHeuristic))
    HeuristicValue = positionHeuristic + sequenceHeuristic
    return total - 1.05*HeuristicValue



def makeDig(matrix, player):

    dig = [matrix[::-1, :].diagonal(i) for i in range(-matrix.shape[1] + 5,
                                                      matrix.shape[1] - 4)]
    diagonal = []
    for i in dig:
        str1 = ''
        for e in i:
            if player == 1:
                if e == 0:
                    str1 += 'e'
                elif (e == -1 or e == 2):
                    str1 += 'n'
                elif(e == 1):
                    str1 += 'x'
            else:
                if e == 0:
                    str1 += 'e'
                elif (e == 1 or e == 2):
                    str1 += 'n'
                elif(e == -1):
                    str1 += 'x'
        diagonal.append(str1)
    dig = [matrix.diagonal(i) for i in range(matrix.shape[1]-5,
                                             -matrix.shape[1] + 4, -1)]
    for i in dig:
        str1 = ''
        for e in i:
            if player == 1:
                if e == 0:
                    str1 += 'e'
                elif (e == -1 or e == 2):
                    str1 += 'n'
                elif(e == 1):
                    str1 += 'x'
            else:
                if e == 0:
                    str1 += 'e'
                elif (e == 1 or e == 2):
                    str1 += 'n'
                elif(e == -1):
                    str1 += 'x'
        diagonal.append(str1)
    return diagonal


def makeLin(matrix, player):

    diagonal = []
    for i in matrix:
        str1 = ''
        for e in i:
            if player == 1:
                if e == 0:
                    str1 += 'e'
                elif (e == -1 or e == 2):
                    str1 += 'n'
                elif(e == 1):
                    str1 += 'x'
            else:
                if e == 0:
                    str1 += 'e'
                elif (e == 1 or e == 2):
                    str1 += 'n'
                elif(e == -1):
                    str1 += 'x'
        diagonal.append(str1)
    return diagonal


def makeCol(matrix, player):

    diagonal = []
    matrix = matrix.copy().T
    for i in matrix:
        str1 = ''
        for e in i:
            if player == 1:
                if e == 0:
                    str1 += 'e'
                elif (e == -1 or e == 2):
                    str1 += 'n'
                elif(e == 1):
                    str1 += 'x'
            else:
                if e == 0:
                    str1 += 'e'
                elif (e == 1 or e == 2):
                    str1 += 'n'
                elif(e == -1):
                    str1 += 'x'
        diagonal.append(str1)
    return diagonal



def searchInList(Lists, searchFor):

    count = 0
    for List in Lists:
        count += countOccurrences(List, searchFor)
    return count



def countOccurrences(text, searchFor):

    return len(re.findall(searchFor, text, overlapped=True))