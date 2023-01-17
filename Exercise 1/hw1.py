#Skeleton file for HW1 - Spring 2021 - extended intro to CS

#Add your implementation to this file

#you may NOT change the signature of the existing functions.
#you can add new functions if needed.

#Change the name of the file to include your ID number (hw1_ID.py).


#Question 4a
def num_different_letters(text):
    chars = "abcdefghijklmnopqrstuvwxyz"
    
    count = {c for c in text if c in chars}
    return len(count)


#Question 4b
def replace_char(text, old, new):
    replaced = ""
    
    for c in text:
        if c == old:
            replaced += new
        else:
            replaced += c
    
    return replaced


#Question 4c
def longest_word(text):
    return max([len(w) for w in text.split()])


#Question 4d
def to_upper(text):
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper_text = ""

    for c in text:
        if c in lower:
            upper_text += chr(ord(c)-32)
        else:
            upper_text += c
    
    return upper_text


#Question 5
def calc(expression):
    if not expression:
        return ""
    if expression[0] != "'":
        return ""
    
    data = expression.split("'")[1:-1]
    strings = data[0::2]
    symbols = data[1::2]
    
    render = strings[0]

    for i,sym in enumerate(symbols):
        if sym == '+':
            render += strings[i+1]
        if sym == '*':
            render = render*(int(strings[i+1]))
    
    return render


########
# Tester
########

def test():
    #testing Q4
    if num_different_letters("aa bb cccc dd ee fghijklmnopqrstuvwxyz") != 26:
        print("error in num_different_letters - 1")
    if num_different_letters("aaa98765432100000000") != 1:
        print("error in num_different_letters - 2")

    if replace_char("abcdabcde", "a", "x") != "xbcdxbcde":
        print("error in replace_char - 1")
    if replace_char("abcd123", "1", "x") != "abcdx23":
        print("error in replace_char - 2")
        
    if longest_word("a bb ccc 4444 e") != 4:
        print("error in longest_word - 1")
    if longest_word("a bb ccc 4444 eeeee fffff") != 5:
        print("error in longest_word - 2")

    if to_upper("abc") != "ABC":
        print("error in to_upper - 1")
    if to_upper("123") != "123":
        print("error in to_upper - 2")

    #testing Q5
    if calc("'123321'*'2'") != "123321123321":
        print("error in calc - 1")
    if calc("'Hi there '*'3'+'you2'") != "Hi there Hi there Hi there you2":
        print("error in calc - 2")
    if calc("'hi+fi'*'2'*'2'") != "hi+fihi+fihi+fihi+fi":
        print("error in calc - 3")
    if calc("'a'*'2'+'b'*'2'") != "aabaab":
        print("error in calc - 4")
