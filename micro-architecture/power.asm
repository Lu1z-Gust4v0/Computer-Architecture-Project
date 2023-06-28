goto main                              # 1 step
wb 0

result ww 0
base ww 10
expoent ww 3 

main  add3 x3, expoent                 # 2 steps
      jz3  x3, expoent_zero            # 2 steps
      add  x1, base                    # 2 steps                    
      cp   x1, x2                      # 2 steps

      goto power                       # 1 step

expoent_zero  del x1                   # x1 <- 0      | 1 step
              inc x1                   # x1 <- x1 + 1 | 1 step
              mov x1, result           # 2 steps
              halt                     # 1 step

power dec3 x3
      jz3 x3, final
      
      mul2 x1, x2
      
      goto power

final mov x1, result                   # 2 steps
      halt                             # 1 step 

