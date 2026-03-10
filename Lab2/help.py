# enumerate() is a built-in function in Python that allows you to loop over an iterable
# (like a list) and have an automatic counter. 
# It returns both the index and the value of each item in the iterable.
fruits = ['apple', 'banana', 'orange']

for index, item in enumerate(fruits):
    print(f"Index: {index}, Value: {item}")




# accessing elements in a 2D list (list of lists)
data = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]

# Access the element in the second row (index 1), third column (index 2)
element = data[1][2] # element will be 6

# Access the entire third row (index 2)
row = data[2] # row will be [7, 8, 9]





# converting a number to a zero-padded binary string using f-string
number = 9
binary_str = f"{number:04b}"
# Result: '1001' (padded to 4 bits)
# :04b means: format as binary (b), padded to 4 digits with zeros


# converting a hex string to a zero-padded binary string
hex_str = "AB"
binary_from_hex = f"{int(hex_str, 16):08b}"
# int(hex_str, 16) converts hex to decimal (AB -> 171)
# :08b formats as 8-bit binary: '10101011'




# converting a binary string to a zero-padded hex string
binary_str = "11000000101101111010100011010000"
hex_from_bin = f"{int(binary_str, 2):016X}"
# int(binary_str, 2) converts binary to decimal
# :016X formats as 16-char uppercase hex, zero-padded
# Result: 'C0B7A8D0'





# ''.join() - joining a list of strings into one string
parts = ['10', '01', '11']
combined = ''.join(parts)
# Result: '100111'


# list comprehension - building a new list from an existing one
original = [1, 2, 3, 4, 5]
doubled = [x * 2 for x in original]
# Result: [2, 4, 6, 8, 10]




# string slicing - getting parts of a string
text = "ABCDEF"
first_three = text[:3]    # 'ABC' (from start to index 3)
last_three = text[3:]     # 'DEF' (from index 3 to end)
middle = text[1:4]        # 'BCD' (from index 1 to 4)


