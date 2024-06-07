import os, sys
from t34Assembler import t34Assembler

def main(path):
    assembler = t34Assembler()

    # Open t34 file
    if not assembler.fopen(path):
        print(f"Unable to open {path}.")
        return False
    
    # Read t34 file
    assembler.fread()
    assembler.assemble()
    assembler.fwrite(path[:-2] + '.o')
    assembler.fclose()
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(sys.argv[0] + " <file>")
    else:
        if os.path.exists(sys.argv[1]):
            main(sys.argv[1])
        else:
            print(f"{sys.argv[1]} is not a valid path or file.")
