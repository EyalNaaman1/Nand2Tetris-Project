// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.
    //check valid R15(len)
    @R15
    D=M
    @END
    D-1;JLE

    //inits max and min and i=0 (the offset)
    @R14
    A=M
    D=M
    @maxval
    M=D
    @R14
    D=M
    @maxadd
    M=D

    @R14
    A=M
    D=M
    @minval
    M=D
    @R14
    D=M
    @minadd
    M=D

    @i
    M=1
//the loop that check each line if there is new max or min
(LOOPLINE)
    //the offset calc + check new max
    @i
    D=M
    @R14
    A=M
    A=A+D
    D=M
    @maxval
    D=D-M
    @CHANGEMAX
    D;JGT

    //the offset calc + check new min
    @i
    D=M
    @R14
    A=M
    A=A+D
    D=M
    @minval
    D=D-M
    @CHANGEMIN
    D;JLT
(HERE)
    //here we check for end of the arr + i=i+1
    @R15
    D=M
    @i
    M=M+1
    D=D-M
    @LOOPLINE
    D;JGT
    @SWAP
    0;JMP

(CHANGEMAX)
    //here we change the maxval to the new one
    @i
    D=M
    @R14
    A=M
    A=A+D
    D=M
    @maxval
    M=D

    //here we change the maxadd to the new one
    @i
    D=M
    @R14
    A=M
    A=A+D
    D=A
    @maxadd
    M=D
    //get back to work...
    @HERE
    0;JMP

(CHANGEMIN)
    //here we change the minval to the new one
    @i
    D=M
    @R14
    A=M
    A=A+D
    D=M
    @minval
    M=D

    //here we change the minadd to the new one
    @i
    D=M
    @R14
    A=M
    A=A+D
    D=A
    @minadd
    M=D
    //get back to work...
    @HERE
    0;JMP

(SWAP)
    //when we finish we do here the final step- switch min-max
    @maxval
    D=M
    @minadd
    A=M
    M=D
    @minval
    D=M
    @maxadd
    A=M
    M=D
    @END
    0;JMP
    
(END)
    @END
    0;JMP