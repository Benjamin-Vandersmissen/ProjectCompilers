grammar smallC;

program 
        : 
        | program SEMICOLON
        | program statement SEMICOLON
        ;

statement 
        : declaration
        | assignment
        | operation
        ;

typeName 
        : INT_TYPE 
        | CHAR_TYPE
        | FLOAT_TYPE
        | typeName STAR
        ;

declaration 
        : typeName  VARIABLE 
        | typeName assignment
        ;
        
assignment
        : VARIABLE EQUALS operation
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
SEMICOLON: ';';

INT_TYPE: 'int';
CHAR_TYPE: 'char';
FLOAT_TYPE: 'float';

EQUALS : '=';
MINUS : '-';
PLUS : '+';
STAR : '*';
FORWARD_SLASH : '/';

DOT : '.';

DIGIT : [0-9]+;
SINGLE_QUOTE : '\'';

WHITE_SPACE: [ \n\r\t]+ -> skip;
ASCII_CHARACTER : SINGLE_QUOTE [\t-~] SINGLE_QUOTE;

VARIABLE : [a-zA-Z_][0-9a-zA-Z_]*;
