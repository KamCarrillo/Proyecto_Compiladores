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
    #counter to track the index of the list
    i = 0
    for line in data:
        # Replace multiple spaces with a single space
        line = re.sub(' +', ' ', line)
        # Split the line by space
        line = line.split(' ')
        # For each word in the line
        for word in line:
            # For each character in the word
            pendingString = ""
            for char in word:
                # If the character is ;
                if char == ';':
                    # Append the pending string to the list
                    lines[i].append(pendingString)
                    # Append the ; to the list
                    lines[i].append(';')
                    # Break the reading of the line
                    i += 1
                    break
