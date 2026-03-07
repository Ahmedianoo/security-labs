def calc(char):
    return ord(char) - ord('A')

def Encryption(key,message):

    """
        we have some conditions
        the key is shorter than the message
        the key is longer than the message

        we should loop over the message, implement some rule and concatenate the result char to the encrypted_msg
        (p+k) mod 26 = encrypted char
        so the k = (assci - assci of a), create a function to do so
    """

    encrypted_message = ""
    running_key = key + message.replace(" ", "")
    i = 0

    for char in message:
        if(char == " "):
            encrypted_message += " "
            continue
        k_char = running_key[i]    
        encrypted_char =  chr(((calc(char) + calc(k_char)) % 26) + ord('A')) 
        encrypted_message += encrypted_char
        i+=1
    return encrypted_message

def Decryption(key, message):
    original_message = ""
    running_key = key
    i = 0

    for char in message:
        if(char == " "):
            original_message += " "
            continue
        k_char = running_key[i]    
        original_char =  chr(((calc(char) - calc(k_char)) % 26) + ord('A')) 
        original_message += original_char
        running_key+=original_char
        i+=1
    return original_message






messages = ["ATTACKATDAWN", "HELLO", "CRYPTO", "SHORT", "HI", "ABCDE", "HELLO WORLD"]
keys = ["QUEENLY", "K", "A", "KEY", "LONG", "Z", "KEY"]
encrypted_messages = []

for i in range(len(messages)):
    encrypted_message = Encryption(keys[i], messages[i])
    encrypted_messages.append(encrypted_message)
    print(encrypted_message)

print("----------------------------------------------------------------")   
for i in range(len(encrypted_messages)):
    original_message = Decryption(keys[i], encrypted_messages[i])
    print(original_message) 


    


