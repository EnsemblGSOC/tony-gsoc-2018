import sys

# test input
## sys.argv = [1, "GRCh38-Chrom17.fasta", 0, 5, "GRCh38-Chrom17.wig"]

# commandline arguments
genomefile = sys.argv[1]
basepair_location = int(sys.argv[2])
window_size = int(sys.argv[3])
counter = 0
percentage = 0
percentage_bp = 1 / window_size * 100
result = open(sys.argv[4], "w+")

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
