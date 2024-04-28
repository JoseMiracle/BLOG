"""
SKILLSFORGE TASK FOR SECTION_1: question1
TO run the program, change directory into SECTION1 and 
enter python question1.py in the terminal
"""


def compress(string):
    

    if (len(string) == 1) :
        return string
    
    compressed_string = ''
    count = 0
    letter = string[0]

    for index in range(len(string)):
        
        if letter == string[index] : # Checks if letter is equal to the current value in a given index
            count += 1
            
            if index == len(string)-1 : # Detect if the index has reached the exact length of string
                compressed_string += letter
                compressed_string += str(count)

        
        elif letter != string[index]: # Checks if letter is not equal to the current value in a given index
            compressed_string += letter
            compressed_string += str(count)
            letter = string[index] # assign letter to the value in the current index
            count = 1
        
    return compressed_string


assert compress("bbcceeee") == "b2c2e4"
assert compress("aaabbbcccaaa") == "a3b3c3a3"
assert compress("a") == "a"
