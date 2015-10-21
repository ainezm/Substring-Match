"""
substring_match.py
Author: Allison I Mann
Last Updated: 10/20/15

Use this code to efficiently find the largest matching substring between two strings.
This was an exercise in algorithm design and hashing. 
The algorithm is based on Rabin-Karp rolling hashing, and runs in O(nlogn) time, where n is the length of the strings.

Instructions:
Where str2 and str1 are the strings of interest, call:
largest_substring_match(str2, str1)
"""


def int_of_char(char):
    """
    Note: Feel free to modify this function, especially if you know that your 'str1' and 'str2' contain only certain chars;
    for example: letters, [ACGT], or numbers. You can create a dictionary char_to_int that maps these characters to integers 
    and in int_of_char(char) return char_to_int[char] to make the hashing more efficient.
    For example, letters:
        
        strint={}
        possibilities=string.ascii_letters
        for x in range(len(possibilities)):
            char_to_int[possibilities[x]]=x 
            
        def int_of_char(char):
            return char_to_int[char]
            
    Args:
        char (char) any character
 
    Returns:
        (int) a unique integer identifier of that character
   """
    return ord(char)

def firsthash(inputstr, base, prime):
    """
    firsthash and rollhash implement Rabin-Karp hashing algorithm. 
    firsthash hashes inputstr based on base and prime normally.
    
    Args:
        inputstr (str) any string
        base (int) the base we are using to hash
        prime (int) the large prime we are using to hash
        
    Returns:
        (int) the hash of inputstr mod prime.
   """
    hashed=0
    for x in range(len(inputstr)):
        hashed += int_of_char(inputstr[x]) * pow(base, len(inputstr) - x - 1, prime)
        hashed = hashed % prime
 
    return hashed % prime
 
def rollhash(prevhash, nextchar, prevchar, base, length, prime):
    """
    firsthash and rollhash implement Rabin-Karp hashing algorithm  
    Say the prevhash was for [prevchar + '...'], rollhash gives the hash of ['...' + nextchar] based on base and prime.
    
    Args:
        prevhash (int) the hash value for previous hashed string
        nextchar (char) the next character we want to add
        prevchar (char) the first char of the previous hashed string we want to remove
        base (int) the base we are using to hash
        length (int) the length of the string we are hashing
        prime (int) the large prime we are using to hash
        
    Returns:
        (int) the hash of ['...' + nextchar] mod prime.
   """
    return (prevhash * base + int_of_char(nextchar) - int_of_char(prevchar) * pow(base, length, prime)) % prime 
    
def hashlengths(hash_table, str2, str1, base, prime, length):
    """
    Use hashing to find any collisions of substrings of size length of 'str1' and 'str2'. Also updates hash_table.
    
   Args:
       hash_table (dict) the current hash table mapping int:int (hash to startindex of substring of str1)
       str2 (str) any string
       str1 (str) any string
       base (int) the base we are using to hash
       prime (int) the large prime we are using to hash
       length (int) the length of the substring
       
 
   Returns:
       (str) A substring of size length that exists in both `str2` and `str1`.      
   """
   #hash all substrings of str1 of size length using Rabin-Karp and add to hash_table
    for startindex in xrange(len(str1) - length + 1):
        stringy = str1[startindex:startindex+length]
        if startindex == 0:
            current_hash = firsthash(stringy, base, prime)
        else:
            current_hash = rollhash(current_hash, str1[startindex+length-1], str1[startindex-1], base, length, prime)
        hash_table[current_hash] = startindex

    for startindex in xrange(len(str2) - length + 1):
        #hash the substring of str2 starting at startindex
        to_hash = str2[startindex:startindex+length]
        if startindex == 0:
            current_hash = firsthash(to_hash, base, prime)
        else:
            current_hash = rollhash(current_hash, str2[startindex+length-1], str2[startindex-1], base, length, prime)
       
        if current_hash in hash_table:
            #there is a collision - some substring in str2 has same hash as substring in str1
            str1_start_index = hash_table[current_hash]
            if to_hash == str1[str1_start_index:str1_start_index + length]:
                #If the substrings are equal, we have a match of size length!
                return str1[str1_start_index:str1_start_index + length]
 
 
def largest_substring_match(str2, str1):
    """
   Args:
       str1 (str) any string
       str2 (str) an string
       Note: For better efficiency, if str1 and str2 both only contain certain characters, then modify 
       int_of_char(char) to return strint[char] rather than ord(char).
 
   Returns:
       (str) The substring of maximum length that exists in both `str2` and `str1`.      
   """
 
    hash_table = {}
    base = 31 
    prime = 203767
    hi = min(len(str1),len(str2))
    lo = 0
    length = (hi + lo) / 2
    #We perform a binary search over possible substring lengths until we find the max length.
    while (True):
        match = hashlengths(hash_table, str2, str1, base, prime, length)
        if match != None:
            #there is a match of size length, so we look for a longer match
            lo = length
        else:
            #there isn't a match of size length, so we recurse on the bottom half.
            hi = length
        length = (hi + lo) / 2
 
        if abs(hi - lo) <= 1:
            #We have found the max matched substring; it has length hi or lo.
            match = hashlengths(hash_table, str2, str1, base, prime, hi)
            if match == None:
                match_found = hashlengths(hash_table, str2, str1, base, prime, lo)
                if match_found != None:
                    return match_found
                else:
                    return ""
            return match
 
        hash_table.clear()
 
