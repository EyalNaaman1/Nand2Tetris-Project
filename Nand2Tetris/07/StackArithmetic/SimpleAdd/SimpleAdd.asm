// C_PUSH constant
@7
D=A
@SP
AM=M+1
A=A-1
M=D
// C_PUSH constant
@8
D=A
@SP
AM=M+1
A=A-1
M=D
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
