from cpu import cpu
from memory import memory
from clock import clock

# # memory[50] = 2
# memory.write_word(50, 2)
# # memory[100] = 2
# memory.write_word(100, 2)
# # memory[77] = 77
# memory.write_word(77, 77)
# # X1 <- X1 + memory[50]
# memory.write_byte(0, 1)
# memory.write_byte(1, 50)
# # X1 <- X1 - memory[100]
# memory.write_byte(2, 3)
# memory.write_byte(3, 100)
# # if X1 == 0 goto 13
# memory.write_byte(4, 8)
# memory.write_byte(5, 13)
# # X1 = X1 + memory[100]
# memory.write_byte(6, 1)
# memory.write_byte(7, 100)
# # X1 = X1 + memory[100]
# memory.write_byte(8, 1)
# memory.write_byte(9, 100)
# # memory[150] = X1
# memory.write_byte(10, 5)
# memory.write_byte(11, 150)
# # halt
# memory.write_byte(12, 255)
# # X1 = X1 + memory[77]
# memory.write_byte(13, 1)
# memory.write_byte(14, 77)
# # memory[150] = X1
# memory.write_byte(15, 5)
# memory.write_byte(16, 150)
# # halt
# memory.write_byte(17, 255)
#
# clock.start(cpu)
#
# print(memory.read_word(150))

memory.write_word(50, 21)
memory.write_word(100, 32)
memory.write_word(130, 10)

# X <- X + memory[50]
memory.write_byte(0, 1)      # X <- X + memory...
memory.write_byte(1, 50)     # ...[50]

# if X=0 goto 7
memory.write_byte(2, 8)
memory.write_byte(3, 6)

# X <- X + memory[100]
memory.write_byte(4, 1)      # X <- X + memory...
memory.write_byte(5, 100)    # ...[100]

# X <- X - memory[130]
memory.write_byte(6, 3)
memory.write_byte(7, 130)

# memory[150] = X
memory.write_byte(8, 5)
memory.write_byte(9, 150)

# stop
memory.write_byte(10, 255)

# run
clock.start(cpu)

print(memory.read_word(150))
