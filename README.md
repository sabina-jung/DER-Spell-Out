# DER Dump
Show the raw DER data of a base64-encoded file. 
Outputs a sequence of fields without syntax.

Tested with Python 2.7 and 3.2.

## Usage
        python derspellout.py <filename>

## Output
Output has the form

        OFFSET TYPE '(' LENGTH ')' = VALUE
        
Where the format of VALUE depends on the TYPE.
Offset refers to the position of the type byte,
not the data. Block elements open with

        OFFSET TYPE '(' LENGTH ')' 'BEGIN'
        
and close with

        OFFSET END TYPE '@' OFFSET

Here is some example output:

        1142 SEQUENCE(14) BEGIN
        1144 OBJECT IDENTIFIER(3) = "c0ffee"
        1149 BOOLEAN(1) = True
        1152 PRINTABLE STRING(4) = "duck"
        1158 END SEQUENCE@1142

