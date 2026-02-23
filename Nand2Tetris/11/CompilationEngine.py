"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.vm_writer = VMWriter(output_stream)
        self.symbol_table = SymbolTable()
        self.tokenizer = input_stream
        self.class_name = ""
        self.label_counter = 0

        if hasattr(self.tokenizer, '_current_token') and self.tokenizer._current_token is None:
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()

    def _get_unique_label(self, suffix: str) -> str:
        self.label_counter += 1
        return f"LABEL_{self.label_counter}_{suffix}"

    def _process(self, expected: str = None) -> str:
        """
        Processes the current token, writes it to the output stream in XML
        format, and advances to the next token. If 'expected' is provided, it
        checks that the current token matches the expected value.
        """
        token_type = self.tokenizer.token_type()
        value = ""

        if token_type == "KEYWORD":
            value = self.tokenizer.keyword().lower()
        elif token_type == "SYMBOL":
            value = self.tokenizer.symbol()
        elif token_type == "IDENTIFIER":
            value = self.tokenizer.identifier()
        elif token_type == "INT_CONST":
            value = str(self.tokenizer.int_val())
        elif token_type == "STRING_CONST":
            value = self.tokenizer.string_val()

        if expected and value != expected:
             raise SyntaxError(f"Expected {expected} but got {value}")

        # if value == "<": xml_val = "&lt;"
        # elif value == ">": xml_val = "&gt;"
        # elif value == "&": xml_val = "&amp;"
        # elif value == '"': xml_val = "&quot;"

        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

        return value

    def compile_class(self) -> None:
        """Compiles a complete class."""

        self._process("class")
        self.class_name = self._process()
        self._process("{")

        while self.tokenizer.token_type() == "KEYWORD" and \
                self.tokenizer.keyword() in ["STATIC", "FIELD"]:
            self.compile_class_var_dec()

        while self.tokenizer.token_type() == "KEYWORD" and \
              self.tokenizer.keyword() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
            self.compile_subroutine()

        self._process("}")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        var_kind = self._process().upper()  # "static" or "field"
        var_type = self._process()  # type
        var_name = self._process()  # varName
        self.symbol_table.define(var_name, var_type, var_kind)

        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self._process(",")
            var_name = self._process()
            self.symbol_table.define(var_name, var_type, var_kind)

        self._process(";")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self.symbol_table.start_subroutine()
        subroutine_kind = self._process().upper()  # "constructor" | "function" | "method"
        self._process()  # return type
        subroutine_name = self._process() # subroutineName

        self._process("(")
        if subroutine_kind == "METHOD":
            self.symbol_table.define("this", self.class_name, "ARG")
        self.compile_parameter_list()
        self._process(")")
        
        self._process("{")
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "VAR":
            self.compile_var_dec()
        
        num_locals = self.symbol_table.var_count("VAR")
        full_subroutine_name = f"{self.class_name}.{subroutine_name}"
        self.vm_writer.write_function(full_subroutine_name, num_locals)
        if subroutine_kind == "METHOD":
            self.vm_writer.write_push("argument", 0)
            self.vm_writer.write_pop("pointer", 0)
        elif subroutine_kind == "CONSTRUCTOR":
            num_fields = self.symbol_table.var_count("FIELD")
            self.vm_writer.write_push("constant", num_fields)
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("pointer", 0)
        self.compile_statements()
        self._process("}")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'."""

        is_type = (self.tokenizer.token_type() == "KEYWORD") or (self.tokenizer.token_type() == "IDENTIFIER")
        
        if is_type:
            type = self._process()
            name = self._process()
            self.symbol_table.define(name, type, "ARG")
            
            while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
                self._process(",")
                type = self._process()
                name = self._process()
                self.symbol_table.define(name, type, "ARG")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""

        self._process("var")
        var_type = self._process()
        var_name = self._process()
        self.symbol_table.define(var_name, var_type, "VAR")

        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self._process(",")
            var_name = self._process()
            self.symbol_table.define(var_name, var_type, "VAR")
        self._process(";")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing '{}'."""

        while self.tokenizer.token_type() == "KEYWORD":
            kw = self.tokenizer.keyword()
            if kw == "LET": self.compile_let()
            elif kw == "IF": self.compile_if()
            elif kw == "WHILE": self.compile_while()
            elif kw == "DO": self.compile_do()
            elif kw == "RETURN": self.compile_return()
            else: break

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._process("do")
        name = self._process()
        
        n_args = 0
        full_subroutine_name = ""

        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ".":
            self._process(".")
            sub_name = self._process()

            type_of_var = self.symbol_table.type_of(name)
            
            if type_of_var is not None:
                kind = self.symbol_table.kind_of(name)
                index = self.symbol_table.index_of(name)
                self.vm_writer.write_push(self.symbol_table.memory_segments[kind], index)
                
                full_subroutine_name = f"{type_of_var}.{sub_name}"
                n_args = 1
            else:
                full_subroutine_name = f"{name}.{sub_name}"
                n_args = 0
                
        else:
            self.vm_writer.write_push("pointer", 0)
            full_subroutine_name = f"{self.class_name}.{name}"
            n_args = 1

        self._process("(")
        n_args += self.compile_expression_list()
        self._process(")")
        self._process(";")

        self.vm_writer.write_call(full_subroutine_name, n_args)
        self.vm_writer.write_pop("temp", 0)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self._process("let")
        var_name = self._process()
        is_array = False

        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "[":
            is_array = True
            self._process("[")
            self.compile_expression()
            self._process("]")
            kind = self.symbol_table.kind_of(var_name)
            index = self.symbol_table.index_of(var_name)
            self.vm_writer.write_push(self.symbol_table.memory_segments[kind], index)
            self.vm_writer.write_arithmetic("ADD")

        self._process("=")
        self.compile_expression()
        self._process(";")

        if is_array:
            self.vm_writer.write_pop("temp", 0)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("temp", 0)
            self.vm_writer.write_pop("that", 0)
        else:
            kind = self.symbol_table.kind_of(var_name)
            index = self.symbol_table.index_of(var_name)
            self.vm_writer.write_pop(self.symbol_table.memory_segments[kind], index)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        start_label = self._get_unique_label("WHILE_START")
        end_label = self._get_unique_label("WHILE_END")

        self.vm_writer.write_label(start_label)
        self._process("while")
        self._process("(")
        self.compile_expression()
        self._process(")")

        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if(end_label)

        self._process("{")
        self.compile_statements()
        self._process("}")

        self.vm_writer.write_goto(start_label)
        self.vm_writer.write_label(end_label)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self._process("return")
        
        if not (self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ";"):
            self.compile_expression()
        else:
            self.vm_writer.write_push("constant", 0)
            
        self._process(";")
        self.vm_writer.write_return()

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        true_label = self._get_unique_label("IF_TRUE")
        false_label = self._get_unique_label("IF_FALSE")
        end_label = self._get_unique_label("IF_END")

        self._process("if")
        self._process("(")
        self.compile_expression()
        self._process(")")

        self.vm_writer.write_if(true_label)
        self.vm_writer.write_goto(false_label)
        
        self.vm_writer.write_label(true_label)
        self._process("{")
        self.compile_statements()
        self._process("}")

        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "ELSE":
            self.vm_writer.write_goto(end_label)
            self.vm_writer.write_label(false_label)
            self._process("else")
            self._process("{")
            self.compile_statements()
            self._process("}")
            self.vm_writer.write_label(end_label)
        else:
            self.vm_writer.write_label(false_label)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term()

        ops = {'+': 'ADD', '-': 'SUB', '*': None, '/': None,
               '&': 'AND', '|': 'OR', '<': 'LT', '>': 'GT', '=': 'EQ'}
        
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in ops:
            op = self._process()
            self.compile_term()

            if op == '*':
                self.vm_writer.write_call("Math.multiply", 2)
            elif op == '/':
                self.vm_writer.write_call("Math.divide", 2)
            else:
                self.vm_writer.write_arithmetic(ops[op])

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine handles all the base cases of expressions:
        constants, variable access, array access, subroutine calls, etc.
        """
        token_type = self.tokenizer.token_type()

        if token_type == "INT_CONST":
            val = self._process()
            self.vm_writer.write_push("constant", int(val))

        elif token_type == "STRING_CONST":
            string_val = self._process()
            self.vm_writer.write_push("constant", len(string_val))
            self.vm_writer.write_call("String.new", 1)
            for char in string_val:
                self.vm_writer.write_push("constant", ord(char))
                self.vm_writer.write_call("String.appendChar", 2)

        elif token_type == "KEYWORD":
            kw = self._process()
            if kw == "true":
                self.vm_writer.write_push("constant", 0)
                self.vm_writer.write_arithmetic("NOT")
            elif kw == "false" or kw == "null":
                self.vm_writer.write_push("constant", 0)
            elif kw == "this":
                self.vm_writer.write_push("pointer", 0)

        elif token_type == "SYMBOL" and self.tokenizer.symbol() in {'-', '~', '^', '#'}:
            op = self._process()
            self.compile_term()
            
            if op == '-':
                self.vm_writer.write_arithmetic("NEG")
            elif op == '~':
                self.vm_writer.write_arithmetic("NOT")
            elif op == '^': 
                self.vm_writer.write_arithmetic("SHIFTLEFT")
            elif op == '#':
                self.vm_writer.write_arithmetic("SHIFTRIGHT")

        elif token_type == "SYMBOL" and self.tokenizer.symbol() == "(":
            self._process("(")
            self.compile_expression()
            self._process(")")

        elif token_type == "IDENTIFIER":
            name = self._process()
            next_token = None
            if self.tokenizer.token_type() == "SYMBOL":
                next_token = self.tokenizer.symbol()

            if next_token == "[":
                self._process("[")
                
                kind = self.symbol_table.kind_of(name)
                index = self.symbol_table.index_of(name)
                self.vm_writer.write_push(self.symbol_table.memory_segments[kind], index)
                
                self.compile_expression()
                self._process("]")
                
                self.vm_writer.write_arithmetic("ADD")

                self.vm_writer.write_pop("pointer", 1) 
                self.vm_writer.write_push("that", 0)

            elif next_token == "(" or next_token == ".":
                full_subroutine_name = ""
                n_args = 0
                
                if next_token == ".":
                    self._process(".")
                    sub_name = self._process()
                    
                    type_of_var = self.symbol_table.type_of(name)
                    
                    if type_of_var is not None: 
                        kind = self.symbol_table.kind_of(name)
                        index = self.symbol_table.index_of(name)
                        self.vm_writer.write_push(self.symbol_table.memory_segments[kind], index)
                        full_subroutine_name = f"{type_of_var}.{sub_name}"
                        n_args = 1
                    else:
                        full_subroutine_name = f"{name}.{sub_name}"
                        n_args = 0
                
                elif next_token == "(":
                    self._process("(")
                    self.vm_writer.write_push("pointer", 0)
                    full_subroutine_name = f"{self.class_name}.{name}"
                    n_args = 1

                if next_token == "(": 
                     self._process("(")
                else:
                     self._process("(")
                     
                n_args += self.compile_expression_list()
                self._process(")")
                
                self.vm_writer.write_call(full_subroutine_name, n_args)
                
            else:
                kind = self.symbol_table.kind_of(name)
                index = self.symbol_table.index_of(name)
                self.vm_writer.write_push(self.symbol_table.memory_segments[kind], index)

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        count = 0
        if not (self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")"):
            self.compile_expression()
            count += 1
            while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
                self._process(",")
                self.compile_expression()
                count += 1
        return count