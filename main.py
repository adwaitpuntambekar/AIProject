import time
import pygame
import math
import tkinter as tk
from tkinter import messagebox
import random

visitedPaths = ""
finalPath = []
level = 0
source_state = ""


class Romania:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Romania Map Traversal")
        self.root.geometry("300x200")
        self.traversal_label = tk.Label(self.root, text="Type of Traversal:")
        self.traversal_entry = tk.Entry(self.root)
        self.source_label = tk.Label(self.root, text="Enter Source:")
        self.source_entry = tk.Entry(self.root)
        self.dest_label = tk.Label(self.root, text="Enter Destination:")
        self.dest_entry = tk.Entry(self.root)
        self.submit_button = tk.Button(
            self.root, text="Submit", command=self.process_input)

        self.traversal_label.grid(row=0, column=0)
        self.traversal_entry.grid(row=0, column=1)
        self.source_label.grid(row=1, column=0)
        self.source_entry.grid(row=1, column=1)
        self.dest_label.grid(row=2, column=0)
        self.dest_entry.grid(row=2, column=1)
        self.submit_button.grid(row=3, columnspan=2)

        self.root.mainloop()

    def process_input(self):
        traversal_type = self.traversal_entry.get()
        source = self.source_entry.get()
        destination = self.dest_entry.get()

        if traversal_type.lower() == 'idfs':
            self.run_idfs(source, destination)
        else:
            messagebox.showerror("Enter Valid Traversal Type")

    def run_idfs(self, source, destination):
        self.root.destroy()

        pygame.init()
        width = 1000 + 300
        height = 694
        self.gameDisplay = pygame.display.set_mode((width, height))
        self.image = pygame.image.load('ro-04.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        pygame.display.set_caption("Romania IDDFS")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.msg_source = self.font.render('Source: ', True, (0, 0, 255))
        self.msg_destination = self.font.render(
            'Destination: ', True, (0, 0, 255))
        self.msg_depth = self.font.render('Depth: ', True, (255, 0, 0))
        self.font1 = pygame.font.SysFont(None, 25)
        self.button_msg = self.font1.render(
            'Increase Depth', True, (255, 255, 255))
        pygame.display.set_caption("Romania IDDFS")

        depth = 0
        self.gameDisplay.fill((255, 255, 255))
        self.gameDisplay.blit(self.image, [0, 0])
        pygame.display.update()

        self.locations = {'Sighetu Marmatiei': (393, 54), 'Satu Mare': (287, 73), 'Baia Mare': (362, 93),
                          'Oradea': (194, 186), 'Zalau': (308, 165), 'Cluj-Napoca': (365, 226), 'Bistrita': (452, 171),
                          'Radauti': (593, 68), 'Suceava': (631, 95), 'Botosani': (670, 83), 'Vatra Dornei': (538, 142),
                          'Iasi': (765, 167), 'Piatra Neamt': (641, 202), 'Turda': (382, 257),
                          'Targu Mures': (457, 259),
                          'Arad': (134, 311), 'Bacau': (695, 255), 'Vaslui': (775, 243), 'Timisoara': (122, 373),
                          'Deva': (295, 357), 'Alba lulia': (360, 328), 'Sighisoara': (483, 306), 'Onesti': (681, 298),
                          'Barlad': (770, 305), 'Resita': (190, 437), 'Hunedoara': (293, 372), 'Sibiu': (415, 367),
                          'Sfantu Gheorghe': (582, 356), 'Focsani': (721, 381), 'Galati': (804, 419),
                          'Targu Jiu': (329, 476),
                          'Ramnicu Valcea': (440, 465), 'Sinaia': (559, 433), 'Braila': (799, 442),
                          'Drobeta-Turnu Severin': (269, 531),
                          'Pitesti': (490, 499), 'Targoviste': (548, 493), 'Ploiesti': (604, 490), 'Buzau': (684, 460),
                          'Craiova': (381, 573), 'Slatina': (440, 560), 'Bucharest': (613, 561), 'Calarasi': (734, 592),
                          'Constanta': (866, 599), 'Mangalia': (860, 646), 'Eforie Nord': (866, 612),
                          'Tulcea': (883, 457)
                          }

        self.connected_cities = {'Sighetu Marmatiei': ['Baia Mare'],
                                 'Baia Mare': ['Sighetu Marmatiei', 'Satu Mare', 'Bist        rita', 'Cluj-Napoca'],
                                 'Satu Mare': ['Zalau', 'Baia Mare', 'Oradea'], 'Zalau': ['Satu Mare', 'Cluj-Napoca'],
                                 'Bistrita': ['Baia Mare', 'Vatra Dornei', 'Targu Mures'],
                                 'Cluj-Napoca': ['Baia Mare', 'Zalau', 'Turda'],
                                 'Oradea': ['Arad', 'Satu Mare', 'Turda', 'Deva'],
                                 'Arad': ['Oradea', 'Deva', 'Timisoara'],
                                 'Turda': ['Oradea', 'Cluj-Napoca', 'Alba lulia', 'Targu Mures'],
                                 'Deva': ['Oradea', 'Arad', 'Timisoara', 'Hunedoara', 'Alba lulia'],
                                 'Vatra Dornei': ['Bistrita', 'Suceava'],
                                 'Targu Mures': ['Bistrita', 'Turda', 'Sighisoara'], 'Radauti': ['Suceava'],
                                 'Suceava': ['Radauti', 'Botosani', 'Piatra Neamt', 'Vatra Dornei'],
                                 'Botosani': ['Suceava', 'Iasi'], 'Piatra Neamt': ['Suceava', 'Bacau'],
                                 'Iasi': ['Botosani', 'Vaslui', 'Bacau'], 'Vaslui': ['Iasi', 'Bacau', 'Barlad'],
                                 'Bacau': ['Iasi', 'Piatra Neamt', 'Onesti', 'Vaslui', 'Focsani'],
                                 'Alba lulia': ['Turda', 'Deva', 'Sibiu'], 'Sighisoara': ['Targu Mures'],
                                 'Timisoara': ['Arad', 'Resita', 'Deva', 'Drobeta-Turnu Severin'],
                                 'Onesti': ['Bacau', 'Sfantu Gheorghe'], 'Focsani': ['Bacau', 'Barlad', 'Buzau'],
                                 'Barlad': ['Vaslui', 'Focsani'], 'Resita': ['Timisoara'],
                                 'Drobeta-Turnu Severin': ['Timisoara', 'Craiova'], 'Hunedoara': ['Deva', 'Targu Jiu'],
                                 'Sibiu': ['Alba lulia', 'Ramnicu Valcea'], 'Sfantu Gheorghe': ['Onesti'],
                                 'Targu Jiu': ['Hunedoara', 'Craiova'], 'Ramnicu Valcea': ['Sibiu', 'Pitesti'],
                                 'Buzau': ['Focsani', 'Braila', 'Ploiesti', 'Bucharest'], 'Galati': ['Braila'],
                                 'Braila': ['Galati', 'Buzau', 'Tulcea', 'Calarasi'], 'Tulcea': ['Braila', 'Constanta'],
                                 'Calarasi': ['Braila', 'Bucharest', 'Constanta'],
                                 'Pitesti': ['Ramnicu Valcea', 'Slatina', 'Bucharest'],
                                 'Slatina': ['Pitesti', 'Craiova'],
                                 'Ploiesti': ['Sinaia', 'Targoviste', 'Buzau', 'Bucharest'], 'Sinaia': ['Ploiesti'],
                                 'Targoviste': ['Ploiesti'],
                                 'Craiova': ['Targu Jiu', 'Drobeta-Turnu Severin', 'Slatina', 'Bucharest'],
                                 'Bucharest': ['Buzau', 'Pitesti', 'Ploiesti', 'Craiova', 'Calarasi', 'Constanta',
                                               'Eforie Nord'],
                                 'Constanta': ['Calarasi', 'Bucharest', 'Mangalia', 'Tulcea'],
                                 'Mangalia': ['Constanta', 'Eforie Nord'], 'Eforie Nord': ['Bucharest', 'Mangalia']}

        self.draw_nodes()

        depth = 0

        source_x, source_y = self.locations.get(source, (0, 0))
        desti_x, desti_y = self.locations.get(destination, (0, 0))

        print("Source Coordinates:", source_x, source_y)
        print("Destination Coordinates:", desti_x, desti_y)

        self.msg_source = self.font.render(
            'Source: ' + str(source), True, (0, 0, 255))
        self.msg_destination = self.font.render(
            'Destination: ' + str(destination), True, (0, 0, 255))

        self.button = pygame.Rect(1050, 300, 200, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.button.collidepoint(x, y):
                        depth += 1
                        self.msg_depth = self.font.render(
                            'Depth: ' + str(depth), True, (0, 0, 0))
                        self.iterativeDFS(source, destination,
                                          depth, self.connected_cities)

            self.gameDisplay.blit(self.msg_source, [1020, 20])
            self.gameDisplay.blit(self.msg_destination, [1020, 45])
            self.gameDisplay.blit(self.msg_depth, [1020, 70])
            pygame.draw.rect(self.gameDisplay, [
                31, 7, 8], self.button)
            self.gameDisplay.blit(self.button_msg, [1090, 315])
            pygame.display.update()
            self.clock.tick(30)

    def draw_nodes(self):
        taken_coordinates = set()
        for city in self.locations.keys():
            while True:
                x = random.randint(50, 950)
                y = random.randint(50, 644)
                if (x, y) not in taken_coordinates:
                    taken_coordinates.add((x, y))
                    break

            for city, (x, y) in self.locations.items():
                pygame.draw.circle(
                    self.gameDisplay, (0, 0, 0), (x, y), 12)
                text_surface = self.font.render(city, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x, y + 20))
                self.gameDisplay.blit(text_surface, text_rect)

    def iterativeDFS(self, source, destination, maxDepth, edges):

        countOfIterarion = 0
        global level, visitedPaths, source_state
        source_state = source

        if source not in edges.keys() or destination not in edges.keys():
            finalPath.append('FAIL')

        for limit in range(maxDepth):
            global arr
            arr = []
            level = limit
            var = self.depthLimitSearch(
                source, destination, limit, edges, source)

            if var:
                countOfIterarion += 1
                finalPath.append(source_state)
                finalPath.reverse()
                self.display_message_box()
                return
        finalPath.append("FAIL")

    def depthLimitSearch(self, source, destination, limit, edges, parent):
        global level, visitedPaths, source_state, finalPath

        if (level - limit) <= 0:
            visitedPaths += '\n' + source

            if (parent != source):
                print(parent + " --- " + source)
                pygame.draw.line(self.gameDisplay, (255, 0, 0),
                                 self.locations[parent], self.locations[source], 4)
                pygame.display.update()
        else:
            visitedPaths += ('\n' + '\t' * (level - limit)) + source
            print(parent + " -- " + source)
            pygame.draw.line(self.gameDisplay, (255, 0, 0),
                             self.locations[parent], self.locations[source], 4)
            pygame.display.update()

        if source == destination:
            return True

        if limit < 1:
            return False

        temp = []

        for adjacentNode in edges[source]:
            temp = edges[adjacentNode]
            if source in temp:
                temp.remove(source)
                edges[adjacentNode] = temp
            time.sleep(0.05)
            if self.depthLimitSearch(adjacentNode, destination, limit - 1, edges, source):
                finalPath.append(adjacentNode)
                return True

        return False

    def display_message_box(self):
        messagebox.showinfo("Target found!")
        self.button_clicked = True


r = Romania()
