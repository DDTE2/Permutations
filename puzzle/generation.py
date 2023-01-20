from random import randint, shuffle, seed
from perm_math.Permutations import perms
from json import dumps
seed()

class puzzle:
    def __init__(self, layers=(0, 100), elements=(0, 999999), use_id_perm=True):
        if isinstance(layers, tuple) or isinstance(layers, list):
            a, b = layers
            if a > b:
                a, b = int(b), int(a)
            self.layers = randint(a, b)
        else:
            self.layers = layers

        if isinstance(elements, tuple) or isinstance(elements, list):
            a, b = elements
            if a > b:
                a, b = int(b), int(a)
            self.elements = randint(a, b)

        if use_id_perm:
            a = randint(0, self.layers)
            moves = [perms() for c in range(a)]
            self.layers -= a
        else:
            moves = []

        for a in range(self.layers):
            moves.append(self.random_perm())

        shuffle(moves)
        self.moves = {a+1: moves[a] for a in range(len(moves))}
        self.random_state()
        self.temporary_saving()

    def random_perm(self):
        end = []
        while not end:
            for a in range(self.elements):
                if randint(0, 1):
                    end.append(a + 1)

        start = end.copy()
        while start == end:
            shuffle(end)

        return perms(start, end)

    def random_state(self):
        *moves, = self.moves
        l = len(moves)
        self.state = self.moves[moves[randint(0, l - 1)]]
        move1 = self.state.copy()

        for a in range(3 * l):
            move2 = self.moves[moves[randint(0, l - 1)]]

            self.state *= move2
            move1, move2 = move2.copy(), False

    def temporary_saving(self):
        moves = {c:self.moves[c].dict for c in self.moves}
        data = {'moves': moves,
                'state': self.state.dict}

        with open('puzzle/save.data', 'w') as file:
            file.write(dumps(data))

    def __str__(self):
        return str(self.state)