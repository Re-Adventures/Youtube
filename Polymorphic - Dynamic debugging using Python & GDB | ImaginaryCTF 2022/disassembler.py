import capstone
import struct

udword = lambda x: struct.unpack("<I", x)[0]
dword  = lambda x: struct.pack("<I", x)

with open('polymorphic', 'rb') as fp:
  data = fp.read()

code = bytearray(data[0x1000:0x1cff])

dis_engine = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

instructions = {}
printed = ["0"]

start = 0
to_break = False
while not to_break:

  inst = dis_engine.disasm(code[start:], 0x000000000401000)

  for decoded in inst:
    # print(start, decoded.size, decoded.mnemonic, decoded.op_str)
    # if tmp in instructions:
      # to_break = True
    start += decoded.size

    # xor dword ptr [rip + 0xa], 0xa5d80c00
    if "xor" in decoded.mnemonic and "dword ptr" in decoded.op_str:
      # instructions.pop() # We dont need this obfuscation instruction
      tmp = decoded.op_str.split()
      xor_val = int(tmp[-1].split('0x')[1], 16)

      if "[rip]" in decoded.op_str:
        offset = 0

      else:
        offset = None
        for j in range(len(tmp)):
          if "rip" in tmp[j]:
            assert "]" in tmp[j+2]
            # If the offset is in hex form
            if tmp[j+2].startswith("0x"):
              offset = int(tmp[j+2][2:-2], 16)
            # decimal form
            else:
              offset = int(tmp[j+2][:-2])


      tmp = udword(code[start + offset:start  + offset + 4])
      code[start + offset:start + offset + 4] = dword(tmp ^ xor_val)
      break

    else:
      tmp = f"{decoded.mnemonic} {decoded.op_str}"
      instructions[decoded.address] = tmp

  for key, value in instructions.items():
    if f"{key:#08x}" not in printed[-1]:
      printed.append(f"{key:#08x}: {value}")
      if "nop" not in printed[-1]:
        print(printed[-1])
        break

    # input("nop" in printed[-1])
