from random import randint
from configparser import ConfigParser

parser = ConfigParser()
parser.read('../config/config.properties')

COMP_OFFSET = int(parser['pass_para']['comp_offset'])
DEFAULT_NUM = int(parser['pass_para']['default_num'])
ZERO_REPLACE = int(parser['pass_para']['zero_replace'])

# COMP_OFFSET = 200
# DEFAULT_NUM = 3
# ZERO_REPLACE = 5


# 3) STEP 3 = Remove Offset from each char
def remove_offset(offset, data):
	offset_msg = ""
	if offset == 0 or offset == 1:
		offset = ZERO_REPLACE
	
	for char in data:
		offset_msg += chr(ord(char) - COMP_OFFSET - offset)
	return offset_msg 

# 2) STEP 2 = Remove garbage
def remove_noise(num2, num3, data):
	noise_removed = ""
	diff = abs(num2 - num3)
	# if diff is less than 4 or zero then divide number 1 by two
	loc = diff if diff !=0 and diff <= 4 else num2 // 3
	if loc == 0:
		loc = 3

	# print(loc)
	index = 0
	
	# remove random string of length num3 at location
	while index in range(len(data)):
		
		for i in range(loc):
			if index >= len(data):
				break
			noise_removed += data[index]
			index += 1

		for i in range(num3):
			index += 1	
			continue	

	return noise_removed		

# 1) STEP 1 = UnReverse by dig4 digit
def unrev_data(dig4, data):
	if dig4 == 0:
		dig4 = ZERO_REPLACE

	return data[dig4:] + data[:dig4]

def get_decrypted_password(key, data):
	if type(key) == int and key > 111:
		key = str(key)	

		dig1, dig2, dig3, dig4 = int(key[0:1]) , int(key[1:2]) , int(key[2:3]) , int(key[3:4])
		
		unreversed = unrev_data(dig4, data)		
		# print(" 1 : ", unreversed)
		
		noise_removed = remove_noise(dig2, dig3, unreversed)
		# print(" 2 : ", noise_removed)
		
		offset_removed = remove_offset(dig1, noise_removed)
		# print(" 3 : ", offset_removed)

		return offset_removed
		
	else:
		print(" Key should be numeric and Greater than 111 ")
		return False


if __name__ == '__main__':
	
	# enc_pass = "ęĳĭěĖċĿĠĘĘİĥģīĭĘČĚĲčČċıĐČĚĽđĜ"
	enc_pass = "ĽĺĸĶĎĬ"
	my_pass = get_decrypted_password(3111, enc_pass)
	print(my_pass)

'''
	new_pass = "107w3qX447"
	offset:  üûĂłþļģÿÿĂ
	noise:  üûĩĚĂłĒĔþļĎĚģÿĪĖÿĂ
	pass:  ĂüûĩĚĂłĒĔþļĎĚģÿĪĖÿ
'''


