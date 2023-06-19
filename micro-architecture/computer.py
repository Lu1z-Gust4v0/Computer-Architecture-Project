import ufc2x as cpu
from memory import memory
import clock as clk

memory.write_word(50, 21) 
memory.write_word(100, 32)
memory.write_word(130, 10)

# X <- X + memory[50]
memory.write_byte(1, 2)      # X <- X + memory...
memory.write_byte(2, 50)     # ...[50]

# if X=0 goto 7
memory.write_byte(3, 15)
memory.write_byte(4, 7)

# X <- X + memory[100]
memory.write_byte(5, 2)      # X <- X + memory...
memory.write_byte(6, 100)    # ...[100]

# X <- X - memory[130]
memory.write_byte(7, 6)
memory.write_byte(8, 130)
    
# memory[150] = X
memory.write_byte(9, 10)
memory.write_byte(10, 150)    
    
# stop
memory.write_byte(11, 255)


clk.start([cpu])

print(memory.read_word(150))