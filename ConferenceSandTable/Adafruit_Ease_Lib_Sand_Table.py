#made by mangochildren
import Adafruit_PCA9685
import random
from time import sleep 

HIGH = 4096
LOW = 0
red_port = 8
green_port = 1
blue_port = 2
current_color = [0, 0, 0]
next_color = [0, 0, 0]
    
color_options = [
      [216,158,229],
      [50,40,0],
      [20,50,60],
      [80,30,70],
      [60,0,20],
      [216,196,17]
   ]
class Adafruit_Ease_Lib():

    

    '''
    offests - if the servo limits are known to be different from the standards, provide the 
    new servo limits in this array. Defaults to noe
    '''
    def __init__(self,offsets = None):
        self.adafruit = Adafruit_PCA9685.PCA9685()
        self.num_pins = 16
        
        print('Adafruit initialized')


    def change_frequency(self, freq):
        self.adafruit.set_pwm_freq(freq)

    '''
    left -  period required for the servo to be at the minimum position/ 0 degrees
    center - period required to move to the center position/ 90 degrees
    right - period required to move to the maximum position/ 180 degrees
    '''
    

    def convert_freq_to_period(self, freq):
        return 1/freq

    def convert_period_to_freq(self, period):
        return 1/period

    '''
    FOR ALL THE FOLLOWING FUNCTIONS:
    
    *If pin is an array, the function will loop through the array of pins and perform the given task on all of them
    *If pin is a string that says 'all', the function will loop through all the pins and perform the given task on them
    *If pin is an int, the function will perform the given task on that specific pin.
    '''
    def set_high(self, pin):
        if pin == 'all':
            self.adafruit.set_all_pwm(HIGH, 0)
        elif isinstance(pin, list):
            for i in range(len(pin)):
                self.adafruit.set_pwm(i, HIGH, 0)
        else:
            self.adafruit.set_pwm(pin, HIGH, 0)

    def set_low(self, pin):
        if pin == 'all':
            self.adafruit.set_all_pwm(LOW, 0)
        elif isinstance(pin, list):
            for i in range(len(pin)):
                self.adafruit.set_pwm(i, LOW, 0)
        else:
            self.adafruit.set_pwm(pin, LOW, 0)

    '''
    percentage - On time percentage in the duty cycle. Use the change_percentage_servo() 
    function for servo movement
    '''
    def change_percentage(self, pin, percent):
        if percent >= 100:
            self.set_high(pin)
            return
        elif percent <= 0:
            self.set_low(pin)
            return
        percentage = int(4095 - (percent/100)*4095)
        if pin == 'all':
            self.adafruit.set_all_pwm(percentage, LOW)

        elif isinstance(pin, list):
            for i in range(len(pin)):
                self.adafruit.set_pwm(i, percentage, LOW)

        else:
            
            self.adafruit.set_pwm(pin, int(percentage), LOW)



    

    def set_color(self, red_percent, green_percent, blue_percent):
        global current_color
        global red_port 
        global green_port
        global blue_port 
        self.change_percentage(red_port, red_percent)
        self.change_percentage(green_port, green_percent)
        self.change_percentage(blue_port, blue_percent)
        current_color = [int(red_percent), int(green_percent), int(blue_percent)]


    def transition_color(self,red_percent, green_percent, blue_percent):
        global next_color
        global current_color
        global red_port 
        global green_port
        global blue_port 
        next_color = [red_percent, green_percent, blue_percent]
        change = []
        #print(next_color)
        #print(current_color)
        for i in range (3):
            if (next_color[i] - current_color[i] > 0):
                change.append(1)
            elif (next_color[i] - current_color[i] < 0):
                change.append(-1)
            else:
                change.append(0)
        #print(change)
        red_done = False
        green_done = False
        blue_done = False

        while (red_done == False or green_done == False or blue_done == False):

            if (red_done == False):
                current_color[0] += change[0]
                self.change_percentage(red_port, current_color[0])
                if (int(current_color[0]) == int(next_color[0])):
                    red_done =  True
                    #print('red done')

            if (green_done == False):
                current_color[1] += change[1]
                self.change_percentage(green_port, current_color[1])
                if (int(current_color[1])== int(next_color[1] )):
                    green_done = True
                    #print('green done')

            if (blue_done == False):
                current_color[2] += change[2]
                self.change_percentage(blue_port, current_color[2])
                if (int(current_color[2]) == int(next_color[2] )):
                    blue_done = True
                    #print('blue done')
        self.set_color(red_percent, green_percent, blue_percent)
        
    def run_lights(self):
        global color_options
        self.set_color(50,50,50)
        sleep(2)
        while True:
            choice = random.randint(0,len(color_options)-1)
            temp = color_options[choice]
            self.transition_color(temp[0], temp[1], temp[2])
            sleep(3)
            #print('done')
           
            
