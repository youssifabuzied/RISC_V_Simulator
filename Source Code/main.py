import numpy as np
import pandas as pd

Labels = []
Labels_map = {}
instructions = []
intructions_tokens = []
instructions_map = {}
memory = {}
pc = 0
registers = {}
RegNames = {}
stack = {}


def binary_to_decimal_unsigned(binary):
    """
    Converts a 32-bit unsigned binary number to its decimal value.
    """
    decimal = 0
    for i in range(31, -1, -1):
        if binary[i] == '1':
            decimal += 2 ** (31 - i)
    return decimal


def binary_to_decimal(bin_str):
    # Convert the binary string to a signed integer using int()
    num = int(bin_str, 2)

    # If the most significant bit (MSB) is 1, the number is negative
    if num & 0x80000000:
        # Convert the number to its two's complement representation
        num = -((num ^ 0xFFFFFFFF) + 1)

    return num


def signed_integer_to_binary(num: int) -> str:
    if num >= 0:
        # Convert positive numbers to binary
        binary = bin(num)[2:].zfill(32)
    else:
        # Convert negative numbers to two's complement binary
        binary = bin((1 << 32) + num)[2:]
    if (len(binary) < 32):
        binary = '0' * (32 - len(binary)) + binary

    return binary


def read_code_file(path):
    file = open(path, "r")
    lines = file.readlines()
    global pc
    global Labels
    global instructions

    for l in lines:
        l = l.strip()
        if (l == "\n"):
            continue
        if (':' in l):
            testLine = l.split(":")
            label = testLine[0].replace(" ", "").replace("\t", "")
            # print(label)
            Labels.append({"Name": label, "Address": pc})
            testLine[1] = testLine[1].replace("\n", "")

            if (len(testLine) > 1 and testLine[1] != '' and testLine[1] != testLine[1][0] * len(testLine[1])):
                starting = 0
                for c in testLine[1]:
                    if (c != " "):
                        break
                    else:
                        starting += 1
                instructions.append({"instruction": testLine[1][starting:], "Address": pc})
            else:
                pc -= 4
        else:
            starting = 0
            for c in l:
                if (c != " "):
                    break
                else:
                    starting += 1
            instructions.append({"instruction": l[starting:], "Address": pc})
        pc += 4
    for ins in instructions:
        ins["instruction"] = ins["instruction"].replace("\t", "").replace("\n", "")


count_instructions = 0


