# Completed in 02:55:26
import re

file_data = None
with open("aray.yara") as fp:
    file_data = fp.readlines()[7].strip()

expressions = file_data.split(" and ")

script = """from z3 import *

filesize = 85
flag = [BitVec(f"flag_{i}", 32) for i in range(filesize)]

solver = Solver()

for elem in flag:
    solver.add(elem > 31)
    solver.add(elem < 127)
"""

hashmap = {
    "738a656e8e8ec272ca17cd51e12f558b": "ul",
    "657dae0913ee12be6fb2a6f687aae1c7": "3A",
    "f98ed07a4d5f50f7de1410d905f1477f": "io",
    "89484b14b36a8d5329426a3d944d2983": "ru",
    "593f2d04aab251f60c9e4b8bbc1e05a34e920980ec08351a18459b2bc7dbf2f6": "fl",
    "0x61089c5c": "re",
    "0x5888fc1b": "eA",
    "0x66715919": "n.",
    "0x7cab8d64": "n:",
    "403d5f23d149670348b147a15eeb7010914701a7e99aad2e43f90cfa0325c76f": " s",
}


for expr in expressions:
    # filesize ^ uint8(11) != 107
    pattern1 = re.compile(r"^filesize (.) uint8\((\d+)\) (..?) (\d+)$")

    # uint8(55) & 128 == 0
    pattern2 = re.compile(r"^uint8\((\d+)\) (.) (\d+) (..?) (\d+)$")

    # uint8(17) > 31
    pattern3 = re.compile(r"^uint8\((\d+)\) (..?) (\d+)$")

    # uint32(52) ^ 425706662 == 1495724241
    pattern4 = re.compile(r"uint32\((\d+)\) (.) (\d+) (..?) (\d+)")

    # hash.md5(0, 2) == "89484b14b36a8d5329426a3d944d2983"
    pattern5 = re.compile(r'^hash.*\((\d+), 2\) == "?(.*?)"?$')

    if pattern1.match(expr):
        matches = pattern1.match(expr)
        left_num = 85
        operation = matches.group(1)
        right_num = matches.group(2)
        condition = matches.group(3)
        result    = matches.group(4)

        eq = f"{left_num} {operation} flag[{right_num}] {condition} {result}"

        script += f"solver.add({eq})\n"

    elif pattern2.match(expr):
        matches = pattern2.match(expr)
        left_num  = matches.group(1)
        operation = matches.group(2)
        right_num = matches.group(3)
        condition = matches.group(4)
        result    = matches.group(5)

        eq = f"flag[{left_num}] {operation} {right_num} {condition} {result}"
        script += f"solver.add({eq})\n"

    elif matches := pattern3.match(expr):
        left_num  = matches.group(1)
        condition = matches.group(2)
        result    = matches.group(3)

        eq = f"flag[{left_num}] {condition} {result}"
        script += f"solver.add({eq})\n"

    elif matches := pattern4.match(expr):
        left_num  = int(matches.group(1))
        operation = matches.group(2)
        right_num = matches.group(3)
        condition = matches.group(4)
        result    = matches.group(5)

        num3 = f"Extract(7, 0, flag[{left_num + 3}])"
        num2 = f"Extract(7, 0, flag[{left_num + 2}])"
        num1 = f"Extract(7, 0, flag[{left_num + 1}])"
        num0 = f"Extract(7, 0, flag[{left_num + 0}])"

        eq = f"Concat({num3}, {num2}, {num1}, {num0}) {operation} {right_num} {condition} {result}"

        script += f"solver.add({eq})\n"

    elif matches := pattern5.match(expr):
        offset = int(matches.group(1))
        hash   = matches.group(2)

        if value := hashmap.get(hash):
            script += f"solver.add(flag[{offset + 0}] == ord('{value[0]}'))\n"
            script += f"solver.add(flag[{offset + 1}] == ord('{value[1]}'))\n"
        else:
            print(f"Hash value not found for hash: {hash}")

    else:
        print(f"'{expr}' doesnt match")
        pass


# Some hashes can be un-hashed using crackstation.net
script += """
# hash.sha256(56, 2) == "593f2d04aab251f60c9e4b8bbc1e05a34e920980ec08351a18459b2bc7dbf2f6"
solver.add(flag[56] == ord("f"))
solver.add(flag[57] == ord("l"))


"""



script += """
print(solver.check())

if solver.check() == sat:
    soln = solver.model()

    output = []
    for i in range(filesize):
        output.append(soln[flag[i]].as_long())

    print(bytes(output))
"""

with open("solver.py", "w") as fp:
    fp.write(script)

