#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,time
import numpy as np
from matplotlib import pyplot as plt
from CodeMatrix_Bonus import code_matrix_puzzle


"""
Note:
 This is the main python script for decoding the "Code Matrix puzzles" in Game ##Cyberpunk 2077##
 The idea start at 01/09 2021 and the final script finished at Sun Jan 10 18:51:30 2021 in Shanghai
 For usage,please refer to this original source.
 It's shared just for fun!!!
"""

# read the readme.md file for more information about the CodeMatrix puzzle

# match list and evaluate the score of this path(list)
def match_list(list,bonus,score):
    """
    check if there are one continuous sequence in the list which mach the bonus list
    :param list: origin input list etc [0xe9, 0x1c, 0xbd, 0xe9, 0x1c, 0x1c]
    :param bonus: bonus list []
    :param score: rate for the bonus:1/3/5
    :return: if match,return the score,else return 0
    """
    bonus_score = 0
    for i in range(len(list) - len(bonus) + 1):
        check_list = []
        for j in range(len(bonus)):
            check_list.append(list[i + j])
        #print(check_list)
        if check_list == bonus:
            bonus_score = score
    return bonus_score


# find all possible decoding path,which give a list of codes
def decoding_matrix(matrix,ram):
    """
    find all possible all possible decoding path according to the  matrix and ram
    path=[:[i,j]],meaning the j+1 item in row i+1 in the matrix
    :param matrix: the input matrix (list type),normally 5x5,4x4
    :param ram: maximum steps:4 or 6
    :return: path and the final list of codes
    """
    '''
    how to define the path
    In the matrix,choose num in row or column [row_n,col_n] in the order of row-col-row-col-...,
    the first step start from row 0
    example:
    step:           1     2     3     4     5     6
    Row/Col:        R     C     R     C     R     C
    path:         [0,0] [2,0] [2,1] [3,1] [3,0] [1 0] 
    Then the path in list form is:[0,0,2,0,2,1,3,1,3,0,1,0]
    '''
    assert type(matrix) is list,'the input matrix is not a list type'
    Matrix=np.array(matrix)
    row_n=Matrix.shape[0]
    column_n=Matrix.shape[1]
    decode_list = []      # length of the ram
    decode_path = []      # length of the ram
    # paths in first step, [[0,1],[0,2],[0,3],[0,4]..] start from row num 0
    path_list=[[0,i] for i in range(row_n)]
    # get all possible path (5120 for ram=6)
    for step in range(2,ram+1):
        path_list=connect_path(path_list,row_n,column_n,step)

    for path in path_list:
        real_path=[]
        # change the path_list to real path coordinate etc [[0,0],[2,0],[2,1],[3,1],[3,0],[1 0]]
        for i in range(0,len(path),2):
            real_path.append([path[i],path[i+1]])
        # avoid choosing same item etc.0xe7 twice
        if not check_duplicate(real_path):
            item_list = []
            decode_path.append(real_path)
            for each_path in real_path:
                # get the item etc.0xe7 from Matrix according to the path [i,j]
                item_list.append(Matrix[each_path[0]][each_path[1]])
            decode_list.append(item_list)
    return decode_path,decode_list


# check if there are same items inside the code list
def check_duplicate(nlist):
    # flag for duplicate
    duplicate=False
    for j in range(len(nlist) - 1):
        for k in range(j + 1, len(nlist)):
            if nlist[j]==nlist[k]:
                duplicate=True
                break
        if duplicate:
            break
    return duplicate


