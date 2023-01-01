from z3 import *

flag_len = 41
result = [BitVec(f"result_{i}", 8) for i in range(flag_len)]

s = Solver()

s.add(result[1] * result[39] * result[21] + result[17] + result[19] * result[30] == 897310)
s.add(result[37] - result[19] * result[12] == -3084)
s.add(result[2] - result[31] + result[33] * result[13] * result[20] - result[17] == 965917)
s.add(result[7] + result[36] * result[15] - result[29] * result[34] == 6373)
s.add(result[21] - result[27] * result[15] - result[17] == -11835)
s.add(result[15] - result[37] * result[8] - result[5] - result[6] == -6565)
s.add(result[35] + result[29] - result[20] + result[26] == 196)
s.add(result[7] * result[32] + result[31] * result[11] == 17866)
s.add(result[29] * result[24] * result[36] + result[37] == 705531)
s.add(result[8] - result[16] - result[12] + result[40] + result[15] == 208)
s.add(result[35] * result[17] * result[0] - result[11] + result[12] * result[7] * result[38] == 1519176)
s.add(result[26] - result[13] + result[3] * result[8] - result[5] == 4280)
s.add(result[3] + result[17] + result[36] + result[20] == 352)
s.add(result[26] - result[21] * result[18] + result[27] * result[25] == 2210)
s.add(result[34] - result[14] + result[5] * result[33] + result[35] == 7128)
s.add(result[5] * result[8] * result[38] * result[25] + result[21] + result[35] == 46819720)
s.add(result[8] * result[8] + result[21] * result[12] - result[36] == 9264)
s.add(result[35] + result[2] - result[7] - result[9] * result[18] + result[2] * result[39] == 734)
s.add(result[5] * (result[17] - 1) - result[6] - result[20] - result[34] * result[23] == -4565)
s.add(result[34] - result[11] + result[11] * result[13] == 10938)
s.add(result[27] + result[18] * result[15] + result[32] + result[9] == 9832)
s.add(result[21] - result[14] * result[29] == -5120)
s.add(result[9] * result[9] - result[10] + result[13] - result[36] - result[20] == 6572)
s.add(result[12] + result[2] + result[34] - result[4] * result[20] * result[23] + result[22] == -719372)
s.add(result[4] + result[5] - result[10] + result[27] == 180)
s.add(result[15] - result[28] - result[37] - result[24] * result[18] * result[0] == -853736)
s.add(result[4] * result[35] + result[25] - result[21] - result[24] * result[20] == -504)
s.add(result[25] + result[10] - result[15] + result[28] - result[33] == 62)
s.add(result[6] - result[25] + result[2] - result[25] + result[1] + result[18] * result[28] == 7865)
s.add(result[11] * (result[5] + result[34] * result[22]) + result[12] + result[34] == 1186707)
s.add(result[3] + result[14] - result[38] - result[13] - result[1] == -128)
s.add(result[30] + result[21] - result[17] - result[23] * result[5] + result[33] == -6909)
s.add(result[7] - result[14] + result[17] + result[33] == 223)
s.add(result[8] - result[3] + result[2] * result[10] * result[10] == 403170)
s.add(result[37] + result[7] - result[19] + result[12] + result[11] == 303)
s.add(result[1] + result[8] * result[20] + result[32] + result[15] == 5754)
s.add(result[17] - result[4] - result[29] * result[18] == -4554)
s.add(result[13] * result[22] - result[10] - result[35] == 13033)
s.add(result[13] + result[11] + result[29] * result[19] == 3785)
s.add(result[25] + result[38] * result[15] - result[11] + result[32] - result[21] * result[34] == 42)
s.add(result[6] * result[9] + result[35] == 3805)

for i in range(flag_len):
  s.add(result[i] > 32)
  s.add(result[i] < 127)

if sat == s.check():
  soln = s.model()
  o = ""
  for i in range(flag_len):
    o += chr(soln[result[i]].as_long())

  print(o)
