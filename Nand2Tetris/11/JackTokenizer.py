"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    KEYWORDS = {"class", "constructor", "function", "method", "field", 
                "static", "var", "int", "char", "boolean", "void", "true",
                "false", "null", "this", "let", "do", "if", "else", 
                "while", "return"}
    
    SYMBOLS = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', 
               '-', '*', '/', '&', '|', '<', '>', '=', '~', '^', '#'}
    
    
    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        input_text = input_stream.read()
        cleaned_text = self._preprocess_text(input_text)
        self._tokens = self._tokenize(cleaned_text)

        self._token_index = -1
        self._current_token = None

    def _preprocess_text(self, input_text: str) -> str:
        result = []
        in_block_comment = False
        in_line_comment = False

        num_of_chars = len(input_text)
        i = 0

        while i < num_of_chars:
            char = input_text[i]

            if in_block_comment:
                if char == '*' and i + 1 < num_of_chars and input_text[i + 1] == '/':
                    in_block_comment = False
                    i += 2
                    continue
                i += 1
                continue
        
            if in_line_comment:
                if char == '\n':
                    in_line_comment = False
                i += 1
                continue
        
            if char == '/' and i + 1 < num_of_chars and input_text[i + 1] == '*':
                in_block_comment = True
                i += 2
                continue
        
            if char == '/' and i + 1 < num_of_chars and input_text[i + 1] == '/':
                in_line_comment = True
                i += 2
                continue
        
            if char.isspace():
                if not result or not result[-1].isspace():
                    result.append(' ')
            else:
                result.append(char)
            
            i += 1
        return "".join(result).strip()

    def _tokenize(self, cleaned_text: str) -> list[str]:
        tokens = []
        current_token = ""
        num_of_chars = len(cleaned_text)
        i = 0
        
        while i < num_of_chars:
            char = cleaned_text[i]
            if char == '"':
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                
                end_quote_index = cleaned_text.find('"', i + 1)
                
                if end_quote_index == -1:
                    raise SyntaxError("Unclosed string constant")
                
                tokens.append(cleaned_text[i:end_quote_index + 1])
                
                i = end_quote_index + 1
                continue
            
            if char in self.SYMBOLS:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                
                tokens.append(char)
                i += 1
                continue
                
            if char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                i += 1
                continue
            
            current_token += char
            i += 1

        if current_token:
            tokens.append(current_token)
            
        return tokens

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        return self._token_index < len(self._tokens) - 1

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        if self.has_more_tokens():
            self._token_index += 1
            self._current_token = self._tokens[self._token_index]

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        # Your code goes here!
        token = self._current_token
        if token is None:
            return None
        if token in self.KEYWORDS:
            return "KEYWORD"
        
        if token in self.SYMBOLS:
            return "SYMBOL"

        if token.startswith('"') and token.endswith('"'):
            return "STRING_CONST"
        
        if token.isdigit():
            return "INT_CONST"
        
        return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        if self.token_type() == "KEYWORD":
            return self._current_token.upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        # Your code goes here!
        if self.token_type() == "SYMBOL":
            return self._current_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        # Your code goes here!
        if self.token_type() == "IDENTIFIER":
            return self._current_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        # Your code goes here!
        if self.token_type() == "INT_CONST":
            return int(self._current_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # Your code goes here!
        if self.token_type() == "STRING_CONST":
            return self._current_token[1:-1]