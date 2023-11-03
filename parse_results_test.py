# load in party_info.txt and put each line of text in an array

with open('party_info.txt', 'r') as file:
    party_info = file.readlines()

# remove the \n from each line
party_info = [line.rstrip() for line in party_info]

# # remove the first 4 and last 1 lines
party_info = party_info[4:-1]

print(party_info)
