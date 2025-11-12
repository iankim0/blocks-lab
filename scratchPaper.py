from ladder import WordLadderSearchSpace

space = WordLadderSearchSpace("train", "prawn")
print(space.get_successors(("train",)))