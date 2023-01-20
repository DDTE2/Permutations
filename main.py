from puzzle.generation import puzzle

puzz = puzzle(layers=(5, 10),
              elements=(5, 20),
              use_id_perm=False)

print(puzz)