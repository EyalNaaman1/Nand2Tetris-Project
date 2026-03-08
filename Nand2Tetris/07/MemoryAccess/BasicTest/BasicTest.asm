// C_PUSH constant
@10
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP local
@LCL
D=M
@0
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
@21
D=A
@SP
AM=M+1
A=A-1
M=D
// C_PUSH constant
@22
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP argument
@ARG
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
// C_POP argument
@ARG
D=M
@1
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
@36
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP this
@THIS
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
// C_PUSH constant
@42
D=A
@SP
AM=M+1
A=A-1
M=D
// C_PUSH constant
@45
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP that
@THAT
D=M
@5
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// C_POP that
@THAT
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
@510
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP temp
@SP
AM=M-1
D=M
@11
M=D
// C_PUSH local
@LCL
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
// C_PUSH that
@THAT
D=M
@5
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
// C_PUSH argument
@ARG
D=M
@1
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
// C_PUSH this
@THIS
D=M
@6
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
// C_PUSH this
@THIS
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
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// C_PUSH temp
@11
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
