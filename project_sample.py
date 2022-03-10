import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '169.254.140.78' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 315 # enter the value in degrees for the identification tower 
tall_tower_angle = 270 # enter the value in degrees for the classification tower
drop_tube_angle = 315#270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = 0 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.16 # offset in meters
bin1_color = [0.6,0,0] # e.g. [1,0,0] for red
bin2_offset = 0.16
bin2_color = [0,1,0]
bin3_offset = 0.16
bin3_color = [0,0,1]
bin4_offset = 0.16
bin4_color = [0.2,0.2,0.2]

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
######################################################
#Container Dispensing Function By: Aum Shah MacID: shaha124
######################################################
def containerDispense(): #This function spawns in a random container with a id from 1 to 6
    randContainer = random.randint(1,6)#It chooses a random number between 1 to 6
    print("id:", randContainer)#It prints out the id of the container dispensed
    table.dispense_container(randContainer)#Dispenses a random container
######################################################
#Container Identification Function By: Aum Shah MacID: shaha124
######################################################
def containerProperties(): #This function determines the properties of the containers that are dispensed 
    
    time.sleep(1)
    table.rotate_table_angle(45)
    time.sleep(1)
    containerprop = []
    checkcontainer = table.photoelectric_sensor(0.2) #This sensor is used to give a value, which helps identify the container type
    checkcontainer2 = table.inductive_sensor(0.2) #This sensor is used to give a value, which helps identify the container type

    if (checkcontainer[0] < 1 and checkcontainer2[0] < 1): #These if statement checks both sensor values if they meet the conditions then it is identified as that type of container
        print("white, plastic container")
        containerprop.append("White")
    elif (checkcontainer[0] > 4 and checkcontainer2[0] > 4):
        print("red, metal container")
        containerprop.append("Red")
    else:
        print("blue, paper container")
        containerprop.append("Blue")
        
    chkCondition = table.load_cell_sensor(0.2) #This sensor helps to determine the weight of the containers
    containerprop.append(chkCondition)
    print(chkCondition)

    if (containerprop[0] == "White" and chkCondition[0] < 10): #These if statements check the value given by the sensor to given values of the containers, if they meet the conditions, it will identify as clean or dirty container
        print("clean white bottle")
        containerprop.append("Clean")
    elif (containerprop[0] == "Red" and chkCondition[0] < 16):
        print("clean red can")
        containerprop.append("Clean")
    elif (containerprop[0] == "Blue" and chkCondition[0] < 11):
        print("clean blue bottle")
        containerprop.append("Clean")
    elif (containerprop[0] == "White" and chkCondition[0] > 10):
        print("dirty white bottle")
        containerprop.append("Dirty")
    elif (containerprop[0] == "Red" and chkCondition[0] > 16):
        print("dirty red can")
        containerprop.append("Dirty")
    else:
        print("dirty blue bottle")
        containerprop.append("Dirty")


    if (containerprop[0] == "White" and containerprop[2] == "Clean"): #This compares the properties of the container to determine the bin they go in
        print("Bin03")
        containerprop.append("3")
    elif (containerprop[0] == "Red" and containerprop[2] == "Clean"):
        print("Bin01")
        containerprop.append("1")
    elif (containerprop[0] == "Red" and containerprop[2] == "Dirty"):
        print("Bin01")
        containerprop.append("1")
    elif (containerprop[0] == "Blue" and containerprop[2] == "Clean"):
        print("Bin02")
        containerprop.append("2")
    else:
        print("Bin04")
        containerprop.append("4")

    print(containerprop)
    table.rotate_table_angle(90)

    return containerprop
######################################################
#Container Pickup function By: Aum Shah MacID: shaha124
######################################################
def pickupContainer(): #These statements use the arm.move command to move the Q-Arm to the specific co-ordinates to pickup the container
    arm.move_arm(0.643, 0.022, 0.237)
    time.sleep(1)    
    arm.control_gripper(40)
    time.sleep(1)

def dropoffLeft(): #These statements use the arm.move command to move the Q-Arm to the specific co-ordinates to dropoff the container on the leftmost side of the hopper
    pickupContainer()
    time.sleep(1)
    arm.move_arm(0.02, -0.46, 0.59)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)
def dropoffMiddle(): #These statements use the arm.move command to move the Q-Arm to the specific co-ordinates to dropoff the container on the middle side of the hopper
    pickupContainer()
    time.sleep(1)
    arm.move_arm(0.02, -0.52, 0.59)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

def dropoffRight(): #These statements use the arm.move command to move the Q-Arm to the specific co-ordinates to dropoff the container on the rightmost side of the hopper
    pickupContainer()
    time.sleep(1)
    arm.move_arm(0.02, -0.59, 0.59)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_shoulder(-40)
    time.sleep(1)
    arm.home()
    time.sleep(1)

