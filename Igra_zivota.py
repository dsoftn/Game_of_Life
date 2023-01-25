import pygame
import json
import os
import datetime
import random
import copy
import csv
from pygameButton import Button


#------------------------------------------------------------------

class Cell_Map():
    SHOW_GRID = False      # prikazuje mrezu na sheet-u sa celijama
    CELL_WIDTH = 10     # sirina jedne celije
    CELL_HEIGHT = 10    # duzina jedne celije
    SHEET_WIDTH = 800   # sirina tabele u kojoj se nalaze celije
    SHEET_HEIGHT = 700  # duzina tabele
    NUMBER_OF_CELLS_X = round(SHEET_WIDTH/CELL_WIDTH)   # broj celija po horizontali
    NUMBER_OF_CELLS_Y = round(SHEET_HEIGHT/CELL_HEIGHT) # broj celija po vertikali
    NUMBER_OF_CELLS = NUMBER_OF_CELLS_X * NUMBER_OF_CELLS_Y     # ukupno celija
    GENERATIONS = 0                 # broj generacija / proracuna

    def __init__(self, display_surface, color_of_live_cells, color_of_grid):
        # ovde se pravi sheet, i poziva se random_fill da ubaci neke zive celije
        self.win = display_surface
        self.cell = []
        new_cell = []
        self.show_cell_color = color_of_live_cells   # boja zivih celija, bela
        self.show_grid_color = color_of_grid         # boja mreze
        self.cell_multicolor = False

        self.mouse_down = False
        self.total_number_of_living_cells = 0
        for x in range(1, self.NUMBER_OF_CELLS_X+1):
            for y in range(1, self.NUMBER_OF_CELLS_Y+1):
                new_cell = (x,y,0,0)
                self.cell.append(new_cell)
        self.random_fill(round(self.NUMBER_OF_CELLS/2))
        self.start_game = True
        self.btn_start = Button(self.win, (30, self.SHEET_HEIGHT+15),100,35,language("btn_start"), font_size = 28, disabled=True)
        self.btn_stop = Button(self.win, (30, self.SHEET_HEIGHT+60),100,35,language("btn_stop"), font_size = 28)
        self.btn_show_grid = Button(self.win, (160, self.SHEET_HEIGHT+15),160,35,language("show_grid"), font_size = 28)
        self.btn_multicolor = Button(self.win, (160, self.SHEET_HEIGHT+60),160,35,language("multicolor"), font_size = 28)
        self.btn_multicolor.btn_fg_color = BLACK
        self.btn_multicolor.btn_bg_color = self.show_cell_color
        self.btn_reset = Button(self.win, (350, self.SHEET_HEIGHT+15),100,80,language("reset"), font_size = 32)
        self.btn_clear = Button(self.win, (480, self.SHEET_HEIGHT+15),100,80,language("clear"), font_size = 32)



    def show_interface(self):
        pygame.draw.rect(self.win, (0,0,255), pygame.Rect((0, self.SHEET_HEIGHT, self.SHEET_WIDTH,self.SHEET_HEIGHT+100)))
        self.btn_start.draw_button()
        self.btn_stop.draw_button()
        self.btn_show_grid.draw_button()
        self.btn_multicolor.draw_button()
        self.btn_reset.draw_button()
        self.btn_clear.draw_button()

        pygame.draw.rect(self.win, (10,14,53), (610, self.SHEET_HEIGHT+15, 185, 35))
        pygame.draw.rect(self.win, (14,41,4), (610, self.SHEET_HEIGHT+60, 185, 35))
        generation_text = language("generation") + ": " + str(self.GENERATIONS)
        live_cells_text = language("live_cells") + ": " + str(self.total_number_of_living_cells)
        font = pygame.font.SysFont("comicms", 24)
        text = font.render(generation_text, 1, (255,255,255))
        x = 615
        y = round((35 - text.get_height())/2)
        if y<0: y=0
        y = self.SHEET_HEIGHT + 15 + y
        self.win.blit(text, (x,y))

        text = font.render(live_cells_text, 1, (255,255,255))
        x = 615
        y = round((35 - text.get_height())/2)
        if y<0: y=0
        y = self.SHEET_HEIGHT + 60 + y
        self.win.blit(text, (x,y))


    
    def draw_on_grid(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True

        if event.type == pygame.MOUSEMOTION and self.mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            # x_mouse = mouse_pos[0]
            # y_mouse = mouse_pos[1]
            x = round(mouse_pos[0]/self.CELL_WIDTH)
            y = round(mouse_pos[1]/self.CELL_HEIGHT)
            if x in range(2, round(self.SHEET_WIDTH/self.CELL_WIDTH)) and y in range(2, round(self.SHEET_HEIGHT/self.CELL_HEIGHT)):
                self.GENERATIONS = 0
                n = self.calculate_cell_id(x,y)
                self.cell[n] =(x,y,1,0)
                n = self.calculate_cell_id(x-1,y)
                self.cell[n] = (x-1,y,1,0)
                n = self.calculate_cell_id(x+1,y)
                self.cell[n] = (x+1,y,1,0)
                n = self.calculate_cell_id(x,y-1)
                self.cell[n] = (x,y-1,1,0)
                n = self.calculate_cell_id(x,y+1)
                self.cell[n] = (x,y+1,1,0)

                self.total_number_of_living_cells = 0
                if self.start_game == False:
                    for i in self.cell:
                        if int(i[2]) == 1:
                            self.total_number_of_living_cells += 1
                    self.show_interface


            self.show(self.win)
            




    def event_handler(self, event):
        self.draw_on_grid(event)
        self.btn_start.event_handler(event)
        if self.btn_start.btn_mouse_click:
            self.btn_Start_mouse_click()

        self.btn_stop.event_handler(event)
        if self.btn_stop.btn_mouse_click:
            self.btn_Stop_mouse_click()

        self.btn_show_grid.event_handler(event)
        if self.btn_show_grid.btn_mouse_click:
            self.btn_show_grid_mouse_click()

        self.btn_multicolor.event_handler(event)
        if self.btn_multicolor.btn_mouse_click:
            self.btn_multicolor_mouse_click()

        self.btn_reset.event_handler(event)
        if self.btn_reset.btn_mouse_click:
            self.btn_reset_mouse_click()

        self.btn_clear.event_handler(event)
        if self.btn_clear.btn_mouse_click:
            self.btn_clear_mouse_click()


        self.show_interface()

    def btn_clear_mouse_click(self):
        n=0
        for i in self.cell:
            self.cell[n] = (i[0], i[1], 0, 0)
            n +=1
        log ("Clear the screen." + "Generations: " + str(self.GENERATIONS) + ". Reset counter.")
        self.GENERATIONS = 0
        self.total_number_of_living_cells = 0
        self.show_interface



    def btn_reset_mouse_click(self):
        self.random_fill(round(self.NUMBER_OF_CELLS/2))
        log ("Game reset." + "Generations: " + str(self.GENERATIONS) + ". Reset counter.")
        self.GENERATIONS = 0
        

    def btn_multicolor_mouse_click(self):
        if self.cell_multicolor == True:
            self.cell_multicolor = False
            self.btn_multicolor.btn_caption = language("multicolor")
            self.btn_multicolor.btn_bg_color = self.show_cell_color
            log("Solid color.")
        else:
            self.cell_multicolor = True
            self.btn_multicolor.btn_caption = language("solid_color")
            self.btn_multicolor.btn_bg_color = (0,254,0)
            log("Multicolor.")

    def btn_show_grid_mouse_click(self):
        if self.SHOW_GRID == True:
            self.SHOW_GRID = False
            self.btn_show_grid.btn_caption = language("show_grid")
            log("Hide grid.")
        else:
            self.SHOW_GRID = True
            self.btn_show_grid.btn_caption = language("hide_grid")
            log("Show grid.")

    def btn_Start_mouse_click(self):
        self.start_game = True
        self.btn_start.btn_disabled = True
        self.btn_stop.btn_disabled = False
        log("Game started.")

    def btn_Stop_mouse_click(self):
        self.start_game = False
        self.btn_start.btn_disabled = False
        self.btn_stop.btn_disabled = True
        log("Game stoped.")


    def random_fill(self, number_of_cells):
        # ubacuje zive celije u sheet
        for i in range(1, number_of_cells+1):
            x = random.randint(1,self.NUMBER_OF_CELLS_X)
            y = random.randint(1,self.NUMBER_OF_CELLS_Y)
            self.cell[self.calculate_cell_id(x,y)] = [x,y,1,0]
        
    def update_map(self, display_win):
        if self.SHOW_GRID == True:
            self.draw_grid(display_win)
        
        self.show_interface()

        if self.start_game:
            self.calculate_life()
        
        self.show(display_win)

    def show(self, display_win):
        if self.SHOW_GRID == True:
            self.draw_grid(display_win)
        self.draw_cell(display_win, self.cell_multicolor)

    def draw_grid(self, win):
        y = self.CELL_WIDTH
        x = self.CELL_HEIGHT
        for i in range(1,self.NUMBER_OF_CELLS_X+1):
            pygame.draw.line(win, self.show_grid_color, (i*x,1), (i*x, self.SHEET_HEIGHT))
        for i in range(1, self.NUMBER_OF_CELLS_Y+1):
            pygame.draw.line(win, self.show_grid_color, (1, y*i), (self.SHEET_WIDTH, y*i))
        
    def draw_cell(self, win, random_color = False ):
        for i in self.cell:
            if int(i[2]) == 1:
                x1 = int(i[0]) * self.CELL_WIDTH - self.CELL_WIDTH
                y1 = int(i[1]) * self.CELL_HEIGHT - self.CELL_HEIGHT
                x2 = int(i[0]) * self.CELL_WIDTH
                y2 = int(i[1]) * self.CELL_HEIGHT
                rect = (x1,y1,x2,y2)
                x_mid = (x1+x2)/2
                y_mid = (y1+y2)/2
                if self.CELL_WIDTH != self.CELL_HEIGHT:
                    radius_kruga = min((self.CELL_WIDTH, self.CELL_HEIGHT))/2
                else:
                    radius_kruga = round(self.CELL_WIDTH/4)
                
                if radius_kruga < 1:
                    radius_kruga = 1
                
                if random_color == True:
                    color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                else:
                    color = self.show_cell_color

                #pygame.draw.rect(win, self.show_cell_color, rect)
                pygame.draw.circle(win, color, (x_mid, y_mid), radius_kruga)
        
    def calculate_life(self):
        self.GENERATIONS += 1
        live_cells = 0
        surrounding_cells = ()
        surrounding_cell_id = 0
        self.total_number_of_living_cells = 0
        cell_is_live = 0
        active_cell_ID = 0
        for j in self.cell:
            x = int(j[0])
            y = int(j[1])
            active_cell_ID = self.calculate_cell_id(x,y)
            surrounding_cells =(
                ((x-1), y),
                ((x+1), y),
                (x, (y-1)),
                (x, (y+1)),
                ((x-1), (y-1)),
                ((x+1), (y-1)),
                ((x+1), (y+1)),
                ((x-1), (y+1))
                )
            live_cells = 0
            for i in surrounding_cells:
                if int(i[0]) > 0 and int(i[0]) <= self.NUMBER_OF_CELLS_X and int(i[1]) > 0 and int(i[1]) <= self.NUMBER_OF_CELLS_Y:
                    surrounding_cell_id = self.calculate_cell_id(i[0], i[1])
                    cell_is_live = int(self.cell[surrounding_cell_id][2])
                    if cell_is_live == 1:
                        live_cells +=1
            
            if int(j[2]) == 0 and live_cells == 3:
                self.cell[active_cell_ID] = (x,y,0,1)
                self.total_number_of_living_cells +=1
            elif int(j[2]) == 1:
                if live_cells == 2 or live_cells == 3:
                    self.cell[active_cell_ID] = (x,y,1,1)
                    self.total_number_of_living_cells +=1
            else:
                self.cell[active_cell_ID] = (x, y, j[2], 0)
            
        a = 0
        n = 0
        for i in self.cell:
            a = int(i[3])
            self.cell[n] = (i[0], i[1], a, 0)
            n +=1

    def calculate_cell_id(self, x, y):
        cell_x = int(x)
        cell_y = int(y)
        cell_id = (cell_x-1)*self.NUMBER_OF_CELLS_Y + cell_y-1
        return cell_id

#----------------------------------------------------------------------

def language(key_name, language_choice = ""):
    # Ukoliko je funkcija pozvana sa argumentom language_choice onda menjam jezik u json fajlu
    # Ako je u language_choice prosledjeno "?" onda samo vracam koji je aktivni jezik trenutno
    # "language_name": ["English", "Srpski Latinica"], 
    # "language_active": ["english"], 
    return_info = ""
    try:        
        file = open (PATH+"languages.json", "r", encoding="UTF-8" )
        language_file = json.load(file)
        active_language = ""

        if language_choice == "?":
            return_info = language_file[key_name][0]
        elif language_choice != "":
            language_file[key_name] = language_choice
            return_info = language_file[key_name]
            log("Language changed / Jezik Promenjen: "+return_info)
        else:
            active_language = language_file["language_active"][0]
            active_language = active_language.split()
            active_language = int(active_language[0])
            return_info =  language_file[key_name][active_language]
        
        if  language_choice != "" and language_choice != "?":
            file = open (PATH+"languages.json", "w", encoding="UTF-8" )
            file = json.dump(language_file)
            file.close
        file.close
        return return_info

    except:
        file.close
        log("Error in languages.json file. / Greska u languages.json fajlu.")
        return ""

def log(text = "", delete_previous_entrys = False):
# Upisuje log.txt, posle svakog pokretanja programa, stari log se brise    
    open_mode = "a"
    if delete_previous_entrys == True:
        open_mode = "w"
    
    file = open(PATH+"log.txt", open_mode, encoding = "UTF-8")
    d, t = date_time()
    file.write(d+t+text+"\n")
    file.close

def date_time():
# Vraca sistemski datum i vreme respektivno
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = datetime.date.today()
    current_date = str(current_date) + " "
    current_time = str(current_time) + " "
    return current_date, current_time

def find_path():
# Pronalazi PATH do ove skripte 
    a = os.path.abspath(os.getcwd())
    c = r" \ "
    c = c.strip()
    a = a + c
    return a

#-------------------------------------------------------------------------

BLACK = (0,0,0)
GRID_COLOR = (64,64,64)
CELL_COLOR = (204,204,0)
FILL_COLOR = (0,0,0)
PATH = find_path()          # direktorijum potreban zbog dodatnih fajlova
current_date = ""           # danasnji datum
current_time = ""           # trenutno vreme
WINDOWS_SIZE = (800,800)    # dimenzije prozora

clock = pygame.time.Clock()     # sat omogucava kontrolu brzine igre

pygame.init()
current_date, current_time = date_time()
log ("*************************************************", delete_previous_entrys=True)
log ("Game of Life - log file /  Igra Zivota - log fajl\n\n")

win = pygame.display.set_mode(WINDOWS_SIZE)
pygame.display.set_caption(language("win_caption"))
game_surface = Cell_Map(win, CELL_COLOR, GRID_COLOR)

run = True
while run:
    clock.tick(60)
    win.fill(FILL_COLOR)
    for event in pygame.event.get():
        game_surface.event_handler(event)

        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
                
            print ("-----------------------------------------------------------")
            print ("Generacija:   ",game_surface.GENERATIONS)
            print ("Zivih celija: ",game_surface.total_number_of_living_cells)

    game_surface.update_map(win)
    
    pygame.display.update()

pygame.quit



