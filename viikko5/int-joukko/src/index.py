import unittest
from int_joukko import IntJoukko


def main():
    joukko = IntJoukko()

    joukko.lisaa_listaan(1)
    joukko.lisaa_listaan(2)
    joukko.lisaa_listaan(3)
    joukko.lisaa_listaan(2)

    print(joukko.to_int_list())


if __name__ == "__main__":
    main()