######################################################
#Line Following Function By: Aum Shah MacID: shaha124
######################################################
def line_follow(): #This is the function for the Q-Bot to travel around using IR sensors to stay on the line while traveling 

    left_IR, right_IR = bot.line_following_sensors() #This records the values of the sensors in the two variables one for the left side and on e for the right side

    if bot.line_following_sensors() == [1,1]: #This if statement is for when the both IR sensors are reading the same value, meaning the bot is goin straight
        bot.set_wheel_speed([0.1,0.1])
        time.sleep(0.1)

    elif left_IR == 1 and right_IR == 0: #This if statement is for when the bot is not going straight and the right IR sensor is not detecting the line, therefore it will correct for it by turning
        bot.set_wheel_speed([0.02, 0.04])

    elif left_IR == 0 and right_IR == 1: #This if statement is for when the bot is not going straight and the left IR sensor is not detecting the line, therefore it will correct for it by turning
        bot.set_wheel_speed([0.04, 0.02])

    else:
        bot.stop
######################################################
#Transfer Container Function By: Aum Shah MacID: shaha124
######################################################
RED01 = [0.6,0,0] #These are the colours of the various bins
GREEN02 = [0,1,0] 
BLUE03 = [0,0,1] 
GREY04 = [0.2,0.2,0.2] 
bot.activate_color_sensor() #Activates the colour sensors

def transfer_container(color): #This functions uses the line following and deposit function, and other bot commands to move the bot to the specified bin to deposit the container

    while True:
        line_follow() #Calls the line following function and the bot starts to move
        color_reading = bot.read_color_sensor()[0] #This function gives the sensor values of the colour sensors, and only gives the 1st rgb value in the list
        
        if  color_reading == RED01 and color == RED01: #This compares the colour of the sensor reading to the colour of inputted in to the function, if it meets the conditions it moves the bot to the container
            line_follow()
            print("Found color", color_reading)
            time.sleep(3.2)
            bot.stop()
            print("move again")
            bot.set_wheel_speed([0.2,0.2]) 
            time.sleep(1)
            bot.stop()
            time.sleep(0.5)
            bot.rotate(11)
            time.sleep(0.5)
            bot.rotate(-94)
            time.sleep(0.5)
            bot.travel_forward(0.125)
            time.sleep(0.5)
            bot.rotate(98)
            time.sleep(0.5)
            deposit_container() #This calls the deposit function to deposit the container
            break

        elif color_reading == GREEN02 and color == GREEN02: #This compares the colour of the sensor reading to the colour of inputted in to the function, if it meets the conditions it moves the bot to the container
            line_follow()
            print("Found color", color_reading)
            time.sleep(3.14)
            bot.stop()
            print("move again")
            bot.set_wheel_speed([0.15,0.15])
            time.sleep(1)
            bot.stop()
            deposit_container()
            break 

        elif  color_reading == BLUE03 and color == BLUE03: #This compares the colour of the sensor reading to the colour of inputted in to the function, if it meets the conditions it moves the bot to the container
            line_follow()
            print("Found color", color_reading)
            bot.stop()
            print("move again")
            bot.forward_distance(0.35)
            bot.rotate(25)
            time.sleep(1)
            bot.stop()
            deposit_container()
            break
        
        elif color_reading == GREY04 and color == GREY04: #This compares the colour of the sensor reading to the colour of inputted in to the function, if it meets the conditions it moves the bot to the container
            line_follow()
            print("Found color", color_reading)
            time.sleep(3.14)
            bot.stop()
            print("move again")
            bot.set_wheel_speed([0.15,0.15])
            time.sleep(1)
            bot.stop()
            deposit_container()
            break
  
######################################################
#Deposit Container Function By: Aum Shah MacID: shaha124
######################################################
def deposit_container(): #This function deposits the contianer in the hopper slowly into the bin
    hopper_angle = 1
    bot.activate_linear_actuator()
    time.sleep(0.1)

    while hopper_angle <= 90: #This while loop increases the angle by 10 degrees everytime till the hopper angle hits 90 deg
        bot.rotate_hopper(hopper_angle)
        time.sleep(0.5)
        hopper_angle += 10

    time.sleep(2)
    bot.rotate_hopper(0) #Returns the hopper to its original position again
    bot.deactivate_linear_actuator()
######################################################
#Return Home Function By: Aum Shah MacID: shaha124
######################################################
def currentPos(): #This function check the position of the bot using the bot.position command 
    home = (1.5,0,0)
    currentLocation = bot.position()
    
    for i in range (3): #This loops it 3 times to check the x,y,z values
        if abs(currentLocation[i] - home[i]) > 0.04:#This checks if the absoulte value of the current location subtract the home position and checks if the difference is greater than 0.4, if it is it returns false
            return False
    return True

