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
// C_POP pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// C_PUSH constant
@0
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP that
@THAT
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
@1
D=A
@SP
AM=M+1
A=A-1
M=D
// C_POP that
@THAT
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
// C_PUSH argument
@ARG
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
// C_PUSH constant
@2
D=A
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
// C_POP argument
@ARG
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
// write_label
(null$MAIN_LOOP_START)
// C_PUSH argument
@ARG
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
// write_if_goto
@SP
AM=M-1
D=M
@null$COMPUTE_ELEMENT
D;JNE
// write_goto
@null$END_PROGRAM
0;JMP
// write_label
(null$COMPUTE_ELEMENT)
// C_PUSH that
@THAT
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
@1
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
// C_PUSH pointer 1
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
// C_PUSH constant
@1
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
// C_POP pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// C_PUSH argument
@ARG
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
// C_PUSH constant
@1
D=A
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
// C_POP argument
@ARG
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
// write_goto
@null$MAIN_LOOP_START
0;JMP
// write_label
(null$END_PROGRAM)
