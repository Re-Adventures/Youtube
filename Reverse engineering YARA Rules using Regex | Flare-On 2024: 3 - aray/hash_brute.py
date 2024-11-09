import hashlib
import binascii

def get_crc32(data):
    return binascii.crc32(data)

crc32_hashes = [
    0x61089c5c,
    0x5888fc1b,
    0x66715919,
    0x7cab8d64,
]

sha256_hashes = [
    "403d5f23d149670348b147a15eeb7010914701a7e99aad2e43f90cfa0325c76f",
]

for hash in crc32_hashes:
    for ch1 in range(256):
        found = False
        for ch2 in range(256):
            possible = chr(ch1) + chr(ch2)
            curr_hash = get_crc32(possible.encode())
            if curr_hash == hash:
                print(f'"{hex(hash)}": "{possible}",')
                found = True

        if found:
            break

for hash in sha256_hashes:
    for ch1 in range(256):
        found = False
        for ch2 in range(256):
            possible = chr(ch1) + chr(ch2)
            curr_hash = hashlib.sha256(possible.encode()).hexdigest()
            if curr_hash == hash:
                print(f'"{hash}": "{possible}",')
                found = True

        if found:
            break