def instruction_tokenization():
    global count_instructions
    try:
        for inst in instructions:
            instr = inst["instruction"]
            sp = instr.split(" ", 1)
            ins = sp[0].upper()
            if (ins == "LUI"):
                one = instr.strip()
                en = 3
                rd = ""
                for i in range(3, len(one)):
                    if (one[i] != ','):
                        rd = rd + one[i]
                        en += 1
                    else:
                        break

                immediate = ""
                for i in range(en + 1, len(one)):
                    immediate += one[i]
                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "LUI", "operands": [rd, immediate], "type": "U"})
            elif (ins == "AUIPC"):
                one = instr.strip()
                en = 5
                rd = ""
                for i in range(5, len(one)):
                    if (one[i] != ','):
                        rd = rd + one[i]
                        en += 1
                    else:
                        break
                immediate = ""
                for i in range(en + 1, len(one)):
                    immediate += one[i]
                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "AUIPC", "operands": [rd, immediate], "type": "U"})
            elif (ins == "JAL"):
                one = instr.strip()
                en = 3
                rd = ""
                for i in range(3, len(one)):
                    if (one[i] != ','):
                        rd = rd + one[i]
                        en += 1
                    else:
                        break
                immediate = ""
                for i in range(en + 1, len(one)):
                    immediate += one[i]
                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "JAL", "operands": [rd, immediate], "type": "J"})
            elif (ins == "BEQ"):
                one = instr.strip()
                en = 3
                rs1 = ""
                for i in range(3, len(one)):
                    if (one[i] != ','):
                        rs1 = rs1 + one[i]
                        en += 1
                    else:
                        break
                rs2 = ""
                en2 = en + 1
                for i in range(en + 1, len(one)):
                    if (one[i] != ','):
                        rs2 = rs2 + one[i]
                        en2 += 1
                    else:
                        break
                label = ""
                for i in range(en2 + 1, len(one)):
                    label = label + one[i]

                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "BEQ", "operands": [rs1, rs2, label], "type": "SB"})
            elif (ins == "BNE"):
                one = instr.strip()
                en = 3
                rs1 = ""
                for i in range(3, len(one)):
                    if (one[i] != ','):
                        rs1 = rs1 + one[i]
                        en += 1
                    else:
                        break
                rs2 = ""
                en2 = en + 1
                for i in range(en + 1, len(one)):
                    if (one[i] != ','):
                        rs2 = rs2 + one[i]
                        en2 += 1
                    else:
                        break
                label = ""
                for i in range(en2 + 1, len(one)):
                    label = label + one[i]

                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "BNE", "operands": [rs1, rs2, label], "type": "SB"})
            elif (ins == "BLT"):
                one = instr.strip()
                en = 3
                rs1 = ""
                for i in range(3, len(one)):
                    if (one[i] != ','):
                        rs1 = rs1 + one[i]
                        en += 1
                    else:
                        break
                rs2 = ""
                en2 = en + 1
                for i in range(en + 1, len(one)):
                    if (one[i] != ','):
                        rs2 = rs2 + one[i]
                        en2 += 1
                    else:
                        break
                label = ""
                for i in range(en2 + 1, len(one)):
                    label = label + one[i]

                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "BLT", "operands": [rs1, rs2, label], "type": "SB"})
            elif (ins == "BGE"):
                one = instr.strip()
                en = 3
                rs1 = ""
                for i in range(3, len(one)):
                    if (one[i] != ','):
                        rs1 = rs1 + one[i]
                        en += 1
                    else:
                        break
                rs2 = ""
                en2 = en + 1
                for i in range(en + 1, len(one)):
                    if (one[i] != ','):
                        rs2 = rs2 + one[i]
                        en2 += 1
                    else:
                        break
                label = ""
                for i in range(en2 + 1, len(one)):
                    label = label + one[i]

                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "BGE", "operands": [rs1, rs2, label], "type": "SB"})
            elif (ins == "BLTU"):
                one = instr.strip()
                en = 4
                rs1 = ""
                for i in range(4, len(one)):
                    if (one[i] != ','):
                        rs1 = rs1 + one[i]
                        en += 1
                    else:
                        break
                rs2 = ""
                en2 = en + 1
                for i in range(en + 1, len(one)):
                    if (one[i] != ','):
                        rs2 = rs2 + one[i]
                        en2 += 1
                    else:
                        break
                label = ""
                for i in range(en2 + 1, len(one)):
                    label = label + one[i]

                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "BLTU", "operands": [rs1, rs2, label], "type": "SB"})
            elif (ins == "BGEU"):
                one = instr.strip()
                en = 4
                rs1 = ""
                for i in range(4, len(one)):
                    if (one[i] != ','):
                        rs1 = rs1 + one[i]
                        en += 1
                    else:
                        break
                rs2 = ""
                en2 = en + 1
                for i in range(en + 1, len(one)):
                    if (one[i] != ','):
                        rs2 = rs2 + one[i]
                        en2 += 1
                    else:
                        break
                label = ""
                for i in range(en2 + 1, len(one)):
                    label = label + one[i]

                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "BGEU", "operands": [rs1, rs2, label], "type": "SB"})
            elif (ins == "SB"):
                one = instr.strip()
                en = 2
                rs1 = ""
                for i in range(2, len(one)):
                    if (one[i] != ','):
                        rs1 = rs1 + one[i]
                        en += 1
                    else:
                        break
                print(rs1)
                offset = ""
                en2 = en + 1
                for i in range(en + 1, len(one)):
                    if (one[i] != '('):
                        offset = offset + one[i]
                        en2 += 1
                    else:
                        break
                rs2 = ""
                for i in range(en2 + 1, len(one) - 1):
                    rs2 = rs2 + one[i]

                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "SB", "operands": [rs1, offset, rs2], "type": "S"})
            elif (ins == "SH"):
                one = instr.strip()
                en = 2
                rs1 = ""
                for i in range(2, len(one)):
                    if (one[i] != ','):
                        rs1 = rs1 + one[i]
                        en += 1
                    else:
                        break
                offset = ""
                en2 = en + 1
                for i in range(en + 1, len(one)):
                    if (one[i] != '('):
                        offset = offset + one[i]
                        en2 += 1
                    else:
                        break
                rs2 = ""
                for i in range(en2 + 1, len(one) - 1):
                    rs2 = rs2 + one[i]

                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "SH", "operands": [rs1, offset, rs2], "type": "S"})
            elif (ins == "SW"):
                one = instr.strip()
                en = 2
                rs1 = ""
                for i in range(2, len(one)):
                    if (one[i] != ','):
                        rs1 = rs1 + one[i]
                        en += 1
                    else:
                        break
                offset = ""
                en2 = en + 1
                for i in range(en + 1, len(one)):
                    if (one[i] != '('):
                        offset = offset + one[i]
                        en2 += 1
                    else:
                        break
                rs2 = ""
                for i in range(en2 + 1, len(one) - 1):
                    rs2 = rs2 + one[i]

                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": "SW", "operands": [rs1, offset, rs2], "type": "S"})
            elif ins == "ADD" or ins == "OR" or ins == "AND" or ins == "SUB" or ins == "SLL" or ins == "SLT" or ins == "SLTU" or ins == "XOR" or ins == "SRL" or ins == "SRA":

                test = sp[1].strip()
                registers = test.split(",", 2)
                rd = registers[0].strip()
                rs2 = registers[1].strip()
                rs1 = registers[2].strip()
                if ins == "ADD":
                    # print(rs1+rs2)
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "ADD", "operands": [rd, rs2, rs1], "type": "R"})


                elif ins == "OR":
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "OR", "operands": [rd, rs2, rs1], "type": "R"})

                elif ins == "AND":
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "AND", "operands": [rd, rs2, rs1], "type": "R"})

                elif ins == "SUB":
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SUB", "operands": [rd, rs2, rs1], "type": "R"})

                elif ins == "SLL":

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SLL", "operands": [rd, rs2, rs1], "type": "R"})

                elif ins == "SLT":

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SLT", "operands": [rd, rs2, rs1], "type": "R"})

                elif ins == "SLTU":

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SLTU", "operands": [rd, rs2, rs1], "type": "R"})

                elif ins == "XOR":
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "XOR", "operands": [rd, rs2, rs1], "type": "R"})

                elif ins == "SRL":
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SRL", "operands": [rd, rs2, rs1], "type": "R"})

                elif ins == "SRA":
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SRA", "operands": [rd, rs2, rs1], "type": "R"})
            elif (
                    ins == "ADDI" or ins == "JALR" or ins == "SLTI" or ins == "SLTIU" or ins == "XORI" or ins == "ORI" or ins == "ANDI" or ins == "SLLI" or ins == "SRLI" or ins == "SRAI"):
                test = sp[1].strip()
                registers = test.split(",", 2)
                rd = registers[0].strip()
                rs1 = registers[1].strip()
                immediate = registers[2].strip()
                if (ins == "ADDI"):
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "ADDI", "operands": [rd, rs1, immediate], "type": "I"})
                elif (ins == "SLTI"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SLTI", "operands": [rd, rs1, immediate], "type": "I"})
                elif (ins == "SLTIU"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SLTIU", "operands": [rd, rs1, immediate], "type": "I"})
                elif (ins == "XORI"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "XORI", "operands": [rd, rs1, immediate], "type": "I"})
                elif (ins == "ORI"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "ORI", "operands": [rd, rs1, immediate], "type": "I"})
                elif (ins == "ANDI"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "ANDI", "operands": [rd, rs1, immediate], "type": "I"})
                elif (ins == "SLLI"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SLLI", "operands": [rd, rs1, immediate], "type": "I"})
                elif (ins == "SRLI"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SRLI", "operands": [rd, rs1, immediate], "type": "I"})
                elif (ins == "SRAI"):
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "SRAI", "operands": [rd, rs1, immediate], "type": "I"})
                elif (ins == "JALR"):
                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "JALR", "operands": [rd, rs1, immediate], "type": "I"})
            elif (ins == "LB" or ins == "LH" or ins == "LW" or ins == "LBU" or ins == "LHU"):
                test = sp[1].strip()
                registers = test.split(",")
                rd = registers[0].strip()
                temp = registers[1].split("(")
                offset = temp[0].strip()
                rs1 = temp[1].split(")")[0].strip()
                if (ins == "LB"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "LB", "operands": [rd, offset, rs1], "type": "I"})
                elif (ins == "LH"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "LH", "operands": [rd, offset, rs1], "type": "I"})
                elif (ins == "LW"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "LW", "operands": [rd, offset, rs1], "type": "I"})
                elif (ins == "LBU"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "LBU", "operands": [rd, offset, rs1], "type": "I"})
                elif (ins == "LHU"):

                    intructions_tokens.append(
                        {"Counter": inst["Address"], "word": "LHU", "operands": [rd, offset, rs1], "type": "I"})
            elif (ins == "FENCE" or ins == "ECALL" or ins == "EBREAK"):
                intructions_tokens.append(
                    {"Counter": inst["Address"], "word": ins, "operands": [-1], "type": "STOP"})
            count_instructions += 4
            # print(count_instructions)
    except IndexError:
        print("Invalid Instruction format at instruction at address   " + str(count_instructions))


