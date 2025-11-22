def divide (a,b):
    if b == 0 :
        return "Second number can't be 0"
    else:
        return a/b


def scoreDived ():
    print("Welcome to Calculator!")
  



    
    x = int(input("First number: "))
    y = int(input("Second number: "))
    print("Result:", divide(x, y))

if __name__ == "__main__":
    scoreDived()