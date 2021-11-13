#BINF 6410 - Assignment 2 - by Shalvi Chirmade - November 15, 2021

#This script will allow the user to input a fasta sequence file and a restriction enzyme file to output the cut sites for each enzyme in the list. 

#-----------------------------------------------------------------------

#Asking the user to input a FASTA file for analysis.

while True: 
    #try:
        fasta_name = input("Please enter the file path to your FASTA sequence file. Your file should end with .fas or .fasta. \n")
        if fasta_name.endswith(".fasta"):
            print("You have entered an appropriate file name.")
            break
        elif fasta_name.endswith(".fas"):
            print("You have entered an appropriate file name.")
            break
        else:
            print("Sorry, you have entered an incorrect file name, please try again.")
    #except:
        #print("Sorry, you have entered an incorrect file name, please try again.") - not being used


#Asking the user to input a restriction enzyme information text file.

while True: 
        enzyme_name = input("Please enter the file path to your restriction enzyme file. Your file should be a .txt file. \n This is an example of what each line of your file should look like: \n EcoRI;G%AATTC \n")
        if enzyme_name.endswith(".txt"):
            print("You have entered an appropriate file name.")
            break
        else:
            print("Sorry, you have entered an incorrect file name, please try again.")


#---------------------------------------------------------------------------

#Take each restriction enzyme and find where it cuts the nucelotide sequence.

#Open fasta file and read each line.
fasta_file = open(fasta_name)
fasta = str()
title = str()
for line in fasta_file:
    if not line.startswith(">"): #disregards title
        fasta = fasta + line.rstrip() 
    else:
        title = title + line 

#Splitting each sequence title into its own line. Each line is now an element corresponding the same element in the FASTA file.
title = title.split("\n")

fasta_file.close()

#Checks to see if code works. 
#print(fasta[0:100])
#print(title[0:15]) - tested on a fasta file containing multiple sequences

#Length of the sequence.
sequence_length = len(fasta)



#Open enzyme file and read each line.
enzyme_file = open(enzyme_name)
enzyme = str()
for line in enzyme_file:
    enzyme = enzyme + line

enzyme = enzyme.split("\n")

enzyme_file.close()

#Check to see if code works.
#print(enzyme[2])

#Need to split the name of the enzyme and its appropirate sequence.
enzyme_type = str()
enzyme_sequence = str()
for line in enzyme:
    test = line.split(";")
    enzyme_type = enzyme_type + "\n" + test[0]
    enzyme_sequence = enzyme_sequence + "\n" + test[1]

#Convert to list and delete the first element which is empty.
enzyme_type = enzyme_type.split("\n")
enzyme_type.pop(0)

enzyme_sequence = enzyme_sequence.split("\n")
enzyme_sequence.pop(0)

#Check to see it code works.
# print(enzyme_type[1])
# print(enzyme_sequence[1])


#Remove the % in the enzyme sequence to search for number of cut sites in FASTA file.
enzyme_sequence_complete = str()
for line in enzyme_sequence:
    full = line.replace("%", "")
    enzyme_sequence_complete += "\n" + full

#Now each element corresponds to the other enzyme variables.
enzyme_sequence_complete = enzyme_sequence_complete.split("\n")
enzyme_sequence_complete.pop(0)

#Check to see if code works. 
#print(enzyme_sequence_complete[1])

#How many cut sites are present in the FASTA file per emzyme.
site_number = str()
fragment_number = str()
for line in enzyme_sequence_complete:
    snumber = fasta.count(line)
    print("For the sequence ", line, "there are ", snumber, " site in the fasta file.")
    fnumber = str(snumber + 1) #number of fragments
    snumber = str(snumber)
    site_number += "\n" + snumber
    fragment_number += "\n" + fnumber

site_number = site_number.split("\n")
site_number.pop(0)

fragment_number = fragment_number.split("\n")
fragment_number.pop(0)

#Check to see if code works.
# print(site_number[1])
# print(fragment_number[1])


#Find where each restriction enzyme cuts the nucelotide sequence.
i = 0
x = 0

for line in range(0,len(enzyme_sequence_complete)):
    start_range = 1
    fragment_length = 0
    position = str()
    while True:
        i = fasta.find(enzyme_sequence_complete[line], i) + 1
        cut_length = 0

        if (i < 1) and (position == ""):
            break
        
        elif i < 1:
            print("length:", sequence_length - x, "\t", "range:", x+1, "-", sequence_length)
            #print("Done", x+1) #check - remove later
            break
        else:
            cut_length += i
            fragment_length = i - start_range + 1
            print ("length:", fragment_length, "\t", "range:", start_range, "-", i) #check - remove later
            position += "\n" + str(i) 
            start_range += cut_length 
            x = i
   
    if position == "":
        print ("There are no sites for", enzyme_type[line], ".")
    else:
        position = position.split("\n")
        position.pop(0)
        #print("Site are: \n" , position) #check to see if code works
        print("There are", site_number[line], "cutting sites for", enzyme_type[line], ", cutting at", enzyme_sequence[line])
        print("There are", fragment_number[line], "fragments:")


#Above code is wrong for AluI

#Need to find a way to count bases before % and after % 

#How to cut the sequence based on this?