def finalize_instructions_and_labels():
    global instructions_map
    global Labels_map
    for inst in intructions_tokens:
        instructions_map[inst["Counter"]] = inst
    for label in Labels:
        Labels_map[label["Name"]] = label["Address"]


def int_to_hex(num):
    # Convert the number to 32-bit two's complement representation
    if num < 0:
        num = (1 << 32) + num
    # Convert the number to hexadecimal string
    hex_str = hex(num)[2:]
    # Pad the string with leading zeroes if necessary
    hex_str = hex_str.zfill(8)
    # Add "0x" before the hexadecimal string
    hex_str = "0x" + hex_str
    # Return the hexadecimal string
    return hex_str


def Display_registers():
    print("     Registers       ")
    print("Register name                binary value      decimal value    hexadecimal value")
    print("zero               " + signed_integer_to_binary(registers[RegNames["zero"]]) + "  " + str(
        registers[RegNames["zero"]]) + "  " + int_to_hex(registers[RegNames["zero"]]))
    print("ra               " + signed_integer_to_binary(registers[RegNames["ra"]]) + "  " + str(
        registers[RegNames["ra"]]) + "  " + int_to_hex(registers[RegNames["ra"]]))
    print("sp               " + signed_integer_to_binary(registers[RegNames["sp"]]) + "  " + str(
        registers[RegNames["sp"]]) + "  " + int_to_hex(registers[RegNames["sp"]]))
    print("gp               " + signed_integer_to_binary(registers[RegNames["gp"]]) + "  " + str(
        registers[RegNames["gp"]]) + "  " + int_to_hex(registers[RegNames["gp"]]))
    print("tp               " + signed_integer_to_binary(registers[RegNames["tp"]]) + "  " + str(
        registers[RegNames["tp"]]) + "  " + int_to_hex(registers[RegNames["tp"]]))
    print("t0               " + signed_integer_to_binary(registers[RegNames["t0"]]) + "  " + str(
        registers[RegNames["t0"]]) + "  " + int_to_hex(registers[RegNames["t0"]]))
    print("t1               " + signed_integer_to_binary(registers[RegNames["t1"]]) + "  " + str(
        registers[RegNames["t1"]]) + "  " + int_to_hex(registers[RegNames["t1"]]))
    print("t2               " + signed_integer_to_binary(registers[RegNames["t2"]]) + "  " + str(
        registers[RegNames["t2"]]) + "  " + int_to_hex(registers[RegNames["t2"]]))
    print("s0               " + signed_integer_to_binary(registers[RegNames["s0"]]) + "  " + str(
        registers[RegNames["s0"]]) + "  " + int_to_hex(registers[RegNames["s0"]]))
    print("s1               " + signed_integer_to_binary(registers[RegNames["s1"]]) + "  " + str(
        registers[RegNames["s1"]]) + "  " + int_to_hex(registers[RegNames["s1"]]))
    print("a0               " + signed_integer_to_binary(registers[RegNames["a0"]]) + "  " + str(
        registers[RegNames["a0"]]) + "  " + int_to_hex(registers[RegNames["a0"]]))
    print("a1               " + signed_integer_to_binary(registers[RegNames["a1"]]) + "  " + str(
        registers[RegNames["a1"]]) + "  " + int_to_hex(registers[RegNames["a1"]]))
    print("a2               " + signed_integer_to_binary(registers[RegNames["a2"]]) + "  " + str(
        registers[RegNames["a2"]]) + "  " + int_to_hex(registers[RegNames["a2"]]))
    print("a3               " + signed_integer_to_binary(registers[RegNames["a3"]]) + "  " + str(
        registers[RegNames["a3"]]) + "  " + int_to_hex(registers[RegNames["a3"]]))
    print("a4               " + signed_integer_to_binary(registers[RegNames["a4"]]) + "  " + str(
        registers[RegNames["a4"]]) + "  " + int_to_hex(registers[RegNames["a4"]]))
    print("a5               " + signed_integer_to_binary(registers[RegNames["a5"]]) + "  " + str(
        registers[RegNames["a5"]]) + "  " + int_to_hex(registers[RegNames["a5"]]))
    print("a6               " + signed_integer_to_binary(registers[RegNames["a6"]]) + "  " + str(
        registers[RegNames["a6"]]) + "  " + int_to_hex(registers[RegNames["a6"]]))
    print("a7               " + signed_integer_to_binary(registers[RegNames["a7"]]) + "  " + str(
        registers[RegNames["a7"]]) + "  " + int_to_hex(registers[RegNames["a7"]]))
    print("s2               " + signed_integer_to_binary(registers[RegNames["s2"]]) + "  " + str(
        registers[RegNames["s2"]]) + "  " + int_to_hex(registers[RegNames["s2"]]))
    print("s3               " + signed_integer_to_binary(registers[RegNames["s3"]]) + "  " + str(
        registers[RegNames["s3"]]) + "  " + int_to_hex(registers[RegNames["s3"]]))
    print("s4               " + signed_integer_to_binary(registers[RegNames["s4"]]) + "  " + str(
        registers[RegNames["s4"]]) + "  " + int_to_hex(registers[RegNames["s4"]]))
    print("s5               " + signed_integer_to_binary(registers[RegNames["s5"]]) + "  " + str(
        registers[RegNames["s5"]]) + "  " + int_to_hex(registers[RegNames["s5"]]))
    print("s6               " + signed_integer_to_binary(registers[RegNames["s6"]]) + "  " + str(
        registers[RegNames["s6"]]) + "  " + int_to_hex(registers[RegNames["s6"]]))
    print("s7               " + signed_integer_to_binary(registers[RegNames["s7"]]) + "  " + str(
        registers[RegNames["s7"]]) + "  " + int_to_hex(registers[RegNames["s7"]]))
    print("s8               " + signed_integer_to_binary(registers[RegNames["s8"]]) + "  " + str(
        registers[RegNames["s8"]]) + "  " + int_to_hex(registers[RegNames["s8"]]))
    print("s9               " + signed_integer_to_binary(registers[RegNames["s9"]]) + "  " + str(
        registers[RegNames["s9"]]) + "  " + int_to_hex(registers[RegNames["s9"]]))
    print("s10               " + signed_integer_to_binary(registers[RegNames["s10"]]) + "  " + str(
        registers[RegNames["s10"]]) + "  " + int_to_hex(registers[RegNames["s10"]]))
    print("s11               " + signed_integer_to_binary(registers[RegNames["s11"]]) + "  " + str(
        registers[RegNames["s11"]]) + "  " + int_to_hex(registers[RegNames["s11"]]))
    print("t3               " + signed_integer_to_binary(registers[RegNames["t3"]]) + "  " + str(
        registers[RegNames["t3"]]) + "  " + int_to_hex(registers[RegNames["t3"]]))
    print("t4               " + signed_integer_to_binary(registers[RegNames["t4"]]) + "  " + str(
        registers[RegNames["t4"]]) + "  " + int_to_hex(registers[RegNames["t4"]]))
    print("t5               " + signed_integer_to_binary(registers[RegNames["t5"]]) + "  " + str(
        registers[RegNames["t5"]]) + "  " + int_to_hex(registers[RegNames["t5"]]))
    print("t6               " + signed_integer_to_binary(registers[RegNames["t6"]]) + "  " + str(
        registers[RegNames["t6"]]) + "  " + int_to_hex(registers[RegNames["t6"]]))


