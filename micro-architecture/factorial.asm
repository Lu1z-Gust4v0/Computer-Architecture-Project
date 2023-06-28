goto main
wb 0

output ww 0
number ww 12 

main  add  x1, number       # x1 <- num
      cp   x1, x2           # x2 <- x1
      dec2 x2               # x2 <- x2 - 1

      goto fat

fat   jz2 x2, final         # if x2 == 0 goto final
      mul2 x1, x2            # x1 <- x1 * x2
      dec2 x2               # x2 <- x2 - 1
 
      goto fat

final mov x1, output
      halt
