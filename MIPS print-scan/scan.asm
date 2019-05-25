.data
error: .asciiz "unrecognised parameter %"

.text
# %c #c
li $t0, 0
sw $t0, ($sp)
li $t0, 37
sw $t0, -4($sp)
li $t0, 102
sw $t0, -8($sp)

la $a0, ($sp)

la $t0, -12($sp)
sw $t0, -16($sp)
subu $sp, $sp, 20

li $a1, 1
move $fp, $sp #temporary, verander in uiteindelijke code 

main:
jal scanf
li $v0, 10
syscall

# a0 = pointer naar string, a1 = #argumenten, argumenten staan op de stack 

# $t0 = pointer naar string
# $t1 = # argumenten + offset voor volgende argument -> eerste argument zit k plekken onder frame, 2de k-1 plekken enz
# $t2 = positie in string
# $t3 = character dat nu bekeken wordt
# $t4 = Addres van variabele die geparsed wordt

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
la $t4, ($fp)
addu $t4, $t4, $t1
subu $t1, $t1, 4 # update offset van variabele
lw $t4, ($t4) 

beq $t3, 0, endScan
beq $t3, 105, scanInt # %i = int
beq $t3, 102, scanFloat # %f = float
beq $t3, 99, scanChar # %c = char

# Error als het niet 1 vd 3 aanvaarde paramters is 
la $a0, error
li $v0, 4
syscall
move $a0, $t4
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
mtc1 $a0, $f12
li $v0, 6
syscall
swc1 $f0, ($t4)
b s_processChar

scanChar:
li $v0, 12
syscall
sw $v0, ($t4)
b s_processChar

endScan:
jr $ra
