# Advent of Code 2022

My solutions to and thoughts about the problems of [AoC2022](https://adventofcode.com/2022).

WARNING: There *will* be spoilers below. Watch out!

## Code Structure

I've given each file a template that includes empty methods for Part 1 and Part 2 of each problem, along with boilerplate code to load the raw input. The input for each problem is stored as the global `INPUT`.

In a lot of problems, code can be shared between Parts 1 and 2, but there's no way to know that ahead of time. So I'll probably end up with some copypasta. I'm okay with that for two reasons: firstly, this is just for fun, and secondly, I would like Parts 1 and 2 to be able to run independently.

## Thoughts

### Day 1

There's not really much to talk about here. For Part 1, we can just keep track of the maximum calorie count seen so far. For Part 2, we could probably keep track of the top three only, but it works just as well to tally up all the calorie counts, sort the list, and add up the top three.

---

### Day 2

For this day, there is Rock-Paper-Scissors logic going on, which we *could* implement in code. But there are only 9 possible outcomes in each part, so instead of writing out all the logic, we can precompute (by hand) the values for each of the 9 possible outcomes, store them in a dictionary, and then use the inputs to index into the dictionary. This saves a lot of time and potential mistakes.

```py
PART1_SCORES = {'A': {'X': 1 + 3, 'Y': 2 + 6, 'Z': 3 + 0},
                'B': {'X': 1 + 0, 'Y': 2 + 3, 'Z': 3 + 6},
                'C': {'X': 1 + 6, 'Y': 2 + 0, 'Z': 3 + 3}}
```

Each score is written as `move_value + outcome_value`, for readability. That ended up being a good decision, as I could easily make the edits for the new scores in Part 2.

---

### Day 3

In this problem, we're looking for overlap between lists of letters, and told that the overlap will be unique. That means that even if there's repetition in the lists, there *won't* be repetition of the overlapping item. So we can treat the lists as *sets* of letters, and use Python's `set` object to do all the heavy lifting for us. That's a powerful tool for a weak problem, but it makes the code short and sweet!

---

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

---

### Day 5

This day was mostly a challenge of parsing a strangely formatted file, espcially the part detailing the initial stack of crates. The test input looks like this.

```
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
```

All the crates have one-character names, so parsing this part isn't too bad. The crates names are every fourth character, starting at index 1. And the final line gives us the number of crates. So we can store all the crates as a `list` of characters from bottom to top.

After that, parsing the instructions wasn't too bad. Something like this `"move 1 from 2 to 1"` could be split on the spaces, and then we can ignore the words `move`, `from`, and `to`. Python's `namedtuple` type was nice here to do print-debugging along the way, but not really necessary.

After the instructions were parsed, we could use Python's `list` operations to do all the heavy lifting for us!

---

### Day 6

This puzzle was the quickest one yet. We can use the power of Python's `set` class again, since it "removes" duplicates. For each slice of length `n`, we can check `len(set(slice)) == n` to see if the slice contains `n` unique characters. Just like last time, this is sort of overkill for the job, but it makes the code short and sweet.

---

### Day 7

This is another AoC classic: file structures! I like the idea of parsing someone's command line log a lot. We could use lists of lists here, and just be careful about what index corresponds to what, but that's not very readable or elegant. So we can use Python's object-oriented capabilities to create two new types: `File` and `Directory`. These classes aren't very complicated, but they do exactly what we need.

```py
class Directory:
    def __init__(self, name: str = None, parent = None):
        self.name = name
        self.parent = parent
        self.children = []

class File:
    def __init__(self, name: str = None, size: int = 0):
        self.name = name
        self.size = size
```

Once we have this, parsing the output of `ls` is a simple matter of instantiating the right classea at the right time. Since the file structure is used in both parts,  we do all of this at the parsing stage.

Both parts of this problem are about the size of directories, so we need a way to calculate that. We can add a method to the directory class:

```py
class Directory:
    def calculate_size(self):
        size = 0
        for child in self.children:
            if type(child) == File:
                size += child.size
            else:
                size += child.calculate_size()
        return size
```

Note that this method has no memoization, so calling it repeatedly is *not* efficient. But the input to this problem is small enough that it won't matter. Once we have this, parts 1 and 2 are very straightforward!

---

### Day 8

> Without meaning to, I switched back to first-person singular here, rather than the mathematician-style "we" I'd been using before. I think I'll just stick with it, it makes the README more personal. :)

