grammar smallC;

start 
        : program
        ;    

program 
        : program SEMICOLON
        | statement SEMICOLON
        | program statement SEMICOLON
        | program SINGLE_LINE_COMMENT
        | program ifBlock
        | program ifBlock elseBlock
        | 
        ;

statement 
        : declaration
        | assignment
        | operation
        | ifStatement
        ;

ifBlock
        : ifStatement statement SEMICOLON
        | ifStatement OPEN_CURLY program CLOSE_CURLY
        | ifStatement OPEN_CURLY CLOSE_CURLY
        ;

elseBlock
        : ELSE statement SEMICOLON
        | ELSE OPEN_CURLY program CLOSE_CURLY
        | ELSE OPEN_CURLY CLOSE_CURLY
        ;

ifStatement
        : IF OPEN_BRACKET assignment CLOSE_BRACKET
        | IF OPEN_BRACKET operation CLOSE_BRACKET
        | IF OPEN_BRACKET typeName assignment CLOSE_BRACKET
        ;

typeName 
        : INT_TYPE 
        | CHAR_TYPE
        | FLOAT_TYPE
        | typeName STAR
        ;

declaration 
        : typeName VARIABLE 
        | typeName assignment
        ;
        
assignment
        : VARIABLE ASSIGN operation
        ;

intValue 
        : MINUS DIGIT
        | PLUS DIGIT
        | DIGIT
        ;
    
floatValue 
        : intValue
        | intValue DOT DIGIT
        ;

charValue
        :  ASCII_CHARACTER 
        ;
        
operator
        : PLUS
        | MINUS
        | STAR
        | FORWARD_SLASH
        | LARGER_THAN
        | SMALLER_THAN
        | EQUALS
        ;

operand
        : VARIABLE
        | intValue
        | floatValue
        | charValue
        ;
operation
        : operand operator operation
        | operand
        | OPEN_BRACKET operation CLOSE_BRACKET
        ;        

OPEN_BRACKET : '(';
CLOSE_BRACKET: ')';
OPEN_CURLY : '{';
CLOSE_CURLY: '}';
SEMICOLON: ';';

INT_TYPE: 'int';
CHAR_TYPE: 'char';
FLOAT_TYPE: 'float';
VOID_TYPE: 'void';

ASSIGN : '=';
MINUS : '-';
PLUS : '+';
STAR : '*';
FORWARD_SLASH : '/';
LARGER_THAN : '>';
SMALLER_THAN : '<';
EQUALS : '==';

DOT : '.';

DIGIT : [0-9]+;
SINGLE_QUOTE : '\'';

WHITE_SPACE: [ \n\r\t]+ -> skip;
ASCII_CHARACTER : SINGLE_QUOTE [\t-~] SINGLE_QUOTE;

IF : 'if';
ELSE : 'else';
WHILE : 'while';
RETURN : 'return';

VARIABLE : [a-zA-Z_][0-9a-zA-Z_]*;

SINGLE_LINE_COMMENT : '//' ~[\n\r]* -> skip;
MULTI_LINE_COMMENT : '/*' [\t-~]* '*/' -> skip;
