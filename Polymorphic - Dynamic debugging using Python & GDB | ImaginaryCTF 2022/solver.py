import subprocess
import os

prog_name = './polymorphic'

# The start address is taken from running program under gdb with empty
# passwd & checking the RIP value when segfaulted
start = 0x00000000004010b6

flag = ""

# Bruteforcing char by char
while "}" not in flag:
  for ch in range(33, 127):
    tmp = flag + chr(ch)

    # Writing the input to pass it using gdb
    with open('inp.txt', 'wb') as fp:
      fp.write(tmp.encode())

    with open('script.gdb', 'wb') as fp:
      fp.write(b'r < inp.txt\n\
                 p $rip\n\
                 q\n')

    # Running the process under gdb
    with subprocess.Popen(['gdb', '-q', prog_name, '-x', 'script.gdb', '--batch'],
                          stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE) as P:

      stdout, stderr = P.communicate()
      stdout = stdout.splitlines()

    # Finding the segfault address
    for i in range(len(stdout)):
      line = stdout[i]
      if b'segmentation fault' in line.lower():
        # addr in in the form 0x00000000004010b6 in _start ()
        addr = stdout[i+1].split(b' ')[0]
        addr = int(addr[2:], 16)
          
    # if the program segfault further this means that we found a correct
    # character
    if addr > start:
      start = addr
      flag = tmp
      print(f"{addr:#08x}: {flag}")
      
      break
