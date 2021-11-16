#BINF 6410 - Assignment 2 - by Shalvi Chirmade - November 15, 2021

#This script will allow the user to input a fasta sequence file and a restriction enzyme file to output the cut sites for each enzyme in the list. 

#-----------------------------------------------------------------------

#Asking the user to input a FASTA file for analysis.

while True: 
        fasta_name = input("\nPlease enter the file path to your FASTA sequence file. Your file should end with .fas or .fasta. \n\n")
        if fasta_name.endswith(".fasta"):
            print("You have entered an appropriate file name.\n")
            break
        elif fasta_name.endswith(".fas"):
            print("You have entered an appropriate file name.\n")
            break
        else:
            print("Sorry, you have entered an incorrect FASTA file name, please try again.\n")
 

#Asking the user to input a restriction enzyme information text file.

while True: 
        enzyme_name = input("Please enter the file path to your restriction enzyme file. Your file should be a .txt file. \n This is an example of what each line of your file should look like: \n EcoRI;G%AATTC \n\n")
        if enzyme_name.endswith(".txt"):
            print("You have entered an appropriate file name.\n")
            break
        else:
            print("Sorry, you have entered an incorrect text file name, please try again.\n")


#---------------------------------------------------------------------------

#Take each restriction enzyme and find where it cuts the nucelotide sequence.

#Extract names of each file.
fasta_name_position = fasta_name.rfind("/")
fasta_file_name = fasta_name[fasta_name_position + 1 :len(fasta_name)]

enzyme_name_position = enzyme_name.rfind("/")
enzyme_file_name = enzyme_name[enzyme_name_position + 1 :len(enzyme_name)]

#Open fasta file and read each line.
fasta_file = open(fasta_name)
fasta = str()
title = str()
for line in fasta_file:
    if not line.startswith(">"): #disregards title
        fasta += line.rstrip() 
    else:
        title += line #I realized too late, that I could have made this easier for myself. However I used this method for creating every list, so I will leave it this way. I understand that this is not the optimal method for doing so. I could have defined the variable as a list in the beginning and used append to add every element.

fasta_file.close()

#Splitting each sequence title into its own line. Each line is now an element corresponding the same element in the FASTA file.
title = title.split("\n")
title.pop()

#Remove the > from the sequence titles.
for i in range(0,len(title)):
    title[i] = title[i].replace(">", "")


#Length of the sequence.
sequence_length = len(fasta)


#Open enzyme file and read each line.
enzyme_file = open(enzyme_name)
enzyme = str()
for line in enzyme_file:
    enzyme = enzyme + line

enzyme_file.close()

enzyme = enzyme.split("\n")

#Enzyme file given had an empty line at the end of the file. I am removing it.
if enzyme[-1] == "":
    enzyme.pop()



#Need to split the name of the enzyme and its appropirate sequence.
enzyme_type = str()
enzyme_sequence = str()
for RE in enzyme:
    sections = RE.split(";")
    enzyme_type = enzyme_type + "\n" + sections[0]
    enzyme_sequence = enzyme_sequence + "\n" + sections[1]

#Convert to list and delete the first element which is empty.
enzyme_type = enzyme_type.split("\n")
enzyme_type.pop(0)

enzyme_sequence = enzyme_sequence.split("\n")
enzyme_sequence.pop(0)


#---------------------------------------------------------------------------

#Find the number of bases before the % sign in each enzyme sequence.
number_bases = 0
initial_site = str()

for percent in enzyme_sequence:
    number_bases = percent.find("%")
    initial_site += "\n" + str(number_bases)

initial_site = initial_site.split("\n")
initial_site.pop(0)


#Convert the string list to integer list
initial_site = [int(i) for i in initial_site] #I used "i" because this was my first time using a one-line for loop; I found it easier to formulate my code.


#Remove the % in the enzyme sequence to search for number of cut sites in FASTA file.
enzyme_sequence_complete = str()
for enzyme in enzyme_sequence:
    full_sequence = enzyme.replace("%", "")
    enzyme_sequence_complete += "\n" + full_sequence

#Now each element corresponds to the other enzyme variables.
enzyme_sequence_complete = enzyme_sequence_complete.split("\n")
enzyme_sequence_complete.pop(0)



