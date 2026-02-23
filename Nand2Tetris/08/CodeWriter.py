"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")

        self._output_stream = output_stream
        self._label_counter = 0
        self._current_file_name = None
        
        self._arithmetic_commands = {
            "add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not",
            "shiftleft", "shiftright"}
        
        self._segment_pointers = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
        self._current_func = "null"

        self._temp_segment_base_address = 5
        self._static_segment_base_address = 16


    def write_init(self) -> None:
        """Writes the assembly code that initializes the VM translator.
        """
        self._output_stream.write(
            "// Bootstrap code\n"
            "@256\n"
            "D=A\n"
            "@SP\n"
            "M=D\n"
        )
        self._current_func = "Sys.init"
        self.write_call("Sys.init", 0)


    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self._current_file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!

        if command in self._arithmetic_commands:
            if command == "add":
                self._output_stream.write(
                    "// add\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "A=A-1\n"
                    "M=M+D\n"
                )
            elif command == "sub":
                self._output_stream.write(
                    "// sub\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "A=A-1\n"
                    "M=M-D\n"
                )
            elif command == "neg":
                self._output_stream.write(
                    "// neg\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=-M\n"
                )
            elif command == "eq":
                label_true = f"EQ_TRUE_{self._label_counter}"
                label_end = f"EQ_END_{self._label_counter}"
                self._label_counter += 1
                self._output_stream.write(
                    f"// eq\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "A=A-1\n"
                    "D=M-D\n"
                    f"@{label_true}\n"
                    "D;JEQ\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=0\n"
                    f"@{label_end}\n"
                    "0;JMP\n"
                    f"({label_true})\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=-1\n"
                    f"({label_end})\n"
                )
            elif command == "gt":
                label_x_poz = f"X_POZ_{self._label_counter}"
                label_end = f"END_{self._label_counter}"
                label_false = f"FALSE_{self._label_counter}"
                label_true = f"TRUE_{self._label_counter}"
                label_same_sign = f"SAME_SIGN{self._label_counter}"
                self._label_counter += 1
                self._output_stream.write(
                    f"// gt\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "@R13\n"
                    "M=D\n"
                    "@SP\n"
                    "A=M-1\n"
                    "D=M\n"
                    "@R14\n"
                    "M=D\n"
                    "D=M\n"
                    f"@{label_x_poz}\n"
                    "D;JGT\n"
                    "@R13\n"
                    "D=M\n"
                    f"@{label_false}\n"
                    "D;JGT\n"
                    f"@{label_same_sign}\n"
                    "0;JMP\n"
                    f"({label_x_poz})\n"
                    "@R13\n"
                    "D=M\n"
                    f"@{label_true}\n"
                    "D;JLT\n"
                    f"({label_same_sign})\n"
                    "@R14\n"
                    "D=M\n"
                    "@R13\n"
                    "D=D-M\n"
                    f"@{label_true}\n"
                    "D;JGT\n"
                    f"({label_false})\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=0\n"
                    f"@{label_end}\n"
                    "0;JMP\n"
                    f"({label_true})\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=-1\n"
                    f"({label_end})\n"
                )
            elif command == "lt":
                label_x_poz = f"X_POZ_{self._label_counter}"
                label_end = f"END_{self._label_counter}"
                label_false = f"FALSE_{self._label_counter}"
                label_true = f"TRUE_{self._label_counter}"
                label_same_sign = f"SAME_SIGN{self._label_counter}"
                self._label_counter += 1
                self._output_stream.write(
                    f"// lt\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "@R14\n"
                    "M=D\n"
                    "@SP\n"
                    "A=M-1\n"
                    "D=M\n"
                    "@R13\n"
                    "M=D\n"
                    "D=M\n"
                    f"@{label_x_poz}\n"
                    "D;JGT\n"
                    "@R14\n"
                    "D=M\n"
                    f"@{label_true}\n"
                    "D;JGT\n"
                    f"@{label_same_sign}\n"
                    "0;JMP\n"
                    f"({label_x_poz})\n"
                    "@R14\n"
                    "D=M\n"
                    f"@{label_false}\n"
                    "D;JLT\n"
                    f"({label_same_sign})\n"
                    "@R14\n"
                    "D=M\n"
                    "@R13\n"
                    "D=D-M\n"
                    f"@{label_true}\n"
                    "D;JGT\n"
                    f"({label_false})\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=0\n"
                    f"@{label_end}\n"
                    "0;JMP\n"
                    f"({label_true})\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=-1\n"
                    f"({label_end})\n"
                )
            elif command == "and":
                self._output_stream.write(
                    "// and\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "A=A-1\n"
                    "M=D&M\n"
                )
            elif command == "or":
                self._output_stream.write(
                    "// or\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "A=A-1\n"
                    "M=D|M\n"
                )
            elif command == "not":
                self._output_stream.write(
                    "// not\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=!M\n"
                )
            elif command == "shiftleft":
                self._output_stream.write(
                    "// shiftleft\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=M<<\n"
                )
            elif command == "shiftright":
                self._output_stream.write(
                    "// shiftright\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=M>>\n"
                )

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        segment_pointer_segments = {
            "local", "argument", "this", "that"
        }

        if command == "C_PUSH":
            if segment == "constant":
                self._output_stream.write(
                    "// C_PUSH constant\n"
                    f"@{index}\n"
                    "D=A\n"
                    "@SP\n"
                    "AM=M+1\n"
                    "A=A-1\n"
                    "M=D\n"
                )
            elif segment in segment_pointer_segments:
                self._output_stream.write(
                    f"// C_PUSH {segment}\n"
                    f"@{self._segment_pointers[segment]}\n"
                    "D=M\n"
                    f"@{index}\n"
                    "A=D+A\n"
                    "D=M\n"
                    "@SP\n"
                    "AM=M+1\n"
                    "A=A-1\n"
                    "M=D\n"
                )
            elif segment == "temp":
                self._output_stream.write(
                    f"// C_PUSH temp\n"
                    f"@{self._temp_segment_base_address + index}\n"
                    "D=M\n"
                    "@SP\n"
                    "AM=M+1\n"
                    "A=A-1\n"
                    "M=D\n"
                )
            elif segment == "static":
                self._output_stream.write(
                    f"// C_PUSH static\n"
                    f"@{self._current_file_name}.{index}\n"
                    "D=M\n"
                    "@SP\n"
                    "AM=M+1\n"
                    "A=A-1\n"
                    "M=D\n"
                )
            elif segment == "pointer":
                address = "THIS" if index == 0 else "THAT"
                self._output_stream.write(
                    f"// C_PUSH pointer {index}\n"
                    f"@{address}\n"
                    "D=M\n"
                    "@SP\n"
                    "AM=M+1\n"
                    "A=A-1\n"
                    "M=D\n")

        elif command == "C_POP":
            if segment in segment_pointer_segments:
                self._output_stream.write(
                    f"// C_POP {segment}\n"
                    f"@{self._segment_pointers[segment]}\n"
                    "D=M\n"
                    f"@{index}\n"
                    "D=D+A\n"
                    "@R13\n"
                    "M=D\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "@R13\n"
                    "A=M\n"
                    "M=D\n"
                )
            elif segment == "temp":
                self._output_stream.write(
                    f"// C_POP temp\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    f"@{self._temp_segment_base_address + index}\n"
                    "M=D\n"
                )
            elif segment == "static":
                self._output_stream.write(
                    f"// C_POP static\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    f"@{self._current_file_name}.{index}\n"
                    "M=D\n"
                )
            elif segment == "pointer":
                address = "THIS" if index == 0 else "THAT"
                self._output_stream.write(
                    f"// C_POP pointer {index}\n"
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    f"@{address}\n"
                    "M=D\n"
                )


    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self._output_stream.write(
            "// write_label\n"
            f"({self._current_func}${label})\n"
        )


    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self._output_stream.write(
            "// write_goto\n"
            f"@{self._current_func}${label}\n"
            "0;JMP\n"
        )


    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self._output_stream.write(
            "// write_if_goto\n"
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{self._current_func}${label}\n"
            "D;JNE\n"
        )


    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self._current_func = function_name

        self._output_stream.write(f"// function {function_name} {n_vars}\n")
        self._output_stream.write(f"({function_name})\n")
        push_zero_assembly = (
            "@SP\n"
            "A=M\n"
            "M=0\n"
            "@SP\n"
            "M=M+1\n"
        )
        self._output_stream.write(push_zero_assembly * n_vars)


    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        return_label = f"{self._current_func}$ret.{self._label_counter}"
        self._label_counter += 1

        self._output_stream.write(
            f"@{return_label}\n"
            "D=A\n"
            "@SP\n"
            "AM=M+1\n"
            "A=A-1\n"
            "M=D\n")

        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self._output_stream.write(
                f"@{segment}\n"
                "D=M\n"
                "@SP\n"
                "AM=M+1\n"
                "A=A-1\n"
                "M=D\n")

        num_to_subtract = 5 + n_args
        self._output_stream.write(
            f"@{num_to_subtract}\n"
            "D=A\n"
            "@SP\n"
            "D=M-D\n"
            "@ARG\n"
            "M=D\n")

        self._output_stream.write(
            "@SP\n"
            "D=M\n"
            "@LCL\n"
            "M=D\n")

        self._output_stream.write(
            f"@{function_name}\n"
            "0;JMP\n")

        self._output_stream.write(f"({return_label})\n")


    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address

        # FRAME = LCL
        self._output_stream.write(
            "@LCL\n"
            "D=M\n"
            "@R13\n"
            "M=D\n")

        # RET = *(FRAME-5)
        self._output_stream.write(
            "@5\n"
            "A=D-A\n"
            "D=M\n"
            "@R14\n"
            "M=D\n")

        # *ARG = pop()
        self._output_stream.write(
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "@ARG\n"
            "A=M\n"
            "M=D\n")

        # SP = ARG + 1
        self._output_stream.write(
            "@ARG\n"
            "D=M+1\n"
            "@SP\n"
            "M=D\n")
        # THAT = *(FRAME-1)
        # THIS = *(FRAME-2)
        # ARG  = *(FRAME-3)
        # LCL  = *(FRAME-4)
        i = 1
        for segment in ["THAT", "THIS", "ARG", "LCL"]:
            self._output_stream.write(
                "@R13\n"
                "D=M\n"
                f"@{i}\n"
                "A=D-A\n"
                "D=M\n"
                f"@{segment}\n"
                "M=D\n")
            i+=1

        self._output_stream.write(
            "@R14\n"
            "A=M\n"
            "0;JMP\n")
