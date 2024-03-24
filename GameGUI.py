import sys
import time
import pygame as pg
import pygame_gui as pgui
from BoardState import BoardState
from BotPlayer import Bot


class GameGUI:
    def __init__(self):
        self.n = 3
        self.m = 3
        self.k = 3
        self.bot_level = 'EASY'
        self.gamemode = 'Singleplayer'
        self.player_piece = 'X'

        pg.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.SCREEN = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption('K-in-a-row')
        self.CLOCK = pg.time.Clock()

        
    def main_menu(self):
        MANAGER = pgui.UIManager((self.WIDTH, self.HEIGHT))
        get_game_mode = pgui.elements.UIDropDownMenu(options_list=['Gamemode: Multiplayer', 'Gamemode: Singleplayer'], starting_option='Gamemode: Singleplayer', relative_rect=pg.Rect((100, 150), (225, 50)), manager=MANAGER)
        get_n = pgui.elements.UIDropDownMenu(options_list=['N: ' + str(i) for i in range(3, 11)], starting_option='N: 3', relative_rect=pg.Rect((350, 150), (100, 50)), manager=MANAGER)
        get_m = pgui.elements.UIDropDownMenu(options_list=['M: ' + str(i) for i in range(3, 11)], starting_option='M: 3', relative_rect=pg.Rect((475, 150), (100, 50)), manager=MANAGER)
        get_k = pgui.elements.UIDropDownMenu(options_list=['K: 3'], starting_option='K: 3', relative_rect=pg.Rect((600, 150), (100, 50)), manager=MANAGER)

        get_bot_level = pgui.elements.UIDropDownMenu(options_list=['Bot Level: Easy', 'Bot Level: Medium', 'Bot Level: Hard'], starting_option='Bot Level: Easy', relative_rect=pg.Rect((215, 250), (175, 50)), manager=MANAGER)
        x_or_o = pgui.elements.UIDropDownMenu(options_list=['Your Piece: X', 'Your Piece: O'], starting_option='Your Piece: X', relative_rect=pg.Rect((415, 250), (175, 50)), manager=MANAGER)
        

        play_button = pgui.elements.UIButton(relative_rect=pg.Rect((315, 400), (175, 75)), text='Play', manager=MANAGER)
        play_button.colours['normal_bg'] = pg.Color('#FF0000')  
        play_button.colours['hovered_bg'] = pg.Color('#00FF00') 
        play_button.colours['disabled_bg'] = pg.Color('#FFFFFF') 
        play_button.rebuild() 

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
                    get_k = pgui.elements.UIDropDownMenu(options_list=new_list, starting_option=start_opt, relative_rect=pg.Rect((600, 150), (100, 50)), manager=MANAGER)

                if event.type ==pgui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element==get_game_mode:
                    if get_game_mode.selected_option=='Gamemode: Multiplayer':
                        if get_bot_level is not None: get_bot_level.kill()
                        if x_or_o is not None: x_or_o.kill()
                    else:
                       get_bot_level = pgui.elements.UIDropDownMenu(options_list=['Bot Level: Easy', 'Bot Level: Medium', 'Bot Level: Hard'], starting_option='Bot Level: Easy', relative_rect=pg.Rect((215, 250), (175, 50)), manager=MANAGER)
                       x_or_o = pgui.elements.UIDropDownMenu(options_list=['Your Piece: X', 'Your Piece: O'], starting_option='Your Piece: X', relative_rect=pg.Rect((415, 250), (175, 50)), manager=MANAGER)

                if event.type == pgui.UI_BUTTON_PRESSED and event.ui_element==play_button:
                    self.n = int(get_n.selected_option.split()[-1])
                    self.m = int(get_m.selected_option.split()[-1])
                    self.k = int(get_k.selected_option.split()[-1])
                    self.gamemode = get_game_mode.selected_option.split()[-1]
                    if get_bot_level is not None: self.bot_level = get_bot_level.selected_option.split()[-1].upper()
                    if x_or_o is not None: self.player_piece = x_or_o.selected_option.split()[-1]
                    self.game_window()

        
                MANAGER.process_events(event)

            MANAGER.update(ref_rate)
            self.SCREEN.fill((0, 0, 51))

            txt = pg.font.SysFont('comicsans', 30).render("Welcome to K-In-A-Row N by M Tic-Tac-Toe!", True, (255, 255, 255))
            self.SCREEN.blit(txt, (75, 10))

            txt = pg.font.SysFont('comicsans', 20).render("(Please select the options below)", True, (255, 255, 255))
            self.SCREEN.blit(txt, (240, 50))

            MANAGER.draw_ui(self.SCREEN)
            pg.display.update()


    def game_window(self):
        MANAGER = pgui.UIManager((self.WIDTH, self.HEIGHT))
        run=True
        back = pgui.elements.UIButton(relative_rect=pg.Rect((50, 25), (100, 50)), text='Back', manager=MANAGER)

        l = 550
        w = 550
        x = 200
        y = 25
        if self.n > self.m:
            ratio = self.m/self.n
            diff = 550*(1 - ratio)/2
            l*=ratio
            x+=diff
        else:
            ratio = self.n/self.m
            diff = 550*(1 - ratio)/2
            w*=ratio
            y+=diff
        rectangle = pg.Rect((x, y), (l, w))

        box_len = l/self.m
        line_end_y = y + w
        line_end_x = x + l

        move_to_button = {}
        button_to_move = {}
        for i in range(self.m):
            for j in range(self.n):
                board_button = pgui.elements.UIButton(relative_rect=pg.Rect((x + box_len*i, y + box_len*j), (box_len, box_len)), text='', manager=MANAGER)
                board_button.colours['normal_bg'] = pg.Color('black')
                button_to_move[board_button] = (j+1, i+1)
                if self.gamemode=='Singleplayer':
                    move_to_button[(j+1, i+1)] = board_button
                board_button.rebuild()


        board = BoardState(self.n, self.m, self.k, None, 'X')
        if self.gamemode=='Singleplayer': bot = Bot(self.bot_level)
        xs_to_draw = []
        os_to_draw = []
        winner=None

        while run:
            ref_rate = self.CLOCK.tick(60)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pgui.UI_BUTTON_PRESSED and event.ui_element==back:
                    run = False
                    break
                
                if event.type == pgui.UI_BUTTON_PRESSED:
                    if self.gamemode=='Multiplayer' or (self.gamemode=='Singleplayer' and board.next_player==self.player_piece):
                        marked = button_to_move[event.ui_element]
                        if board.next_player=='X':
                            xs_to_draw.append(marked)
                        else:
                            os_to_draw.append(marked)
                        board = board.move(marked)
                        winner = board.is_goal_state()
                        del button_to_move[event.ui_element]
                        event.ui_element.kill()


                MANAGER.process_events(event)

            
            MANAGER.update(ref_rate)
            self.SCREEN.fill((0, 0, 51))
            
            #drawing board
            pg.draw.rect(self.SCREEN, pg.Color('white'), rectangle.inflate(5, 5))
            pg.draw.rect(self.SCREEN, pg.Color('black'), rectangle)

            for i in range(1, self.m):
                pg.draw.line(self.SCREEN, pg.Color('white'), (i*box_len + x, y), (i*box_len + x, line_end_y), 2)

            for i in range(1, self.n):
                pg.draw.line(self.SCREEN, pg.Color('white'), (x, i*box_len + y), (line_end_x, i*box_len + y), 2)
            
            
            MANAGER.draw_ui(self.SCREEN)

            self.draw_marks(xs_to_draw, 'X', box_len, x, y)
            self.draw_marks(os_to_draw, 'O', box_len, x, y)
            

            #Game over check
            if winner!=None:
                for button in button_to_move:
                    button.kill()
                if winner=='X':
                    txt = pg.font.SysFont('comicsans', 30).render("X wins!", True, pg.Color('red'))
                    self.SCREEN.blit(txt, (60, 100))
                elif winner=='O':
                    txt = pg.font.SysFont('comicsans', 30).render("O wins!", True, pg.Color('blue'))
                    self.SCREEN.blit(txt, (60, 100))
                else:
                    txt = pg.font.SysFont('comicsans', 30).render("Draw!", True, pg.Color('green'))
                    self.SCREEN.blit(txt, (60, 100))
                
                
                pg.display.update()
                time.sleep(3)
                break
        
            pg.display.update()

            #bot move, this is after the display update since choose_move may have a time delay
            if self.gamemode=='Singleplayer' and board.next_player!=self.player_piece and winner==None:
                bot_move = bot.choose_move(board)
                if board.next_player=='X':
                    xs_to_draw.append(bot_move)
                else:
                    os_to_draw.append(bot_move)

                board = board.move(bot_move)
                winner = board.is_goal_state()
                bot_button = move_to_button[tuple(bot_move)]
                del button_to_move[bot_button]
                del move_to_button[tuple(bot_move)]
                bot_button.kill()

        
    def draw_marks(self, to_draw, mark, box_len, x, y):
        for piece in to_draw:
            j = piece[0] - 1 
            i = piece[1] - 1 
            if mark=='X':
                pg.draw.line(self.SCREEN, pg.Color('red'), (x+0.1*box_len + i*box_len, y+0.1*box_len + j*box_len), (x+box_len - 0.1*box_len + i*box_len, y+box_len - 0.1*box_len + j*box_len), 5)
                pg.draw.line(self.SCREEN, pg.Color('red'), (x+0.1*box_len + i*box_len, y+box_len - 0.1*box_len + j*box_len), (x+box_len - 0.1*box_len  + i*box_len, y+0.1*box_len + j*box_len), 5)
            else:
                pg.draw.circle(self.SCREEN, pg.Color('blue'), (x + 0.5*box_len + i*box_len, y + 0.5*box_len + j*box_len), 0.46*box_len, 5)
        



game = GameGUI()
game.main_menu()
    