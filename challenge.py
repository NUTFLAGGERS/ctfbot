from Crypto.Util.number import getPrime, bytes_to_long

e = 3
p = getPrime(512)
q = getPrime(512)
N = p * q

flag = b"NUT{wh4t_1s_e_valu3?}"
m = bytes_to_long(flag)
c = pow(m, e, N)
with open("output.txt", "w") as f:
    f.write(f"N = {N}\n")
    f.write(f"e = {e}\n")
    f.write(f"c = {c}\n")

print("Challenge files generated!")