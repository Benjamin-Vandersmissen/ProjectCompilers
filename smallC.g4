grammar smallC;

start
        : program
        ;

program
        : program declaration SEMICOLON
        | program functionDeclaration SEMICOLON
        | program functionDefinition
        | program INCLUDE_STDIO
        | declaration SEMICOLON
        | functionDeclaration SEMICOLON
        | functionDefinition
        | INCLUDE_STDIO
        | 
        ;

codeBody
        : codeBody SEMICOLON
        | statement SEMICOLON
        | codeBody statement SEMICOLON
        | codeBody SINGLE_LINE_COMMENT
        | codeBody ifBlock
        | codeBody ifBlock elseBlock
        | codeBody whileBlock
        |
        ;

statement 
        : declaration
        | assignment
        | operation
        | RETURN operation
        ;

ifBlock
        : ifStatement statement SEMICOLON
        | ifStatement OPEN_CURLY CLOSE_CURLY
        | ifStatement OPEN_CURLY codeBody CLOSE_CURLY
        ;

elseBlock
        : ELSE statement SEMICOLON
        | ELSE OPEN_CURLY CLOSE_CURLY
        | ELSE OPEN_CURLY codeBody CLOSE_CURLY
        ;

ifStatement
        : IF OPEN_BRACKET assignment CLOSE_BRACKET
        | IF OPEN_BRACKET operation CLOSE_BRACKET
        | IF OPEN_BRACKET typeName assignment CLOSE_BRACKET
        ;
        
whileStatement
        : WHILE OPEN_BRACKET operation CLOSE_BRACKET
        | WHILE OPEN_BRACKET assignment CLOSE_BRACKET
        | WHILE OPEN_BRACKET typeName assignment CLOSE_BRACKET
        ;
        
whileBlock
        : whileStatement statement SEMICOLON
        | whileStatement OPEN_CURLY CLOSE_CURLY
        | whileStatement OPEN_CURLY codeBody CLOSE_CURLY
        ;

typeName 
        : INT_TYPE 
        | CHAR_TYPE
        | FLOAT_TYPE
        | typeName STAR
        ;

declaration 
        : typeName identifier
        | typeName assignment
        | typeName identifier OPEN_SQUARE operation CLOSE_SQUARE
        | typeName identifier OPEN_SQUARE operation CLOSE_SQUARE ASSIGN OPEN_CURLY arrayList CLOSE_CURLY
        | typeName identifier OPEN_SQUARE CLOSE_SQUARE ASSIGN OPEN_CURLY arrayList CLOSE_CURLY
        ;
    
arrayList
        : arrayList COMMA operation
        | operation
        ;
        
    
functionDeclaration
        : returnType identifier OPEN_BRACKET argumentDeclarationList CLOSE_BRACKET
        | returnType identifier OPEN_BRACKET CLOSE_BRACKET
        ;
        
argumentDeclarationList
        : typeName identifier
        | typeName
        | argumentDeclarationList COMMA typeName identifier
        ;
        
functionDefinition
        : functionDeclaration OPEN_CURLY codeBody CLOSE_CURLY
        ;
        
returnType
        : VOID_TYPE
        | typeName
        ;
        
arrayElement
        : identifier OPEN_SQUARE operation CLOSE_SQUARE
        ;
        
assignment
        : identifier ASSIGN operation
        | arrayElement ASSIGN operation
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
        
functionCall
        : identifier OPEN_BRACKET CLOSE_BRACKET
        | identifier OPEN_BRACKET argumentList CLOSE_BRACKET
        ;
        
argumentList
        : operation
        | argumentList COMMA operation
        ;
        
comparator
        : LARGER_THAN
        | SMALLER_THAN
        | EQUALS
        ;

operand
        : identifier
        | intValue
        | floatValue
        | charValue
        | functionCall
        | arrayElement
        | OPEN_BRACKET operation CLOSE_BRACKET
        ;
      
sumOperation
        : productOperation PLUS productOperation
        | productOperation MINUS productOperation
        | sumOperation PLUS productOperation
        | sumOperation MINUS productOperation
        | productOperation
        ;

productOperation
        : productOperation STAR productOperation
        | productOperation FORWARD_SLASH productOperation
        | operand
        ;

operation
        : sumOperation
        | operation comparator operation
        ;        

identifier
        : VARIABLE
        ;



OPEN_BRACKET : '(';
CLOSE_BRACKET: ')';
OPEN_CURLY : '{';
CLOSE_CURLY: '}';
OPEN_SQUARE : '[';
CLOSE_SQUARE : ']';
SEMICOLON: ';';
COMMA: ',';

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
MULTI_LINE_COMMENT : '/*' .*? '*/' -> skip;

INCLUDE_STDIO: '#include' [ ]+ '<stdio.h>';
