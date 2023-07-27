from cgitb import small
import csv
import sys


db = []
seq = ""


def main():
    # Check for command-line usage
    if len(sys.argv) < 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return

    # Read database file into a variable
    f1 = open(sys.argv[1], "r")
    reader = csv.DictReader(f1)
    for d in reader:
        db.append(d)

    # Read DNA sequence file into a variable
    f2 = open(sys.argv[2], "r")
    seq = f2.read()

    # Find longest match of each STR in DNA sequence
    agatc_count = longest_match(seq, "AGATC")
    ttttttct_count = longest_match(seq, "TTTTTTCT")
    aatg_count = longest_match(seq, "AATG")
    tctag_count = longest_match(seq, "TCTAG")
    gata_count = longest_match(seq, "GATA")
    tatc_count = longest_match(seq, "TATC")
    gaaa_count = longest_match(seq, "GAAA")
    tctg_count = longest_match(seq, "TCTG")

    # Check database for matching profiles
    for i in db:
        if "large" in sys.argv[1]:
            if (int(i["AGATC"]) == agatc_count and int(i["TTTTTTCT"]) == ttttttct_count and int(i["AATG"]) == aatg_count and int(i["TCTAG"]) == tctag_count and int(i["GATA"]) == gata_count and int(i["TATC"]) == tatc_count and int(i["GAAA"]) == gaaa_count and int(i["TCTG"]) == tctg_count):
                print(i["name"])
                return i["name"]
        elif "small" in sys.argv[1]:
            if (int(i["AGATC"]) == agatc_count and int(i["AATG"]) == aatg_count and int(i["TATC"]) == tatc_count):
                print(i["name"])
                return i["name"]

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            
            # If there is no match in the substring
            else:
                break
        
        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()