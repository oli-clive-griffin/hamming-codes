import numpy as np
import operator as op
from math import log2, sqrt, ceil
from functools import reduce
from random import randrange
from sys import argv


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    YELLOW_BG = "\033[30;103m"


def generate_random_bits(length):
    bits = np.random.randint(0, 2, length)
    bits[0] = 0 
    return bits

def xor(bits):
    return reduce(op.xor, [i for i, bit in enumerate(bits) if bit])


def prepare_bits(bits):
    parity_position = xor(bits)
    length = len(bits)
    
    for i in reversed([2**x for x in range(int(log2(length)))]):
        if parity_position >= i:
            bits[i] = not bits[i]
            parity_position = parity_position - i   

    return bits


def random_bit_flip(bits):
    i = randrange(0, len(bits))
    bits[i] = not bits[i]
    return i, bits


def check_properly_prepared(bits):
    if (xor(bits) == 0):
        return True
    return False


def repair_bits(bits):
    flipped_bit = xor(bits)
    bits[flipped_bit] = not bits[flipped_bit]
    return bits


# TODO make into a comprehension
def print_bits(bits, flat=False, bit_flipped=None, bit_repaired=None):
    length = len(bits)

    display_width = get_print_width(length)

    if flat:
        print([bit for i, bit in enumerate(bits)])
    else:
        for i, bit in enumerate(bits):
            if i == bit_flipped:
                print(f"{bcolors.RED}{bcolors.BOLD}{bit}{bcolors.ENDC}", end=" ")
            elif i == bit_repaired:
                print(f"{bcolors.OKGREEN}{bcolors.BOLD}{bit}{bcolors.ENDC}", end=" ")
            elif i in [2**x for x in range(ceil(log2(length)))]:
                print(f"{bcolors.OKBLUE}{bit}{bcolors.ENDC}", end=" ")
            else:
                print(bit, end=" ")

            if i % display_width == display_width - 1:
                print("")

    print("\n\n")


def get_print_width(bit_length):
    closest_power_of_2 = 2 ** up_to_even(log2(bit_length))
    display_width = int(closest_power_of_2 ** 0.5)
    return display_width


def up_to_even(x):
    return x if x % 2 == 0 else x + 1


def add_padding(bits):
    length = len(bits)
    dead_space = 0 
    for i in [2**x for x in range(13)]:
        if i >= length:
            dead_space = i - length
            break
    zeros = np.array([0 for i in range(dead_space)])
    print(f"lenftL: {len(zeros)}")
    if len(zeros):
        bits = np.concatenate((bits, zeros))
    return bits



if __name__ == '__main__':

    if len(argv) > 1:
        DIMENSION = int(argv[1])
    else:
        DIMENSION = 64

    bits = generate_random_bits(DIMENSION)
    bits = add_padding(bits) 
    print(len(bits))
    
    print("\n")
    print(f"{bcolors.OKCYAN}Initial bits: {bcolors.ENDC}")
    print_bits(bits)

    bits = prepare_bits(bits)
    INITIAL_BITS = bits 
    print(f"{bcolors.OKCYAN}Prepared bits: {bcolors.ENDC}")
    print_bits(bits)

    if not check_properly_prepared(bits):
        raise NameError("Preparing failed")
    
    bit_flipped, bits = random_bit_flip(bits)
    print(f"{bcolors.OKCYAN}Bit {bit_flipped} flipped {bcolors.ENDC}")
    print_bits(bits, bit_flipped=bit_flipped)
    
    bits = repair_bits(bits)
    print(f"{bcolors.OKCYAN}Repaired bits: {bcolors.ENDC}")
    print_bits(bits, bit_repaired=bit_flipped)
    

    if (np.allclose(bits, INITIAL_BITS)):
        print(bcolors.OKGREEN + "Message successfully repaired" + bcolors.ENDC)
    else:
        print(bcolors.RED + "Message could not be repaired" + bcolors.ENDC)