def Display_memory():
    keys = memory.keys()
    keys = list(keys)
    keys.sort()
    print("Memory")
    print("Memory Location                binary value      decimal value    hexadecimal value")
    for key in keys:
        if (key % 4 == 0):
            validate_memory(key)
            validate_memory(key + 1)
            validate_memory(key + 2)
            validate_memory(key + 3)
            bin_content = memory[key + 3] + memory[key + 2] + memory[key + 1] + memory[key]
            int_rep = binary_to_decimal(bin_content)
            print(str(key) + "       " + bin_content + "    " + str(int_rep) + "    " + int_to_hex(int_rep))


def initialize_registers():
    global registers
    for i in range(0, 32):
        registers["x" + str(i)] = 0
        RegNames["x" + str(i)] = "x" + str(i)
    RegNames["zero"] = "x0"
    RegNames["ra"] = "x1"
    RegNames["sp"] = "x2"
    RegNames["gp"] = "x3"
    RegNames["tp"] = "x4"
    RegNames["t0"] = "x5"
    RegNames["t1"] = "x6"
    RegNames["t2"] = "x7"
    RegNames["s0"] = "x8"
    RegNames["s1"] = "x9"
    RegNames["a0"] = "x10"
    RegNames["a1"] = "x11"
    RegNames["a2"] = "x12"
    RegNames["a3"] = "x13"
    RegNames["a4"] = "x14"
    RegNames["a5"] = "x15"
    RegNames["a6"] = "x16"
    RegNames["a7"] = "x17"
    RegNames["s2"] = "x18"
    RegNames["s3"] = "x19"
    RegNames["s4"] = "x20"
    RegNames["s5"] = "x21"
    RegNames["s6"] = "x22"
    RegNames["s7"] = "x23"
    RegNames["s8"] = "x24"
    RegNames["s9"] = "x25"
    RegNames["s10"] = "x26"
    RegNames["s11"] = "x27"
    RegNames["t3"] = "x28"
    RegNames["t4"] = "x29"
    RegNames["t5"] = "x30"
    RegNames["t6"] = "x31"


