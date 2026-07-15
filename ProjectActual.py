#Auxilliary Variables and Functions
 
IDctr = 0 #Self-explanatory
ScheduleProjectsList = [] #This is the queue

try:
    """Initializes the headers of both the main saveFile and completedProjects"""
    with open('saveFile.txt', 'w') as file:
        file.write(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15} \n")

    with open('completedProjects.txt', 'w') as file:
        file.write(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15} \n")
except IOError as e:
    print(f"Critical Error initializing system files: {e}")    
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
        try:
            choice = input("Choice: ")
            if choice in choices:
                return choice
            else:
                print("Please enter a valid choice from the menu.")
        except KeyboardInterrupt:
            # Handles if the user presses Ctrl+C to force quit
            print("\nForce quitting... Goodbye!")
            exit()        
        
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
            while True:
                pSize = input('Enter Project Size: ').strip()
                pPriority = input('Enter Project Priority: ').strip()
                
                if pSize.isdigit() and pPriority.isdigit():
                    break # Exits the loop safely
                else:
                    print('Error: Size and Priority must be integer values. Please try again.')
            pStatus = "Pending"

            newProject = Project(pID, pName, pSize, pPriority, pStatus)
            try:
                with open('saveFile.txt' , 'a') as file:
                    file.write(f"{newProject.ID:<15} | {newProject.NAME:<20} | {newProject.SIZE:<15} | {newProject.PRIORITY:<20} | {newProject.STATUS:<15} \n")
                IDctr+=1
            except Exception as e:
                print(f"Error saving project: {e}")
            
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
                    while True:
                        ID = input('Enter Project ID number: ')
                        if ID.isdigit():
                            break
                        else:
                            print("Invalid input. Please enter a valid numeric Project ID number.")
                    try:
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
                    except FileNotFoundError:
                        print("Error: 'saveFile.txt' not found. It may have been deleted.")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                            
                case 'b':
                    print('=====COMPLETED PROJECTS=====')
                    try:
                        with open('completedProjects.txt', 'r') as file:
                            lines = file.readlines()
                            if len(lines) == 1:
                                print('There are no completed projects currently saved.')
                            else:
                                for line in lines:
                                    print(line)
                    except FileNotFoundError:
                        print("Error: 'completedProjects.txt' not found.")
                    print()
                    
                case 'c':
                    """This part essentially just reads what readlines() return and iterates over it with the for loop.
                    It'll then print all the lines, thereafter."""
                    try:
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
                    except FileNotFoundError:
                        print("Error: One or both project files are missing.")
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
                    try:
                        with open('saveFile.txt' , 'r') as file:
                            lines = file.readlines()
                            if len(lines) > 1:
                                # Safer alternative for next(file)
                                for line in lines[1:]:
                                    if line.isspace():
                                        continue
                                    data = line.split('|')
                                    try:
                                        ScheduleProjectsList.append(dict(ID=data[0].strip(), NAME=data[1].strip(), SIZE=data[2].strip(), PRIORITY=data[3].strip(), STATUS=data[4].strip()))
                                    except IndexError:
                                        continue
                            """Basically just sorts the Queue based on the contents of the sub content of ScheduleProjectsList by considering
                            both PRIORITY and SIZE values in ascending order"""
                            ScheduleProjectsList.sort(key= lambda project : (project['PRIORITY'], project['SIZE']))
                            print(ScheduleProjectsList)
                    except FileNotFoundError:
                        print("Error: 'saveFile.txt' not found.")
                        
                case 'b':
                    """Same as Create Schedule but for Reading only. If the ScheduleProjectsList is empty, It'll create the queue, else it'll just read what's inside ScheduleProjectsList"""
                    if not ScheduleProjectsList:
                        print("Error: The schedule has not been created yet. Please select [a] Create Schedule first.\n")
                    else:
                        print(f"{'PROJECTID':<15} | {'PROJECTNAME':<20} | {'PROJECTSIZE':<15} | {'PROJECTPRIORITY':<20} | {'PROJECTSTATUS':<15}")
                        for data in ScheduleProjectsList:
                            print(f"{data['ID']:<15} | {data['NAME']:<20} | {data['SIZE']:<15} | {data['PRIORITY']:<20} | {data['STATUS']:<15}")
                        print()    
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
                
                try:
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
                except FileNotFoundError:
                    print("Error: File missing during queue update.")
                except Exception as e:
                    print(f"An error occurred while updating the queue: {e}")
        case 5:
            print("Exiting System. Goodbye!")
            break
