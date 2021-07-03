import numpy as np
import operator as op
from functools import reduce
from random import randrange


# This is all hard coded for a 16 bit hamming code for now, easy to expand to any 2**x


def generate_bits():
	bits = np.random.randint(0, 2, 16)
	bits[0] = 0 
	return bits


def xor(bits):
	return reduce(op.xor, [i for i, bit in enumerate(bits) if bit])


def prepare_bits(bits):
	parity_position = xor(bits)
	
	#4 hard coded for now
	for i in reversed([2**i for i in range(4)]):
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

def print_bits(bits, flat=False):
	if flat:
		print([bit for i, bit in enumerate(bits)])
	else:
		for i, bit in enumerate(bits):
			print(bit, end="  ")
			if i%4 == 3:
				print("")
		# Would this work?
		# print([bit if i%4!=3 else f"{bit}\n"] 
		#		for i, bit in enumerate(bits))

	print(f"xor(bits) {xor(bits)}")
	print("\n\n")



if __name__ == '__main__':
	bits = generate_bits()
	print(f"\ninitial bits:")
	print_bits(bits)


	bits = prepare_bits(bits)
	print("prepared bits:")
	print_bits(bits)

	if not check_properly_prepared(bits):
		raise NameError("preparing failed")
	
	bit_flipped, bits = random_bit_flip(bits)
	print(f"bit flipped: {bit_flipped}")
	print_bits(bits)
	
	bits = repair_bits(bits)
	print(f"repaired bits:")
	print_bits(bits)
	
