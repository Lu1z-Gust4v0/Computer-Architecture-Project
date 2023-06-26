goto main 
wb 0

o ww 0
a ww 10
b ww 5
c ww 1

main  add  x1, b # x1 = 5 -> 4 -> 3 -> 2 -> 1 -> 0
      jz   x1, final 
      add2 x2, a # x2 = 10 + 10 + 10 + 10 + 10

      dec  x1    # x1 = 4 -> 3 -> 2 -> 1 -> 0
      mov  x1, b # b  = 4 -> 3 -> 2 -> 1 -> 0
      del  x1,   # x1 = 0
      
      goto main

final mov2 x2, o
      halt
