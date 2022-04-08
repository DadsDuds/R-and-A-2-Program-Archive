# Marshall Sullivan
# ENGN4080 - Robotics & Automation II
# A4

import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image
from PIL import ImageTk
import os
import random

num_grids = 9  # This is a square

player_x = -1
player_y = -1

goal_x = -1
goal_y = -1

cnt = 0


class MyGUI:
    def __init__(self):

        self.goal_flag = False
        self.update_flag = False
        
        self.random_flag = False
        self.smarter_flag = False
        self.random_goal_flag = False
        self.random_non_flag = False

        self.master = tk.Tk()
        self.master.wm_title("ENGN4080 Navigation project")
        self.Width = 70
        grid = []
        path = os.getcwd() + "/images/"
        
        x = int(num_grids)
        (x, y) = (x, x)
        path = os.getcwd() + "/images/"
        self.wall_pic = ImageTk.PhotoImage(image=Image.open(path+'wall.png'))
        self.diamond_pic = ImageTk.PhotoImage(image=Image.open(path+'diamond.png'))
        self.robot_pic = ImageTk.PhotoImage(image=Image.open(path+'robot.png'))
        
        self.board = tk.Canvas(self.master, width=x*self.Width, height=y*self.Width)
        self.frame_button = tk.Frame(self.master)
        self.button_random = tk.Button(self.frame_button, text = "Random Moves", command = self.random_button)
        self.button_smarter = tk.Button(self.frame_button, text = "Smarter agent", command =self.smarter_button)
        self.button_random_goal = tk.Button(self.frame_button, text = "Random Goal Moves", command = self.random_goal_button)
        self.button_nondeterministic = tk.Button(self.frame_button, text = "Non deterministic world", command = self.nondetermin_button)
        
         #Create the grids   
        for i in range(9):
            for j in range(9):
                self.board.create_rectangle(
                    i*self.Width, j*self.Width, (i+1)*self.Width, (j+1)*self.Width, fill="white", width=1)
        
        self.board.pack(side=tk.LEFT)
        self.frame_button.pack(side = tk.LEFT)
        self.button_random.pack()
        self.button_smarter.pack()
        self.button_random_goal.pack()
        self.button_nondeterministic.pack()
        grid = [[0 for row in range(x)] for col in range(y)]
        self.item_grid = [[0 for row in grid[0]] for col in grid]

        self.master.after(10, self.task)
        self.master.mainloop()
        
    def task(self):
        self.update()
        self.master.after(100, self.task)
    
    def alert_popup1(self):
        global cnt
        tk.messagebox.showinfo("Message", "I made it to the goal in " + str(cnt) + " moves!")
    
    def alert_popup2(self):
        tk.messagebox.showinfo("Message", "Work smarter, not harder!")
    
    def alert_popup3(self):
        tk.messagebox.showinfo("Message", "Damn, that was annoying!")
    
    def alert_popup4(self):
        tk.messagebox.showinfo("Message", "Reality is often disappointing.")

    def random_button(self):
        global cnt
        self.random_flag = True
        self.smarter_flag = False
        self.random_goal_flag = False
        self.random_non_flag = False
        self.update_flag = True
        self.goal_flag = False
        self.ClearBoard()
        cnt = 0

    def smarter_button(self):
        global cnt
        self.random_flag = False
        self.smarter_flag = True
        self.random_goal_flag = False
        self.random_non_flag = False
        self.update_flag = True
        self.goal_flag = False
        self.ClearBoard()
        cnt = 0

        
    def random_goal_button(self):
        global cnt
        self.random_flag = False
        self.smarter_flag = False
        self.random_goal_flag = True
        self.random_non_flag = False
        self.update_flag = True
        self.goal_flag = False
        self.ClearBoard()
        cnt = 0

        
    def nondetermin_button(self):
        global cnt
        self.random_flag = False
        self.smarter_flag = False
        self.random_goal_flag = False
        self.random_non_flag = True
        self.update_flag = True
        self.goal_flag = False
        self.ClearBoard()
        cnt = 0


    def update(self):
        if self.random_flag == True:
            self.random_logic()
        elif self.smarter_flag == True:
            self.smarter_logic()
        elif self.random_goal_flag == True:
            self.random_goal_logic()
        elif self.random_non_flag == True:
            self.random_non_det_logic()
            

    def CheckGoal(self):
        global player_x, player_y, goal_x, goal_y
        if player_x == goal_x and player_y == goal_y and player_x is not None:
            self.goal_flag = True
            print("---------------")
            print("WE MADE IT!!!!!")
            print("---------------")
            
    # -- The robot moves in 4 random directions until it reaches the goal --
    def random_logic(self):
        global cnt, player_x, player_y, goal_x, goal_y
        if self.update_flag is True:
            self.PlaceStart(0, 0)
            self.PlaceEnd(5, 6)
            self.update_flag = False
            self.goal_flag = False
            
        my_list = [self.MoveDown, self.MoveUp, self.MoveRight, self.MoveLeft]
        random.choice(my_list)()
        self.CheckGoal()
        
        if self.goal_flag == True:
            self.random_flag = False
            self.alert_popup1()
      
     # -- Implements a smarter algorithm that involves comparing x,y coordinates --  
    def smarter_logic(self):
        global cnt, player_x, player_y, goal_x, goal_y
        if self.update_flag is True:
            self.PlaceStart(random.randrange(0, 9), random.randrange(0, 9))
            self.PlaceEnd(random.randrange(0, 9), random.randrange(0, 9))
            self.update_flag = False
            self.GetGoalPosition()
            self.GetMyPosition()
            
        self.whereamI()     # refer to line 411
        self.CheckGoal()
        
        if self.goal_flag == True:
            self.smarter_flag = False
            self.alert_popup2()
    
    # -- The previous algorithm but with a 25% chance of the goal changing positions --
    def random_goal_logic(self):
        global cnt, player_x, player_y, goal_x, goal_y
        chance = random.randint(0, 100)
        
        if self.update_flag is True:
            self.PlaceStart(random.randrange(0, 9), random.randrange(0, 9))
            self.PlaceEnd(random.randrange(0, 9), random.randrange(0, 9))
            self.update_flag = False
            self.GetGoalPosition()
            self.GetMyPosition()
            
        self.whereamI()     # refer to line 411
        self.CheckGoal()
        
        if chance <= 75:
            pass
        
        if chance <= 25:
            self.ChangeGoal(random.randrange(0, 9), random.randrange(0, 9))
            self.GetGoalPosition()
        
        if self.goal_flag == True:
            self.random_goal_flag = False
            self.alert_popup3()

    # -- Implements an algorithm that reflects a nondeterministic world affecting both the robot & goal --
    def random_non_det_logic(self):
        global cnt, player_x, player_y, goal_x, goal_y
        
        g_Chance = random.randint(0, 100)
        p_Chance = random.randint(0, 100)
        
        if self.update_flag is True:
            self.PlaceStart(random.randrange(0, 9), random.randrange(0, 9))
            self.PlaceEnd(random.randrange(0, 9), random.randrange(0, 9))
            self.update_flag = False
            
        self.CheckGoal()
        
        a = self.GetMyPosition()
        b = self.GetGoalPosition()
        
        if a[0] > b[0]:     ## player goes to the left
            if p_Chance <= 85:
                self.MoveLeft()
                
            elif p_Chance <= 86 and 90:
                self.MoveRight()
                print(" ** 5% RIGHT ** ")
                
            elif p_Chance <= 91 and 95:
                self.MoveUp()
                print(" ** 5% UP ** ")
                
            elif p_Chance <= 96 and 100:
                self.MoveDown()
                print(" ** 5% DOWN ** ")
        
        if a[0] < b[0]:     ## player goes to the right
            if p_Chance <= 85:
                self.MoveRight()
                
            elif p_Chance <= 86 and 90:
                self.MoveLeft()
                print(" ** 5% LEFT ** ")
                
            elif p_Chance <= 91 and 95:
                self.MoveUp()
                print(" ** 5% UP ** ")
                
            elif p_Chance <= 96 and 100:
                self.MoveDown()
                print(" ** 5% DOWN ** ")
                
        
        if a[1] > b[1]:     ## player goes upward
            if p_Chance <= 85:
                self.MoveUp()
                
            elif p_Chance <= 86 and 90:
                self.MoveLeft()
                print(" ** 5% LEFT ** ")
                
            elif p_Chance <= 91 and 95:
                self.MoveRight()
                print(" ** 5% RIGHT ** ")
                
            elif p_Chance <= 96 and 100:
                self.MoveDown()
                print(" ** 5% DOWN ** ")
                
        
        if a[1] < b[1]:     ## player goes down
            if p_Chance <= 85:
                self.MoveDown()
                
            elif p_Chance <= 86 and 90:
                self.MoveLeft()
                print(" ** 5% LEFT ** ")
                
            elif p_Chance <= 91 and 95:
                self.MoveUp()
                print(" ** 5% UP ** ")
                
            elif p_Chance <= 96 and 100:
                self.MoveRight() 
                print(" ** 5% RIGHT ** ")
                        
        if g_Chance <= 75:
            pass
        
        if g_Chance <= 25:
            self.ChangeGoal(random.randrange(0, 9), random.randrange(0, 9))
            self.GetGoalPosition()
        
        if self.goal_flag == True:
            self.random_non_flag = False
            self.alert_popup4()
        
        
