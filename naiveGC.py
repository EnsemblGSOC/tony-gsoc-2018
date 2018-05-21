import sys
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument("input_file", type=str, help="Name of the input file in FASTA format")
parser.add_argument("-o", "--output_file", type=str, help="Name of the output file")
parser.add_argument("window_size", type=int, help="Number of base pairs where the GC percentage is calculated for")
parser.add_argument("shift", type=int, help="The shift increment")
parser.add_argument("-ot", "--omit_tail", action="store_true", help="True: if the trailing sequence should be omitted. "
                                                                    "Default behaviour is to retain the leftover"
                                                                    "sequence.")
parser.add_argument("-f", "--output_format", type=str, choices=["wig", "wiggle", "bigwig", "bw", "gzip"])
args = parser.parse_args()

# commandline arguments
genomefile = args.input_file
basepair_location = 0
window_size = args.window_size
counter = 0
percentage = 0
percentage_bp = 1 / window_size * 100

if args.output_file:
    result = open(args.output_file, "w+")
else:
    result = open(args.input_file.split(".")[0] + ".wig", "w+")

with open(genomefile) as f:
    # read track line
    title = f.readline()
    result.write(title)
    # add step info
    result.write("variableStep span=" + str(window_size) + "\n")
    while True:
        # read file one bp at a time
        a = f.read(1)
        # if not EOF and not newline
        if a != "" and a != "\n":
            counter += 1
            # if bp is G or C
            if a in ['G', 'C']:
                percentage += percentage_bp
            # if reached window size, write percentage
            if counter == window_size:
                result.write(str(basepair_location) + "  " + str(int(percentage)) + "\n")
                basepair_location += window_size
                counter = 0
                percentage = 0
        elif a == '':
            # if end of file and still bp remains
            if counter != 0:
                result.write(str(basepair_location) + "  " + str(int(percentage * window_size / counter)) + "\n")
                basepair_location += window_size
                break
            else:
                break

result.close()
