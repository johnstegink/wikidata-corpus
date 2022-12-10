# Script to covert a WikiSim or WiRe csv to a format that is compatiple with gWikiMatch
# run as: wire2gwikimatch.py -i <inputfile> -o <outputfile>
import sys,argparse
import csv
def read_arguments():
    """
    Read arguments from the command line
    :return: (outputdirectory, language)
    """

    parser = argparse.ArgumentParser(description='Convert WiRe or WikiSim csv files to the format of the gWikiDataset.')
    parser.add_argument('-i', '--input', help='The WiRe or WikiSim file to convert', required=True)
    parser.add_argument('-o', '--output', help='The ouput file in the format of the gWikiDataset', required=True)
    args = vars(parser.parse_args())

    return (args["input"], args["output"])



def calculate_relatedness( value):
    """
    Translate a value between 0 and 1 to a value between 1 and 10 if the value contains a .
    :param value: string value
    :return: integer value between 0 and 10
    """

    if "." in value:
        return int( round( float( value) * 10))
    else:
        return int(value)


WikipediaUrlPrefix = "http://en.wikipedia.org/wiki/"

# Main part of the script
if __name__ == '__main__':
    (input, output) = read_arguments()

    with open( input, "r", newline='') as wire_file:
        with open(output, "w") as match_file:

            # Read the input file as a csv file
            wire_reader = csv.reader(wire_file)
            for fields in wire_reader:

                # read the header
                if wire_reader.line_num == 1:
                    srcindex = fields.index('srcWikiTitle')
                    dstindex = fields.index('dstWikiTitle')
                    relindex = fields.index('relatedness')
                    nr_of_fields = len(fields)
                else: # Not a header: process the lines
                    if len(fields) == nr_of_fields:
                        # Write a tsv line
                        match_file.write(
                            str(calculate_relatedness(fields[relindex])) + "\t" +
                            WikipediaUrlPrefix + fields[srcindex] + "\t" +
                            WikipediaUrlPrefix + fields[dstindex] + "\n"
                        )
                    elif len(fields) > 0:
                        print(f"Error reading line: {wire_reader.line_num}")

    print("done")