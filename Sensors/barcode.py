while True:
    file = open("test.txt", "a")
    test = input()
    file.write(test)
    file.write("\n")
    file.close()
