grammar smallC;

program 
        : 
        | program SEMICOLON
        | program statement SEMICOLON
        ;

statement 
        : declaration
        | assignment
        | VARIABLE 
        ;

typeName 
        : INT_TYPE 
        | CHAR_TYPE
        | FLOAT_TYPE
        ;

declaration 
        : typeName  VARIABLE 
        | typeName assignment
        ;
        
assignment
        : VARIABLE EQUALS VARIABLE
        | VARIABLE EQUALS intValue
        | VARIABLE EQUALS floatValue
        | VARIABLE EQUALS charValue
        ;

intValue 
        : MINUS DIGIT
        | DIGIT
        ;
    
floatValue 
        : intValue
        | intValue DOT DIGIT
        ;

charValue
        :  ASCII_CHARACTER 
        ;

OPEN_BRACKET : '(';
CLOSE_BRACKET: ')';
SEMICOLON: ';';

INT_TYPE: 'int';
CHAR_TYPE: 'char';
FLOAT_TYPE: 'float';

EQUALS : '=';
MINUS : '-';

DOT : '.';

DIGIT : [0-9]+;
SINGLE_QUOTE : '\'';

WHITE_SPACE: [ \n\r\t]+ -> skip;
ASCII_CHARACTER : SINGLE_QUOTE [\t-~] SINGLE_QUOTE;

VARIABLE : [a-zA-Z_][0-9a-zA-Z_]*;
