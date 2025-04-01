import pygame
import numpy as np
import time
import tkinter as tk
import sys
import os

params = {
    "grid_x": 100,
    "grid_y": 100,
    "bg_color": "#000000",
    "colors": ["#FFFFFF", "#345345"], # -1, 1
}

def read_output_file(filename):
    data = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

        
        data['N'] = int(lines[0].split('=')[1])
        data['p'] = float(lines[1].split('=')[1])
        iteration = None
        matrix = []
        
        for line in lines[2:]:
            line = line.strip()
            
            if line.startswith("iteration="):
                if iteration is not None:
                    data[iteration] = {'consensus': consensus, 'matrix': matrix}
                
                iteration = int(line.split('=')[1])
                matrix = []  # Reset matrix for new iteration
            
            elif line.startswith("consensus="):
                consensus = float(line.split('=')[1])
                
            elif line.startswith("[[") or line.startswith("["):
                row = list(map(int, line.replace("[", "").replace("]", "").split()))
                matrix.append(row)
                
        if iteration is not None:
            data[iteration] = {'consensus': consensus, 'matrix': matrix}  # Store last iteration
        
    return data


def read_output_files():
    files = [f for f in os.listdir() if f.endswith('.txt')]

    data = {}
    for f in files:
        data[f] = read_output_file(f)
    
    return data

def help():
    popup = tk.Tk()
    popup.wm_title("Help")
    label = tk.Label(popup, text = '''
    Commands:
    - x: closes window
    - space: pauses/reloads game
    - h: opens help''')
    label.pack(side="top", padx=20, pady=10)
    button = tk.Button(popup, text="OK", command=popup.destroy)
    button.pack()
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width - popup.winfo_reqwidth()) / 2
    y = (screen_height - popup.winfo_reqheight()) / 2
    popup.geometry("+%d+%d" % (x, y))
    popup.mainloop()

def main():

    pygame.init()

    output_file = sys.argv[1]

    data = read_output_file(output_file)
    params["grid_x"] = data['N']
    params["grid_y"] = data['N']

    screen_info=pygame.display.Info()

    width, height = screen_info.current_w,screen_info.current_h
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

    bg = params["bg_color"]
    screen.fill(bg)
    nxC, nyC = data['N'], data['N']

    dimCW = width / nxC
    dimCH = height / nyC

    gameState = np.zeros((nxC, nyC))

    pauseExec = True # Could begin as false
    running = True

    iteration = 0
    title = f"Simulacion de Sistemas - Metropolis Montecarlo. Press SPACE to begin"

    pygame.display.set_caption(title)

    data.pop('N')
    data.pop('p')
    generations = list(data.keys())
    i = 0

    print("Generations: ", generations)

    while running:

        iteration = generations[i]
        print("Generation: ", iteration)

        time.sleep(0.05)
        newGameState = np.copy(gameState)

        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    running = False
                if event.key == pygame.K_SPACE:
                    pauseExec = not pauseExec
                if event.key == pygame.K_h:
                    help()

        if not pauseExec:
            newGameState = np.copy(data[iteration]['matrix']) 
            title = f"Iteration number: {iteration}"
        screen.fill(bg)
        for y in range(0, nyC):
            for x in range(0, nxC):
                pol = [ ((x)   * dimCW, (y)   * dimCH),
                        ((x+1) * dimCW, (y)   * dimCH),
                        ((x+1) * dimCW, (y+1) * dimCH),
                        ((x)   * dimCW, (y+1) * dimCH)]

                if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, (20, 20, 20), pol, width=1)
                else:
                    if newGameState[x, y] == 1:
                        color = params["colors"][0]
                    else:
                        color = params["colors"][1]
                    pygame.draw.polygon(screen, color, pol, width=0)

        pygame.display.set_caption(title)
        gameState = np.copy(newGameState)

        pygame.display.flip()
        #time.sleep(0.1)

        if not pauseExec:
            i += 1
            if i >= len(generations):  
                i = len(generations) - 1
                pauseExec = True  

if __name__ == "__main__":
	main()