#How many cut sites are present in the FASTA file per emzyme.
site_number = str()
fragment_number = str()
for sequence in enzyme_sequence_complete:
    snumber = fasta.count(sequence) #number of cut sites
    fnumber = str(snumber + 1) #number of fragments
    snumber = str(snumber)
    site_number += "\n" + snumber
    fragment_number += "\n" + fnumber

site_number = site_number.split("\n")
site_number.pop(0)

fragment_number = fragment_number.split("\n")
fragment_number.pop(0)


#---------------------------------------------------------------------------

#Print the heading of the output.
print("") #Empty line after entering file paths; creates a separation for this result output.
print("-"*65)
print("Restriction enzyme analysis of sequence from file ", fasta_file_name, ".", sep = "")
print("Cutting with enzymes found in file ", enzyme_file_name, ".", sep = "")
print("-"*65)

#Depending if the fasta file entered has a sequence title or not.
if not title:
    print ("There is no sequence name for this sequence.")
else:
    print("Sequence name:", title[0]) #indexed because we are assuming only one sequence is inputted, otherwise this print statement and the next one would have been in a for loop
print("Sequence is", sequence_length, "bases long.")

#Find where each restriction enzyme cuts the nucelotide sequence. Print outputs.
frag_end_pos = 0
last_frag_pos = 0
no_sites = str()

import math

#This for loop is for printing the whole output. It is iterated for the number of enzymes in the enzyme file.
for enz_seq in range(0,len(enzyme_sequence_complete)):
    start_range = 1
    fragment_length = 0
    position = str()
    start = 0
    end = 0
    
    #This if statement extracts the names of the enzymes with no cut sites.
    if site_number[enz_seq] == "0":
        enzyme = enzyme_type[enz_seq]
        no_sites += "\n" + enzyme
        
    #Else prints the length, range and the fragment sequences for each enzyme with cut sites.
    else:
        print("-"*65)
        print("There are ", site_number[enz_seq], " cutting sites for ", enzyme_type[enz_seq], ", cutting at ", enzyme_sequence[enz_seq], sep ="")
        print("There are", fragment_number[enz_seq], "fragments:\n")
    
    #For printing the whole sequence until the last fragment is detected.
    while True:
        frag_end_pos = fasta.find(enzyme_sequence_complete[enz_seq], frag_end_pos) + 1 
        cut_length = 0

        inc = initial_site[enz_seq]

        #When there are no cut sites.
        if (frag_end_pos < 1) and (position == ""):
            break 
        
        #Printing the last fragment.
        elif frag_end_pos < 1:
            print("length: ", sequence_length - last_frag_pos, " range: ", last_frag_pos + 1, "-", sequence_length, sep = "")

            length = int(math.ceil((sequence_length - last_frag_pos)/10))
            print_newline = 0

            #Separting bases in groups of ten and adding a new line when there are six groups.
            for bases in range(0, length + 1):
                end = start + 10
                if end > sequence_length:
                    print(fasta[start:sequence_length])
                    start = sequence_length
                else:
                    print(fasta[start:end], end = " ")
                    start = end
                print_newline += 1
                if print_newline == 6:
                    print("")
                    print_newline = 0

            break
        
        #Printing the rest of the fragments.
        else:
            frag_end_pos += inc - 1
            fragment_length = frag_end_pos - start_range + 1 
            print ("length: ", fragment_length, " range: ", start_range, "-", frag_end_pos, sep = "") 
    
            length = int(math.ceil(fragment_length/10)) 
            print_newline = 0

            #Separting bases in groups of ten and adding a new line when there are six groups.
            for bases in range(0, length + 1):
                end = start + 10
                if end > frag_end_pos:
                    print(fasta[start:frag_end_pos], end = " ")
                    start = frag_end_pos
                    break
                else:
                    print(fasta[start:end], end = " ")
                    start = end
                print_newline += 1
                if print_newline == 6:
                    print("")
                    print_newline = 0
            print("")
            
            position += "\n" + str(frag_end_pos) 
            start_range = frag_end_pos +1  
            last_frag_pos = frag_end_pos
   
    if position == "":
        print ("")
    else:
        position = position.split("\n")
        position.pop(0)

print("\n" + "-"*65)

#Making list of enzymes without cut sites.
no_sites = no_sites.split("\n")
no_sites.pop(0)

#Print the enzymes without cut sites.
for enzyme in range(0,len(no_sites)):
    print("There are no sites for ", no_sites[enzyme], ".", sep ="")
    print("-"*65)

