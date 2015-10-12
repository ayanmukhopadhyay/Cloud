from math import ceil
import sys

def isNumberPrime (number):
    for counter in range(2, int(ceil(number/2))):
        if number%counter == 0:
            return False
    return True


if __name__ == '__main__':
    print isNumberPrime(int(sys.argv[1]))


