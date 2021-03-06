grammar smallC;

program
        : globalDeclaration? EOF
        ;

globalDeclaration
        : (functionDeclaration|constantDeclaration|constantAssignment)? SEMICOLON globalDeclaration?
        | functionDefinition globalDeclaration?
        | INCLUDE_STDIO globalDeclaration?
        ;

codeBody
        : OPEN_CURLY ((statement? SEMICOLON|ifStatement|whileStatement|codeBody))* CLOSE_CURLY
        ;

statement
        : constantAssignment
        | operatorAssignment
        | assignment
        | declaration
        | constantExpression
        | expression
        | returnStatement
        ;

returnStatement
        : RETURN (assignment|constantExpression|expression)?
        ;

constantExpression
        : constantExpression (STAR|FORWARD_SLASH) constantExpression #constantProduct
        | constantExpression (MINUS|PLUS) constantExpression #constantSum
        | constantExpression (LARGER_THAN|SMALLER_THAN|EQUALS) constantExpression #constantComparison
        | constant #constantValue
        ;

expression
        : expression (STAR|FORWARD_SLASH) expression #product
        | expression (PLUS|MINUS) expression #sum
        | expression (LARGER_THAN|SMALLER_THAN|EQUALS) expression #comparison
        | constant #const
        | operand #value
        ;

ifStatement
        : IF OPEN_BRACKET (assignment|expression) CLOSE_BRACKET (statement SEMICOLON|codeBody) elseStatement?
        ;

elseStatement
        : ELSE (statement SEMICOLON|codeBody)
        ;
        
whileStatement
        : WHILE OPEN_BRACKET (expression|assignment) CLOSE_BRACKET (statement SEMICOLON|codeBody)
        ;

typeName 
        : (INT_TYPE|CHAR_TYPE|FLOAT_TYPE) STAR*
        ;

declaration
        : constantDeclaration
        | typeName identifier (ASSIGN expression)?
        | arrayDeclaration
        ;

arrayDeclaration
        : typeName identifier OPEN_SQUARE constantExpression? CLOSE_SQUARE ASSIGN stringValue
        | typeName identifier OPEN_SQUARE constantExpression? CLOSE_SQUARE ASSIGN OPEN_CURLY arrayList CLOSE_CURLY
        | typeName identifier OPEN_SQUARE constantExpression CLOSE_SQUARE (ASSIGN OPEN_CURLY arrayList? CLOSE_CURLY)?
        ;

constantDeclaration
        : typeName identifier
        | typeName constantAssignment
        | constantArrayDeclaration
        ;

constantArrayDeclaration
        : typeName identifier OPEN_SQUARE constantExpression? CLOSE_SQUARE ASSIGN stringValue
        | typeName identifier OPEN_SQUARE constantExpression CLOSE_SQUARE (ASSIGN OPEN_CURLY constantArrayList? CLOSE_CURLY)?
        | typeName identifier OPEN_SQUARE constantExpression? CLOSE_SQUARE (ASSIGN OPEN_CURLY constantArrayList? CLOSE_CURLY)
        ;

arrayList
        : (expression COMMA)* expression
        ;

constantArrayList
        : (constantExpression COMMA)* constantExpression
        ;

arrayType
        : typeName identifier OPEN_SQUARE constantExpression? CLOSE_SQUARE
        ;

argumentDeclarationList
        : ((typeName identifier? | arrayType) COMMA)* (typeName identifier? | arrayType)
        ;

functionDeclaration
        : returnType identifier OPEN_BRACKET argumentDeclarationList? CLOSE_BRACKET
        ;
        
functionDefinition
        : functionDeclaration codeBody
        ;
        
returnType
        : VOID_TYPE
        | typeName
        ;
        
arrayElement
        : identifier OPEN_SQUARE (constantExpression|expression) CLOSE_SQUARE
        ;

assignment
        : (identifier|depointer) ASSIGN expression
        | arrayElement ASSIGN expression
        ;

operatorAssignment
        : (identifier|dereference|depointer|arrayElement) (PLUS|MINUS|STAR|FORWARD_SLASH) ASSIGN expression
        ;

constantAssignment
        : identifier ASSIGN constantExpression
        ;
        
functionCall
        : identifier OPEN_BRACKET argumentList? CLOSE_BRACKET
        ;
        
argumentList
        : (expression COMMA)* expression
        ;


operand
        : identifier
        | depointer
        | dereference
        | constant
        | functionCall
        | arrayElement
        | OPEN_BRACKET expression CLOSE_BRACKET
        ;

constant
        : intValue
        | floatValue
        | charValue
        | OPEN_BRACKET constantExpression CLOSE_BRACKET
        | dereference //Only for references to global variables, check in AST
        ;

identifier
        : VARIABLE
        ;

intValue
        : (MINUS|PLUS)? DIGIT
        ;

floatValue
        : (MINUS|PLUS)? DIGIT DOT DIGIT
        ;

charValue
        : ASCII_CHARACTER
        ;

stringValue
        : STRING
        ;

dereference
        : AMPERSAND VARIABLE
        ;

depointer
        : STAR* VARIABLE
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
AMPERSAND: '&';
FORWARD_SLASH : '/';
LARGER_THAN : '>';
SMALLER_THAN : '<';
EQUALS : '==';

DOT : '.';

DIGIT : [0-9]+;
SINGLE_QUOTE : '\'';
DOUBLE_QUOTE : '"';

WHITE_SPACE: [ \n\r\t]+ -> skip;
ASCII_CHARACTER : SINGLE_QUOTE [ -~] SINGLE_QUOTE;
STRING : DOUBLE_QUOTE [ -~]* DOUBLE_QUOTE;

IF : 'if';
ELSE : 'else';
WHILE : 'while';
RETURN : 'return';

VARIABLE : [a-zA-Z_][0-9a-zA-Z_]*;

SINGLE_LINE_COMMENT : '//' ~[\n\r]* -> skip;
MULTI_LINE_COMMENT : '/*' .*? '*/' -> skip;

INCLUDE_STDIO: '#include' [ ]+ '<stdio.h>';
