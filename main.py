import os
import sys
import regex as re
import pandas as pd

if __name__ == '__main__':
    #List of operators and punctuations
    # TODO: Check if the operators and punctuations are correct and complete
    operators = {'+', '-', '*', '=', '/', '%', '!', '<', '>'}
    punctuation = {'{', '}', '(', ')', '[', ']', ';', ','}
    # Read the file
    try:
        with open('input.txt', 'r') as file:
            data = file.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    # Split the data by line
    data = data.split('\n')

    # Create a list of lists
    lines = [[]]
    for line in data:
        # Replace multiple spaces with a single space
        line = re.sub(' +', ' ', line)
        # Remove the comments
        if line.find('//') != -1:
            line = line[:line.find('//')]
        # Split the line by space
        line = line.split(' ')
        # For each word in the line
        for word in line:
            # For each character in the word
            pendingString = ""
            for char in word:
                # If the character is ;
                if char == ';':
                    # Append the pending string to the list if it is not empty
                    if pendingString != "":
                        lines[len(lines)-1].append(pendingString)
                    # Append the ; to the list
                    lines[len(lines)-1].append(';')
                    # Reset the pending string
                    pendingString = ""
                elif char in punctuation:
                    # If the character is a punctuation append the pending string to the list if it is not empty
                    if pendingString != "":
                        lines[len(lines)-1].append(pendingString)
                    # Append the punctuation to the list
                    lines[len(lines)-1].append(char)
                    # Reset the pending string
                    pendingString = ""
                elif char in operators:
                    # If the character is an operator append the pending string to the list if it is not empty
                    if pendingString != "":
                        lines[len(lines)-1].append(pendingString)
                    # Append the operator to the list
                    lines[len(lines)-1].append(char)
                    # Reset the pending string
                    pendingString = ""
                else:
                    # If the character is a letter or number
                    # Append the character to the pending string
                    pendingString += char
            if pendingString != "":
                lines[len(lines)-1].append(pendingString)
        # Append a jump line to the list
        lines[len(lines)-1].append('\n')
        lines.append([])
    # Remove the empty lists
    lines = [x for x in lines if x != []]
    preProcessedStrings = []
    for line in lines:
        for word in line:
            preProcessedStrings.append(word)
    # Remove the multiline comments
    preProcessed = []
    # Flags
    multilineComment = False
    slash = False
    asterisk = False
    # Iterate over the pre processed strings
    for word in preProcessedStrings:
        if word == '/' and multilineComment == False:
            slash = True
            asterisk = False
        elif word == '*' and slash and multilineComment == False:
            asterisk = False
            slash = False
            multilineComment = True
        elif word == '*' and multilineComment:
            asterisk = True
            slash = False
        elif word == '/' and asterisk and multilineComment:
            multilineComment = False
            asterisk = False
            slash = False
        elif not multilineComment:
            preProcessed.append(word)
    # Print all the pre processed strings
    print("Preprocessed strings:")
    print(preProcessed)

    #Symbol table with word and token type
    Symbol_Table={'int':'keyword','char':'keyword','bool':'keyword','float':'keyword',
                'break':'keyword','const':'keyword', 'continue':'keyword','default':'keyword',
                'do':'keyword','while':'keyword','if':'keyword','else':'keyword',
                'for':'keyword','return':'keyword','switch':'keyword','case':'keyword',
                'void':'keyword','double':'keyword','long':'keyword','goto':'keyword',
                'printf':'keyword','scanf':'keyword','puts':'keyword','getchar':'keyword',
                'puts':'keyword','short':'keyword'}
    
    #Classify lexemes into tokens
    Tokens_Types=[[]]
    act=0;
    for word in preProcessed:
        if word =='\n':
            Tokens_Types.append([])
            act+=1
            continue
        if word in operators:
            Tokens_Types[act].append('op')
            continue
        if word in punctuation:
            Tokens_Types[act].append('punct')
            continue
        if word in Symbol_Table:
            Tokens_Types[act].append(Symbol_Table[word])
            continue
        if word in operators:
            Tokens_Types[act].append('op')
            continue
        if re.match('^[A-Za-z]([A-Zz-z0-9_])*$',word):
            Symbol_Table[word]='Id'
            Tokens_Types[act].append('Id')
            continue
        if re.match('^[0-9]+$', word):
            Symbol_Table[word] = 'const'
            Tokens_Types[act].append('const')
            continue

    # Print all the Tokens
    print("Tokens: ")
    for line in Tokens_Types:
        print(line)

    

    
