from pathlib import Path

DAY = 1
full_input_ = Path(f"{DAY}.txt").read_text()

E = [sum(map(int, chunk.split("\n"))) for chunk in full_input_.split("\n\n")]
print(max(E))
print(sum(sorted(E)[-3:]))
