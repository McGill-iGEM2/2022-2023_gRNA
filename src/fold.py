import glob

# f = glob.glob("../data/*.fsa")[0]

# seq = ""

# with open(f) as fl:
#     for line in fl:
#         if line.startswith(">"):
#             continue
#         else:
#             l = line.strip()
#             seq += l

# with open("../data/seq.txt", "w") as fl:
#     fl.write(seq)

fs = glob.glob("../data/mfold/HMG2/seq.txt_*.ct")

# Rank based on energy
min = 1000
idx = 0

for f in fs:
    with open(f) as fl:
        l = fl.readline().strip().split()
        dg = float(l[3])
        
        if dg < min:
            min = dg
            idx = f.split("_")[-1].split(".")[0]
            
print(idx, min)