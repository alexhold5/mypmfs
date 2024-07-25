#REQUIRES BATCH DOWNLOAD AND TRAINING COMMANDS IN DIRECTORY AS SCRIPT

import os
import argparse

def __main__():
    
    parser = argparse.ArgumentParser(description="Energy Matrix Generator")
    
    parser.add_argument('--protein_file', default = None, type = argparse.FileType('r'), help = "protein file")
    parser.add_argument('--matrix', default = None, help = "Output Matrix")
    args = parser.parse_args()

    aa = ["C", "M", "F", "I", "L", "V", "W", "Y", "A", "G", "T", "S", "N", "Q", "D", "E", "H", "R", "K", "P"]
    C, M, F, I, L, V, W, Y, A, G, T, S, N, Q, D, E, H, R, K, P = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
    dict = {"C" : C, "M" : M, "F" : F, "I" : I, "L" : L, "V" : V, "W" : W, "Y" : Y, "A" : A, "G" : G, "T" : T, "S" : S, "N" : N, "Q" : Q, "D" : D, "E" : E, "H" : H, "R" : R, "K" : K, "P" : P}
    matrix = "    C       M       F       I       L       V       W       Y       A       G       T       S       N       Q       D       E       H       R       K       P\n"

    temp = args.protein_file.read()
    with open("protein_file", "w") as f:
        f.write(temp)
    # os.makedirs("./results/pdb_files")
    os.chdir("./results/pdb_files/")

    download = f"../../commands/batch_download.sh -f ../../protein_file -p"
    os.system(download)
    os.system("gzip -d *")

    os.chdir("../")

    x=""
    with open(f"../protein_file") as f:
        for l in f:
            x += l.replace(",", "\n")



    with open("dataset.txt", "w") as text_file:
        text_file.write(x)


    os.system("../commands/training -l dataset.txt -d pdb_files/ -o data_potentials")

    with open("./data_potentials/top_energies.tsv") as f:
        for line in f:  
            if line:
                l = line.strip().split('\t')
                (dict[l[0][0]])[l[0][3]] = l[1]
                (dict[l[0][3]])[l[0][0]] = l[1]

    for i in range(len(aa)):
        for k in range(i):
            matrix = matrix + "0e+00 "
        for j in range(i, len(aa)):
            matrix = matrix + str(dict[aa[i]][aa[j]]) + "e+00 "
        matrix = matrix + '\n'

    with open(args.matrix, "w") as text_file:
        text_file.write(matrix)

if __name__ == "__main__":
    __main__()