#Auxilliary Variables and Functions
 
IDctr = 0 #Self-explanatory
ScheduleProjectsList = [] #This is the queue
 
"""Initializes the headers of both the main saveFile and completedProjects"""
with open('saveFile.txt', 'w') as file:
    file.write(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15} \n")

with open('completedProjects.txt', 'w') as file:
    file.write(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15} \n")
    
#Ends here    

class Project: 
    def __init__(self, ID, NAME, SIZE, PRIORITY, STATUS):
        """This wont be utilized much; This is just for initializing or applying classes"""
        self.ID = ID
        self.NAME = NAME
        self.SIZE = SIZE
        self.PRIORITY = PRIORITY
        self.STATUS = STATUS

def Check_menu(choices): #Added this validation for menu -Bri
    """Validation for menu choices, ensures that the user input valid choices"""
    while True:
        choice = input("Choice: ")
        if choice in choices:
            return choice
        else:
            print("Please enter a valid choice from the menu.")
        
while(True):
    print('=====PROJECT MANAGEMENT SYSTEM=====')
    print('[1] Input Project Details')
    print('[2] View Projects')
    print('[3] Schedule Projects')
    print('[4] Get Project')
    print('[5] Exit')
    print('===================================')
    choice = Check_menu(['1', '2', '3', '4', '5'])
    choice = int(choice)
    
    match choice:
        case 1:
            print('=====INPUT PROJECT DETAILS=====')
            pID = 202600001 + IDctr
            pName = input('Enter Project Name: ')
            pSize = input('Enter Project Size: ')
            pPriority = input('Enter Project Priority: ')
            pStatus = "Pending"
            
            newProject = Project(pID, pName, pSize, pPriority, pStatus)
            with open('saveFile.txt' , 'a') as file:
                file.write(f"{newProject.ID:<15} | {newProject.NAME:<20} | {newProject.SIZE:<15} | {newProject.PRIORITY:<20} | {newProject.STATUS:<15} \n")
            IDctr+=1
            
        case 2:
            print('=====VIEW PROJECTS=====')
            print('[a] One Project')
            print('[b] Completed')
            print('[c] All Projects')
            print('=======================')
            choice = Check_menu(['a', 'b', 'c'])
            
            match choice:
                case 'a':
                    located = False
                    ID = input('Enter Project ID number: ')

                    if not ID.isdigit():
                        print("Invalid input. Please enter a valid Project ID number.")
                    else:
                        with open('saveFile.txt' , 'r') as file:
                            lines = file.readlines()
                            for line in lines:
                                data = line.split('|')
                                if data[0].strip() == ID:
                                    located = True
                                    print(f"{data[0].strip():<15} | {data[1].strip():<20} | {data[2].strip():<15} | {data[3].strip():<20} | {data[4].strip():<15}")
                                    break
                            
                            if not located:
                                print("The Project your looking for isn't in the saveFile")
                            
                case 'b':
                    print('=====COMPLETED PROJECTS=====')
                    with open('completedProjects.txt', 'r') as file:
                        lines = file.readlines()
                        if len(lines) == 1:
                            print('There are no completed projects currently saved.')
                        else:
                            for line in lines:
                                print(line)
                    print()
                    
                case 'c':
                    """This part essentially just reads what readlines() return and iterates over it with the for loop.
                    It'll then print all the lines, thereafter."""
                    with open('saveFile.txt', 'r') as f1, open('completedProjects.txt', 'r') as f2:
                        active_lines = f1.readlines()
                        completed_lines = f2.readlines()                    
                    combined_data = []                   
                    # Skip the first line (headers) of both files using [1:]
                    if len(active_lines) > 1:
                        combined_data.extend([line.strip() for line in active_lines[1:] if not line.isspace()])
                    if len(completed_lines) > 1:
                        combined_data.extend([line.strip() for line in completed_lines[1:] if not line.isspace()])                   
                    # Check if there are actually any projects in the combined list
                    if not combined_data:
                        print('There are no projects currently saved in either file.')
                    else:
                        # Sort the combined list (Default sorts by PROJECTID since it's the first string)
                        combined_data.sort() 
                        # Print a single, unified header
                        print(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15}")
                        # Display all sorted projects
                        for line in combined_data:
                            print(line)
                    print()
                                
        case 3:
            print('=====SCHEDULE PROJECTSS=====')
            print('[a] Create Schedule')
            print('[b] View Updated Schedule')
            print('===========================')
            choice = Check_menu(['a', 'b'])
            match choice:
                case 'a':
                    """This part essentially just reads what readlines() return and iterates over it with the for loop.
                    It'll then split the returned line(string), then creates a dictionary containing those seperate info and appends It
                    to a list"""
                    
                    ScheduleProjectsList = [] #This is to avoid appending the same contents to the list when reading
                    
                    with open('saveFile.txt' , 'r') as file:
                        lines = file.readlines()
                        if len(lines) > 1:
                            # Safer alternative for next(file)
                            for line in lines[1:]:
                                if line.isspace():
                                    continue
                                data = line.split('|')
                                ScheduleProjectsList.append(dict(ID=data[0].strip(), NAME=data[1].strip(), SIZE=data[2].strip(), PRIORITY=data[3].strip(), STATUS=data[4].strip()))
                        
                        """Basically just sorts the Queue based on the contents of the sub content of ScheduleProjectsList by considering
                        both PRIORITY and SIZE values in ascending order"""
                        ScheduleProjectsList.sort(key= lambda project : (project['PRIORITY'], project['SIZE']))
                        print(ScheduleProjectsList)
                        
                case 'b':
                    """Same as Create Schedule but for Reading only. If the ScheduleProjectsList is empty, It'll create the queue, else it'll just read what's inside ScheduleProjectsList"""
                    with open('saveFile.txt' , 'r') as file:
                        if not ScheduleProjectsList:
                            lines = file.readlines()
                            if len(lines) > 1:
                                for line in lines[1:]:
                                    if line.isspace():
                                        continue
                                    data = line.split('|')
                                    ScheduleProjectsList.append(dict(ID=data[0].strip(), NAME=data[1].strip(), SIZE=data[2].strip(), PRIORITY=data[3].strip(), STATUS=data[4].strip()))
                            ScheduleProjectsList.sort(key= lambda project : (project['PRIORITY'], project['SIZE']))
                            
                            print(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15} \n")
                            for data in ScheduleProjectsList:
                                print(f"{data['ID']:<15} | {data['NAME']:<20} | {data['SIZE']:<15} | {data['PRIORITY']:<20} | {data['STATUS']:<15} \n")
                                
                        else:
                            print(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15} \n")
                            for data in ScheduleProjectsList:
                                print(f"{data['ID']:<15} | {data['NAME']:<20} | {data['SIZE']:<15} | {data['PRIORITY']:<20} | {data['STATUS']:<15} \n")
                    
        case 4:     
            if not ScheduleProjectsList:
                print("\nThe queue is currently empty! Please create/update a schedule first.\n")
            else:
                print('=====PREVIOUS QUEUE=====')
                print(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15} \n")
                for data in ScheduleProjectsList:
                    print(f"{data['ID']:<15} | {data['NAME']:<20} | {data['SIZE']:<15} | {data['PRIORITY']:<20} | {data['STATUS']:<15}")
                print('========================')
                
                
                completed_id = ScheduleProjectsList[0]['ID'] # 1. Save the ID before you pop it so we can use it to filter saveFile.txt
                print(f"Project: {ScheduleProjectsList[0]['ID']} was removed\n")
                
                with open('completedProjects.txt', 'a') as file:
                    file.write(f"{ScheduleProjectsList[0]['ID']:<15} | {ScheduleProjectsList[0]['NAME']:<20} | {ScheduleProjectsList[0]['SIZE']:<15} | {ScheduleProjectsList[0]['PRIORITY']:<20} | {'Finished':<15}\n")
                
                ScheduleProjectsList.pop(0)
                
                # Read all current lines in the save file
                with open('saveFile.txt', 'r') as file:
                    lines = file.readlines()
                
                # Overwrite the save file, keeping only the header and projects that DO NOT match the completed_id
                with open('saveFile.txt', 'w') as file:
                    for line in lines:
                        if line.isspace():
                            continue
                        
                        data = line.split('|')
                        
                        # If the line is the header OR the ID doesn't match the one we just completed, write it back
                        if data[0].strip() == 'PROJECTID' or data[0].strip() != completed_id:
                            file.write(line)

                print('=====CURRENT QUEUE=====')
                print(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15} \n")
                for data in ScheduleProjectsList:
                    print(f"{data['ID']:<15} | {data['NAME']:<20} | {data['SIZE']:<15} | {data['PRIORITY']:<20} | {data['STATUS']:<15}")
                print('=======================')
        
        case 5:
            print("Exiting System. Goodbye!")
            break
