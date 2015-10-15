""" 
Most probable letter in english is 'e'.

The code to the cipher is 3 letters long. We can build a histogram for 
each of the 3 letters and sort by probability of mapping to e. 

Then decrypt the text with each sample cipher and see what produces English.

To run, execute `time python decrypt.py`
"""





import json

def to_unichr(decrypted_ord):
	return ''.join(unichr(c) for c in decrypted_ord) 

def decrypt_ord(cipher, xor):
	## returns None if definitly not english (no Capital or ' ' detected)
	capital_letter_range = (65, 90)
	capital_flag = False
	space_flag = False

	decrypted = []
	for i, c in enumerate(cipher):
		xor_i = i % 3
		xor_c = xor[xor_i]
		decrypted_ord = xor_c ^ int(c)
		decrypted += [decrypted_ord]


		if i <= 10:
			# set sanity flags
			if decrypted_ord >= 65 and decrypted_ord <= 90:
				capital_flag = True
			if decrypted_ord == 32:
				space_flag = True

		if i == 10:
			if not (capital_flag and space_flag):
				return None # does not pass sanity check

	return decrypted

def get_xor(hash_list):
	# iterates over each hash list to figure out which of the codes should
	# map to e (the most frequent letter), starting in order from most
	# frequent to least frequent.

	hash_list_sorted = [[]] * len(hash_list)
	for i, hash in enumerate(hash_list):
		hash_sorted = sorted(hash.items(), key=lambda x: x[1], reverse=True)
		sorted_letters = [x[0] for x in hash_sorted]
		hash_list_sorted[i] = sorted_letters

	for i, a in enumerate(hash_list_sorted[0]):
		for j, b in enumerate(hash_list_sorted[1][:(i+6)]):
			for c in hash_list_sorted[2][:(j+6)]:
				print (a,b,c)
				yield (ord('e') ^ a, ord('e') ^ b, ord('e') ^ c)

def num_english(words, english_words):
	num_e = sum([1 for x in words if x in english_words])
	num_non_e = len(words) - num_e
	return num_e, num_non_e

with open('cipher.txt') as f:
	cipher = f.read()
	cipher = cipher.split(',')
	hist = [{}, {}, {}]
	for i, l in enumerate(cipher):
		cipher_i = i % 3
		cipher_dict = hist[cipher_i]
		l_int = int(l)
		cipher_dict[int(l)] = cipher_dict.get(l_int, 0) + 1

with open('words.txt') as words:
	english_words = set(words.read().split("\n"))

print hist[0]
print 'ok'

xor_gen = get_xor(hist)
for i in range(1000):
	xor = xor_gen.next()
	# print i, xor
	decrypted = decrypt_ord(cipher, xor)
	if decrypted:
		uni = to_unichr(decrypted)
		words = uni.lower().split()
		num_e, num_non_e = num_english(words, english_words)
		# print uni
		if num_e > 10 and num_e > num_non_e:
			print uni
			print 'Passed English test'
			print 'Sum of ASCII values: ', sum([ord(a) for a int uni])
			break
		else: 
			print 'Did not pass English test', num_e

	else:
		print "None"


