using Pkg
Pkg.activate("gRNA/src/grna")

using RNAstructure, Glob
using PlotRNA

files = Glob.glob("gRNA/data/*.txt")
dbn = readline(files[1])
seq = readline(files[2])

# RNAstructure
f = mfe(seq)

open("gRNA/data/julia_fold.txt", "w") do file
    write(file, f[2])
end

VARNA.plot(dbn, seq=seq, savepath="gRNA/data/julia_fold.png")