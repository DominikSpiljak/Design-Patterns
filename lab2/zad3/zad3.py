
def mymax(iterable, key=None):
    my_max = None
    for x in iterable:
        if key is None:
            if my_max is None:
                my_max = x
            elif x > my_max:
                my_max = x
        else:
            if my_max is None:
                my_max = x
            elif key(x) > key(my_max):
                my_max = x
    return my_max

def main():
    maxint = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
    maxchar = mymax("Suncana strana ulice")
    maxstring = mymax([
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"])
    D = {'burek':8, 'buhtla':5}
    maxdict = mymax(D, key=D.get)

    print(maxint)
    print(maxchar)
    print(maxstring)
    print(maxdict)

    names = [("Dominik", "Spiljak"), ("Ivan", "Ivkovic"), ("Marko", "Markovic"), ("Zadnji", "Zadnjikovic")]
    print(mymax(names, lambda x: x[1]))
    
if __name__ == "__main__":
    main()