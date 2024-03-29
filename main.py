import sys
import regex as re
def dictionaryIncrement(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1
    return dictionary
if __name__ == '__main__':
    input_file = "input.txt"
    output_file = "output.txt"
    # Check if the user provided the input and output files
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        if len(sys.argv) == 2:
            input_file = sys.argv[1]
            output_file = "output_" + input_file
        else:
            input_file = sys.argv[1]
            output_file = sys.argv[2]
    # Dictionary to store the final tokens
    keywordTokens = {}
    idTokens = {}
    constTokens = {}
    litTokens = {}
    opTokens = {}
    punctTokens = {}
    totalTokens = 0
    #List of operators and punctuations
    operators = {'+', '-', '*', '=', '/', '%', '!', '<', '>'}
    punctuation = {'{', '}', '(', ')', '[', ']', ';', ','}

    #Symbol table with word and token type
    Keywords={'int':'keyword','char':'keyword','bool':'keyword','float':'keyword',
            'break':'keyword','const':'keyword', 'continue':'keyword','default':'keyword',
            'do':'keyword','while':'keyword','if':'keyword','else':'keyword',
            'for':'keyword','return':'keyword','switch':'keyword','case':'keyword',
            'void':'keyword','double':'keyword','long':'keyword','goto':'keyword',
            'short':'keyword'}
    
    # Auxiliar lists
    preProcessed = []
    preProcessedStrings = []
    # Final list where the tokens will be stored
    Tokens_Types=[[]]
    
    # Flags
    multilineComment = False
    slash = False
    asterisk = False

    # Read the file
    try:
        with open(input_file, 'r') as file:
            data = file.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    # Split the data by line
    data = data.split('\n')

    # Create a list of lists
    Comment=False
    lines = [[]]
    for line in data:
        line = re.split('(".*")+', line)
        temp = []
        for subLine in line:
            if re.match('(".*")+', subLine):
                temp.append(subLine)
                continue
            if subLine == '':
                continue
            # Replace multiple spaces with a single space
            subLine = re.sub(' +', ' ', str(subLine))
            # Remove the comments
            if subLine.find('//') != -1:
                subLine = subLine[:subLine.find('//')]
                Comment=True
            # Split the line by space
            subLine = subLine.split(' ')
            for piece in subLine:
                if piece == '':
                    continue
                temp.append(piece)
            #Check if the rest of the line is a comment
            if Comment:
                Comment=False
                break
        line = temp
        # For each word in the line
        for word in line:
            if word == '':
                continue
            if re.match('(".*")+', word):
                lines[len(lines)-1].append(word)
                continue
            # For each character in the word
            pendingString = ""
            for char in word:
                # If the character is ;
                if char in punctuation:
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
    for line in lines:
        for word in line:
            preProcessedStrings.append(word)


    # Iterate over the pre processed strings
    for word in preProcessedStrings:
        if word != '/' and word != '*':
            slash = False
            asterisk=False
        if word == '/' and multilineComment == False:
            slash = True
            asterisk = False
            preProcessed.append(word)
        elif word == '*' and slash and multilineComment == False:
            asterisk = False
            slash = False
            multilineComment = True
            preProcessed.pop()
        elif word == '*' and multilineComment:
            asterisk = True
            slash = False
        elif word == '/' and asterisk and multilineComment:
            multilineComment = False
            asterisk = False
            slash = False
        elif not multilineComment:
            preProcessed.append(word)

    #Classify lexemes into tokens
    act=0
    for word in preProcessed:
        if word =='\n':
            Tokens_Types.append([])
            act+=1
            continue
        if word in operators:
            Tokens_Types[act].append('op')
            opTokens = dictionaryIncrement(opTokens, word)
            totalTokens += 1
            continue
        if word in punctuation:
            Tokens_Types[act].append('punct')
            punctTokens = dictionaryIncrement(punctTokens, word)
            totalTokens += 1
            continue
        if word in Keywords:
            Tokens_Types[act].append(Keywords[word])
            keywordTokens = dictionaryIncrement(keywordTokens, word)
            totalTokens += 1
            continue
        if re.match('^[A-Za-z]([A-Za-z0-9_])*$',word):
            idTokens = dictionaryIncrement(idTokens, word)
            totalTokens += 1
            Tokens_Types[act].append('Id')
            continue
        if re.match('^[0-9]+$', word):
            constTokens = dictionaryIncrement(constTokens, word)
            totalTokens += 1
            Tokens_Types[act].append('const')
            continue
        if re.match('(".*")+',word):
            litTokens = dictionaryIncrement(litTokens, word)
            totalTokens += 1
            Tokens_Types[act].append('lit')
            continue
    # Remove the empty lists
    Tokens_Types = [x for x in Tokens_Types if x != []]
    # Write tokenns into the file
    try:
        with open(output_file, 'w') as file:
            if(totalTokens==0):
                file.write("No tokens found")
                sys.exit(0)
            file.write("Tokens:\n")
            for line in Tokens_Types:
                for token in line:
                    file.write(token + " ")
                file.write('\n')
            file.write("\n")
            file.write("Tokens recount:\n")
            if len(keywordTokens) > 0:
                file.write("\tKeywords:\n\t\t")
                for key in keywordTokens:
                    file.write(f"{key} -> {keywordTokens[key]}, ")
                file.write("\n")
            if len(idTokens) > 0:
                file.write("\tIdentifiers:\n\t\t")
                for key in idTokens:
                    file.write(f"{key} -> {idTokens[key]}, ")
                file.write("\n")
            if len(constTokens) > 0:
                file.write("\tConstants:\n\t\t")
                for key in constTokens:
                    file.write(f"{key} -> {constTokens[key]}, ")
                file.write("\n")
            if len(litTokens) > 0:
                file.write("\tLiterals:\n\t\t")
                for key in litTokens:
                    file.write(f"{key} -> {litTokens[key]}, ")
                file.write("\n")
            if len(opTokens) > 0:
                file.write("\tOperators:\n\t\t")
                for key in opTokens:
                    file.write(f"{key} -> {opTokens[key]}, ")
                file.write("\n")
            if len(punctTokens) > 0:
                file.write("\tPunctuations:\n\t\t")
                for key in punctTokens:
                    file.write(f"{key} -> {punctTokens[key]}, ")
                file.write("\n")
            file.write("\n")
            file.write(f"Total Tokens: {totalTokens}")
    except Exception as e:
        print(f"An error occurred while writing the file: {e}")
        sys.exit(1)