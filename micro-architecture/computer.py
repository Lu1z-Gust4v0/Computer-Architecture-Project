from cpu import cpu
from memory import memory
from clock import clock

# memory[50] = 2
memory.write_word(50, 2)
# memory[100] = 2
memory.write_word(100, 2)
# X1 <- X1 + memory[50]
memory.write_byte(0, 1)
memory.write_byte(1, 50)
# X1 <- X1 + memory[100]
memory.write_byte(2, 1)
memory.write_byte(3, 100)

clock.start(cpu)

print(cpu.registers["X1"])

""" memory.write_word(50, 21) 
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
 """

clock.start(cpu)

# print(memory.read_word(150))