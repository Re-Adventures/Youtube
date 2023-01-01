import struct
dword = lambda x: struct.unpack("<I", x)[0]

with open('armageddon', 'rb') as fp:
  data = bytearray(fp.read())

nop = bytes.fromhex("0770a0e1") # mov r7, r7 --> 0x0770a0e1

i = 0
while i < len(data) - 4:
  if dword(data[i:i+4]) == 0xea000000:
    data[i:i + 4] = nop
    data[i + 4:i + 8] = nop
    i += 8
  else:
    i += 1

open('patched.bin', 'wb').write(data)
