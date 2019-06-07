.data
error: .asciiz "unrecognised parameter %"

.text
# a0 = pointer naar string, a1 = #argumenten, argumenten staan op de stack 

# $t0 = pointer naar string
# $t1 = # argumenten + offset voor volgende argument -> eerste argument zit k plekken onder frame, 2de k-1 plekken enz
# $t2 = positie in string
# $t3 = character dat nu bekeken wordt
# $t4 = Addres van variabele die geparsed wordt
# $t5-$t7 = temporary variables for %s

scanf:
move $t0, $a0 # Sla pointer op in 
move $t1, $a1 # Sla aantal argumenten op
sll $t1, $t1, 2 # Doe aantal argumenten * 4 ==> Beter voor de offset
li $t2, 0 # initialiseer de index in de string op 0

s_processChar:
addu $t3, $t0, $t2 # vind het adres van de character op index $t2
lw, $t3, ($t3) # laad het character in 
addi $t2, $t2, 4 # verhoog de index met 4 (= bytes )
beq $t3, 0, endScan # Als nulterminated, stop dan scanen
beq $t3, 37, s_percent # Als het een percentage is, spring dan naar percentage
b s_processChar 

s_percent:
# update character
addu $t3, $t0, $t2
lw $t3, ($t3)
addi $t2, $t2, 4

# Laad variabele in
la $t4, ($sp)
addu $t4, $t4, $t1
subu $t1, $t1, 4 # update offset van variabele
lw $t4, ($t4) 

beq $t3, 0, endScan
beq $t3, 105, scanInt # %i = int
beq $t3, 102, scanFloat # %f = float
beq $t3, 99, scanChar # %c = char
beq $t3, 115, scanString # %s = string

# Error als het niet 1 vd 3 aanvaarde paramters is 
la $a0, error
li $v0, 4
syscall
move $a0, $t3
li $v0, 11
syscall
li $v0, 10
syscall

scanInt:
li $v0, 5
syscall
sw $v0, ($t4)
b s_processChar

scanFloat:
li $v0, 6
syscall
swc1 $f0, ($t4)
b s_processChar

scanChar:
li $v0, 12
syscall
sw $v0, ($t4)
b s_processChar

scanString:
li $v0, 8
move $a0, $t4
li $a1, 255 # buffer is 255 bytes => 255 characters including 0 terminator
syscall
move $t5, $a0
move $t7, $sp

scanString1: # convert each char to a word
lb $t6, ($t5)
beq $t6, 10, scanString2  # strings are terinated by \n in input = 10 instead of 0
sw $t6, ($t7)
addiu $t5, $t5, 1
subiu $t7, $t7, 4
b scanString1

scanString2:
sw $zero, ($t7)
subiu $t7, $t7, 4
subu $t6, $sp, $t7  # offset

scanString3: # replace byte string with word string
beqz $t6, s_processChar
subu $t5, $sp, $t6
addiu $t5, $t5, 4
lw $t7, ($t5)
addu $t5, $t4, $t6
subiu $t5, $t5, 4
sw $t7, ($t5)
subu $t6, $t6, 4
b scanString3

endScan:
jr $ra
