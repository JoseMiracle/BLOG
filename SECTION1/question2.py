"""
SKILLSFORGE TASK FOR SECTION_1: question2
TO run the program, change directory into SECTION1 and 
enter python question2.py in the terminal

"""


from functools import cmp_to_key
def largestNumber(arr):
    # Convert the input array to an array of integers
    nums = [int(x) for x in arr]

    # Define a custom comparison function
    def compare(x, y):
        xy = str(x) + str(y)
        yx = str(y) + str(x)
        if xy > yx:
            return -1
        elif xy < yx:
            return 1
        else:
            return 0

    # Sort the array using the custom comparison function
    nums.sort(key=cmp_to_key(compare))

    # Convert the sorted array back to an array of strings
    result = [str(x) for x in nums]

    # Concatenate the sorted strings and return the result
    return ''.join(result)
