import random

score=0

rand=random.randint(0,100)

totalGames=0
wins=0
lose=0
score=0

def readFromFile():
    openFile = open("file.txt", "r")
    readFile=openFile.readline()
    fileValues=readFile.split(",")
    totalGames = fileValues[0]
    wins = fileValues[1]
    lose = fileValues[2]
    score = int(wins) - int(lose)
    openFile.close()

def writeOnFile(totalGames, wins, lose):
    line = [str(totalGames),",",str(wins),",",str(lose)]
    openFile = open("file.txt", "w")
    openFile.writelines(line)
    openFile.close()

def printScores():
    print("Score: ", score)
    print("Wins: ", wins)
    print("Lose: ", lose)
    print("Total Games: ", totalGames)

def winner():
    print("You won!")
    global score
    score += 1
    global wins
    wins += 1
    global totalGames
    totalGames += 1
    global lose
    writeOnFile(totalGames, wins, lose)

def loser():
    print("You Lose!")
    global score
    if score > 0:
        score -= 1
    global lose
    lose += 1
    global totalGames
    totalGames += 1
    global wins
    writeOnFile(totalGames, wins, lose)

    print("Score: ", score)
    print("Wins: ", wins)
    print("Lose: ", lose)
    print("Total Games: ", totalGames)

def checkRestart():
    restart = input("Do you want to play again? (y/n) ")
    if restart == "y":
        global rand
        rand=random.randint(0,100)
        startGame(10)
        return True
    else:
        print("Thanks for playing!")
        return False

def startGame(try_number):
    print(rand)
    i = try_number
    while i > 0:
        num = input("Guess a number between 0 and 100: ")
        print(num)
        if num.isdecimal():
            guess = (int)(num)
            if guess == rand:
                winner()
                printScores()
                if checkRestart():
                    return
                break
            elif guess > rand:
                print("Too high!")
                i -= 1
            elif guess < rand:
                print("Too low!")
                i -= 1
        else:
            print("That's not a number!")
            i -= 1

    loser()
    printScores()
    if checkRestart():
        return

startGame(10)