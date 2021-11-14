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

#Extract names of each file.
fasta_name_position = fasta_name.rfind("/")
fasta_file_name = fasta_name[fasta_name_position + 1 :len(fasta_name)]
#print(fasta_file_name)

enzyme_name_position = enzyme_name.rfind("/")
enzyme_file_name = enzyme_name[enzyme_name_position + 1 :len(enzyme_name)]
#print(enzyme_file_name)

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
title.pop()

#Remove the > from the sequence titles.
for i in range(0,len(title)):
    title[i] = title[i].replace(">", "")

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

if enzyme[-1] == "":
    enzyme.pop()

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


#Find the number of bases before the % sign in each enzyme sequence.
number_bases = 0
initial_site = str()

for percent in enzyme_sequence:
    number_bases = percent.find("%")
    initial_site += "\n" + str(number_bases)

initial_site = initial_site.split("\n")
initial_site.pop(0)
#print(initial_site) #check if this works

#Convert the string list to integer list
initial_site = [int(i) for i in initial_site]
#print(initial_site) #check if it works


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
    #print("For the sequence ", line, "there are ", snumber, " site in the fasta file.")
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


#Print the heading of the output.
print("-"*80)
print("Restriction enzyme analysis of sequence from file", fasta_file_name, ".")
print("Cutting with enzymes found in file", enzyme_file_name, ".")
print("-"*80)

if not title:
    print ("There is no sequence name for this sequence.")
else:
    print("Sequence name:", title[0]) #indexed because we are assuming only one sequence is inputted, otherwise this print statement and the next one would have been in a for loop
print("Sequence is", sequence_length, "bases long.")

#Find where each restriction enzyme cuts the nucelotide sequence.
i = 0
x = 0
y = 1
no_sites = str()


import math

for line in range(0,len(enzyme_sequence_complete)):
    start_range = 1
    fragment_length = 0
    position = str()
    start = 0
    end = 0
    
    if site_number[line] == "0":
        #print("-"*80)
        #print("There are no sites for", enzyme_type[line], ".") #this line and above prints in between.
        no = enzyme_type[line]
        no_sites += "\n" + no
        
    else:
        print("-"*80)
        print("There are", site_number[line], "cutting sites for", enzyme_type[line], ", cutting at", enzyme_sequence[line])
        print("There are", fragment_number[line], "fragments:")
    
    while True:
        i = fasta.find(enzyme_sequence_complete[line], i) + 1 #was +1
        cut_length = 0

        y = initial_site[line]

        # if y != 1:
        #     i += y - 1

        if (i < 1) and (position == ""):
            break
        
        elif i < 1:
            print("length:", sequence_length - x, " ", "range:", x+1, "-", sequence_length)
            #print(fasta[(x): sequence_length])

            length = int(math.ceil((sequence_length - x)/10))
            if length > 6:
                for bases in range(0,6):
                    end = start + 10
                    print(fasta[start:end], end = " ")
                    start = end
                print("")
                for bases in range(7, length + 1):
                    end = start + 10
                    if end > sequence_length:
                        print(fasta[start:sequence_length])
                        start = sequence_length
                    else:
                        print(fasta[start:end], end = " ")
                        start = end
                print("")
                
            else:    
                for bases in range(0, length):
                    end = start + 10
                    if end > sequence_length:
                        print(fasta[start:sequence_length])
                        start = sequence_length
                    else:
                        print(fasta[start:end], end = " ")
                        start = end
            print("")

            break
        else:
            i += y - 1
            #cut_length += i
            fragment_length = i - start_range + 1 # was +1
            print ("length:", fragment_length, " ", "range:", start_range, "-", i) 
            #print(fasta[(start_range - 1): i])
    
            length = int(math.ceil(fragment_length/10)) 

            if length > 6:
                for bases in range(0,6):
                    end = start + 10
                    print(fasta[start:end], end = " ")
                    start = end
                print("")
                for bases in range(7, length + 1):
                    end = start + 10
                    if end > i:
                        print(fasta[start:i])
                        start = i
                    else:
                        print(fasta[start:end], end = " ")
                        start = end
                print("")
                
            else:    
                for bases in range(0, length):
                    end = start + 10
                    if end > i:
                        print(fasta[start:i])
                        start = i
                    else:
                        print(fasta[start:end], end = " ")
                        start = end

            position += "\n" + str(i) 
            start_range = i +1  #+= cut_length
            x = i
   
    if position == "":
        print ("")
    else:
        position = position.split("\n")
        position.pop(0)
        #print("Site are: \n" , position) #check to see if code works
        # print("There are", site_number[line], "cutting sites for", enzyme_type[line], ", cutting at", enzyme_sequence[line])
        # print("There are", fragment_number[line], "fragments:")

print("-"*80)

no_sites = no_sites.split("\n")
no_sites.pop(0)

for line in range(0,len(no_sites)):
    print("There are no sites for", no_sites[line], ".")
    print("-"*80)

#Find way to separate printed sequence in tabs of 10 bases, 60 bases per line

# import math
# start = 0
# end = 0

# length = int(math.ceil(sequence_length/10))
# six_increment = math.ceil(length/6)

# n = 6
# six_multiples = list(range(0,(six_increment+1)*n,n)) #multiple of six until six_increment
# print(six_multiples)

# for six in range(0,six_increment):
#     for bases in range(six_multiples[bases],six_multiples[bases + 1]):
#         end = start + 10
#         print(fasta[start:end], end = "\t")
#         start = end
#     print("")


# if length > 6:
#     for bases in range(0,6):
#         end = start + 10
#         print(fasta[start:end], end = "\t")
#         start = end
#     print("")
#     for bases in range(7, length + 1):
#         end = start + 10
#         print(fasta[start:end], end = "\t")
#         start = end
#     print("")
    
# else:    
#     for bases in range(0,length):
#         end = start + 10
#         print(fasta[start:end], end = "\t")
#         start = end

# #original sequence printed tabs
# length = int(math.ceil(fragment_length/10))
# for bases in range(0, length):
#     end = start + 10
#     if end > i:
#         print(fasta[start:i])
#         start = i
#     else:
#         print(fasta[start:end], end = "\t")
#         start = end

# #To separate in groups of 6
# length = int(math.ceil((sequence_length - x)/10))
# if length > 6:
#     for bases in range(0,6):
#         end = start + 10
#         print(fasta[start:end], end = "\t")
#         start = end
#     print("")
#     for bases in range(7, length + 1):
#         end = start + 10
#         if end > sequence_length:
#             print(fasta[start:sequence_length])
#             start = sequence_length
#         else:
#             print(fasta[start:end], end = "\t")
#             start = end
#     print("")
    
# else:    
#     for bases in range(0, length):
#         end = start + 10
#         if end > sequence_length:
#             print(fasta[start:sequence_length])
#             start = sequence_length
#         else:
#             print(fasta[start:end], end = "\t")
#             start = end

