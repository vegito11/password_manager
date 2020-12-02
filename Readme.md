## Description:
	
	- This programm generate password - encrypt it using PIN from User and store it in file . 
	- Also we can delete password, Update password , Get Password 

## 1) Run code
	$ python3 code/main.py

Limitation:

* if File size is increased performance will decrease - for update and delete we overwriting 
  entire file 
* Currently only support 4 digit PIN for encryption 
* Not tested for some edge cases - Possibility of bugs
