import sys
from memory import memory
from cpu import cpu
from clock import clock
from disk import disk

disk.read(str(sys.argv[1]))

clock.start(cpu)

print(f"Result\nWord 1: {memory.read_word(1)}\nWord 2: {memory.read_word(2)}")
