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

    def clear(self):
        while not self.is_empty():
            self.dequeue()

    def print_queue(self):
        queue = []
        element = self.first

        while element is not None:
            queue.append(element.value)
            element = element.next

        print("queue elements", queue)

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

    def fetch(self, memory):
        # fetch 32 bits at a time
        if self.shift_register.length < 4:
            for index in range(BYTES_IN_WORD):
                self.shift_register.enqueue(
                    memory.read_byte(self.IMAR + index)
                )
            self.IMAR += 4

    def load(self, cpu):
        first_bits = 0
        second_bits = 0

        if not self.shift_register.is_empty():
            first_bits = self.shift_register.first.value
            if self.shift_register.first.next is not None:
                second_bits = self.shift_register.first.next.value

        cpu.registers["MBR1"] = first_bits
        cpu.registers["MBR2"] = (second_bits << 8) | first_bits

    def consume_mbr1(self):
        self.shift_register.dequeue()

    def consume_mbr2(self):
        self.shift_register.dequeue()
        self.shift_register.dequeue()

    def update_imar(self, pc):
        # PC stores the current byte and IMAR stores the current word.
        # We have to convert bytes count to word count
        self.IMAR = pc
        self.shift_register.clear()


ifu = IFU()

