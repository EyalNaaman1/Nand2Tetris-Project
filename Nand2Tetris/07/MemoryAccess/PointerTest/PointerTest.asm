// C_PUSH constant
@3030
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// C_PUSH constant
@3040
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// C_PUSH constant
@32
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP this
@THIS
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// C_PUSH constant
@46
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP that
@THAT
D=M
@6
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// C_PUSH pointer 0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// C_PUSH this
@THIS
D=M
@2
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// C_PUSH that
@THAT
D=M
@6
A=D+A
D=M
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