This day was interesting! And I really like the theme. For Part 1, I wrote four `for` loops that checked the visibility in each direction. After some finagling, they were all correct, and the problem worked! But the code was rather ugly. In four different spots, I had something like the following.

```py
    tree_height = INPUT[y][x]
    if tree_height > highest_seen:
        visible[y][x] = True
        highest_seen = tree_height
```

Code duplication within the same part of the problem is something I'm trying to avoid, so I decided to factor out this code into its own function, included below. This makes the solution much more readable. The only downside here is that this function has side-effects! In general, I like to avoid that type of thing, but I didn't want to spend too much more time refactoring. So I made a comment and moved onto part two! (Note that `INPUT` is a global, so we don't need to pass that in.)

```py
# Note: modifies the visible list
def update_visible(x: int, y: int, highest_seen: int, visible: list):
    tree_height = INPUT[y][x]
    if tree_height > highest_seen:
        visible[y][x] = True
        highest_seen = tree_height
    return highest_seen
```

In part two, I saw the potential for the same code duplication to happen, so I started with a function that could count visible trees in any direction (including diagonally, but we didn't need that here). No side-effects on this one!

```py
def count_visible(x0: int, y0: int, dx: int, dy: int):
    width = len(INPUT[0])
    height = len(INPUT)
    starting_height = INPUT[y0][x0]

    x, y = x0+dx, y0+dy
    count = 0
    while 0 <= x < width and 0 <= y < height:
        if INPUT[y][x] < starting_height:
            count += 1
        if INPUT[y][x] >= starting_height: # We can also see the last tree!
            count += 1
            break
        x += dx
        y += dy
    
    return count
```

Then it was simply a matter of searching for the tree with the highest `scenic_score`!

---

### Day 9

> I'm backtracking a little on the "we" thing from earlier. The mathematician in me can't help but write it when talking about problem solving. So I'll just mix-and-match. I think it reads pretty well still.

This day was very reminiscent of SNAKE! I really liked the visuals of the rope.

For part one, we just have a head and a tail to keep track of. The head moves only orthogonally, and we have to keep the tail next to the head, but "next to" includes diagonally. 

First, I want to show a convenient trick that I like to use whenever there is movement like this. We could code up four `if` statements (one for each direction). But the bodies of each of those statements will probably be almost identical. So we can instead use a dictionary to do the heavy lifting:

```py
directions = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}
```

Then, when we want to know how much to move, we can write something like this!

```py
move_x, move_y = directions[dir]
```

Okay, so onto the logic for the tail. Let's let `dx` and `dy` represent how far the head and tail are from each other horizontally and vertically, respectively. At each step, we have five situations:

- The head is next to the tail, i.e. `dx` and `dy` are both `<=1`. In this case the tail doesn't move.
- The head is not next to the tail and moved horizontally, i.e. `dx == 2`.
  - If `dy == 0`, the tail needs to move horizontally only.
  - Otherwise, the tail needs to move horizontally and vertically.
- The head is not next to the tail and moved vertically, i.e. `dy == 2`.
  - If `dx == 0`, the tail needs to move vertically only.
  - Otherwise, the tail needs to move horizontally and vertically.

If we allow `dx` and `dy` to be negative, we can capture the direction of horizontal/vertical movement as well. Putting this all together, we get code that looks like this.

```py
dx, dy = head_x - tail_x, head_y - tail_y

if abs(dx) == 2:
    tail_x += dx//2
    if abs(dy) == 1:
        tail_y += dy

if abs(dy) == 2:
    tail_y += dy//2
    if abs(dx) == 1:
        tail_x += dx
```

And that works perfectly! The tail moves exactly where it's supposed to. When I initally did part one, I had this code chunk in my `part1()` function. But then part two has *nine* segments that all need to move that way, so I factored it out into its own function, `get_new_location(head, tail)`, and used that in both parts.

The final step is to keep track of the unique tail locations, which we can do using a `set`. Then we just return the number of elements in the `set` and [job's done](https://www.youtube.com/watch?v=5r06heQ5HsI)!

There's one other thing I want to mention here. When I worked through part one using the test case, I wrote a function that printed out the current state of the head and tail, matching the style on the website. I can't overstate how useful this was, as I could visually inspect and identify the steps where my code was going wrong. They even recommend doing that during part two of the problem. I would highly recommend it!

---