.data
error: .asciiz "unrecognised parameter %"

.text
# %c #c
li $t0, 0
sw $t0, ($sp)
li $t0, 50
sw $t0, -4($sp)
li $t0, 37
sw $t0, -8($sp)
li $t0, 99
sw $t0, -12($sp)
li $t0, 37
sw $t0, -16($sp)

la $a0, ($sp)
subu $sp, $sp, 28

li $t0, 60
sw $t0, 4($sp)
li $t0, 61
sw $t0, 8($sp)

li $a1, 2
move $fp, $sp #temporary, verander in uiteindelijke code 

main:
jal printf
li $v0, 10
syscall

# a0 = pointer naar string, a1 = #argumenten, argumenten staan op de stack 

# $t0 = pointer naar string
# $t1 = # argumenten + offset voor volgende argument -> eerste argument zit k plekken onder frame, 2de k-1 plekken enz
# $t2 = positie in string
# $t3 = character dat nu bekeken wordt
# $t4 = variabele die geparsed wordt

printf:
move $t0, $a0 # Sla pointer op in 
move $t1, $a1 # Sla aantal argumenten op
sll $t1, $t1, 2 # Doe aantal argumenten * 4 ==> Beter voor de offset
li $t2, 0 # initialiseer de index in de string op 0

p_processChar:
addu $t3, $t0, $t2 # vind het adres van de character op index $t2
lw, $t3, ($t3) # laad het character in 
addi $t2, $t2, 4 # verhoog de index met 4 (= bytes )
beq $t3, 0, endPrint # Als nulterminated, stop dan printen
beq $t3, 37, p_percent # Als het een percentage is, spring dan naar percentage

# print het character
move $a0, $t3
li $v0, 11
syscall

b p_processChar 

p_percent:
# update character
addu $t3, $t0, $t2
lw $t3, ($t3)
addi $t2, $t2, 4

# Laad variabele in
la $t4, ($fp)
addu $t4, $t4, $t1
subu $t1, $t1, 4 # update offset van variabele

lw $a0, ($t4) # laad argument voor syscall in 
beq $t3, 0, endPrint
beq $t3, 105, printInt # %i = int
beq $t3, 102, printFloat # %f = float
beq $t3, 99, printChar # %c = char

# Error als het niet 1 vd 3 aanvaarde paramters is 
la $a0, error
li $v0, 4
syscall
move $a0, $t4
li $v0, 11
syscall
li $v0, 10
syscall

printInt:
li $v0, 1
syscall
b p_processChar

printFloat:
mtc1 $a0, $f12
li $v0, 2
syscall
b p_processChar

printChar:
li $v0, 11
syscall
b p_processChar

endPrint:
jr $ra
