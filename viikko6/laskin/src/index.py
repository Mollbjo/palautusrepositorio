from tkinter import Tk
from kayttoliittyma import Kayttoliittyma
from sovelluslogiikka import Sovelluslogiikka

#Muutos testi, viiikon 7 tehtävää varten

def main():
    sovellus = Sovelluslogiikka()

    window = Tk()
    window.title("Laskin")

    kayttoliittyma = Kayttoliittyma(sovellus, window)
    kayttoliittyma.kaynnista()

    window.mainloop()

if __name__ == "__main__":
    main()
