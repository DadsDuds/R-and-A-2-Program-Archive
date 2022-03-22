# Marshall Sullivan
# Assignment 3
# ENGN4080 - Robotics & Automation II

import tkinter as tk
import serial
import time


class ParkingTime:
    def __init__(self):

        self.main_win = tk.Tk()
        self.main_win.title('GUI')
        self.main_win.geometry("400x400")
        
        self.serial_arduino = self.initialize_serial()
        
        self.T_Layer = tk.Frame(self.main_win)
        self.M_Layer = tk.Frame(self.main_win)
        self.P_Layer = tk.Frame(self.main_win)
        self.B_Layer = tk.Frame(self.main_win)
        
        self.radio_var = tk.IntVar()
        self.radio_var.set(1)
        
        self.park_var = tk.IntVar()
        self.park_var.set(1)
        
        self.dialogue = tk.StringVar()
        self.dialogue.set('Initialized')
        
        self.status = tk.Label(self.T_Layer,
                               text = "Current state: ")
        
        self.placeholder = tk.Label(self.T_Layer,
                                    textvar = self.dialogue)
        
        self.top_div = tk.Label(self.M_Layer,
                                text = "------- MOVE OBJECTS --------")
        
        self.MoveO1 = tk.Radiobutton(self.M_Layer,
                                     text = "Move O1",
                                     variable = self.radio_var,
                                     value = 1)
        
        self.MoveO2 = tk.Radiobutton(self.M_Layer,
                                     text = "Move O2",
                                     variable = self.radio_var,
                                     value = 2)
        
        self.MoveO3 = tk.Radiobutton(self.M_Layer,
                                     text = "Move O3",
                                     variable = self.radio_var,
                                     value = 3)
        
        self.ConfirmButton = tk.Button(self.M_Layer,
                                       text = "Move selected object",
                                       command = self.confirmation)
        
        self.middle_div = tk.Label(self.P_Layer,
                                text = "------- PARK OBJECTS --------")
        
        self.Park1 = tk.Radiobutton(self.P_Layer,
                               text = "Park O1",
                               variable = self.park_var,
                               value = 1)
        
        self.Park2 = tk.Radiobutton(self.P_Layer,
                               text = "Park O2",
                               variable = self.park_var,
                               value = 2)
        
        self.Park3 = tk.Radiobutton(self.P_Layer,
                               text = "Park O3",
                               variable = self.park_var,
                               value = 3)
        
        self.ParkButton = tk.Button(self.P_Layer,
                                    text = "Park selected object",
                                    command = self.park_this)
        
        self.bottom_div = tk.Label(self.B_Layer,
                                text = "---------------")
        
        self.quitter = tk.Button(self.B_Layer,
                                text = "Quit",
                                command = self.i_quit)
        
        self.T_Layer.pack()
        self.M_Layer.pack()
        self.P_Layer.pack()
        self.B_Layer.pack()
        
        self.status.pack()
        self.placeholder.pack()
        
        self.top_div.pack()
        self.MoveO1.pack()
        self.MoveO2.pack()
        self.MoveO3.pack()
        self.ConfirmButton.pack()
        
        self.middle_div.pack()
        self.Park1.pack()
        self.Park2.pack()
        self.Park3.pack()
        self.ParkButton.pack()
        
        self.bottom_div.pack()
        self.quitter.pack()
             
        tk.mainloop()
    
    def initialize_serial(self):
        try:
            self.serial_arduino = serial.Serial("COM3", 115200, timeout = 2)
            time.sleep(10)
            self.serial_arduino.write('<i, 0, 0, 0, 0, 0, 0>'.encode())
            tmp = self.serial_arduino.readline().decode('utf-8')
            print("--------------")
            print(tmp)
            
            if tmp == "Ready!\r\n":
                print("Arduino is ready.")
                print("---------------")
                return self.serial_arduino
            
            else:
                return False
        
        except serial.serialutil.SerialException:
            print("---------------")
            print("SERIAL ERROR!")
            print("Check if the correct COM port is selected.")
            print("Make sure the baudrate matches on both the py and ino files.")
            print("Check parts of the python/arduino code for mistakes.")
            print("Try unplugging and plugging the arduino board to the laptop if all else fails.")
            print("---------------")

    def confirmation(self):
        if self.radio_var.get() == 1:

            print("O1 is being moved.")
            self.serial_arduino.write('<M_O1>'.encode())
            
            time.sleep(8)
            print("O1 is no longer in its parking spot.")
            self.dialogue.set("O1 has been moved")
        
        if self.radio_var.get() == 2:
            
            print("O2 is being moved.")
            self.serial_arduino.write('<M_O2>'.encode())
            
            time.sleep(8)
            print("O2 is no longer in its parking spot.")
            self.dialogue.set("O2 has been moved")

        if self.radio_var.get() == 3:
            
            print("O3 is being moved.")
            self.serial_arduino.write('<M_O3>'.encode())
                
            time.sleep(10)
            print("O1 has been parked.")
            self.dialogue.set("O3 has been moved")
    
    def park_this(self):
        if self.park_var.get() == 1:
        
            print("Parking O1!")
            self.serial_arduino.write('<P_O1>'.encode())
            
            time.sleep(8)
            print("O1 has been parked.")
            self.dialogue.set("O1 has been parked")
        
        if self.park_var.get() == 2:
                
            print("Parking O2!")
            self.serial_arduino.write('<P_O2>'.encode())
            
            time.sleep(8)
            print("O2 has been parked.")
            self.dialogue.set("O2 has been parked")

        if self.park_var.get() == 3:
                
            print("Parking O3!")
            self.serial_arduino.write('<P_O3>'.encode())
            
            time.sleep(10)    
            print("O3 has been parked.")
            self.dialogue.set("O3 has been parked")
    
    def i_quit(self):
        self.serial_arduino.close()
        print("Arduino port successfully closed.")
        self.main_win.destroy()

if __name__ == '__main__':
    my_gui = ParkingTime()        