import argparse

def __main__():
    
    parser = argparse.ArgumentParser(description="Energy Matrix Generator")
    parser.add_argument('--protein_file', default = None, type = argparse.FileType('r'), help = "protein file")
    args = parser.parse_args()
    
    temp = args.protein_file.read()
    temp = temp.replace(",", "\n")

    with open("dataset.txt", "w") as f:
        f.write(temp)

if __name__ == "__main__":
    __main__()