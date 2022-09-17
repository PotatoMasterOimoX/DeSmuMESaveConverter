import os
import sys

trimSize = 122

footer = [124, 60, 45, 45, 83, 110, 105, 112, 32, 97, 98, 111, 118, 101, 32, 104,
          101, 114, 101, 32, 116, 111, 32, 99, 114, 101, 97, 116, 101, 32, 97, 32,
          114, 97, 119, 32, 115, 97, 118, 32, 98, 121, 32, 101, 120, 99, 108, 117,
          100, 105, 110, 103, 32, 116, 104, 105, 115, 32, 68, 101, 83, 109, 117, 77,
          69, 32, 115, 97, 118, 101, 100, 97, 116, 97, 32, 102, 111, 111, 116, 101,
          114, 58, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0,
          0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 124, 45, 68, 69, 83, 77,
          85, 77, 69, 32, 83, 65, 86, 69, 45, 124]


def usage():
    """Print usage information to stderr and exit."""
    print("""\
Usage: main.py INPUT(File)

Convert DSV (DeSmuME save file) to SAV (raw save file) and vice versa.


Usage: main.py INPUT(Directory)

Convert DSV to SAV and vice versa. (recursive)
""", file=sys.stderr)
    exit(2)

def main():
    args = sys.argv[1:]
    if len(args) == 1:
        if os.path.isdir(args[0]):
            for file in iter_valid_files(args[0]):
                convert(file)
            return

        if os.path.isfile(args[0]):
            convert(args[0])
            return

    usage()

def iter_valid_files(dir_):
    VALID_EXTENSIONS = ('.dsv', '.sav')

    for root, _, files in os.walk(dir_, topdown=False):
        for f in files:
            if os.path.splitext(f)[1] in VALID_EXTENSIONS:
                yield os.path.join(root, f)

def convert(inFilepath):

    name = os.path.basename(inFilepath)

    def dsv_to_sav():
        ext = ".sav"
        outFilepath = os.path.join(os.path.dirname(inFilepath), name[:-4] + ext)
        fileSize = os.stat(inFilepath).st_size
        readTo = fileSize - trimSize
        with open(inFilepath, 'rb') as inFile:
            with open(outFilepath, 'wb') as outFile:
                outFile.write(inFile.read()[:readTo])
        print("dsv->sav: Converted '" + name + "' to '" + name[:-4] + ext + "'")

    def sav_to_dsv():
        ext = ".dsv"
        outFilepath = os.path.join(os.path.dirname(inFilepath), name[:-4] + ext)
        binary = bytearray(footer)
        with open(inFilepath, 'rb') as inFile:
            with open(outFilepath, 'wb') as outFile:
                contents = inFile.read()
                outFile.write(contents)
                outFile.write(binary)
        print("sav->dsv: Converted '" + name + "' to '" + name[:-4] + ext + "'")


    if inFilepath.endswith(".dsv"):
        dsv_to_sav()
        return

    if inFilepath.endswith(".sav"):
        sav_to_dsv()
        return

    usage()

if __name__ == '__main__':
    main()
