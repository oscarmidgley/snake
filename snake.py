import random
import tkinter as tk

class GameUI:
    def __init__(self, master):

        self.master = master
        self.cellSize = 70
        self.size = 8
        self.grid = [[0] * self.size for x in range(self.size)]
        self.grid, self.leading, self.tail = self.createSnake()
        self.direction = [0, 1]
        self.directions = [[0, 1] for x in range (2)]
        self.running = False

        self.canvas = tk.Canvas(master, height = self.cellSize * self.size, width = self.cellSize * self.size)
        self.canvas.pack()

        self.drawGrid()

        self.button = tk.Button(master, text = "Play", justify = "center", width = 20, height = 10, padx = 10, pady = 10, command = self.toggle_running)
        self.button.pack(side=tk.LEFT)

        self.loseText = tk.Label(master, text = "You Lose", width = 20, height = 10, padx = 30)

        self.restartButton = tk.Button(master, text = "Restart", width = 20, height = 10, padx = 10, pady = 10, command = self.restart)

        self.master.bind("<KeyPress>", self.changeDirection)

    def drawGrid(self):

        direction = self.direction

        self.canvas.delete("all")

        for y in range(self.size):
            for x in range(self.size):
                x1 = x * self.cellSize
                x2 = x1 + self.cellSize
                y1 = y * self.cellSize
                y2 = y1 + self.cellSize

                if self.grid[y][x] == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline = "gray", fill = "white")
                elif self.grid[y][x] == 1:
                    if y == self.leading[0] and x == self.leading[1]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, outline = "gray", fill = "white")
                        self.canvas.create_rectangle(x1 if direction != [0, -1] else x1  + self.cellSize / 2, y1 if direction != [-1, 0] else y1 + self.cellSize / 2, x2 if direction != [0, 1] else x2 - self.cellSize / 2 , y2 if direction != [1, 0] else y2 - self.cellSize / 2, fill = "black")
                        self.canvas.create_oval(x1, y1, x2, y2, fill = "black")
                        self.canvas.create_oval(x1 + self.cellSize / 3, y1 + self.cellSize / 3, x2 - self.cellSize / 3 * 2, y2 - self.cellSize / 3, fill = "green")
                        self.canvas.create_oval(x1 + self.cellSize / 3 * 2, y1 + self.cellSize / 3, x2 - self.cellSize / 3, y2 - self.cellSize / 3, fill = "green")
                    else:
                        self.canvas.create_rectangle(x1, y1, x2, y2, outline = "black", fill = "black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline = "gray", fill = "white")
                    self.canvas.create_oval(x1 + self.cellSize / 10, y1 + self.cellSize / 10, x2 - self.cellSize / 10, y2 - self.cellSize / 10, outline = "red", fill = "red")
                

    def generateFruit(self):

        pos = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]

        while self.grid[pos[0]][pos[1]] != 0:
            pos = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]
        
        self.grid[pos[0]][pos[1]] = 2

        return self.grid

    def createSnake(self):

        mid = int(round(self.size / 2, 0)) - 1

        for x in range(3):
            self.grid[mid][mid - x] = 1
        
        self.leading = [mid, mid]
        self.tail = [mid, mid - 2]

        self.grid[self.leading[0]][self.leading[1] + 2] = 2
        
        return self.grid, self.leading, self.tail

    def end_game(self):
        self.loseText.pack()
        self.canvas.destroy()
        self.button.destroy()
        self.restartButton.pack()
    
    def restart(self):
        self.loseText.destroy()
        self.restartButton.destroy()
        game = GameUI(self.master)
    
    def changeDirection(self, event):
        if event.keysym == "w" and self.directions[len(self.directions) - 1] != [1, 0]:
            self.direction = [-1, 0]
        elif event.keysym == "s" and self.directions[len(self.directions) - 1] != [-1, 0]:
            self.direction = [1, 0]
        elif event.keysym == "a" and self.directions[len(self.directions) - 1] != [0, 1]:
            self.direction = [0, -1]
        elif event.keysym == "d" and self.directions[len(self.directions) - 1] != [0, -1]:
            self.direction = [0, 1]
        elif event.keysym == "Return":
            self.toggle_running()

    def nextState(self):

        direction = self.direction

        self.leading = [self.leading[0] + direction[0], self.leading[1] + direction[1]]

        if self.leading[0] > self.size - 1 or self.leading[1] > self.size - 1 or self.leading[0] < 0 or self.leading[1] < 0 or self.grid[self.leading[0]][self.leading[1]] == 1:
            self.grid[self.tail[0]][self.tail[1]] = 0
            self.drawGrid()
            self.end_game()
            pass
        else:
            if self.grid[self.leading[0]][self.leading[1]] != 2:
                self.grid[self.tail[0]][self.tail[1]] = 0
                self.tail[0] += self.directions[0][0]
                self.tail[1] += self.directions[0][1]
                self.directions.pop(0)
            else:
                self.grid[self.leading[0]][self.leading[1]] = 1
                self.grid = self.generateFruit()

            self.grid[self.leading[0]][self.leading[1]] = 1

            self.directions.append(direction)
        
    def toggle_running(self):

        self.running = not self.running

        if self.running:
            self.button.config(text="Stop")
            self.run()
        else:
            self.button.config(text="Play")

    def run(self):

        if self.running == True:
            self.nextState()
            self.drawGrid()
            self.master.after(300, self.run)

if __name__ == "__main__":

    root = tk.Tk(screenName = "Snake")
    root.title = "Snake"
    game = GameUI(root)
    root.mainloop()