class Node: 
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self, max_length):
        self.first = None
        self.last = None 
        self.length = 0
        self.max_length = max_length

    def is_full(self):
        if self.length == self.max_length:
            return True
        return False

    def is_empty(self):
        if self.length == 0:
            return True
        return False

    def enqueue(self, value):
        if self.is_full():
            return 
        
        new_node = Node(value)

        if self.is_empty(): 
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node

        self.length += 1

    def dequeue(self):
        if self.is_empty():
            return 
        
        node = self.first

        if self.length == 1:
            self.first = None
            self.last = None        
        else:
            self.first = node.next  

        self.length -= 1

        return node.value

MAX_SIZE_IN_BYTES = 7
BYTES_IN_WORD = 4

class IFU:
    def __init__(self):
        self.IMAR = 0
        self.shift_register = Queue(max_length=MAX_SIZE_IN_BYTES)

    def get_byte(self, word, index):
        return (word >> index * 8) & 0b11111111 

    def fetch(self, memory):
        # 32 bits
        if self.shift_register.length < 4:
            word = memory.read_word(self.IMAR)
            self.IMAR += 1

            for index in range(BYTES_IN_WORD):
                self.shift_register.enqueue(self.get_byte(word, index))
    
    def load(self, cpu):
        first_bits = 0
        second_bits = 0
        
        if not self.shift_register.is_empty():
            first_bits = self.shift_register.first  
            if self.shift_register.first.next is not None:
                second_bits = self.shift_register.first.next  

        cpu.registers["MBR1"] = first_bits
        cpu.registers["MBR2"] = (second_bits << 8) | first_bits

    def consume_mbr1(self):
        self.shift_register.dequeue()

    def consume_mbr2(self):
        self.shift_register.dequeue()
        self.shift_register.dequeue()

IFO = IFU()