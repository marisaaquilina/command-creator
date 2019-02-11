# Command Creator
A program that writes its own programs to produce a desired output, using a genetic algorithm

## Getting Started
Run `python3 command-creator.py`

## Create a Command!
Type a space-separated sequence of integers like 1 2 -3 then press Enter.
The program will output the sequence of commands that construct your desired sequence of integers. 

If you run the same input of integers more than once, you'll most likely get a different sequence of commands. This is because the genetic algorithm uses some randomization by nature. While they are both valid, one of them may be more concise than the other.

## What Do the Commands Mean?
`>` to move right
`<` to move left
`+` to increment value
`-` to decrement value

## Quitting the Game
Type Q, press Enter