def return_home(): #This function returns the Q-Bot to the inital starting position
    go_Home = currentPos() #This calls the currentpos function 
    while go_Home == False: #If the currentpos function returns false it will continue to move till it returns true then it breaks the while loop
        line_follow()
        go_Home = currentPos()
        if go_Home == True:
            bot.stop()
            break
######################################################
#Main Function By: Aum Shah MacID: shaha124
######################################################
def main(): # This is the main function that combines all the functions in the code and helps run multiple cycles

    remaining_container = False #This is a vraible to help identify if there are any container on the table
    lastContainer = []
    while True: #This is an infinte while loop so the bot will do an infinte amount of cycles

        loadContainer = []
        weight = 0
        tableweight = 0

        if (remaining_container == False): #If there are no containers on the table, then it will execute the following lines below
            
            containerDispense() #This dispenses the container
            dispensedContainer = containerProperties() #This takes the container properties given by the Container properties function and assigns it to a variable

            if (dispensedContainer[3] == "1"): #It checks the fourth index, which is the bin ID and if it meets the condtions then it will execute the following lines below
                dropoffRight()
                loadContainer.append(dispensedContainer[3]) #Appends the bin# to the current container variable
                weight += dispensedContainer[1][0] #This adds the weight of the container to the variable
                loadContainer.append(RED01) #This appends the destination of the bin the container is supposed to go to 
                
            
            elif (dispensedContainer[3] == "2"): #It checks the fourth index, which is the bin ID and if it meets the condtions then it will execute the following lines below
                dropoffRight()
                loadContainer.append(dispensedContainer[3])
                weight += dispensedContainer[1][0]
                loadContainer.append(GREEN02)
         
            elif (dispensedContainer[3] == "3"): #It checks the fourth index, which is the bin ID and if it meets the condtions then it will execute the following lines below
                dropoffRight()
                loadContainer.append(dispensedContainer[3])
                weight += dispensedContainer[1][0]
                loadContainer.append(BLUE03)
            
            else: #Else it will execute the following lines below
                dropoffRight()
                loadContainer.append(dispensedContainer[3])
                weight += dispensedContainer[1][0]
                loadContainer.append(GREY04)
                
        else: #If there is a container on the table then it will execute the lines below
            dropoffRight() #This will drop off the container on the right side of the hopper
            loadContainer.append(lastContainer[3]) #This will append the bin id to the loadContainer
            loadContainer.append(lastContainer[4]) #This will append the bin location in rgb form with three values
            weight += lastContainer[1][0] #This adds the weight of the container to the variable
            print(loadContainer)
            

        print(loadContainer)
        containerDispense()
      
        dispensedContainer = containerProperties()
        if (dispensedContainer[3] == loadContainer[0] and weight < 90): #This if statements checks to see, if the second container dispensed has the same bin number and the total weight is less the 90
            dropoffMiddle()#This will drop off the container on the middle of the hopper
            loadContainer.append(dispensedContainer[3])
            weight += dispensedContainer[1][0]
        else:
            lastContainer = dispensedContainer #This will take the container that didn't have the same bin# or if the weight exceeded 90, it will copy the properties to another variable that won't become empty again once the while loop iterates again
            if (lastContainer[3] == "1"):
                lastContainer.append(RED01)
            elif (lastContainer[3] == "2"):
                lastContainer.append(GREEN02)
            elif (lastContainer[3] == "3"):
                lastContainer.append(BLUE03)
            else:
                lastContainer.append(GREY04)
                      
            remaining_container = True #This will make the variable True since, there is a container left on the table
            transfer_container(loadContainer[1]) #Transfers the container to the bin destination decided earlier
            return_home() #Calls the return home function to let it return to the intial position
            continue #This starts the loop again from the beginning since the bot has returned home and it does not need to dispense another container
          
                    
        containerDispense()
        dispensedContainer = containerProperties()
        print(dispensedContainer)
        if (dispensedContainer[3] == loadContainer[0] and weight < 90): #This is for the third container and checks if has the same bin# and the total mass is less than 90
            dropoffLeft()
            loadContainer.append(dispensedContainer[3])
            weight += dispensedContainer[1][0]
            print(weight)
            transfer_container(loadContainer[1])
            return_home()
        else:
            lastContainer = dispensedContainer
            if (lastContainer[3] == "1"):
                lastContainer.append(RED01)
            elif (lastContainer[3] == "2"):
                lastContainer.append(GREEN02)
            elif (lastContainer[3] == "3"):
                lastContainer.append(BLUE03)
            else:
                lastContainer.append(GREY04)
            remaining_container = True
            print(weight)
            transfer_container(loadContainer[1])
            return_home()
            continue
   
            



main()

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
