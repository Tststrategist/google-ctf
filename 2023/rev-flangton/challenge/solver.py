# Copyright 2023 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# The values below can be extracted from the circuit in various ways.

RANDOM_BITS1 = "10001001111001110100000010110001101100101100110010000010111111101110001000111101111100001010111110101000110111000000111001001010001100001101001001101100100011111001111100000110101010110010000010101110000110001111100100000110111100110011110000001010010010011101011111001101001011110001101001110100010110010100101101100101011101001100001111101110001101001110011000111111100000111111101010110111111011001110001001100010110101010000011000011111001111001000111111110011111000000101101010101100111011100011110010000011"
RANDOM_BITS2 = "11001010110101111000000000111001010001110100110100000011100001101100100001000010000100100111110111010000101011001100111010000100101101110110110111010110010111110000100011111000000111111101100001011001110010011110001111011000110111100010100001101011011100001100111110101010100111001000010100110101000100111000010000110001000000110110011010110000011101011100000011110000110011000110011001011011000010011010100010111011000101001001010001010011111100011110101000101111101010010100011011111000010110100011100011101101"
RANDOM_BITS3 = "11001000001001011100110010100010010111001101110001010001000010000101110011011110111111010010000101000000100110100101110010101000111101110100011111010100110010000100111110110101101001001101010110000000001111111001101101010110001110111001111110011000110111001011101010010111111110000011011011111010101100110010111101001001010111101010000000000000000100000001011000011101000110001000000101011100100110011000000101110101000000110011010100101010010001010101100000010110001001101011011010000110011111111010101010101000"
FLAG_BITS = '10010000110101110110101110100100100001011100110101000000110001101110101101111100011010100000010010011011010101111111101001111001000001001000111110010101100011000110100001000001'

N_BITS = len(FLAG_BITS)

# Nibble-wise bitswap, misaligned to thwart byte-by-byte attack.
f = []
for i in range(0, N_BITS, 16):
    f.append(FLAG_BITS[i:i+6])
    f.append(FLAG_BITS[i+6:i+10][::-1])
    f.append(FLAG_BITS[i+10:i+16])

FLAG_BITS = "".join(f)
print("Tripled:", FLAG_BITS)

f = int(FLAG_BITS[::-1], 2)
f *= pow(3, -1, 2**N_BITS)
f &= 2**N_BITS - 1
FLAG_BITS = ("{:0%db}" % N_BITS).format(f)[::-1]
print("Bit-swapped:", FLAG_BITS)

f = []
for i in range(0, N_BITS, 8):
    f.append(FLAG_BITS[i:i+3][::-1])
    f.append(FLAG_BITS[i+3:i+6][::-1])
    f.append(FLAG_BITS[i+6:i+8])

FLAG_BITS = "".join(f)
print("Random xored:", FLAG_BITS)

f = []
for i in range(N_BITS):
    f.append(str(int(RANDOM_BITS3[i]) ^ (int(RANDOM_BITS2[i]) & int(RANDOM_BITS1[i])) ^ int(FLAG_BITS[i])))

FLAG_BITS = "".join(f)
print("Bit-swapped:", FLAG_BITS)

f = []
for i in range(0, N_BITS, 4):
    f.append(FLAG_BITS[i:i+4][::-1])

FLAG_BITS = "".join(f)
print("Xorshifted:", FLAG_BITS)

f = int(FLAG_BITS[::-1], 2)
for i in range(30):
    f ^= f << (1<<i)
f &= 2**N_BITS - 1
FLAG_BITS = ("{:0%db}" % N_BITS).format(f)[::-1]
print("Negated:", FLAG_BITS)

FLAG_BITS = FLAG_BITS.replace("0", "x").replace("1", "0").replace("x", "1")
print("Flag bits:", FLAG_BITS)
flag = ""
for i in range(len(FLAG_BITS) // 7):
    bits = FLAG_BITS[i*7:i*7+7]
    c = chr(int(bits, 2))
    flag += c
print(flag)
