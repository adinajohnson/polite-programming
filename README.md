# Polite Programming

## Usage
interpret.py can simply be run on the command line as
```
python3 interpret.py filename
```
and it will interpret the contents of filename.

You can find the web app in action on [my website](polite.adinacheniae.com).

## Rationale
This is not in any way meant to be a practical or useful language—rather, something to help me better learn and practice the fundamentals of compilers while inserting at least some humor and entertainment.

I used [this tutorial](https://ruslanspivak.com/lsbasi-part1/) to learn about interpreter construction.

## Language Rules
* programs must begin with "hello" and end with "goodbye"
* each command must begin with "please" and end with "thankyou"
* comments begin with "disregard," which will cause the computer to disregard everything until the closing "thankyou"
* variables are assigned with the keyword "call" 
  * e.g. to give a the value 1, write "please call a 1 thankyou"
* to print something, use "say" 
  * e.g. "please say a thankyou"
  * or "please say "hi" thankyou"
* for boolean statements, use "is" 
  * e.g. "please 1+1 is 2 thankyou"
* for if statements, use "perchance" and "naturally" 
  * e.g. "please perchance 1+1 is 2 naturally please say a thankyou thankyou"
* for while loops, use "whilst" and "naturally"  
  * e.g. "please whilst a is 3 naturally please say a thankyou please call a a+1 thankyou"