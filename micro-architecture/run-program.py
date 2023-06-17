
import sys
from memory import memory
from cpu import cpu 
import clock as clk 
import disk

disk.read(str(sys.argv[1]))

clk.start([cpu])

print("Depois: ", memory.read_word(1))
