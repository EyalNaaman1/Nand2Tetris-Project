"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
    input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    parser = Parser(input_file)
    symbol_table = SymbolTable()
    first_pass(parser, symbol_table)
    parser.reset()
    second_pass(parser, symbol_table)
    parser.reset()
    convert_to_binary(parser, symbol_table, output_file)

    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")

def first_pass(parser: Parser, symbol_table: SymbolTable) -> None:
    rom_address = 0
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == "A_COMMAND" or command_type == "C_COMMAND":
            rom_address += 1
        elif command_type == "L_COMMAND":
            symbol = parser.symbol()
            symbol_table.add_entry(symbol, rom_address)

def second_pass(parser: Parser, symbol_table: SymbolTable) -> None:
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "A_COMMAND":
            symbol = parser.symbol()
            if not symbol_table.contains(symbol):
                if not symbol.isdigit():
                    symbol_table.add_entry(
                        symbol, symbol_table.get_next_available_address())
                    symbol_table.increment_next_available_address()

def convert_to_binary(parser: Parser, symbol_table: SymbolTable, output_file: typing.TextIO) -> None:
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "A_COMMAND":
            symbol = parser.symbol()
            if symbol.isdigit():
                address = int(symbol)
            else:
                address = symbol_table.get_address(symbol)
            binary_code = '0' + format(address, '015b')
            output_file.write(binary_code + '\n')
        elif parser.command_type() == "C_COMMAND":
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()
            comp_bits = Code.comp(comp)
            dest_bits = Code.dest(dest)
            jump_bits = Code.jump(jump)
            binary_code = comp_bits + dest_bits + jump_bits
            output_file.write(binary_code + '\n')

if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)