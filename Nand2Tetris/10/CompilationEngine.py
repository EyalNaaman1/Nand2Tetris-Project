"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer

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
        self.tokenizer = input_stream
        self.output_stream = output_stream
        self.indent_level = 0

        if hasattr(self.tokenizer, '_current_token') and self.tokenizer._current_token is None:
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()

    def _write_line(self, line: str) -> None:
        """Writes a line to the output stream with proper indentation."""
        indent = '  ' * self.indent_level
        self.output_stream.write(f"{indent}{line}\n")

    def _process(self, expected: str = None) -> None:
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

        xml_val = value
        if value == "<": xml_val = "&lt;"
        elif value == ">": xml_val = "&gt;"
        elif value == "&": xml_val = "&amp;"
        elif value == '"': xml_val = "&quot;"

        tag_map = {
            "KEYWORD": "keyword",
            "SYMBOL": "symbol",
            "IDENTIFIER": "identifier",
            "INT_CONST": "integerConstant",
            "STRING_CONST": "stringConstant"
        }
        tag = tag_map.get(token_type, "unknown")
        
        self._write_line(f"<{tag}> {xml_val} </{tag}>")

        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self._write_line("<class>")
        self.indent_level += 1

        self._process("class")
        self._process()
        self._process("{")

        while self.tokenizer.token_type() == "KEYWORD" and \
              self.tokenizer.keyword() in ["STATIC", "FIELD"]:
            self.compile_class_var_dec()

        while self.tokenizer.token_type() == "KEYWORD" and \
              self.tokenizer.keyword() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
            self.compile_subroutine()

        self._process("}")

        self.indent_level -= 1
        self._write_line("</class>")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self._write_line("<classVarDec>")
        self.indent_level += 1

        self._process()
        self._process()
        self._process()

        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self._process(",")
            self._process()

        self._process(";")

        self.indent_level -= 1
        self._write_line("</classVarDec>")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self._write_line("<subroutineDec>")
        self.indent_level += 1

        self._process()
        self._process()
        self._process()
        self._process("(")
        self.compile_parameter_list()
        self._process(")")

        self._write_line("<subroutineBody>")
        self.indent_level += 1
        
        self._process("{")
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "VAR":
            self.compile_var_dec()
        
        self.compile_statements()
        self._process("}")
        
        self.indent_level -= 1
        self._write_line("</subroutineBody>")

        self.indent_level -= 1
        self._write_line("</subroutineDec>")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'."""
        self._write_line("<parameterList>")
        self.indent_level += 1

        is_type = (self.tokenizer.token_type() == "KEYWORD") or \
                  (self.tokenizer.token_type() == "IDENTIFIER")
        
        if is_type:
            self._process()
            self._process()
            
            while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
                self._process(",")
                self._process()
                self._process()

        self.indent_level -= 1
        self._write_line("</parameterList>")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self._write_line("<varDec>")
        self.indent_level += 1

        self._process("var")
        self._process()
        self._process()

        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self._process(",")
            self._process()

        self._process(";")

        self.indent_level -= 1
        self._write_line("</varDec>")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing '{}'."""
        self._write_line("<statements>")
        self.indent_level += 1

        while self.tokenizer.token_type() == "KEYWORD":
            kw = self.tokenizer.keyword().upper()
            if kw == "LET": self.compile_let()
            elif kw == "IF": self.compile_if()
            elif kw == "WHILE": self.compile_while()
            elif kw == "DO": self.compile_do()
            elif kw == "RETURN": self.compile_return()
            else: break

        self.indent_level -= 1
        self._write_line("</statements>")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._write_line("<doStatement>")
        self.indent_level += 1
        self._process("do")
        self._process()
        
        if self.tokenizer.symbol() == ".":
            self._process(".")
            self._process()
            
        self._process("(")
        self.compile_expression_list()
        self._process(")")
        self._process(";")

        self.indent_level -= 1
        self._write_line("</doStatement>")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self._write_line("<letStatement>")
        self.indent_level += 1

        self._process("let")
        self._process()

        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "[":
            self._process("[")
            self.compile_expression()
            self._process("]")

        self._process("=")
        self.compile_expression()
        self._process(";")

        self.indent_level -= 1
        self._write_line("</letStatement>")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self._write_line("<whileStatement>")
        self.indent_level += 1

        self._process("while")
        self._process("(")
        self.compile_expression()
        self._process(")")
        self._process("{")
        self.compile_statements()
        self._process("}")

        self.indent_level -= 1
        self._write_line("</whileStatement>")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self._write_line("<returnStatement>")
        self.indent_level += 1

        self._process("return")
        
        if not (self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ";"):
            self.compile_expression()
            
        self._process(";")

        self.indent_level -= 1
        self._write_line("</returnStatement>")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self._write_line("<ifStatement>")
        self.indent_level += 1

        self._process("if")
        self._process("(")
        self.compile_expression()
        self._process(")")
        self._process("{")
        self.compile_statements()
        self._process("}")

        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "ELSE":
            self._process("else")
            self._process("{")
            self.compile_statements()
            self._process("}")

        self.indent_level -= 1
        self._write_line("</ifStatement>")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self._write_line("<expression>")
        self.indent_level += 1
        self.compile_term()

        ops = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in ops:
            self._process()
            self.compile_term()

        self.indent_level -= 1
        self._write_line("</expression>")

    def compile_term(self) -> None:
        """Compiles a term. Lookahead is required here."""
        self._write_line("<term>")
        self.indent_level += 1

        token_type = self.tokenizer.token_type()

        if token_type == "INT_CONST" or token_type == "STRING_CONST" or \
           (token_type == "KEYWORD" and self.tokenizer.keyword() in ["TRUE", "FALSE", "NULL", "THIS"]):
            self._process()
            
        elif token_type == "SYMBOL" and self.tokenizer.symbol() in {'-', '~', '^', '#'}:
            self._process()
            self.compile_term()
            
        elif token_type == "SYMBOL" and self.tokenizer.symbol() == "(":
            self._process("(")
            self.compile_expression()
            self._process(")")
            
        elif token_type == "IDENTIFIER":
            
            identifier = self.tokenizer.identifier()
            self._process()
            
            if self.tokenizer.token_type() == "SYMBOL":
                sym = self.tokenizer.symbol()
                
                if sym == "[":
                    self._process("[")
                    self.compile_expression()
                    self._process("]")
                    
                elif sym == "(":
                    self._process("(")
                    self.compile_expression_list()
                    self._process(")")
                    
                elif sym == ".":
                    self._process(".")
                    self._process()
                    self._process("(")
                    self.compile_expression_list()
                    self._process(")")
                
        self.indent_level -= 1
        self._write_line("</term>")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self._write_line("<expressionList>")
        self.indent_level += 1

        if not (self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")"):
            self.compile_expression()
            
            while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
                self._process(",")
                self.compile_expression()

        self.indent_level -= 1
        self._write_line("</expressionList>")