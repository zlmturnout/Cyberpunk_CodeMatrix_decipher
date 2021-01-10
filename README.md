# Cyberpunk_CodeMatrix_decipher

## Main purpose:
There's one interesting puzzle-solving game in CyberPunk2077-"Breaching the Code Matrix" <br>
This commitment tend to find (all)  the best route（s） to solve these puzzle.<br>

    An example Follows:
```bash

    The code matrix               Buffer(6) -- -- -- -- -- --
       7A  55  55  55  7A  BD        Sequence required to upload
       1C  55  1C  55  7A  1C        ----------------------------
       BD  7A  7A  1C  7A  1C        7A  7A               Level1
       7A  55  E9  BD  55  7A        BD  1C  1C           Level2
       55  55  1C  E9  7A  7A        7A  1C  7A           Level3
       E9  1C  7A  7A  7A  7A
```
You need to find a route in the CodeMatrix box to acquire sequences which meet the required sequence, sequences with higher level means more bonus.<br>
you have 6 BUffer meaning you have six steps (choose one code each step,and one code can only be chosen once).<br>

## Define the Problem

```bash
To clarify the puzzle, let's add some position index and bonus into the matrix

    R/C 0   1   2   3   4   5
     0  7A  55  55  55  7A  BD        Sequence required to upload
     1  1C  55  1C  55  7A  1C        ----------------------------
     2  BD  7A  7A  1C  7A  1C        7A  7A               get 1 score
     3  7A  55  E9  BD  55  7A        BD  1C  1C           get 3 score
     4  55  55  1C  E9  7A  7A        7A  1C  7A           get 5 score
     5  E9  1C  7A  7A  7A  7A

how to define the route
    Rule:
    Inside the matrix,choose code in row or column [row_n,col_n] by the order of row-col-row-col-...,
    the first step start from row 0
    Position identifier such as [2,0] means the code in row 2 and column 0 was chosen (offcouse it start from 0-1-2-3...) 
    for example:
    step:           1     2     3     4     5     6
    Row/Col:        R     C     R     C     R     C
    path:         [0,5] [2,5] [2,3] [5,3] [5,1] [2,1] 
    choose:        BD     1C    1C    7A    1C    7A
    This path in list form is:[0,5,2,5,2,3,5,3,5,1,2,1]
    Bonus:by this route, you finished uploading two sequence BD-1C-1C and 7A-1C-7A, and get 8 (3+5) scores! 
 ```
* Now the question comes: can we find a best route to obtain more bonus (more scores,9 at maximum)
 `Roughly estimate all the possible routes:`<br>
 * for a 6X6 Code Matrix with 6 buffers:<br> 
        6*5*5*5*5*5=18750
        less than 18750 routes,since you can't choose one code twice
 
 
