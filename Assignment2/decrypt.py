from struct import pack, unpack

def F(w):
    return ((w * 31337) ^ (w * 1337 >> 16)) % 2**32

def decrypt(block):
    # unpack 4 unsigned integers from a block(16 Bytes)
    a, b, c, d = unpack("<4I", block)
    # Do some computations 32 times (inversing the encryption process)
    for i in range(32):
    # decrypting the second step in encrypt
        # keep a in a temp to use later
        tempa = a
        # get the old d from the new d
        d = d ^ 1337
        # get the old a from the new c and the old d
        a = c ^ (F(d | F(d) ^ d))
        # get the old b from the new b, the old d and a
        b = b ^ (F(d ^ F(a) ^ (d | a)))
        # get the old c from the new a, the old d, b and a
        c = tempa ^ (F(d | F(b ^ F(a)) ^ F(d | b) ^ a))
    # decrypting the frist step in encrypt
        # keep a in a temp to use later
        tempa = a
        # get the older a from the old a
        a = d ^ 31337
        # get the older d from the old c and the older a
        d = c ^ (F(a | F(a) ^ a))
        # get the older c from the old b, the older a and d
        c = b ^ (F(a ^ F(d) ^ (a | d)))
        # get the older b from the old a, the older a, c and d
        b = tempa ^ (F(a | F(c ^ F(d)) ^ F(a | c) ^ d))
    # repack the 4 unsigned ints into 16 Bytes and format them as a string
    tex = "{}".format(pack("<4I", a, b, c, d))
    # return only the plain text without "b''" of the string "b'text'"
    return tex[2:-1]

# Open the cipher text file and read as bytes("rb")
ct = open("flag.enc", "rb").read()
# empty string to carry the output
out = ""
# walk through the cipher text
for i in range(0,len(ct), 16):
    # decrypt every 16 bytes and add them to the output
    out = out + decrypt(ct[i:i+16])
# print the plain text after decryption
print(out)