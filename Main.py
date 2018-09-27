from PIL import Image
from urllib.request import urlretrieve
from lorem.text import TextLorem

def main():
    choice = int(input("1. Encode image\n2. Decode image\n3. Encode text\n4. Decode text\n\n"))

    if choice == 1:
        encode()
    elif choice == 2:
        decode()
    elif choice == 3:
        text = input("Enter something to hide:\n\n")
        textToText(text)
    elif choice == 4:
        text = input("Enter text to decode:\n\n")
        decodeText(text)

    else:
        print("Invalid choice, try agian.\n")

        main()

def encode():
    choice = int(input("1. Enter image name(without extension)\n2. Enter image link\n\n"))

    if choice == 1:
        imgName = input("Enter image name(without extension):\n\n")
        image = Image.open(imgName + ".png", "r")

        text = input("Enter something to hide:\n\n")

        img = image.copy()

        modifyPicture(img,text)

    elif choice == 2:
        url = input("Enter URL\n")
        urlretrieve(url, 'downloaded.jpg')
        image = Image.open('downloaded.jpg', "r")

        text = str(input("Enter something to hide:\n\n"))

        img = image.copy()
        modifyPicture(img, text)


    else:
        encode()


def modifyPicture(image,text):

    #getting the pixels from the image
    pixels = list(image.getdata())

    editPixels = []

    #converting a list of tupples to a list of lists so we can edit the pixels
    for x in range(0, len(pixels)):
        editPixels.append(list(pixels[x]))

    binaryData = []
    #converting the text to ascii and then to binary
    for letter in text:
        binaryData.append(format(ord(letter), '08b'))


    binaryLength = len(binaryData)
    setCounter = 0
    valueCounter = 0

   #iterating through each binary in the list
    for binary in range(0, binaryLength):
        #iterating through each individual number in that binary
        for number in binaryData[binary]:

            #if statements for every scenario
            # if statement if the number is 0 and the pixel is even
            if int(number) == 0 and pixels[setCounter][valueCounter] % 2 == 0:
                valueCounter += 1
            # number is 0 and pixel is odd
            elif pixels[setCounter][valueCounter] % 2 == 0 and int(number) == 1:
                # editing each pixel to even for 0's and odd for 1's
                editPixels[setCounter][valueCounter] = editPixels[setCounter][valueCounter] + 1
                valueCounter += 1
            # number is 0 and pixel is odd
            elif pixels[setCounter][valueCounter] % 2 != 0 and int(number) == 0:
                # editing each pixel to even for 0's and odd for 1's
                editPixels[setCounter][valueCounter] = editPixels[setCounter][valueCounter] + 1
                valueCounter += 1
            # number is 1 and pixel is odd
            elif pixels[setCounter][valueCounter] % 2 != 0 and int(number) == 1:
                valueCounter += 1
            # a counter for each pixel
            # once every RGB value is modified it goes onto the next pixel
            if valueCounter > 2:
                valueCounter = 0
                setCounter += 1

        #checking if it's the end of the binary list
        if binary == binaryLength - 1:
            # checking if the last value of the pixel is even
            if pixels[setCounter][valueCounter] % 2 == 0:
                # if both are true we modify it to be even
                # that is how we know that it's the end of the sequence
                # each binary is 8 digits long, we modify the first 3 pixels with their RGB values
                # the 3rd pixel value's B color is what is changed here
                # if the number is odd it means stop decoding if it's even it means continue decoding
                editPixels[setCounter][valueCounter] = editPixels[setCounter][valueCounter] + 1

        # resetting value counter and moving onto the next pixel
        elif pixels[setCounter][valueCounter] % 2 == 0:
            valueCounter = 0
            setCounter += 1

        else:
            editPixels[setCounter][valueCounter] = editPixels[setCounter][valueCounter] + 1
            valueCounter = 0
            setCounter += 1

    saveImage(image,editPixels)

def saveImage(img,pixels):
    # width of the image
    w = img.size[0]
    (x, y) = (0, 0)

    for pixel in pixels:

        # Putting modified pixels in the new image
        img.putpixel((x, y), tuple(pixel))
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

    name = input("Enter a name for the modified image(without extension):\n\n")
    img.save(name + ".png")
    img.show()



def decode():

    name = input("Enter the name of the image to decode:\n\n")

    readImg = Image.open(name + ".png", "r")
    pixels = list(readImg.getdata())

    counter = 0
    pixelList = []
    # iterating through the pixels in the image
    for pixel in pixels:
        # adding the RGB values of each pixel to the list
        pixelList.append(pixel[0])
        pixelList.append(pixel[1])
        pixelList.append(pixel[2])
        counter += 1
        # one letter is contained in 3 pixels
        # once we reach the 3rd pixel we test the B value of the pixel
        # if it's even we continue decoding
        # if it's odd we stop decoding
        if counter > 2:
            if pixel[2] % 2 != 0:
                # remove the last value since it's only an indicator for the end
                del pixelList[-1]
                break
            # remove the last value since it's only an indicator for the end
            del pixelList[-1]
            # reset our counter
            counter = 0

    pixelToLetter(pixelList)

def pixelToLetter(pixelList):
    counter = 0
    number = ""
    binaryList = []
    # iterating through the pixel list
    for item in pixelList:
        # checking each value
        # even = 0, odd = 1
        if item % 2 == 0:
            number = number + str(0)
        else:
            number = number + str(1)

        counter += 1

        # 7 digits form 1 letter so we add the binary to the list and reset our counter
        if counter > 7:
            binaryList.append(number)
            number = ""
            counter = 0

    decodedWord = ""
    letter = ""
    #converting the binary into ascii and then string
    for item in binaryList:
        letter = chr(int(item, 2))
        decodedWord += letter
    print("Decoded word: "  + decodedWord)

def textToText(text):
    #parameters for the lorem ipsum
    lorem = TextLorem(wsep=' ')

    binaryData = []
    # converting to binary
    for letter in text:
        binaryData.append(format(ord(letter), '08b'))


    sentence = ""
    sentenceList = []

    # sentences based on the number of letters
    for number in range(0, len(binaryData)):
        for element in binaryData[number]:
            word = lorem._word()
            # iterating until we find a word of sufficient length
            if int(element) == 0:
                word = lorem._word()
                # 0 for any word less than 6 letters
                while len(word) > 6:
                    word = lorem._word()

                sentence += word + " "

            # 1 for any word more than 7 letters
            elif int(element) == 1:
                word = lorem._word()
                while len(word) < 7:
                    word = lorem._word()

                sentence += word + " "

        sentence = sentence[0].capitalize() + sentence[1:]
        sentenceList.append(sentence[:-1] + ".")
        sentence = ""

    output = ""
    for text in sentenceList:
        output += text + " "

    print(output)



def decodeText(text):
    # splitting based on every sentence
    parahraph = text.split(".")
    del parahraph[-1]
    binaryList = []

    # iterating through the sentences
    for sentence in parahraph:
        binary = ""
        # splitting each sentence into individual words
        words = sentence.split(" ")
        # iterating through every word
        for word in words:
            # if the word is longer than or equal to 7  it's 1
            if len(word) >= 7:
                binary += "1"
            # everything else is a 0
            else:
                binary += "0"

        binaryList.append(binary)


    decodedWord = ""
    letter = ""
    # converting the binary into ascii and then string
    for item in binaryList:
        letter = chr(int(item, 2))
        decodedWord += letter
    print("Decoded word: " + decodedWord)

main()