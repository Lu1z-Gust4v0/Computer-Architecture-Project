goto main
wb 0

result ww 0
rest ww 0
a ww 17
b ww 2

main  add   X1, a           # x1 <- a  
      add2  X2, b           # x2 <- b
      div2  X1, X2          # H <- x1 // x2
      movh  H, result   

      mod2  X1, X2          # H <- X1 % X2
      movh  H, rest

      halt

