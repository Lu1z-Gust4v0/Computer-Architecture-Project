from array import array

# We have 1 MB of space. Since each memory word has 32 bits (4 bytes), we have to divide 
# 1 MB by 4 bytes to get the amount of words in our memory. 
# We'll have 262.144 avaliable positions in the memory.
ONE_MEGABYTE = 1024 * 1024
WORD_SIZE = 4

class Memory: 
    def __init__(self, total_space=ONE_MEGABYTE, word_size=WORD_SIZE):
        self.memory = array("l", [0]) * (total_space // word_size)

    # Access functions
    def read_word(self, address):
        # get the first 18 bits of address
        word_address = address & 0b111111111111111111
        return self.memory[word_address]

    def write_word(self, address, value):
        # get the first 18 bits of address
        word_address = address & 0b111111111111111111
        # get the first 32 bits of value
        word_value = value & 0xFFFFFFFF
        self.memory[word_address] = word_value

    def read_byte(self, address):
        # Get the word address
        # 00000000_00000000_00000000_00000000
        word_address = (address & 0b111111111111111111) 
        # Get the byte position within the word
        byte_address = address & 0b11   # division rest
        
        word_value = self.memory[word_address]
        byte_value = word_value >> (byte_address << 3)
        byte_value = byte_value & 0xFF

        return byte_value

    def write_byte(self, address, value):
        # Get 8 bits of value
        byte_value = value & 0xFF 
        word_address = (address & 0b111111111111111111) 
        byte_address = address & 0b11   

        # Filter others bytes from word
        mask = ~(0xFF << (byte_address << 3))  
        
        word_value = self.memory[word_address] & mask         
        new_byte_value = byte_value << (byte_address << 3)       
        new_word_value = word_value | new_byte_value          

        self.memory[word_address] = new_word_value

memory = Memory()  
