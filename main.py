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
                    # Break the reading of the line
                    lines.append([])
                    pendingString = ""
                    break
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
        lines.append([])
    # Remove the empty lists
    lines = [x for x in lines if x != []]
    # Print the list of lists
    print(lines)
