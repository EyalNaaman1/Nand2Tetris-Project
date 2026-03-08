// C_PUSH constant
@111
D=A
@SP
AM=M+1
A=A-1
M=D
// C_PUSH constant
@333
D=A
@SP
AM=M+1
A=A-1
M=D
// C_PUSH constant
@888
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP static
@SP
AM=M-1
D=M
@StaticTest.8
M=D
// C_POP static
@SP
AM=M-1
D=M
@StaticTest.3
M=D
// C_POP static
@SP
AM=M-1
D=M
@StaticTest.1
M=D
// C_PUSH static
@StaticTest.3
D=M
@SP
AM=M+1
A=A-1
M=D
// C_PUSH static
@StaticTest.1
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
// C_PUSH static
@StaticTest.8
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
