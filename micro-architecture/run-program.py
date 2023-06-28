import sys
from memory import memory
from cpu import cpu
from clock import clock
from disk import disk

disk.read(str(sys.argv[1]))

clock.start(cpu)

print(f"""| Result
| Word 01: {memory.read_word(1)}
| Word 02: {memory.read_word(0)}
--------------------------------------
""")
