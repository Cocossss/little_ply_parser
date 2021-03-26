# little_ply_parser
a parser for a language with basic syntax and simple conditional optimization

# if optimization
Examples of optimization:

>if 0 then {x := 13;} else {x := 42;};
>>x := 42;
>>
>if --(x==x) then {x := 13;} else {};
>>empty instructions
>>
>if x == y then {x := 13;} else {};
>>if x == y then {x := 13;} else {}; - if values of x and y are unknown


# Run commands (from root directory, no install needed)
python parser.py filename

filename - path to file with text to parse

# Test commands
python parser.py Tests/test#.txt

'#' - number of test

Tests/test1.txt -  expression test

Tests/test2.txt - instruction (while, if, return, assignment) test

Tests/test3.txt - if optimization test


