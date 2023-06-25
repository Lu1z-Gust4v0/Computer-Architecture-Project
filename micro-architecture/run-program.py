import sys
from memory import memory
from cpu import cpu
from clock import clock
from disk import disk

disk.read(str(sys.argv[1]))

clock.start(cpu)

print("After: ", memory.read_word(1))
