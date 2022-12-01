# Advent of Code 2022

My solutions to and thoughts about the problems of [AoC2022](https://adventofcode.com/2022).

## Code Structure

I've given each file a template that includes empty methods for Part 1 and Part 2 of each problem, along with boilerplate code to load the raw input. The input for each problem is stored as the global `INPUT`.

In a lot of problems, code can be shared between Parts 1 and 2, but there's no way to know that ahead of time. So I'll probably end up with some copypasta. I'm okay with that for two reasons: firstly, this is just for fun, and secondly, I would like Parts 1 and 2 to be able to run independently.

## Thoughts

### Day 1

There's not really much to talk about here. For Part 1, we can just keep track of the maximum calorie count seen so far. For Part 2, we could probably keep track of the top three only, but it works just as well to tally up all the calorie counts, sort the list, and add up the top three.