#You probably do not want to change code under this point'''
    def PlaceStart(self,x,y):
        global player_x, player_y
        self.item_grid[y][x] = self.board.create_image(x*self.Width+35, y*self.Width+35, image=self.robot_pic)
        player_x = x
        player_y = y
        
    def PlaceEnd(self,x,y):
        global goal_x, goal_y
        self.item_grid[y][x] = self.board.create_image(x*self.Width+35, y*self.Width+35, image=self.diamond_pic)
        goal_x = x
        goal_y = y
        
    def ChangeGoal(self,x,y):
        global goal_x, goal_y
        self.board.delete(self.item_grid[goal_y][goal_x])
        self.item_grid[y][x] = self.board.create_image(x*self.Width+35, y*self.Width+35, image=self.diamond_pic)

        goal_x = x
        goal_y = y
        
        print(" ** Goal has changed positions. ** ")
       
        
    def MoveRight(self):
        global cnt, player_x, player_y, num_grids
        if player_x < num_grids - 1:
            print("Moving player right")
            self.goin_UP = False
            self.goin_DOWN = False
            self.goin_LEFT = False
            self.goin_RIGHT = True
            self.board.delete(self.item_grid[player_y][player_x])
            player_x += 1
            self.item_grid[player_y][player_x] = self.board.create_image(player_x*self.Width+35, player_y*self.Width+35, image=self.robot_pic)
            cnt += 1
            print(cnt)
    
    def MoveLeft(self):
        global cnt, player_x, player_y, num_grids
        if player_x > 0 :
            print("Moving player left")
            self.goin_UP = False
            self.goin_DOWN = False
            self.goin_LEFT = True
            self.goin_RIGHT = False
            self.board.delete(self.item_grid[player_y][player_x])
            player_x -= 1
            self.item_grid[player_y][player_x] = self.board.create_image(player_x*self.Width+35, player_y*self.Width+35, image=self.robot_pic)
            cnt += 1
            print(cnt)
    
    def MoveDown(self):
        global cnt, player_x, player_y, num_grids
        if player_y < num_grids -1 :
            print("Moving player down")
            self.goin_UP = False
            self.goin_DOWN = True
            self.goin_LEFT = False
            self.goin_RIGHT = False
            self.board.delete(self.item_grid[player_y][player_x])
            player_y += 1
            self.item_grid[player_y][player_x] = self.board.create_image(player_x*self.Width+35, player_y*self.Width+35, image=self.robot_pic)
            cnt += 1
            print(cnt)
    
    def MoveUp(self):
        global cnt, player_x, player_y, num_grids
        if player_y > 0:
            print("Moving player up")
            self.goin_UP = True
            self.goin_DOWN = False
            self.goin_LEFT = False
            self.goin_RIGHT = False
            self.board.delete(self.item_grid[player_y][player_x])
            player_y -= 1
            self.item_grid[player_y][player_x] = self.board.create_image(player_x*self.Width+35, player_y*self.Width+35, image=self.robot_pic)
            cnt += 1
            print(cnt)
   
    def ClearBoard(self):
        for i in range(9):
                for j in range(9):
                    self.board.create_rectangle(
                        i*self.Width, j*self.Width, (i+1)*self.Width, (j+1)*self.Width, fill="white", width=1)
                    self.item_grid[i][j] =0
            
        self.goal_flag = False
    
        
    def GetMyPosition(self):
        global player_x, player_y
        print("player coords: ", player_x, player_y)
        return (player_x, player_y)
    
    
    def GetGoalPosition(self):
        global goal_x, goal_y
        print("goal coords: ", goal_x, goal_y)
        return (goal_x, goal_y)
    
    ## -- This function compares the x,y coordinates of both the robot & goal --
    def whereamI(self):
        global player_x, player_y, goal_x, goal_y
        
        if player_x > goal_x:
            print("I need to go towards the left.")
            self.MoveLeft()
            
        elif player_x < goal_x:
            print("I need to go towards the right.")
            self.MoveRight()
            
        elif player_x == goal_x:
            print("I am in the correct x position.")
        
        if player_y > goal_y:
            print("I need to go upward.")
            self.MoveUp()
            
        elif player_y < goal_y:
            print("I need to go downward.")
            self.MoveDown()
            
        elif player_y == goal_y:
            print("I am in the correct y position.")
             

if __name__ == '__main__':
    my_gui = MyGUI()