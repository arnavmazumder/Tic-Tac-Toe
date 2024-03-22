import sys
import time
import pygame as pg
import pygame_gui as pgui


class GameGUI:
    def __init__(self):
        self.n = 3
        self.m = 3
        self.k = 3
        self.bot_level = 'EASY'
        self.bot_time_limit = 2.0

        pg.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.SCREEN = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption('K-in-a-row')
        self.CLOCK = pg.time.Clock()
        self.MANAGER = pgui.UIManager((self.WIDTH, self.HEIGHT))
        
    def main_menu(self):

        get_game_mode = pgui.elements.UIDropDownMenu(options_list=['Gamemode: Multiplayer', 'Gamemode: Singleplayer'], starting_option='Gamemode: Singleplayer', relative_rect=pg.Rect((100, 150), (225, 50)), manager=self.MANAGER)
        get_n = pgui.elements.UIDropDownMenu(options_list=['N: ' + str(i) for i in range(3, 11)], starting_option='N: 3', relative_rect=pg.Rect((350, 150), (100, 50)), manager=self.MANAGER)
        get_m = pgui.elements.UIDropDownMenu(options_list=['M: ' + str(i) for i in range(3, 11)], starting_option='M: 3', relative_rect=pg.Rect((475, 150), (100, 50)), manager=self.MANAGER)
        get_k = pgui.elements.UIDropDownMenu(options_list=['K: 3'], starting_option='K: 3', relative_rect=pg.Rect((600, 150), (100, 50)), manager=self.MANAGER)

        get_bot_level = pgui.elements.UIDropDownMenu(options_list=['Bot Level: Easy', 'Bot Level: Medium', 'Bot Level: Hard'], starting_option='Bot Level: Easy', relative_rect=pg.Rect((315, 250), (175, 50)), manager=self.MANAGER)
        

        while True:
            ref_rate = self.CLOCK.tick(60)/1000
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pgui.UI_DROP_DOWN_MENU_CHANGED and (event.ui_element==get_n or event.ui_element==get_m):
                    upper_bound = max(int(get_m.selected_option.split()[-1]), int(get_n.selected_option.split()[-1])) + 1
                    new_list = ['K: '+str(i) for i in range(3, upper_bound)]
                    curr_k = get_k.selected_option
                    if curr_k in new_list: start_opt = curr_k
                    else: start_opt = new_list[-1]
                    if get_k is not None: get_k.kill()
                    get_k = pgui.elements.UIDropDownMenu(options_list=new_list, starting_option=start_opt, relative_rect=pg.Rect((600, 150), (100, 50)), manager=self.MANAGER)

                if event.type ==pgui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element==get_game_mode:
                    if get_game_mode.selected_option=='Gamemode: Multiplayer':
                        if get_bot_level is not None: get_bot_level.kill()
                    else:
                       get_bot_level = pgui.elements.UIDropDownMenu(options_list=['Bot Level: Easy', 'Bot Level: Medium', 'Bot Level: Hard'], starting_option='Bot Level: Easy', relative_rect=pg.Rect((315, 250), (175, 50)), manager=self.MANAGER)
        


                self.MANAGER.process_events(event)

            self.MANAGER.update(ref_rate)
            self.SCREEN.fill((0, 0, 51))

            txt = pg.font.SysFont('comicsans', 30).render("Welcome to K-In-A-Row N by M Tic-Tac-Toe!", True, (255, 255, 255))
            self.SCREEN.blit(txt, (75, 10))

            txt = pg.font.SysFont('comicsans', 20).render("(Please select the options below)", True, (255, 255, 255))
            self.SCREEN.blit(txt, (240, 50))

            self.MANAGER.draw_ui(self.SCREEN)
            pg.display.update()
        



game = GameGUI()
game.main_menu()
    