# Advent of Code 2022

My solutions to and thoughts about the problems of [AoC2022](https://adventofcode.com/2022).

WARNING: There *will* be spoilers below. Watch out!

## Code Structure

I've given each file a template that includes empty methods for Part 1 and Part 2 of each problem, along with boilerplate code to load the raw input. The input for each problem is stored as the global `INPUT`.

In a lot of problems, code can be shared between Parts 1 and 2, but there's no way to know that ahead of time. So I'll probably end up with some copypasta. I'm okay with that for two reasons: firstly, this is just for fun, and secondly, I would like Parts 1 and 2 to be able to run independently.

## Thoughts

### Day 1

There's not really much to talk about here. For Part 1, we can just keep track of the maximum calorie count seen so far. For Part 2, we could probably keep track of the top three only, but it works just as well to tally up all the calorie counts, sort the list, and add up the top three.

### Day 2

For this day, there is Rock-Paper-Scissors logic going on, which we *could* implement in code. But there are only 9 possible outcomes in each part, so instead of writing out all the logic, we can precompute (by hand) the values for each of the 9 possible outcomes, store them in a dictionary, and then use the inputs to index into the dictionary. This saves a lot of time and potential mistakes.

```py
PART1_SCORES = {'A': {'X': 1 + 3, 'Y': 2 + 6, 'Z': 3 + 0},
                'B': {'X': 1 + 0, 'Y': 2 + 3, 'Z': 3 + 6},
                'C': {'X': 1 + 6, 'Y': 2 + 0, 'Z': 3 + 3}}
```

Each score is written as `move_value + outcome_value`, for readability. That ended up being a good decision, as I could easily make the edits for the new scores in Part 2.

### Day 3

In this problem, we're looking for overlap between lists of letters, and told that the overlap will be unique. That means that even if there's repetition in the lists, there *won't* be repetition of the overlapping item. So we can treat the lists as *sets* of letters, and use Python's `set` object to do all the heavy lifting for us. That's a powerful tool for a weak problem, but it makes the code short and sweet!

### Day 4

This is a classic Advent of Code-style problem! We're checking two ranges of integers for overlaps, call them $[a,b]$ and $[c,d]$.

In Part 1, we're checking for complete containment, which we can visualize as follows.

```
      Case 1                Case 2
      
      [----]               [--]
   [----------]    OR    [----------]
   |  |    |  |          | |  |     |
   a  c    d  b          c a  b     d
```

So we need to check $(a \le c \textrm{ and } d \le b)$ or $(c \le a \textrm{ and } b \le d)$. So just two cases!

In Part 2, we're checking for any overlap at all, i.e. $[a,b]\cap[c,d] \ne \emptyset$. At first, it seems like there will be more cases, because the two intervals could overlap *or* one could be entirely contained within the other. But we actually don't care *how* the intervals overlap. After some consideration, we could come up with this visualization.

```
      Case 1                Case 2
      
       [--...                [--...
   [----------]    OR    [----------]
   |   |      |          |   |      |
   a   c      b          c   a      d
```

One of the intervals will start earlier on the number line (or the same spot). So we only need to check whether or not the later interval *starts* inside the first one. Once we know that, it doesn't matter where the second interval ends because we already know that they overlap! So we again have two cases: $(a \le c \le b)$ or $(c \le a \le d)$.

### Day 5

Today was mostly a challenge of parsing a strangely formatted file, espcially the part detailing the initial stack of crates. The test input looks like this.

```
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
```

All the crates have one-character names, so parsing this part isn't too bad. The crates names are every fourth character, starting at index 1. And the final line gives us the number of crates. So we can store all the crates as a `list` of characters from bottom to top.

After that, parsing the instructions wasn't too bad. Something like this `"move 1 from 2 to 1"` could be split on the spaces, and then we can ignore the words `move`, `from`, and `to`. Python's `namedtuple` type was nice here to do print-debugging along the way, but not really necessary.

After the instructions were parsed, we could use Python's `list` operations to do all the heavy lifting for us!