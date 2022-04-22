from multiprocessing.connection import wait
from re import A
import timeit
from tkinter.tix import Tree

while True:

    print("\n--------------Welcome to AES-128 Bit Encryption and Decryption with 4-Bit S-Box-------------\n")
    print("\nWhich S-Box do you use? \n 1- Press 1 for the x^4+x+1 polynomial. \n 2- Press 2 for the x^4+x^3+1 polynomial. \n 3- Press 3 for the x^4+x^3+x^2+x+1 polynomial.  ")
    press = int(input())

    if press == 1:

        sBox = (
            0x3, 0xD, 0xA, 0x2,
            0x1, 0x7, 0xB, 0x5,
            0xC, 0xE, 0xF, 0x6,
            0x9, 0x8, 0x0, 0x4,
        )

        invSbox = (
            0xE, 0x4, 0x3, 0x0,
            0xF, 0x7, 0xB, 0x5,
            0xD, 0xC, 0x2, 0x6,
            0x8, 0x1, 0x9, 0xA,
        )

        rCon = (
            0x0, 0x1, 0x2, 0x4, 0x8, 0x3, 0x6, 0xC, 0xB, 0x5, 0xA,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        )

    elif press == 2:

        sBox = (
            0x9, 0xE, 0xF, 0x2,
            0xA, 0x6, 0x4, 0x1,
            0x0, 0x8, 0xB, 0xC,
            0x7, 0x5, 0xD, 0x3,
        )

        invSbox = (
            0x8, 0x7, 0x3, 0xF,
            0x6, 0xD, 0x5, 0xC,
            0x9, 0x0, 0x4, 0xA,
            0xB, 0xE, 0x1, 0x2,
        )

        rCon = (
            0x0, 0x1, 0x2, 0x4, 0x8, 0x9, 0xB, 0xF, 0x7, 0xE, 0x5,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        )

    elif press == 3:

        sBox = (
            0xC, 0x7, 0x3, 0x6,
            0x1, 0x5, 0x9, 0xA,
            0x2, 0xE, 0x0, 0x8,
            0x4, 0xF, 0xD, 0xB,
        )

        invSbox = (
            0xA, 0x4, 0x8, 0x2,
            0xC, 0x5, 0x3, 0x1,
            0xB, 0x6, 0x7, 0xF,
            0x0, 0xE, 0x9, 0xD,
        )

        rCon = (
            0x0, 0x1, 0x2, 0x4, 0x8, 0xF, 0x1, 0x2, 0x4, 0x8, 0xF,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        )

    else:
        print("You entered an incorrect number. Program will start again. Please enter a number between 1-3.")
        progressed_second = 0
        continue
    # key = "5468617473206D79204B756E67204675"
    # text = "54776F204F6E65204E696E652054776F"

    Nb = 8    # Number of columns
    Nk = 4
    Nr = 10    # Number of rounds

    print("\nEnter the 16-character 'key' you want to encrypt the text with.\n If you want to continue with default key press '1' \n")
    keymessage = input()

    if keymessage == '1':
        key = "5468617473206D79204B756E67204675"

    else:
        key = keymessage.encode("utf-8").hex()
    
        keyAppend = stringToList(key)

        if (len(key) < 32):
            for i in range(0, 32-len(key)):
                key = keyAppend.append('0')
        
        key = listToString(keyAppend)
    print("Enter the 16-character or less than 16-character 'text' you want to encrypt.\n")

    message = input()
    text = message.encode("utf-8").hex()

    def stringToList(string):

        list1 = []
        list1[:0] = string
        return list1
    
    def listToString(s): 
        
        str1 = "" 
        
        for i in s: 
            str1 += i  
        
        # return string 
        return str1     
    
    def text2matrix_4bit(text, len=32):

        state = []

        for i in range(len):
            # two hex characters == 1 byte
            fourBit = int(text[i*1:i*1+1], 16)
            if i % 4 == 0:
                # this means that the byte to append is the first of the column
                state.append([fourBit])
            else:
                # Append byte to the row i // 4
                state[i // 4].append(fourBit)

        return state
    
    def addRoundKey(s, k):

        for i in range(Nb):
            for j in range(4):
                s[i][j] ^= k[i][j]

        return s
    
    def substituteBytes(s):

        for i in range(Nb):
            for j in range(4):
                s[i][j] = sBox[s[i][j]]

        return s

    def shiftRows(s):

        s[0][1], s[1][1], s[2][1], s[3][1], s[4][1], s[5][1], s[6][1], s[7][1] = s[2][1], s[3][1], s[4][1], s[5][1], \
            s[6][1], s[7][1], s[0][1], s[1][1]
        s[0][2], s[1][2], s[2][2], s[3][2], s[4][2], s[5][2], s[6][2], s[7][2] = s[4][2], s[5][2], s[6][2], s[7][2], \
            s[0][2], s[1][2], s[2][2], s[3][2]
        s[0][3], s[1][3], s[2][3], s[3][3], s[4][3], s[5][3], s[6][3], s[7][3] = s[6][3], s[7][3], s[0][3], s[1][3], \
            s[2][3], s[3][3], s[4][3], s[5][3]

        return s
    
    def matrix2text_4bit(s, len=32):

        text = ""
        for i in range(len // 4):
            for j in range(4):
                text += format(s[i][j], '01x')

        return text
        
    def text2matrix(text, len=16):

        state = []

        for i in range(len):
            # two hex characters == 1 byte
            byte = int(str(text)[i*2:i*2+2], 16)
            if i % 4 == 0:
                # this means that the byte to append is the first of the column
                state.append([byte])
            else:
                # Append byte to the row i // 4
                state[i // 4].append(byte)

        return state
    
    def xTime(b):

            if b & 0x80:
                # check if b7 of the given polynomial is 1 or 0.
                b = b << 1
                b ^= 0x1B
            else:
                b = b << 1

            return b & 0xFF  # get the first 8 bits.

    def mixOneColumn(c):

        t = c[0] ^ c[1] ^ c[2] ^ c[3]
        u = c[0]
        c[0] ^= xTime(c[0] ^ c[1]) ^ t
        c[1] ^= xTime(c[1] ^ c[2]) ^ t
        c[2] ^= xTime(c[2] ^ c[3]) ^ t
        c[3] ^= xTime(c[3] ^ u) ^ t

    def mixColumns(s):

        for i in range(4):
            mixOneColumn(s[i])

        return s

    def matrix2text(s, len=16):

        text = ""
        for i in range(len // 4):
            for j in range(4):
                text += format(s[i][j], '02x')

        return text

    def rotateWord(w):
        w[0], w[1], w[2], w[3] = w[1], w[2], w[3], w[0]


    def subWord(w):
        for i in range(len(w)):
            w[i] = sBox[w[i]]


    def keyExpansion(key):

        key = text2matrix_4bit(key)

        roundKeys = key

        for i in range(8, Nb * (Nr + 1)):
            roundKeys.append([0, 0, 0, 0])
            temp = roundKeys[i - 1][:]
            if i % 8 == 0:
                rotateWord(temp)
                subWord(temp)
                temp[0] = temp[0] ^ rCon[i // 8]

            for j in range(4):
                roundKeys[i][j] = roundKeys[i - 8][j] ^ temp[j]

        return roundKeys
    
    def invSubBytes(s):

        for i in range(Nb):
            for j in range(4):
                s[i][j] = invSbox[s[i][j]]

        return s

    def invShiftRows(s):

        s[0][1], s[1][1], s[2][1], s[3][1], s[4][1], s[5][1], s[6][1], s[7][1] = s[6][1], s[7][1], s[0][1], s[1][1], \
            s[2][1], s[3][1], s[4][1], s[5][1]
        s[0][2], s[1][2], s[2][2], s[3][2], s[4][2], s[5][2], s[6][2], s[7][2] = s[4][2], s[5][2], s[6][2], s[7][2], \
            s[0][2], s[1][2], s[2][2], s[3][2]
        s[0][3], s[1][3], s[2][3], s[3][3], s[4][3], s[5][3], s[6][3], s[7][3] = s[2][3], s[3][3], s[4][3], s[5][3], \
            s[6][3], s[7][3], s[0][3], s[1][3]

        return s

    def invMixColumns(s):

        for i in range(4):
            u = xTime(xTime(s[i][0] ^ s[i][2]))
            v = xTime(xTime(s[i][1] ^ s[i][3]))
            s[i][0] ^= u
            s[i][1] ^= v
            s[i][2] ^= u
            s[i][3] ^= v

        mixColumns(s)

        return s
    
    def cipher(text, key):

        j = keyExpansion(key)
        a = text2matrix_4bit(text)

        for i in range(1, 10):
            if i == 1:
                c = addRoundKey(a, j[:8])
            else:
                c = o
            d = substituteBytes(c)
            e = shiftRows(d)
            f = matrix2text_4bit(e)
            g = text2matrix(f)
            h = mixColumns(g)
            p = matrix2text(h)
            k = text2matrix_4bit(p)
            o = addRoundKey(k, j[8 * i: 8 * (i + 1)])
            # round = matrix2text_4bit(o)
            # print("After Round " + str(i) + " :     " + round)

        r = substituteBytes(o)
        s = shiftRows(r)
        t = addRoundKey(s, j[80:88])
        end = matrix2text_4bit(t)
        # print("After Round 10 :    " + end + "\n")

        return end
        
    def decipher(text):

            j = keyExpansion(key)
            a = text2matrix_4bit(text)
            for i in range(9, 0, -1):

                if i == 9:
                    b = addRoundKey(a, j[80:88])
                else:
                    b = m

                c = invShiftRows(b)
                d = invSubBytes(c)
                e = addRoundKey(d, j[8 * i: 8 * (i + 1)])
                f = matrix2text_4bit(e)
                g = text2matrix(f)
                h = invMixColumns(g)
                k = matrix2text(h)
                m = text2matrix_4bit(k)

            n = invShiftRows(m)
            o = invSubBytes(n)
            p = addRoundKey(o, j[:8])
            end = matrix2text_4bit(p)

            return end
    
    print("\nOur key is : " + key)

    if len(text) <= 32:

        textToList = stringToList(text)

        if (len(text) < 32):
            for i in range(0,32-len(text)):
                text = textToList.append('0')

        text = listToString(textToList)

        print("\nOur plaintext :     " + text)

        start = timeit.default_timer()
        encryption = cipher(text, key)
        stop = timeit.default_timer()
        executionTimeEnc = stop - start
        millieSecondEnc = executionTimeEnc * 1000

        start = timeit.default_timer()
        decryption = decipher(encryption)
        stop = timeit.default_timer()
        executionTimeDec = stop - start
        millieSecondDec = executionTimeDec * 1000

        print("After Encryption : " + encryption)
        print("After Decryption : " + decryption)
        print("\nAfter convert to Our Decryption message is:  " + bytes.fromhex(decryption).decode('utf-8') + "\n")
        
        print("Program executed for 'Encryption' : " + str(executionTimeEnc) + " S(second).")
        print("If we convert that to 'Milliesecond' : " + str(millieSecondEnc) + " Ms(MillieSecond).")
        print("Program executed for 'Decryption' : " + str(executionTimeDec) + " second.")
        print("If we convert that to 'Milliesecond' : " + str(millieSecondDec) + " Ms(MillieSecond).")

    else:
        print("\nOur plaintext : " + text)
        # print("\nOur plaintext is divided into 16-character Parts.")

        emptyNumberTimerEnc = 0
        emptyNumberTimerDec = 0
        emptyTextEnc = ""
        emptyTextDec = ""
        numberInputInt = len(text) // 32
        numberInputFloat = len(text) / 32
        textToList = stringToList(text)
        if (numberInputInt != numberInputFloat):
            
            lastList = textToList[numberInputInt * 32:]
            lastListToString = listToString(lastList)
            
            if (len(lastListToString) < 32):
                for i in range(0,32-len(lastListToString)):
                    lastListToString = lastList.append('0')

            afterDivStringLast = listToString(lastList)
            numberInputInt += 1

        for i in range(0, numberInputInt):
            
            if(numberInputInt != numberInputFloat and i != numberInputInt -1):
            
                textWithList = textToList[i * 32:(i * 32) + 32]
                textParts = listToString(textWithList)

            elif(numberInputInt != numberInputFloat and i == numberInputInt - 1):
                
                textParts = afterDivStringLast

            elif(numberInputInt == numberInputFloat):

                textWithList = textToList[i * 32:(i * 32) + 32]
                textParts = listToString(textWithList)
            
            startEnc = timeit.default_timer()
            encryption = cipher(textParts, key)
            stopEnc = timeit.default_timer()
            executionTimeEnc = stopEnc - startEnc
            
            emptyNumberTimerEnc = emptyNumberTimerEnc + executionTimeEnc
            millieSecondEnc = emptyNumberTimerEnc * 1000
            
            startDec = timeit.default_timer()
            decryption = decipher(encryption)
            stopDec = timeit.default_timer()
            executionTimeDec = stopDec - startDec

            emptyNumberTimerDec = emptyNumberTimerDec + executionTimeDec
            millieSecondDec = emptyNumberTimerDec * 1000
            emptyTextEnc = emptyTextEnc + encryption
            emptyTextDec = emptyTextDec + decryption

            
            # print("\nOur Plaintext " + str(i + 1) + ". Part :" + textParts)
            # print("\nAfter convert of  " + str(i + 1) + ". Part :" + bytes.fromhex(textParts).decode('utf-8'))
            # print("After Encryption of " + str(i + 1) + ". Part : " + encryption)
            # print("After Decryption of " + str(i + 1) + ". Part : " + decryption)

        print("\n------------------------------------------------------------------------------------ENCRPYTION PART------------------------------------------------------------------------------------\n")
        print("\n-----------------------------------------------------------------------------After encrypting all the text-----------------------------------------------------------------------------\n" + emptyTextEnc + "\n")
        # print("\nAll text with Decryption : \n" + emptyTextDec)
        # print("\nAfter convert to Our Decryption message is:  " + bytes.fromhex(emptyTextDec).decode('utf-8') + "\n")
        print("Time for Encryption :                  " + str(emptyNumberTimerEnc) + " Second")
        print("If we convert that to 'Milliesecond' : " + str(millieSecondEnc) + " Ms(MillieSecond).")
        print("Time for Decryption :                  " + str(emptyNumberTimerDec) + " Second")
        print("If we convert that to 'Milliesecond' : " + str(millieSecondDec) + " Ms(MillieSecond).")
        

    print("Do you want to continue another Encryption and Decryption? - 'For continue press 'y' - For stop press 'n' ")
    endornot = input()


    if endornot == 'y':

        continue

    elif endornot == 'n':
        print("Thank you for giving importance to information security. Bye :)")
        exit()
        
    else:
        print("You pressed wrong character. Program shut down.")
        exit()



