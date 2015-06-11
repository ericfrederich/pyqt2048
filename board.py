#!/usr/bin/env python3

from enum import Enum, unique
from random import Random

rand = Random()

DEBUG = False

class Direction(Enum):
    up    = 1
    down  = 2
    left  = 3
    right = 4

def collapse_left(row):
    n_blanks = row.count(0)
    non_blanks = [x for x in row if x]
    i = -1
    while i < len(non_blanks) - 2:
        i += 1
        if DEBUG: print('looking at', non_blanks, 'with i = ', i)
        if non_blanks[i] == non_blanks[i+1]:
            non_blanks[i] *= 2
            del non_blanks[i+1]
            n_blanks += 1

    non_blanks.extend([0] * n_blanks)
    return non_blanks

class Board(object):
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.data = []
        for i in range(5):
            row  = []
            for j in range(5):
                row.append(0)
            self.data.append(row)

        self.add()
        self.add()

    def add(self):
        blanks = []
        for i, row in enumerate(self.data):
            for j, val in enumerate(row):
                if not val:
                    blanks.append((i,j))

        i, j = rand.choice(blanks)
        self.data[i][j] = 2

    def dump(self):
        for row in self.data:
            print(' '.join([str(x) if x else '-' for x in row]))

    def flip_left_right(self):
        self.data = [row[::-1] for row in self.data]

    def rows_to_cols(self):
        self.data = [[row[c] for row in self.data] for c in range(len(self.data[0]))]

    def move(self, direction):

        do_add = False

        if direction == Direction.up:
            self.rows_to_cols()
        if direction == Direction.down:
            self.rows_to_cols()
            self.flip_left_right()
        if direction == Direction.left:
            pass
        if direction == Direction.right:
            self.flip_left_right()

        # do the move
        for row in self.data:
            new = collapse_left(row)
            if row != new:
                row[:] = new
                do_add = True

        if direction == Direction.up:
            self.rows_to_cols()
        if direction == Direction.down:
            self.flip_left_right()
            self.rows_to_cols()
        if direction == Direction.left:
            pass
        if direction == Direction.right:
            self.flip_left_right()

        if do_add:
            self.add()


if __name__ == '__main__':
    b = Board()
    b.dump()

    for start, finish in [
        ('22200', '42000'),
        ('40004', '80000'),
        ('40040', '80000'),
        ('40400', '80000'),
        ('44000', '80000'),
        ('44404', '88000'),
        ('02442', '28200'),
    ]:
        start = [int(x) for x in start]
        finish = [int(x) for x in finish]
        result = collapse_left(start)
        if result != finish:
            print('*' * 80)
            print('Expected', start, '->', finish)
            print('Got     ', start, '->', result)
            print('*' * 80)
        else:
            print('Good', start, '->', finish)
