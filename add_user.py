#!/usr/bin/env python3

#Name: Mohammed Mohammedtayib
#Date: 10/10/2022
#RIT Email: mnm6346@rit.edu

import os
import time
import csv
import crypt
import random 

#Adding colors to texts to make it readable for the user
red = "\u001b[31m"
green = "\u001b[32m"
white = "\u001b[37m"

#Defining a function to encypt user passwords by also using the crypt library
def encryption():
	hash = crypt.crypt("password")
	return hash


#Clearing out the terminal
print("Hello Friend, welcome to the add_user script, the screen will be cleared in 2 seconds")
time.sleep(3)
os.system('clear')





def group():
	with open('linux_users.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			Group = row['Group']
			valid_groups = ["Office", "Pubsafety"]
			with open("/etc/group") as group_file:
				group_list = []
				for line in group_file:
					the_group = line.split(":")[0]
					group_list.append(the_group)
				if Group not in group_list:
					if Group != "area51":
						os.system(f'sudo groupadd {Group}')
				else:
					continue


#Opening the CSV file
def user():
	with open('linux_users.csv') as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		line_count = 0

		#Reading the data without the headers
		for row in csv_reader:
			csv_users = []
			EmployeeID = row['EmployeeID']
			LastN = row['LastName']
			FirstN = row['FirstName']
			Office = row['Office']
			Phone = row['Phone']
			Department = row['Department']
			Group = row['Group']


			if FirstN != '':
				if LastN != '':
					#Printing first name first character and lastname fully lowercased and if there is a character like a comma or an apostrophe it will exclude it
					UserName = FirstN[0].lower() + LastN.lower().replace("'","")
					csv_users.append(UserName)

				#The valid groups are office and pubsaftey and the users within those groups will be added
				valid_groups = ["Office", "Pubsafety"]

				#If the users arent within the valid groups it will print out a message mentioning that their EmployeeID is not valid and the group they are in is not valid
				if Group == 'area51':
					print(f'{white}Cannot process employee ID: {EmployeeID}      {red}{UserName} is not in a valid group')
					
				
				else:
					#passfile users is a list that will be filled with users in etc/passwd
					#used to verify and check if a user is already present within /etc/passwd which helps deal with duplicates
					passfile_users = []
					with open("/etc/passwd") as passfile:
						pass_contents = passfile.readlines()
						for line in pass_contents:
							user = line.split(":")[0]
							passfile_users.append(user)
					for user in csv_users:
						if user in passfile_users:
							dup_user = user+ str(random.randint(1,7))
							passfile_users.append(dup_user)
							if Group == "office":
								os.system(f"sudo useradd -p '{encryption()}' -g {Group} -s /bin/csh -d /home/{Department} -m {dup_user}")
								print(f'{white}Processing employee ID: {EmployeeID}      {green}{dup_user} has been added!')
								os.system(f"sudo passwd -e {dup_user}")
							else:
								os.system(f"sudo useradd -p '{encryption()}' -g {Group} -s /bin/bash -d /home/{Department} -m {dup_user}")
								print(f'{white}Processing employee ID: {EmployeeID}      {green}:{dup_user} has been added!')
								os.system(f"sudo passwd -e {dup_user}")



						#Since we have the user passfile list, we check if a user is within and theyre not then it adds them to the list 
						#THen it checks their group if its equal to office it gives them csh otherwise it is bash
						#csh is the c shell and bash is bourne again shell
						#Then it expires the users password so that they have to renew/change their password
						elif user not in passfile_users:
							passfile_users.append(user)
							if Group == "office":
								os.system(f"sudo useradd -p '{encryption()}' -g {Group} -s /bin/csh -d /home/{Department} -m {user}")
								print(f'{white}Processing employee ID: {EmployeeID}     {green}{user} has been added!')
								os.system(f"sudo passwd -e {user}")
							else:
								os.system(f"sudo useradd -p '{encryption()}' -g {Group} -s /bin/bash -d /home/{Department} -m {user}")
								print(f'{white}Processing employee ID: {EmployeeID}      {green}{user} has been added!')
								os.system(f"sudo passwd -e {user}")

			#If the the user doesnt belong to any group or it is invalid it will print the following
			else:
				print(f"{white}Cannot process employee ID: {EmployeeID}       {red}Invalid or missing data")
 
 
	csv_file.close()



def main():
	group()
	user()

main()