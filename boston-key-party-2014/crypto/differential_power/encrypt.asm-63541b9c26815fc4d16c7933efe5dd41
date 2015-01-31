add $t1, $zero, $zero# clear out $t1 ; 00004820
addi $t1, $t1, 0x9e# TEA magic is 0x9e3779b7 ; 2129009E
sll $t1, $t1, 8# shift out making room in the bottom 4; 00094a00
addi $t1, $t1, 0x37 ; 21290037
sll $t1, $t1, 8 ; 00094a00
addi $t1, $t1, 0x79 ; 21290079
sll $t1, $t1, 8 ; 00094a00
addi $t1, $t1, 0xb9 # now $t1 holds the magic 0x9e3779b9 ; 212900b9
add $t2, $zero, $zero# $t2 is the counter ; 00005020    
add $t0, $zero, $zero# $t0 is the sum ; 00004020        
lw $t8, $zero, 8# k0 mem[8-23] = k ; 8c180008   
lw $s7, $zero, 12# k1 ; 8C17000C
lw $s6, $zero, 16# k2 ; 8C160010
lw $t3, $zero, 20# k3 now our keys are in registers ;  8c0b0014 
lw $t7, $zero, 0# v0 mem[0-7] = v ; 8c0f0000
lw $t6, $zero, 4# v1, our plaintext is in the registers ; 8c0e0004
loop: add $t0, $t0, $t1# sum+=delta ; 01094020
sll $s4, $t6, 4# (v1 << 4) ; 000ea100   
add $s4, $s4, $t8# +k0  part 1 is in s4 ; 0298a020  
add $s3, $t6, $t0# (v1 + sum) part 2 is in s3 ; 01c89820    
srl $s2, $t6, 5# (v1 >> 5) ; 000e9142   
add $s2, $s2, $s7# +k1, now do the xors part 3 in s2 ; 02579020 
xor $s1, $s2, $s3# xor 2 and 3 parts ; 02728826
xor $s1, $s1, $s4# xor 1(2,3) ; 2348826
add $t7, $t7, $s1# done with line 2 of the tea loop ; 01f17820  
sll $s4, $t7, 4# (v0 << 4) ; 000fa100
add $s4, $s4, $s6# +k2 part 1 in s4 ; 0296a020  
add $s3, $t7, $t0# (v0 + sum) part 2 in s3  ; 01e89820  
srl $s2, $t7, 5# (v0 >> 5) ; 000f9142   
add $s2, $s2, $t3# +k3 part 2 in s2 ; 024b9020  
xor $s1, $s2, $s3# xor 2 and 3 parts ; 2728826
xor $s1, $s1, $s4# xor 1(2,3) ; 2348826
add $t6, $t6, $s1# done with line 2! ; 01d17020 
addi $s0, $zero, 32# for compare ; 20100020 
addi $t2, $t2, 1# the counter ; 214a0001    
bne $t2, $s0, 17# bne loop, now save back to the memory ; 15500010  
; here t6 and t7 are the two values we need :-)



00004820
2129009E
00094a00
21290037
00094a00
21290079
00094a00
212900b9
00005020
00004020
8c180008    
8C17000C
8C160010
8c0b0014
8c0f0000
8c0e0004
01094020
000ea100
0298a020
01c89820
000e9142
02579020
02728826
02348826
01f17820
000fa100
0296a020
01e89820
000f9142
024b9020
02728826
02348826
01d17020
20100020
214a0001
15500010

000048202129009E00094a002129003700094a002129007900094a00212900b900005020000040208c1800088C17000C8C1600108c0b00148c0f00008c0e000401094020000ea1000298a02001c89820000e914202579020027288260234882601f17820000fa1000296a02001e89820000f9142024b9020027288260234882601d1702020100020214a000115500010

