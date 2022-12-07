from pathlib import Path
from typing import NamedTuple, Union, Dict, Optional, Tuple

DAY = 7
full_input_ = Path(f"{DAY}.txt").read_text()


class File(NamedTuple):
    name: str
    size: int
    parent: "Folder"


class Folder(NamedTuple):
    name: str
    subs: Dict[str, Union["Folder", File]]
    parent: Optional["Folder"]


def recurse(cwd: Folder, level: Tuple[str], sizes: Dict[Tuple[str], int]) -> int:
    cwdsize = 0
    for fname, sub in cwd.subs.items():
        if isinstance(sub, File):
            cwdsize += sub.size
        else:
            assert isinstance(sub, Folder)
            cwdsize += recurse(
                sub,
                level
                + tuple(
                    sub.name,
                ),
                sizes,
            )
    assert level not in sizes
    sizes[level] = cwdsize
    return cwdsize


def solvep1(root: Folder):
    sizes = {}
    total_size = recurse(root, ("/",), sizes)

    answer = 0
    for level, size in sizes.items():
        if size < 100000:
            answer += size

    return answer


def solvep2(root: Folder):
    sizes = {}
    total_size = recurse(root, ("/",), sizes)

    space_total = 70000000
    space_needed = 30000000
    space_free = space_total - total_size
    space_lack = space_needed - space_free

    found = total_size
    for level, size in sizes.items():
        if size >= space_lack:
            found = min(size, found)
    return found


def parse(input: str):
    root = Folder("/", {}, None)
    cwd = root

    chunks = input.split("\n$")
    for chunk in chunks:
        lines = [l.strip() for l in chunk.split("\n") if l]
        instruction, output = lines[0], lines[1:]
        if instruction == "$ cd /":
            assert not output
            continue

        if instruction.startswith("cd "):
            cmd, arg = instruction.split(" ")
            assert not output
            if arg == "/":
                cwd = root
            elif arg == "..":
                cwd = cwd.parent
            else:
                cwd = cwd.subs[arg]

        elif instruction == "ls":
            for sub in output:
                left, right = sub.split(" ")
                if left == "dir":
                    cwd.subs[right] = Folder(right, {}, cwd)
                else:
                    cwd.subs[right] = File(right, int(left), cwd)
        else:
            assert False
    return root


def testp1():
    input_ = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k    
"""
    parsed = parse(input_)
    result = solvep1(parsed)
    assert result == 95437


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)
