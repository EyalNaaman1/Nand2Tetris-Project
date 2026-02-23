"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        input_lines = input_file.read().splitlines()
        cleaned_lines = []
        for line in input_lines:
            line = self._remove_comments_and_whitespace(line)
            if line:
                cleaned_lines.append(line)
        self._commands = cleaned_lines
        self._current_index = -1
        self._current_command = None
        pass

    def _remove_comments_and_whitespace(self, line: str) -> str:
        if '//' in line:
            line = line[:line.index('//')]

        line = line.strip().upper()
        line = line.replace(' ', '').replace('\t', '')

        return line

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return len(self._commands) -1 > self._current_index

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.has_more_commands():
            self._current_index += 1
            self._current_command = self._commands[self._current_index]

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self._current_command.startswith('@'):
            return "A_COMMAND"
        elif self._current_command.startswith('(') and self._current_command.endswith(')'):
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or
            "L_COMMAND".
        """
        if self.command_type() == "A_COMMAND":
            return self._current_command[1:]
        elif self.command_type() == "L_COMMAND":
            return self._current_command[1:-1]
        pass

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND":
            if '=' in self._current_command:
                return self._current_command.split('=')[0]
            else:
                return ''
        pass

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND":
            if '=' in self._current_command:
                return self._current_command.split('=')[1].split(';')[0]
            elif ';' in self._current_command:
                return self._current_command.split(';')[0]
            else:
                return ''
        pass

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND":
            if ';' in self._current_command:
                return self._current_command.split(';')[1]
            else:
                return ''
        pass

    def get_current_index(self) -> int:
        """Returns the current index of the parser in the command list.

        Returns:
            int: the current index.
        """
        return self._current_index

    def reset(self):
        self._current_index = -1
        self._current_command = None