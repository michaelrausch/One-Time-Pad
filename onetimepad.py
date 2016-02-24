#!/usr/bin/env python

""" 
Simple One Time Pad Library

Run this file, or call test() to run tests.
Usage in main()

"""

__author__ = "Michael Rausch"
__version__ = "1.0"
__email__ = "me@michaelrausch.nz"
__status__ = "Alpha"

import unittest

class OneTimePadTest(unittest.TestCase):
    def test_alphabet_values(self):
        """
        Checks that alphabet returns correct numbers
        """
        a = Alphabet()
        letter = "H"
        letter_as_num = a.get_letter_as_number("H")
        num_as_letter = a.get_number_as_letter(letter_as_num)
        self.assertEqual(num_as_letter, letter)
        
        
    def test_get_modulus(self):
        """
        Tests the get_modulus method, returns 26 for the default alphabet
        """
        a = Alphabet()
        self.assertEqual(a.get_modulus(), 26)
        
        
    def test_new_alphabet(self):
        a = Alphabet()
        a.set_new(['a','b'])
        modulus = a.get_modulus()
        self.assertEqual(modulus, 2)
        
        
    def test_data_obj(self):
        """
        Tests the generic data objects used for the CT, message, key etc
        """
        do = DataObject("Test")
        self.assertEqual(do.get(), "Test")
        do.set("t1")
        self.assertEqual(do.get(), "t1")
        
    
    def test_add_letters(self):
        """
        Test addition of letters
        """
        self.assertEqual(add_letters("b", "c"), 'D')
        
        
    def test_subtract_letters(self):
        """
        Tests subtraction of letters
        """
        self.assertEqual(subtract_letters("d", "c"), 'B')
        
        
    def test_encrypt(self):
        """
        Test Encryption
        """
        key = Key("jdfksadsjkflaffaskjfkgnfd")
        send_msg = Message("testmsg")
        enc_m = encrypt(key, send_msg)
        self.assertEqual(enc_m.get(), "CHXDESJ")
        
        
    def test_decrypt(self):
        """
        Test Decryption
        """
        enc_m = CipherText("CHXDESJ")
        key = Key("jdfksadsjkflaffaskjfkgnfd")
        dec_m = decrypt(key, enc_m)
        self.assertEqual(dec_m.get(), "TESTMSG")
            
            
class DataObject:
    """
    Generic data object that can be used to store a string
    """
    def __init__(self, data):
        self.data = data
    
    
    def set(self, data):
        self.data = data
        
        
    def get(self):
        return self.data
    
    
    def __str__(self):
        return self.data
    
        
class Message(DataObject):
    """
    Holds the message before encryption and after decryption
    """
    def __init__(self, message):
        DataObject.__init__(self, message)
        
        
class CipherText(DataObject):
    """
    Holds the encrypted ciphertext
    """
    def __init__(self, cipher_text):
        DataObject.__init__(self, cipher_text)
        
        
class Key(DataObject):
    """
    Holds the key used for encryption and decryption
    """
    def __init__(self, key):
        DataObject.__init__(self, key)
        
        
class Alphabet:
    """
    Holds an alphabet of supported characters
    """
    def __init__(self):
        self.alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
        
    def get_letter_as_number(self, letter):
        """
        Returns the index of the letter in the array
        """
        for i in range(0, len(self.alphabet)):
            if self.alphabet[i] == letter.upper():
                return i
            
            
    def get_number_as_letter(self, number):
        """
        Returns the letter from the index in the alphabet
        """
        try:
            return self.alphabet[number]
        
        except IndexError:
            print("Number is not a valid index")
            
            
    def get_modulus(self):
        """
        Returns the modulus used when adding/subtracting letters
        """
        return len(self.alphabet)
    
    
    def set_new(self, new):
        """
        Sets a new alphabet,
        new = An array of supported characters
        """
        self.alphabet = new
            
            
def add_letters(letter_a, letter_b):
    """
    Adds two letters together using the modulus of the alphabet
    """
    a = Alphabet()
    letter_a_num = a.get_letter_as_number(letter_a)
    letter_b_num = a.get_letter_as_number(letter_b)
    
    return a.get_number_as_letter((letter_a_num + letter_b_num) % a.get_modulus())


def subtract_letters(letter_a, letter_b):
    """
    Subtracts two letters and returns the value of the resulting letter within the alphabet
    """
    a = Alphabet()
    letter_a_num = a.get_letter_as_number(letter_a)
    letter_b_num = a.get_letter_as_number(letter_b)
    
    return a.get_number_as_letter((letter_a_num - letter_b_num) % a.get_modulus())
    
    
def encrypt(key_obj, message_obj):
    """
    Encrypts a message with the key
    """
    key = key_obj.get()
    message = message_obj.get()
    encrypted = ""
    
    if len(key) < len(message):
        return None
    
    for i in range(0, len(message)):
        encrypted += add_letters(message[i], key[i])
        
    return CipherText(encrypted)


def decrypt(key_obj, cipher_text_obj):
    """
    Decrypts the ciphertext into a message using the key
    """
    key = key_obj.get()
    cipher_text = cipher_text_obj.get()
    decrypted = ""
    
    if len(key) < len(cipher_text):
        return None
    
    for i in range(0, len(cipher_text)):
        decrypted += subtract_letters(cipher_text[i], key[i])
        
    return Message(decrypted)


def test():
    unittest.main(exit=False)
    
    
def main():
    key = Key("jdfksadsjkflaffaskjfkgnfd")
    send_msg = Message("fireatnoon")
    enc_m = encrypt(key, send_msg)    
    dec_m = decrypt(key, enc_m)
    print("Encrypted: {}".format(enc_m))
    print("Decrypted: {}".format(dec_m))    
            

if __name__ == "__main__": 
    test()
    main()
