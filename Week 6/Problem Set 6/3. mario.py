def main():
    # ask for positive number (if user provides something else this will ask again)
    height = -1
    while(height < 1 or height > 8):
        try:
            height = int(input("Height (Please enter a positive number): "))
        except:
            continue

    # prints the pyramids
    for n in range(1, height + 1):
        print_x_times(height - n, " ")
        print_x_times(n, "#")
        print("  ", end="")
        print_x_times(n, "#")
        print("", end="\n")


def print_x_times(x, y):
    # take character and number x as a input and prints that character x times
    for n in range(x):
        print(y, end="")


main()