def read_and_initialize_memory(path):
    file = open(path, 'r')
    lines = file.readlines()
    for l in lines:
        temp = l.split(',', 1)
        binar = signed_integer_to_binary(int(temp[1]))
        base = int(temp[0])
        memory[base] = binar[24:32]
        memory[base + 1] = binar[16:24]
        memory[base + 2] = binar[8:16]
        memory[base + 3] = binar[0:8]


def validate_memory(addr):
    global memory
    if (addr not in memory.keys()):
        memory[addr] = "00000000"


def execute_instructions(starting_address, end_address):
    global memory
    global registers
    inst_address = starting_address
    while (inst_address != end_address and inst_address in instructions_map.keys()):
        try:

            instruction = instructions_map[inst_address]
            print("instruction: " + instruction["word"] + " " + str(instruction["operands"]))
            print("Program Counter: " + str(inst_address))
            ins = instruction["word"]
            if (
                    ins == "ADDI" or ins == "SLTI" or ins == "SLTIU" or ins == "XORI" or ins == "ORI" or ins == "ANDI" or ins == "SLLI" or ins == "SRLI" or ins == "SRAI"):
                rs1 = instruction["operands"][1]
                imm = instruction["operands"][2]
                rd = instruction["operands"][0]
                if (rs1 not in RegNames.keys() or rd not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + int(inst_address))
                    return
                elif (int(imm) >= 2048 or int(imm) < -2048):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    if (instruction["word"] == "ADDI"):
                        result = signed_integer_to_binary(int(registers[RegNames[rs1]]) + int(imm))
                        result = result[len(result) - 32:]
                        registers[RegNames[rd]] = binary_to_decimal(result)
                        inst_address += 4
                    elif (instruction["word"] == "ANDI"):
                        temp = signed_integer_to_binary(int(imm))
                        temp = temp[len(temp) - 12:]
                        immediate = 20 * temp[len(temp) - 12] + temp
                        comp = binary_to_decimal_unsigned(immediate)
                        result = registers[RegNames[rs1]] & comp
                        registers[RegNames[rd]] = binary_to_decimal(signed_integer_to_binary(result))
                        inst_address += 4
                    elif (instruction["word"] == "ORI"):
                        temp = signed_integer_to_binary(int(imm))
                        temp = temp[len(temp) - 12:]
                        immediate = 20 * temp[len(temp) - 12] + temp
                        comp = binary_to_decimal_unsigned(immediate)
                        result = registers[RegNames[rs1]] | comp
                        registers[RegNames[rd]] = binary_to_decimal(signed_integer_to_binary(result))
                        inst_address += 4
                    elif (instruction["word"] == "XORI"):
                        temp = signed_integer_to_binary(int(imm))
                        temp = temp[len(temp) - 12:]
                        immediate = 20 * temp[len(temp) - 12] + temp
                        comp = binary_to_decimal_unsigned(immediate)
                        result = registers[RegNames[rs1]] ^ comp
                        registers[RegNames[rd]] = binary_to_decimal(signed_integer_to_binary(result))
                        inst_address += 4
                    elif (instruction["word"] == "SLTIU"):
                        if (abs(registers[RegNames[rs1]]) < abs(int(imm))):
                            registers[RegNames[rd]] = 1
                        else:
                            registers[RegNames[rd]] = 0
                        inst_address += 4
                    elif (instruction["word"] == "SLTI"):
                        if (registers[RegNames[rs1]] < int(imm)):
                            registers[RegNames[rd]] = 1
                        else:
                            registers[RegNames[rd]] = 0
                        inst_address += 4
                    elif (instruction["word"] == "SLLI"):
                        if (int(imm) >= 32):
                            print("Shift amount out of range at instruction at address = " + str(inst_address))
                        else:
                            content = signed_integer_to_binary(registers[RegNames[rs1]] << int(imm))
                            content = content[len(content) - 32:]
                            registers[RegNames[rd]] = binary_to_decimal(content)
                        inst_address += 4
                    elif (instruction["word"] == "SRLI"):
                        if (int(imm) >= 32):
                            print("Shift amount out of range at instruction at address = " + str(inst_address))
                        else:
                            # print(signed_integer_to_binary(registers[RegNames[rs1]]))
                            content = signed_integer_to_binary(registers[RegNames[rs1]])
                            res = '0' * int(imm) + content[0:len(content) - int(imm)]
                            # print(res)
                            registers[RegNames[rd]] = binary_to_decimal(res)
                            # print(signed_integer_to_binary(registers[RegNames[rd]]))
                        inst_address += 4
                    elif (instruction["word"] == "SRAI"):
                        if (int(imm) >= 32):
                            print("Shift amount out of range at instruction at address = " + str(inst_address))
                        else:
                            registers[RegNames[rd]] = registers[RegNames[rs1]] >> int(imm)
                        inst_address += 4
            elif (ins == "LB" or ins == "LH" or ins == "LW" or ins == "LBU" or ins == "LHU"):
                rs1 = instruction["operands"][2]
                imm = instruction["operands"][1]
                rd = instruction["operands"][0]
                if (rs1 not in RegNames.keys() or rd not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + int(inst_address))
                    return
                elif (int(imm) >= 2048 or int(imm) < -2048):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    if (instruction["word"] == "LW"):
                        content = ""
                        addr = int(registers[RegNames[rs1]]) + int(imm)
                        validate_memory(addr)
                        validate_memory(addr + 1)
                        validate_memory(addr + 2)
                        validate_memory(addr + 3)
                        content = memory[addr + 3] + memory[addr + 2] + memory[addr + 1] + memory[addr]
                        result = binary_to_decimal(content)
                        # print(content)
                        # print(result)
                        # print(rd)
                        registers[RegNames[rd]] = result
                        inst_address += 4
                    elif (instruction["word"] == "LHU"):
                        content = ""
                        addr = int(registers[RegNames[rs1]]) + int(imm)
                        validate_memory(addr)
                        validate_memory(addr + 1)
                        content = "0" * 16 + memory[addr + 1] + memory[addr]
                        result = binary_to_decimal(content)
                        registers[RegNames[rd]] = result
                        inst_address += 4
                    elif (instruction["word"] == "LBU"):
                        content = ""
                        addr = int(registers[RegNames[rs1]]) + int(imm)
                        validate_memory(addr)
                        content = "0" * 24 + memory[addr]
                        result = binary_to_decimal(content)
                        registers[RegNames[rd]] = result
                        inst_address += 4
                    elif (instruction["word"] == "LH"):
                        content = ""
                        addr = int(registers[RegNames[rs1]]) + int(imm)
                        validate_memory(addr)
                        validate_memory(addr + 1)
                        content = memory[addr + 1][0] * 16 + memory[addr + 1] + memory[addr]
                        result = binary_to_decimal(content)
                        registers[RegNames[rd]] = result
                        inst_address += 4
                    elif (instruction["word"] == "LB"):
                        content = ""
                        addr = int(registers[RegNames[rs1]]) + int(imm)
                        validate_memory(addr)
                        content = memory[addr][0] * 24 + memory[addr]
                        result = binary_to_decimal(content)
                        registers[RegNames[rd]] = result
                        inst_address += 4
            elif (instruction["word"] == "SW"):
                rs1 = instruction["operands"][2].strip()
                imm = instruction["operands"][1].strip()
                rd = instruction["operands"][0].strip()
                imm_bin = signed_integer_to_binary(int(imm))
                if (rs1 not in RegNames.keys() or rd not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (int(imm) >= 2048 or int(imm) < -2048):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    content = signed_integer_to_binary(int(registers[RegNames[rd]]))
                    if (len(content) > 32):
                        content = content[len(content) - 32:len(content)]
                    addr = int(registers[RegNames[rs1]]) + int(imm)
                    validate_memory(addr)
                    validate_memory(addr + 1)
                    validate_memory(addr + 2)
                    validate_memory(addr + 3)
                    memory[addr] = content[24:32]
                    memory[addr + 1] = content[16:24]
                    memory[addr + 2] = content[8:16]
                    memory[addr + 3] = content[0:8]
                inst_address += 4
            elif (instruction["word"] == "SH"):
                rs1 = instruction["operands"][2].strip()
                imm = instruction["operands"][1].strip()
                rd = instruction["operands"][0].strip()
                # print(int(imm))
                # print(bin(int(imm)))
                imm_bin = signed_integer_to_binary(int(imm))
                if (rs1 not in RegNames.keys() or rd not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (int(imm) >= 2048 or int(imm) < -2048):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    content = signed_integer_to_binary(int(registers[RegNames[rd]]))
                    # print(rd)
                    # print(content)
                    # print(len(content))
                    if (len(content) > 32):
                        content = content[len(content) - 32:len(content)]
                    addr = int(registers[RegNames[rs1]]) + int(imm)
                    validate_memory(addr)
                    validate_memory(addr + 1)
                    memory[addr] = content[24:32]
                    memory[addr + 1] = content[16:24]
                inst_address += 4
            elif (instruction["word"] == "SB"):
                rs1 = instruction["operands"][2].strip()
                imm = instruction["operands"][1].strip()
                rd = instruction["operands"][0].strip()
                # print(int(imm))
                # print(bin(int(imm)))
                imm_bin = signed_integer_to_binary(int(imm))
                if (rs1 not in RegNames.keys() or rd not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (int(imm) >= 2048 or int(imm) < -2048):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    content = signed_integer_to_binary(int(registers[RegNames[rd]]))
                    # print(rd)
                    # print(content)
                    # print(len(content))
                    if (len(content) > 32):
                        content = content[len(content) - 32:len(content)]
                    addr = int(registers[RegNames[rs1]]) + int(imm)
                    validate_memory(addr)
                    memory[addr] = content[24:32]
                inst_address += 4
            elif (ins == "BEQ"):
                rs1 = instruction["operands"][0].strip()
                rs2 = instruction["operands"][1].strip()
                label = instruction["operands"][2].strip()
                if (rs1 not in RegNames.keys() or rs2 not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (label not in Labels_map.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    if (registers[RegNames[rs1]] == registers[RegNames[rs2]]):
                        inst_address = Labels_map[label]
                    else:
                        inst_address += 4
            elif (ins == "BNE"):
                rs1 = instruction["operands"][0].strip()
                rs2 = instruction["operands"][1].strip()
                label = instruction["operands"][2].strip()
                if (rs1 not in RegNames.keys() or rs2 not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (label not in Labels_map.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    if (registers[RegNames[rs1]] != registers[RegNames[rs2]]):
                        inst_address = Labels_map[label]
                    else:
                        inst_address += 4
            elif (ins == "BLT"):
                rs1 = instruction["operands"][0].strip()
                rs2 = instruction["operands"][1].strip()
                label = instruction["operands"][2].strip()
                if (rs1 not in RegNames.keys() or rs2 not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (label not in Labels_map.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    if (registers[RegNames[rs1]] < registers[RegNames[rs2]]):
                        inst_address = Labels_map[label]
                    else:
                        inst_address += 4
            elif (ins == "BGE"):
                rs1 = instruction["operands"][0].strip()
                rs2 = instruction["operands"][1].strip()
                label = instruction["operands"][2].strip()
                if (rs1 not in RegNames.keys() or rs2 not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (label not in Labels_map.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    if (registers[RegNames[rs1]] >= registers[RegNames[rs2]]):
                        inst_address = Labels_map[label]
                    else:
                        inst_address += 4
            elif (ins == "BGEU"):
                rs1 = instruction["operands"][0].strip()
                rs2 = instruction["operands"][1].strip()
                label = instruction["operands"][2].strip()
                if (rs1 not in RegNames.keys() or rs2 not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (label not in Labels_map.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    if (abs(registers[RegNames[rs1]]) >= abs(registers[RegNames[rs2]])):
                        inst_address = Labels_map[label]
                    else:
                        inst_address += 4
            elif (ins == "BLTU"):
                rs1 = instruction["operands"][0].strip()
                rs2 = instruction["operands"][1].strip()
                label = instruction["operands"][2].strip()
                if (rs1 not in RegNames.keys() or rs2 not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (label not in Labels_map.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    if (abs(registers[RegNames[rs1]]) < abs(registers[RegNames[rs2]])):
                        inst_address = Labels_map[label]
                    else:
                        inst_address += 4
            elif (ins == "ECALL" or ins == "FENCE" or ins == "EBREAK"):
                print("Execution terminated at address " + str(inst_address))
                return
            elif (ins == "JAL"):
                label = instruction["operands"][1].strip()
                rd = instruction["operands"][0].strip()
                if (label in Labels_map.keys()):
                    registers[RegNames[rd]] = inst_address + 4
                    inst_address = Labels_map[label]

                elif (int(label) in Labels_map.values()):
                    registers[RegNames[rd]] = inst_address + 4
                    inst_address = int(label)
                else:
                    print("Invalid address at instruction address" + str(inst_address))
            elif (ins == "JALR"):
                # print("here")
                imm = instruction["operands"][2].strip()
                rs = instruction["operands"][1].strip()
                rd = instruction["operands"][0].strip()
                # print("here2")
                if (rs not in RegNames.keys() or rd not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                elif (int(imm) >= 2048 or int(imm) < -2048):
                    print("Invalid Instruction Format at address " + str(inst_address))
                    return
                else:
                    registers[RegNames[rd]] = inst_address + 4
                    # print(imm)
                    inst_address = registers[RegNames[rs]] + int(imm)
                    # print(inst_address)
            elif (
                    ins == "ADD" or ins == "OR" or ins == "AND" or ins == "SUB" or ins == "SLL" or ins == "SLT" or ins == "SLTU" or ins == "XOR" or ins == "SRL" or ins == "SRA"):
                rs1 = instruction["operands"][1].strip()
                rs2 = instruction["operands"][2].strip()
                rd = instruction["operands"][0].strip()
                if (rs1 not in RegNames.keys() or rd not in RegNames.keys() or rs2 not in RegNames.keys()):
                    print("Invalid Instruction Format at address " + int(inst_address))
                    return
                else:
                    if (ins == "ADD"):
                        res = registers[RegNames[rs1]] + registers[RegNames[rs2]]
                        temp = signed_integer_to_binary(res)
                        registers[RegNames[rd]] = binary_to_decimal(temp[len(temp) - 32:])
                        inst_address += 4
                    elif (ins == "SUB"):
                        res = registers[RegNames[rs1]] - registers[RegNames[rs2]]
                        temp = signed_integer_to_binary(res)
                        registers[RegNames[rd]] = binary_to_decimal(temp[len(temp) - 32:])
                        inst_address += 4
                    elif (ins == "OR"):
                        registers[RegNames[rd]] = registers[RegNames[rs1]] | registers[RegNames[rs2]]
                        inst_address += 4
                    elif (ins == "XOR"):
                        registers[RegNames[rd]] = registers[RegNames[rs1]] ^ registers[RegNames[rs2]]
                        inst_address += 4
                    elif (ins == "AND"):
                        registers[RegNames[rd]] = registers[RegNames[rs1]] & registers[RegNames[rs2]]
                        inst_address += 4
                    elif (ins == "SLT"):
                        if (registers[RegNames[rs1]] < registers[RegNames[rs2]]):
                            registers[RegNames[rd]] = 1
                        else:
                            registers[RegNames[rd]] = 0
                        inst_address += 4
                    elif (ins == "SLTU"):
                        # print(abs(registers[RegNames[rs1]]))
                        # print(abs(registers[RegNames[rs2]]))
                        if (abs(registers[RegNames[rs1]]) < abs(registers[RegNames[rs2]])):

                            registers[RegNames[rd]] = 1
                        else:
                            registers[RegNames[rd]] = 0
                        inst_address += 4
                    elif (ins == "SLL"):
                        temp = signed_integer_to_binary(registers[RegNames[rs2]])
                        shamt = temp[len(temp) - 5:]
                        shamt = binary_to_decimal(shamt)
                        content = registers[RegNames[rs1]] << shamt
                        content = signed_integer_to_binary(content)
                        content = content[len(content) - 32:]
                        registers[RegNames[rd]] = binary_to_decimal(content)
                        inst_address += 4
                    elif (ins == "SRA"):
                        temp = signed_integer_to_binary(registers[RegNames[rs2]])
                        shamt = temp[len(temp) - 5:]
                        shamt = binary_to_decimal(shamt)
                        content = registers[RegNames[rs1]] >> shamt
                        content = signed_integer_to_binary(content)
                        content = content[len(content) - 32:]
                        registers[RegNames[rd]] = binary_to_decimal(content)
                        inst_address += 4
                    elif (ins == "SRL"):
                        temp = signed_integer_to_binary(registers[RegNames[rs2]])
                        shamt = temp[len(temp) - 5:]
                        # print(type(shamt))
                        shamt = binary_to_decimal(shamt)
                        content = signed_integer_to_binary(registers[RegNames[rs1]])
                        # print(shamt)
                        res = '0' * shamt + content[0:len(content) - shamt]
                        # print(content)
                        registers[RegNames[rd]] = binary_to_decimal(res)
                        inst_address += 4
            elif (ins == "LUI"):
                imm = instruction["operands"][1].strip()
                rd = instruction["operands"][0].strip()
                if (rd not in RegNames.keys() or int(imm) > 524287 or int(imm) < -524288):
                    print("Error in instruction at address = " + str(inst_address))
                    return
                else:
                    content = signed_integer_to_binary(int(imm))
                    content = content[12:32] + '0' * 12
                    print(content)
                    registers[RegNames[rd]] = binary_to_decimal(content)
                    inst_address += 4
            elif (ins == "AUIPC"):
                # print("here")
                imm = instruction["operands"][1].strip()
                rd = instruction["operands"][0].strip()
                if (rd not in RegNames.keys() or int(imm) > 524287 or int(imm) < -524288):
                    print("Error in instruction at address = " + str(inst_address))
                    return
                else:
                    content = signed_integer_to_binary(int(imm))
                    content = content[12:32] + '0' * 12
                    # print(content)
                    registers[RegNames[rd]] = binary_to_decimal(content) + inst_address
                    inst_address += 4
            registers[RegNames["x0"]] = 0
            Display_registers()
            Display_memory()
        except:
            print("Error in instruction at address = " + str(inst_address))
            return


if __name__ == '__main__':
    path = "code.txt"
    read_code_file(path)
    instruction_tokenization()
    finalize_instructions_and_labels()
    initialize_registers()
    registers[RegNames["sp"]] = 40000000
    read_and_initialize_memory("data.txt")
    if ("main" not in Labels_map.keys()):
        print("Please define the main function at the starting instruction of your program")
    else:
        starting_address = Labels_map["main"]
        addresses = list(instructions_map.keys())
        end_address = addresses[len(addresses) - 1] + 4
        execute_instructions(starting_address, end_address)

