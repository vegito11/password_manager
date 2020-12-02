from random import randint
from configparser import ConfigParser

parser = ConfigParser()
parser.read('../config/config.properties')

COMP_OFFSET = int(parser['pass_para']['comp_offset'])
DEFAULT_NUM = int(parser['pass_para']['default_num'])
ZERO_REPLACE = int(parser['pass_para']['zero_replace'])
PASS_LEN = int(parser['pass_para']['pass_len'])

# COMP_OFFSET = 200
# DEFAULT_NUM = 3
# ZERO_REPLACE = 5

def generate_password():

	password = ""
	
	for i in range(0, PASS_LEN):
	
		if randint(1, 10) % 3 < 2:
			password += str(randint(0, 10))
		else:	
			ch = randint(1, 61)
			ch = chr(65 + ch)
			password += ch
	return password

# 1) STEP 1 = Add Offset to each char
def add_offset(offset, data):
	offset_msg = ""
	if offset == 0 or offset == 1:
		offset = ZERO_REPLACE
	
	for char in data:
		offset_msg += chr(ord(char) + COMP_OFFSET + offset)
	return offset_msg 

# 2) STEP 2 = Add Garbage at regular interval 
def add_noise(num2, num3, data):
	noise_added = ""
	diff = abs(num2 - num3)
	# if diff is less than 4 or zero then divide number 1 by two
	loc = diff if diff !=0 and diff <= 4 else num2 // 3
    
	if loc == 0 :
		loc = 3
	# add random string of length num3 at location
	for index in range(len(data)):
		if index % loc== 0 and index !=0 :
			noise_added += "".join([chr(randint(65, 100) + COMP_OFFSET) for x in range(num3 + 1) if x])
		noise_added += data[index] 	

	return noise_added	

# 3) STEP 3 = Reverse by dig4 digit
def rev_data(dig4, data):
	if dig4 == 0:
		dig4 = ZERO_REPLACE
	return (data[-dig4:] + data[:-dig4])

def get_encrypted_password(key, data):
	
	if type(key) == int and key > 111:
		key = str(key)	
		dig1, dig2, dig3, dig4 = int(key[0:1]) , int(key[1:2]) , int(key[2:3]) , int(key[3:4])
		offset_added = add_offset(dig1, data)
		noise_added = add_noise(dig2, dig3, offset_added)

		return rev_data(dig4, noise_added)
		
	else:
		print(" Key should be numeric and Greater than 111 ")
		return False



if __name__ == '__main__':
	# password = generate_password()
	password = "omkar"
	encrypted_password = get_encrypted_password(3111, password)
	print("Encrypted Password: ",encrypted_password)