# return all the possible path based on previous path
def connect_path(pathList,row_num,column_num,step):
    """
    :param pathList: input list contains all the path of first n-1 steps,shape:[maximum_n * steps]
    :param row_num: row number in the matrix
    :param column_num: column number in the matrix
    :param step: the current n step [1-6],should be int
    :return:
    """
    '''
        how to define the path
        In the matrix,choose num in row or column [row_n,col_n] in the order of row-col-row-col-...,
        the first step start from row 0
        example:
        step:           1     2     3     4     5     6
        Row/Col:        R     C     R     C     R     C
        path:         [0,0] [2,0] [2,1] [3,1] [3,0] [2 0] 
        Then the path in list form is:[0,0,2,0,2,1,3,1,3,0,2,0]
    '''
    new_path=[]
    # if step %2==1,choose num(etc.0xBD) from row
    if step % 2 == 1:
        for path in pathList:
            add_path = []
            col_index = path[-1]
            row_index = path[-2]
            for i in range(column_num):
                if i != col_index:
                    add_path=path+[row_index,i]
                    new_path.append(add_path)
                add_path=[]

    # if step %2==0,choose num(etc.0x1C) from column
    if step % 2 == 0:
        for path in pathList:
            add_path=[]
            col_index = path[-1]
            row_index = path[-2]
            for j in range(row_num):
                if j != row_index:
                    add_path=path+[j,col_index]
                    new_path.append(add_path)
                add_path=[]
    return new_path

def to_log(text, filename, path):
    """
    save  data to log file
    :param text:str text to write
    :param filename: filename end with .text .dat .log
    :param path: path to file
    :return: None
    """
    filepath=os.path.join(path,filename)
    with open(filepath, 'a') as f:
        f.write(text+'\n')
        f.close()







if __name__ == "__main__":
    start_time=time.time()
    # import one Code Matrix puzzle from the codeMatrix library (CodeMatrix_Bonus.py)
    CodeMatrix,Bonus=code_matrix_puzzle(1)
    # Ram:the maximum length of the code list 4/6
    Ram = 6
    Total_score=0
    path_evaluation={}
    full_path,full_list = decoding_matrix(CodeMatrix, Ram)
    for i in range(len(full_list)):
        score_1 = match_list(full_list[i], Bonus[0], 1)
        score_3 = match_list(full_list[i], Bonus[1], 3)
        score_5 = match_list(full_list[i], Bonus[2], 5)
        Total_score = score_1 + score_3 + score_5
        # index=full_list.index(route)
        path_evaluation[str(full_path[i])]=Total_score
    # find path with the score==9 or 8,6,5,4,3,1,0
    all_score=[]
    route_score9=list()
    route_score8=list()
    each_score=np.array([[9,8,6,5,4,3,1,0],
                         [0,0,0,0,0,0,0,0]])
    for (path,score) in path_evaluation.items():
        all_score.append(score)
        if score == 9:
            each_score[1][0]+=1
            route_score9.append(path)
        if score == 8:
            each_score[1][1] += 1
            route_score8.append(path)
        if score == 6:
            each_score[1][2]+=1
        if score == 5:
            each_score[1][3]+=1
        if score == 4:
            each_score[1][4]+=1
        if score == 3:
            each_score[1][5]+=1
        if score == 1:
            each_score[1][6]+=1
        if score == 0:
            each_score[1][7]+=1

    print("Successfully decode the CodeMatrix puzzle")
    end_time = time.time()
    print('The decode time:', '%8.2lf seconds' %(end_time - start_time))
    # print and save the routes wih score 8 and 9 to txt files
    filedir = os.getcwd()
    to_log('Routes with score 9:', 'route_score9.txt', filedir)
    to_log('Routes with score 8:', 'route_score8.txt', filedir)
    if len(route_score9)>0:
        print('Routes with score 9:')
        for route in route_score9:
            to_log(str(route),'route_score9.txt',filedir)
            print(route)

    if len(route_score8)>0:
        print('Routes with score 8:')
        for route in route_score8:
            to_log(str(route),'route_score8.txt',filedir)
            print(route)

    # plot bar image  of each score with routes counted
    print('The deciphered results:[score,'
          'routes]')
    print(each_score)
    x = np.arange(len(each_score[0]))  # the label locations
    width = 0.5  # the width of the bars
    fig, ax = plt.subplots()
    rects = ax.bar(x, each_score[1], width, label='route')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Scores')
    ax.set_ylabel('All_possible_routes')
    ax.set_title('cyberpunk2077_codeMatrix_decipher')
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(each_score[0])
    ax.legend()

    # auto label for bar plot,from examples in matplotlib official documents
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects)
    fig.tight_layout()
    plt.show()
    print('the end')