def main():
    # ask for enter a number
    dollars = get_input()

    # converts dollar to cents
    cents = dollars * 100

    # calculate number of quarters
    quarters = calculate_quarters(cents)
    cents = cents - quarters * 25

    # calculate number of dimes
    dimes = calculate_dimes(cents)
    cents = cents - dimes * 10

    # calculate number of nickels
    nickels = calculate_nickels(cents)
    cents = cents - nickels * 5

    # calculate number of pennies
    pennies = calculate_pennies(cents)
    cents = cents - pennies

    # calculate total number of coins
    total_coins = quarters + dimes + nickels + pennies

    # if calculate correctly prints number of coins else print error
    if (cents == 0):
        print(int(total_coins))
    else:
        print("error")


def get_input():
    # ask for positive number (if user provides something else this will ask again)
    dollar = -1
    while(dollar <= 0):
        try:
            dollar = float(input("Dollars (Please enter a positive number): "))
        except:
            continue
    return dollar


def calculate_quarters(c):
    # take cents as a argument and calculate number of quarters
    n = c // 25
    return n


def calculate_dimes(c):
    # take cents as a argument and calculate number of dimes
    n = c // 10
    return n


def calculate_nickels(c):
    # take cents as a argument and calculate number of nickels
    n = c // 5
    return n


def calculate_pennies(c):
    # take cents as a argument and calculate number of pennies
    return c


main()