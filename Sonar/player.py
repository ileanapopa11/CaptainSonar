from PodSixNet.Connection import ConnectionListener, connection
import time
import pygame
import math
import image_search
import random

global map_name 
map_name = "italia.png"

class SonarGame(ConnectionListener): # object that receives messages from the server. Subclass ConnectionListener
    def initGraphics(self):
        self.barV = pygame.image.load("graphics\\way.png")
        self.barH = pygame.transform.rotate(pygame.image.load("graphics\\way.png"), -90)

        self.op_barV = pygame.image.load("graphics\\op_way.png")
        self.op_barH = pygame.transform.rotate(pygame.image.load("graphics\\op_way.png"), -90)

        self.separators = pygame.image.load("graphics\\separators.png")
        self.start_point = pygame.image.load("graphics\\start_point.png")
        
        self.margin_h = pygame.image.load("graphics\\margin.png")
        self.margin_v = pygame.transform.rotate(pygame.image.load("graphics\\margin.png"), -90)
        self.slice_h = pygame.image.load("graphics\\map_slice.png")
        self.slice_v = pygame.transform.rotate(pygame.image.load("graphics\\map_slice.png"), -90)

        self.captain = pygame.image.load("graphics\\" + map_name)
        
        self.radio_operator = pygame.image.load("graphics\\" + map_name)
        self.first_mate = pygame.image.load("graphics\\first_mate.png")
        self.engineer = pygame.image.load("graphics\\engineer.png")
        self.disabled = pygame.image.load("graphics\\disabled.png")
        
        self.radio_filter = pygame.image.load("graphics\\radio_filter.png")

        self.off_square = pygame.image.load("graphics\\pink_square.png")
        self.on_square = pygame.image.load("graphics\\green_square.png")

        self.lost_life = pygame.image.load("graphics\\lost_life.png")
        self.light_square = pygame.image.load("graphics\\light_square.png")
        self.disabled_square = pygame.image.load("graphics\\disabled_square.png")
        self.launch_square = pygame.image.load("graphics\\launch_square.png")

        self.fm_mine = pygame.image.load("graphics\\load_mine.png")
        self.fm_torpedo = pygame.image.load("graphics\\load_torpedo.png")
        self.fm_drone = pygame.image.load("graphics\\load_drone.png")
        self.fm_sonar = pygame.image.load("graphics\\load_sonar.png")

        self.eng_t_square = pygame.image.load("graphics\\eng_t_square.png")
        self.eng_cross = pygame.image.load("graphics\\cross.png")

        self.load_one = pygame.image.load("graphics\\load_one.png")
        self.load_two = pygame.image.load("graphics\\load_two.png")
        self.load_three = pygame.image.load("graphics\\load_three.png")
        self.load_four = pygame.image.load("graphics\\load_four.png")

        self.done_one = pygame.image.load("graphics\\done_one.png")
        self.done_two = pygame.image.load("graphics\\done_two.png")
        self.done_three = pygame.image.load("graphics\\done_three.png")
        self.done_four = pygame.image.load("graphics\\done_four.png")

        self.yellow_square = pygame.image.load("graphics\\yellow_square.png")
        self.orange_square = pygame.image.load("graphics\\orange_square.png")
        self.grey_square = pygame.image.load("graphics\\grey_square.png")

        self.bomb1 = pygame.image.load("graphics\\bomb1.png")
        self.bomb2 = pygame.image.load("graphics\\bomb2.png")
        self.mine = pygame.image.load("graphics\\mine.png")
        
        self.game_won = pygame.image.load("graphics\\game_won.png")
        self.game_lost = pygame.image.load("graphics\\game_lost.png")
        
        self.sector_yellow = pygame.image.load("graphics\\sector_yellow.png")
        self.sector_orange = pygame.image.load("graphics\\sector_orange.png")
        
        self.wait = pygame.image.load("graphics\\wait.png")
        
        self.one = pygame.image.load("graphics\\unu.png")
        self.two = pygame.image.load("graphics\\doi.png")
        self.three = pygame.image.load("graphics\\trei.png")
        self.four = pygame.image.load("graphics\\patru.png")
        self.five = pygame.image.load("graphics\\cinci.png")
        self.six = pygame.image.load("graphics\\sase.png")
        self.seven = pygame.image.load("graphics\\sapte.png")
        self.eight = pygame.image.load("graphics\\opt.png")
        self.nine = pygame.image.load("graphics\\noua.png")


    def __init__(self, host, port):
        pass
        pygame.init()
        pygame.font.init()

        self.margin_size = 5.0
        self.separator_size = 5.0
        self.side_size = 23.0
        self.map_points = 15
        self.fm_square_dim = 107
        self.map_size = self.side_size * (self.map_points - 1) + self.separator_size
        self.width = int(3 * self.margin_size + 2 * self.map_size)
        self.height = self.width
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sonar")
        self.players = []
        self.players.append(Player(1))
        self.players.append(Player(2))

        self.clock = pygame.time.Clock()

        self.boardh = [[False for x in range(self.map_points - 1)] for y in range(15)]
        self.boardv = [[False for x in range(15)] for y in range(self.map_points - 1)]
        
        self.locations = image_search.get_locations_list("graphics\\" + map_name)
        self.map_sent = False
        self.robot_opp = False

        self.opponent_loc = list(self.locations)

        self.initGraphics()
        
        # CAPTAIN & RADIO OPERATOR
        self.turn = True
        self.justplaced = 10
        self.pickPoint = True
        self.startPicked = False
        self.start_point_location = []
        self.submarine_current_location = []
        self.submarine_current_index = []
        self.user_message = "Pick a spot to sink your submarine"
        self.submarine_x = 0
        self.submarine_y = 0
        
        self.action_list = []

        # FIRST MATE
        self.deaths = 0

        self.clocks = [self.fm_mine, self.fm_drone, self.fm_sonar, self.fm_torpedo]
        self.clock_poz = [(67, 110), (190, 110), (190, 235), (67, 235)]
        self.clock_score = [0, 0, 0, 0]

        self.fm_squares = [(53, 426), (177, 426), (177, 548), (53, 548)]
        self.c_index = -1

        self.clock_disabled = [False, False, False, False]
        self.clock_ready = [False, False, False, False]

        # ENGINEER
        self.turn_direction = False

        self.cross_poz = [(17, 189), (17, 223), (17, 257), (47, 207), (47, 241)]
        self.cross_poz += [(96, 257), (111, 189), (111, 228), (126, 257)]
        self.cross_poz += [(175, 228), (175, 257), (205, 207), (205, 257)]
        self.cross_poz += [(254, 207), (254, 241), (283, 189), (283, 223), (283, 257)]

        self.eng_system = []
        for c in range(0, 5):
            self.eng_system.append([self.cross_poz[c], False, "W"])

        for c in range(5, 9):
            self.eng_system.append([self.cross_poz[c], False, "N"])

        for c in range(9, 13):
            self.eng_system.append([self.cross_poz[c], False, "S"])

        for c in range(13, 18):
            self.eng_system.append([self.cross_poz[c], False, "E"])

        for c in range(0, 18):
            if c in [3, 8, 11, 12, 14]:
                self.eng_system[c].append("red")
            if c in [0, 4, 6, 7, 9, 13, 16]:
                self.eng_system[c].append("green")
            if c in [1, 2, 5, 10, 15, 17]:
                self.eng_system[c].append("blue")

        self.eng_square_poz = {"W" : (8, 150), "N" : (87, 150), "S" : (166, 150), "E" : (245, 150)}

        # TURN
        self.game_status = "Running"
        self.current_role = {"Captain" : True, "Radio operator" : True, "First mate" : False, "Engineer" : False}
        self.role_poz = {}
        self.role_poz["Captain"] = [self.margin_size, self.margin_size]
        self.role_poz["Radio operator"] = [self.map_size + 2 * self.margin_size, self.margin_size]
        self.role_poz["First mate"] = [self.margin_size, self.map_size + 2 * self.margin_size]
        self.role_poz["Engineer"] = [self.map_size + 2 * self.margin_size, self.map_size + 2 * self.margin_size]
        self.opponent_x = False
        self.opponent_y = False
        self.moves = 0

        # TORPEDO ON
        self.torpedo_on = False
        self.direction = False
        self.power = 0
        self.explosion = False
        self.explosion_poz = []
        
        # MINE ON
        self.mine_on = False
        self.mine_choose_coord = []
        self.planted_mines = []
        self.attack_explosion = False
        
        # DRONE ON
        self.drone_on = False
        self.drone_picked = False
        self.drone_hover = False
        first_last = 105
        middle = 115
        x = self.map_size + 2 * self.margin_size
        y = self.margin_size
        self.x_section = [x, x + first_last, x + first_last + middle, x + 2 * first_last + middle]
        self.y_section = [y, y + first_last, y + first_last + middle, x + 2 * first_last + middle]
        
        # RAIN ON
        self.sonar_on = False
        self.rain_poz = False
        self.rain_time = False
        self.rain_attack = False
        
        self.Connect((host, port))

        self.player = None
        self.gameID = None


    def drawBoard(self):
        if not self.map_sent and self.robot_opp == True:
            self.Send({"action": "image_loc", "locations": self.locations, "player": self.player, "gameID": self.gameID})
            self.map_sent = True
            
        self.screen.blit(self.margin_h, [0, 0])
        self.screen.blit(self.margin_v, [0, 0])

        self.screen.blit(self.margin_h, [0, self.height - self.margin_size])
        self.screen.blit(self.margin_v, [self.width - self.margin_size, 0])

        self.screen.blit(self.margin_h, [0, self.margin_size + self.map_size])
        self.screen.blit(self.margin_v, [self.margin_size + self.map_size, 0])
        
        self.screen.blit(self.captain, self.role_poz["Captain"])
        self.screen.blit(self.radio_operator, self.role_poz["Radio operator"])
        self.screen.blit(self.radio_filter, self.role_poz["Radio operator"])
        
        self.screen.blit(self.slice_h, [0, self.margin_size + self.map_size / 3 - 5])
        self.screen.blit(self.slice_h, [0, self.margin_size + 2 * self.map_size / 3 + 1])
        self.screen.blit(self.slice_v, [self.margin_size + self.map_size / 3 - 5, 0])
        self.screen.blit(self.slice_v, [self.margin_size + 2 * self.map_size / 3 + 1, 0])
        
        radio = self.margin_size + self.map_size
        self.screen.blit(self.slice_h, [radio, self.margin_size + self.map_size / 3 - 5])
        self.screen.blit(self.slice_h, [radio, self.margin_size + 2 * self.map_size / 3 + 1])
        self.screen.blit(self.slice_v, [radio + self.margin_size + self.map_size / 3 - 5, 0])
        self.screen.blit(self.slice_v, [radio + self.margin_size + 2 * self.map_size / 3 + 1, 0])
        

        # CAPTAIN
        numbers = [self.one, self.two, self.three, self.four, self.five, self.six, self.seven, self.eight, self.nine]
        n = 0
        for y in range(1, 4):
            for x in range(1, 4):
                self.screen.blit(numbers[n], [x * 110 - 80, y * 110 - 80])
                n += 1

        for x in range(14):
            for y in range(15):
                if self.boardh[y][x]:
                    self.screen.blit(self.barH, [x * self.side_size + 10, y * self.side_size + 5])
        
        for x in range(15):
            for y in range(14):
                if self.boardv[y][x]:
                    self.screen.blit(self.barV, [x * self.side_size + 5, y * self.side_size + 10])
        
        for x in range(15):
            for y in range(15):
                if self.locations[x][y] != "land":
                    self.screen.blit(self.separators, [x * self.side_size + 5, y * self.side_size + 5])
                if self.locations[x][y] == "mine":
                    self.screen.blit(self.mine, [x * self.side_size - 3, y * self.side_size - 3])
                    
        if self.startPicked:
            self.screen.blit(self.start_point, self.start_point_location)
        
        # RADIO OPERATOR
        n = 0
        for y in range(1, 4):
            for x in range(1, 4):
                self.screen.blit(numbers[n], [x * 110 + 250, y * 110 - 80])
                n += 1
        
        for x in range(15):
            for y in range(15):
                if self.opponent_loc[x][y] != "land":
                    self.screen.blit(self.separators, [x * self.side_size + self.role_poz["Radio operator"][0], y * self.side_size + 5])

        # FIRST MATE
        self.screen.blit(self.first_mate, self.role_poz["First mate"])

        x_poz = self.margin_size + 164
        for draw in range(self.deaths):
            self.screen.blit(self.lost_life, [x_poz, self.role_poz["First mate"][1] + 39])
            x_poz += 37

        for c in range(len(self.clocks)):
            x_poz = self.clock_poz[c][0]
            y_poz = self.clock_poz[c][1]
            self.screen.blit(self.clocks[c], [self.margin_size + x_poz, self.role_poz["First mate"][1] + y_poz])
            score = self.clock_score[c]

            if score >= 1:
                self.screen.blit(self.done_one, [self.margin_size + x_poz + 30, self.role_poz["First mate"][1] + y_poz - 18])
            else:
                self.screen.blit(self.load_one, [self.margin_size + x_poz + 30, self.role_poz["First mate"][1] + y_poz - 18])

            if score >= 2:
                self.screen.blit(self.done_two, [self.margin_size + x_poz + 54, self.role_poz["First mate"][1] + y_poz - 2])
            else:
                self.screen.blit(self.load_two, [self.margin_size + x_poz + 54, self.role_poz["First mate"][1] + y_poz - 2])

            if score >= 3:
                self.screen.blit(self.done_three, [self.margin_size + x_poz + 54, self.role_poz["First mate"][1] + y_poz + 30])
            else:
                self.screen.blit(self.load_three, [self.margin_size + x_poz + 54, self.role_poz["First mate"][1] + y_poz + 30])

            if score == 4:
                self.screen.blit(self.done_four, [self.margin_size + x_poz + 29, self.role_poz["First mate"][1] + y_poz + 55])
            elif self.clocks[c] == self.fm_drone:
                self.screen.blit(self.load_four, [self.margin_size + x_poz + 29, self.role_poz["First mate"][1] + y_poz + 55])


        if self.c_index != -1:
            self.screen.blit(self.light_square, [self.fm_squares[self.c_index][0], self.fm_squares[self.c_index][1]])

        for c in range(len(self.clock_disabled)):
            if self.clock_disabled[c] and self.clock_ready[c]:
                self.screen.blit(self.disabled_square, [self.fm_squares[c][0], self.fm_squares[c][1]])

        for c in range(len(self.clock_ready)):
            if not self.clock_disabled[c] and self.clock_ready[c]:
                self.screen.blit(self.launch_square, [self.fm_squares[c][0], self.fm_squares[c][1]])


        # ENGINEER
        self.screen.blit(self.engineer, self.role_poz["Engineer"])

        x_eng = self.role_poz["Engineer"][0]
        y_eng = self.role_poz["Engineer"][1]

        for c in range(len(self.eng_system)):
            if self.eng_system[c][1]:
                self.screen.blit(self.eng_cross, [x_eng + self.eng_system[c][0][0], y_eng + self.eng_system[c][0][1]])

        if self.turn_direction != False:
            for s in self.eng_square_poz:
                if self.turn_direction == s:
                    continue
                x = self.eng_square_poz[s][0]
                y = self.eng_square_poz[s][1]
                self.screen.blit(self.eng_t_square, [self.role_poz["Engineer"][0] + x, self.role_poz["Engineer"][1] + y])

        # TURN
        for c in self.current_role:
            if not self.current_role[c]:
                self.screen.blit(self.disabled, self.role_poz[c])

        # TORPEDO ON
        if self.torpedo_on:
            x_poz = self.submarine_current_location[0] - 7
            y_poz = self.submarine_current_location[1] - 7
            
            if not self.explosion:
                # draw explosion picker cross
                self.screen.blit(self.yellow_square, [x_poz, y_poz])
                for i in range(1, 5):
                    if self.submarine_x - i >= 0:
                        if i <= self.power and self.direction == "UP":
                            self.screen.blit(self.orange_square, [x_poz, y_poz - i * 23]) # UP
                        else:
                            self.screen.blit(self.yellow_square, [x_poz, y_poz - i * 23])

                    if self.submarine_x + i <= 14:
                        if i <= self.power and self.direction == "DOWN":
                            self.screen.blit(self.orange_square, [x_poz, y_poz + i * 23]) # DOWN
                        else:
                            self.screen.blit(self.yellow_square, [x_poz, y_poz + i * 23])

                    if self.submarine_y - i >= 0:
                        if i <= self.power and self.direction == "LEFT":
                            self.screen.blit(self.orange_square, [x_poz - i * 23, y_poz]) # LEFT
                        else:
                            self.screen.blit(self.yellow_square, [x_poz - i * 23, y_poz])

                    if self.submarine_y + i <= 14:
                        if i <= self.power and self.direction == "RIGHT":
                            self.screen.blit(self.orange_square, [x_poz + i * 23, y_poz]) # RIGHT
                        else:
                            self.screen.blit(self.yellow_square, [x_poz + i * 23, y_poz])
        
        # MINE ON
        if self.mine_on:
            x_poz = self.submarine_current_location[0] - 7
            y_poz = self.submarine_current_location[1] - 7
            
            x_square = self.submarine_current_index[0]
            y_square = self.submarine_current_index[1]
            
            mine_coord = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
            self.screen.blit(self.grey_square, [x_poz, y_poz])
            
            for it in self.mine_choose_coord:
                if it[1] == "on":
                    self.screen.blit(self.yellow_square, [x_poz + it[0][0] * 23, y_poz + it[0][1] * 23])
                elif it[1] == "off":
                    self.screen.blit(self.grey_square, [x_poz + it[0][0] * 23, y_poz + it[0][1] * 23])
                elif it[1] == "hover":
                    self.screen.blit(self.orange_square, [x_poz + it[0][0] * 23, y_poz + it[0][1] * 23])
            
            self.mine_choose_coord = []
            for c in mine_coord:
                if x_square + c[0] in range(0, 15) and y_square + c[1] in range(0, 15):
                    if self.locations[x_square + c[0]][y_square + c[1]] not in ["path", "land", "mine"]:
                        self.mine_choose_coord.append([(c[0], c[1]), "on"])
                    else:
                        self.mine_choose_coord.append([(c[0], c[1]), "off"])
        
        if self.explosion and self.explosion in range(0, 15):
            self.screen.blit(self.bomb1, self.explosion_poz)
            self.explosion += 1
        elif self.explosion in range(15, 30):
            self.screen.blit(self.bomb2, self.explosion_poz)
            self.explosion += 1
        elif self.explosion in range(30, 45):
            self.screen.blit(self.bomb1, self.explosion_poz)
            self.explosion += 1
        elif self.explosion == 45:
            # animation finished
            self.explosion = False
            self.check_explosion_damage()
            explosion_location = self.get_map_loc_from_coord(self.explosion_poz)
            x = explosion_location[0] + 1
            y = explosion_location[1] + 1
            if self.locations[x][y] in ["mine", "hidden_mine"]:
                self.locations[x][y] = "water"
            if not self.attack_explosion:
                self.Send({"action": "explode", "poz": self.explosion_poz, "player": self.player, "gameID": self.gameID})
            else:
                self.attack_explosion = False
            
        # DRONE ON
        if self.drone_on:
            if self.drone_picked:
                x = self.drone_picked[0]
                y = self.drone_picked[1]
                self.screen.blit(self.sector_orange, [self.x_section[x] - 1, self.y_section[y] - 1])
                self.drone_on += 1
                if self.drone_on == 50:
                    self.drone_on = False
                    self.drone_picked = False
                    self.current_role = {"Captain" : False, "Radio operator" : True, "First mate" : False, "Engineer" : True}
            elif self.drone_hover:
                x = self.drone_hover[0]
                y = self.drone_hover[1]
                self.screen.blit(self.sector_yellow, [self.x_section[x] - 1, self.y_section[y] - 1])
        
        # RAIN ON
        if self.rain_time > 0:
            if self.rain_time == 20 and not self.rain_attack:
                self.Send({"action": "rain", "poz": self.rain_poz, "player": self.player, "gameID": self.gameID})
            rain_on = range(0, 2) + range(4, 6) + range(10, 14) + range(16, 20)
            if self.rain_time in rain_on:
                for x in range(15):
                    for y in range(15):
                        if self.opponent_loc[x][y] != "land":
                            if self.rain_poz == 0 and ((x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1)):
                                self.screen.blit(self.bomb1, [x * self.side_size + self.role_poz["Radio operator"][0] - 23 - 5, y * self.side_size + 5 - 23 - 5])
                            elif self.rain_poz == 1 and ((x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1)):
                                self.screen.blit(self.bomb1, [x * self.side_size + self.role_poz["Radio operator"][0] - 23 - 5, y * self.side_size + 5 - 23 - 5])
            self.rain_time -= 1
        elif self.rain_time == 0:
            self.rain_attack = False
            
        # TURN
        if not self.turn:
            self.screen.blit(self.wait, [0, 0])
            

    def pick_start(self):
        mouse = pygame.mouse.get_pos()
        # The position on the grid (coordinates of the square)
        x_square = int(math.floor((mouse[0] - 5.0 + self.side_size/2) / self.side_size))
        y_square = int(math.floor((mouse[1] - 5.0 + self.side_size/2) / self.side_size))
        
        try:
            if self.locations[x_square][y_square] != "land":
                self.screen.blit(self.start_point, [x_square * self.side_size + 5.0 - 2.0, y_square * self.side_size + 5.0 - 2.0])
                # Current location of the submarine
                self.submarine_x = y_square
                self.submarine_y = x_square

            if pygame.mouse.get_pressed()[0] and self.locations[x_square][y_square] != "land":
                self.startPicked = True
                self.user_message = "Use the arrows to draw the line"
                self.start_point_location = [x_square * self.side_size + 5.0 - 2.0, y_square * self.side_size + 5.0 - 2.0]
                self.submarine_current_location = list(self.start_point_location)
                self.locations[self.submarine_y][self.submarine_x] = "path"

        except:
            pass


    def draw_path(self):
        new_path = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:

                x = self.submarine_x
                y = self.submarine_y

                possible_way = False
                if x != 0  and self.locations[y][x - 1] not in  ["path", "land"]:
                    possible_way = True
                    if event.key == pygame.K_UP:
                        self.boardv[self.submarine_x - 1][self.submarine_y] = True
                        self.Send({"action": "move", "way": "Up", "player": self.player, "gameID": self.gameID})
                        self.submarine_current_location[1] -= 23
                        self.submarine_x -= 1
                        x -= 1
                        self.turn_direction = "N"
                        new_path = True
                        
                        if self.locations[y][x] in ["mine", "hidden_mine"]:
                            self.explosion = 1
                            self.explosion_poz = [(y - 1) * 23, (x - 1) * 23]
                        self.locations[y][x] = "path"

                if x != self.map_points - 1 and self.locations[y][x + 1] not in ["path", "land"]:
                    possible_way = True
                    if event.key == pygame.K_DOWN:
                        self.boardv[self.submarine_x][self.submarine_y] = True
                        self.Send({"action": "move", "way": "Down", "player": self.player, "gameID": self.gameID})
                        self.submarine_current_location[1] += 23
                        self.submarine_x += 1
                        x += 1
                        self.turn_direction = "S"
                        new_path = True
                        
                        if self.locations[y][x] in ["mine", "hidden_mine"]:
                            self.explosion = 1
                            self.explosion_poz = [(y - 1) * 23, (x - 1) * 23]
                        self.locations[y][x] = "path"
                        
                if y != 0 and self.locations[y - 1][x] not in ["path", "land"]:
                    possible_way = True
                    if event.key == pygame.K_LEFT:
                        self.boardh[self.submarine_x][self.submarine_y - 1] = True
                        self.Send({"action": "move", "way": "Left", "player": self.player, "gameID": self.gameID})
                        self.submarine_current_location[0] -= 23
                        self.submarine_y -= 1
                        y -= 1
                        self.turn_direction = "W"
                        new_path = True
                        
                        if self.locations[y][x] in ["mine", "hidden_mine"]:
                            self.explosion = 1
                            self.explosion_poz = [(y - 1) * 23, (x - 1) * 23]
                        self.locations[y][x] = "path"

                if y != self.map_points - 1 and self.locations[y + 1][x] not in ["path", "land"]:
                    possible_way = True
                    if event.key == pygame.K_RIGHT:
                        self.boardh[self.submarine_x][self.submarine_y] = True
                        self.Send({"action": "move", "way": "Right", "player": self.player, "gameID": self.gameID})
                        self.submarine_current_location[0] += 23
                        self.submarine_y += 1
                        y += 1
                        self.turn_direction = "E"
                        new_path = True
                        
                        if self.locations[y][x] in ["mine", "hidden_mine"]:
                            self.explosion = 1
                            self.explosion_poz = [(y - 1) * 23, (x - 1) * 23]
                        self.locations[y][x] = "path"
                        
                if not possible_way:
                    self.resurface()
        if new_path:
            self.current_role = {"Captain" : False, "Radio operator" : True, "First mate" : True, "Engineer" : False}


    def draw_opponent_path(self):
        # Drawing the action list from the other player
        mouse = pygame.mouse.get_pos()

        x_square = int(math.floor((mouse[0] - 15.0 + self.side_size/2) / self.side_size))
        y_square = int(math.floor((mouse[1] - 5.0 + self.side_size/2) / self.side_size))

        possible_road = True
        map_x_square = x_square - (self.map_points - 1)

        x_point = 0
        y_point = 0
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0

        if map_x_square not in range(0, self.map_points) or y_square not in range(0, self.map_points) or self.opponent_loc[map_x_square][y_square] == "land":
            possible_road = False

        for action in self.action_list:
            if map_x_square + x_point not in range(0, self.map_points) or y_square + y_point not in range(0, self.map_points):
                possible_road = False
                break

            if (map_x_square + x_point == 0 and action == "Left") or (y_square + y_point == self.map_points - 1 and action == "Down"):
                possible_road = False
                break

            if (map_x_square + x_point == self.map_points - 1 and action == "Right") or (y_square + y_point == 0 and action == "Up"):
                possible_road = False
                break

            if action == "Down":
                self.screen.blit(self.op_barV, [(x_square + x_point) * self.side_size + 15.0, (y_square + y_point) * self.side_size + 5.0 + 5.0])
                y_point += 1
            elif action == "Up":
                self.screen.blit(self.op_barV, [(x_square + x_point) * self.side_size + 15.0, (y_square + y_point - 1) * self.side_size + 5.0 + 5.0])
                y_point -= 1
            elif action == "Right":
                self.screen.blit(self.op_barH, [(x_square + x_point) * self.side_size + 15.0 + 5.0, (y_square + y_point) * self.side_size + 5.0])
                x_point += 1
            elif action == "Left":
                self.screen.blit(self.op_barH, [(x_square + x_point - 1) * self.side_size + 15.0 + 5.0, (y_square + y_point) * self.side_size + 5.0])
                x_point -= 1

            min_x = min(min_x, x_point)
            min_y = min(min_y, y_point)
            max_x = max(max_x, x_point)
            max_y = max(max_y, y_point)

            if map_x_square + x_point not in range(0, self.map_points) or y_square + y_point not in range(0, self.map_points):
                break

            if self.opponent_loc[map_x_square + x_point][y_square + y_point] == "land":
                possible_road = False

        x_point = 0
        y_point = 0

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if possible_road:
                    self.screen.blit(self.on_square, [(x_square + x) * self.side_size + 15.0 + 2.5, (y_square + y) * self.side_size + 5.0 + 2.5])
                else:
                    self.screen.blit(self.off_square, [(x_square + x) * self.side_size + 15.0 + 2.5, (y_square + y) * self.side_size + 5.0 + 2.5])


    def load_first_mate(self):
        clock_picked = False
        mouse = pygame.mouse.get_pos()

        x_poz = int(math.floor(mouse[0]))
        y_poz = int(math.floor(mouse[1]))

        self.c_index = -1
        add_to_index = -1
        
        reset_clock = -1

        for it in range(len(self.fm_squares)):
            x = self.fm_squares[it][0]
            y = self.fm_squares[it][1]
            if x_poz in range(x, x + self.fm_square_dim) and y_poz in range(y, y + self.fm_square_dim):
                self.c_index = it

                if pygame.mouse.get_pressed()[0] and not self.clock_ready[it] :
                    clock_picked = True
                    add_to_index = it 
                elif pygame.mouse.get_pressed()[0] and self.clock_ready[it] and not self.clock_disabled[it]:
                    if it == 0:
                        self.mine_on = True
                        reset_clock = it
                    elif it == 1:
                        self.drone_on = 1
                        reset_clock = it
                    elif it == 2:
                        self.sonar_on = True
                        reset_clock = it
                    elif it == 3:
                        self.torpedo_on = True
                        reset_clock = it
                    
        if add_to_index >= 0:
            self.clock.tick(10)
            score = self.clock_score[add_to_index]
            if score < 3 or (score == 3 and add_to_index == 1):
                self.clock_score[add_to_index] += 1
            
        if reset_clock in range(4):
            self.clock_score[reset_clock] = 0
            self.clock_ready[reset_clock] = False
            
        if clock_picked:
            self.current_role = {"Captain" : False, "Radio operator" : True, "First mate" : False, "Engineer" : True}


    def fm_verify_disabled(self):
        red_disabled = False
        green_disabled = False 
        for s in self.eng_system:
            if s[1] == True and s[3] == "red":
                red_disabled = True
                self.clock_disabled[0] = True
                self.clock_disabled[3] = True
            if s[1] == True and s[3] == "green":
                green_disabled = True
                self.clock_disabled[1] = True
                self.clock_disabled[2] = True
        if not red_disabled:
            self.clock_disabled[0] = False
            self.clock_disabled[3] = False

        if not green_disabled:
            self.clock_disabled[1] = False
            self.clock_disabled[2] = False


    def fm_verify_ready(self):
        if self.clock_score[0] == 3:
            self.clock_ready[0] = True
        else:
            self.clock_ready[0] = False

        if self.clock_score[1] == 4:
            self.clock_ready[1] = True
        else:
            self.clock_ready[1] = False

        if self.clock_score[2] == 3:
            self.clock_ready[2] = True
        else:
            self.clock_ready[2] = False

        if self.clock_score[3] == 3:
            self.clock_ready[3] = True
        else:
            self.clock_ready[3] = False


    def eng_pick_a_system(self):
        system_picked = False
        mouse = pygame.mouse.get_pos()

        x_poz = int(math.floor(mouse[0]))
        y_poz = int(math.floor(mouse[1]))

        for it in range(len(self.eng_system)):
            if self.turn_direction != False:
                if self.turn_direction != self.eng_system[it][2]:
                    continue

            x = int(self.eng_system[it][0][0] + self.map_size + 2 * self.margin_size)
            y = int(self.eng_system[it][0][1] + self.map_size + 2 * self.margin_size)

            if x_poz in range(x, x + 30) and y_poz in range(y, y + 30):
                self.screen.blit(self.eng_cross, [x, y])
                self.clock.tick(30)

                if pygame.mouse.get_pressed()[0]:
                    self.eng_system[it][1] = True
                    system_picked = True

        if system_picked:
            self.current_role = {"Captain" : True, "Radio operator" : True, "First mate" : False, "Engineer" : False}


    def eng_auto_repair(self):
        if self.eng_system[6][1] and self.eng_system[9][1]:
            self.eng_system[6][1] = False
            self.eng_system[9][1] = False

        if self.eng_system[3][1] and self.eng_system[4][1] and self.eng_system[14][1]:
            self.eng_system[3][1] = False
            self.eng_system[4][1] = False
            self.eng_system[14][1] = False

        if self.eng_system[11][1] and self.eng_system[13][1]:
            self.eng_system[11][1] = False
            self.eng_system[13][1] = False


    def erase_breakdowns(self):
        for s in self.eng_system:
            s[1] = False
        self.clock.tick(5)


    def check_damage(self):
        radiation_index = [1, 2, 5, 10, 15, 17]

        count = 0
        for i in radiation_index:
            if self.eng_system[i][1]:
                count += 1
        if count == len(radiation_index):
            self.erase_breakdowns()
            self.deaths += 1

        count = 0
        for c in range(0, 5):
            if self.eng_system[c][1]:
                count += 1
        if count == 5:
            self.erase_breakdowns()
            self.deaths += 1

        count = 0
        for c in range(5, 9):
            if self.eng_system[c][1]:
                count += 1
        if count == 4:
            self.erase_breakdowns()
            self.deaths += 1

        count = 0
        for c in range(9, 13):
            if self.eng_system[c][1]:
                count += 1
        if count == 4:
            self.erase_breakdowns()
            self.deaths += 1

        count == 0
        for c in range(13, 18):
            if self.eng_system[c][1]:
                count += 1
        if count == 5:
            self.erase_breakdowns()
            self.deaths += 1


    def launch_torpedo(self):
        if self.direction == False and self.power == 0:
            x_poz = self.submarine_current_location[0] - 27
            y_poz = self.submarine_current_location[1] - 27
            self.explosion_poz = [x_poz, y_poz]
            self.current_role = {"Captain" : True, "Radio operator" : True, "First mate" : False, "Engineer" : False}
            self.clock_score[3] == 0
            self.clock_ready[3] == False
        x = self.submarine_x
        y = self.submarine_y

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if self.power < 4:
                    if event.key == pygame.K_UP and x != 0  and self.direction in [False, "UP"]:
                        self.power += 1
                        self.direction = "UP"
                        x -= 1
                        self.explosion_poz[1] -= 23

                    if event.key == pygame.K_DOWN and x != self.map_points - 1 and self.direction in [False, "DOWN"]:
                        self.power += 1
                        self.direction = "DOWN"
                        x += 1
                        self.explosion_poz[1] += 23

                    if event.key == pygame.K_LEFT and y != 0 and self.direction in [False, "LEFT"]:
                        self.power += 1
                        self.direction = "LEFT"
                        y -= 1
                        self.explosion_poz[0] -= 23

                    if event.key == pygame.K_RIGHT and y != self.map_points - 1 and self.direction in [False, "RIGHT"]:
                        self.power += 1
                        self.direction = "RIGHT"
                        y += 1
                        self.explosion_poz[0] += 23

                if event.key == pygame.K_RETURN:
                    self.explosion = 1
                    self.torpedo_on = False
                    self.direction = False
                    self.power = 0
                    self.current_role = {"Captain" : False, "Radio operator" : True, "First mate" : False, "Engineer" : True}


    def drop_mine(self):
        self.current_role = {"Captain" : True, "Radio operator" : True, "First mate" : False, "Engineer" : False}
        self.clock_score[0] == 0
        self.clock_ready[0] == False
        
        mouse = pygame.mouse.get_pos()
        x_poz = int(math.floor(mouse[0]))
        y_poz = int(math.floor(mouse[1]))
        x_square = self.submarine_current_index[0]
        y_square = self.submarine_current_index[1]
        
        mine_location = []
        
        for it in range(len(self.mine_choose_coord)):
            x = (x_square + self.mine_choose_coord[it][0][0]) * 23
            y = (y_square + self.mine_choose_coord[it][0][1]) * 23
            if self.mine_choose_coord[it][1] == "on" and x_poz in range(x, x + 23) and y_poz in range(y, y + 23):
                self.mine_choose_coord[it][1] = "hover"
                if pygame.mouse.get_pressed()[0]:
                    self.planted_mines.append([x, y])
                    self.locations[x//23][y//23] = "mine"
                    self.mine_on = False
                    self.current_role = {"Captain" : False, "Radio operator" : True, "First mate" : False, "Engineer" : True}
                    mine_location = [x//23, y//23]
                    break
        if not mine_location == []:
            print "planted mine at location: ", mine_location
            self.Send({"action": "mine", "location": mine_location, "player": self.player, "gameID": self.gameID})
                
            
    def launch_drone(self):
        self.current_role = {"Captain" : False, "Radio operator" : True, "First mate" : False, "Engineer" : False}
        if self.opponent_x == False and self.opponent_y == False:
            self.opponent_x = -1
            self.opponent_y = -1
            self.Send({"action": "askLoc", "player": self.player, "gameID": self.gameID})
        mouse = pygame.mouse.get_pos()
        x_poz = int(math.floor(mouse[0]))
        y_poz = int(math.floor(mouse[1]))
        
        opp_x = self.opponent_x / 5
        opp_y = self.opponent_y / 5
        
        for x in range(3):
            for y in range(3):
                if x_poz in range(int(self.x_section[x]), int(self.x_section[x + 1])) and y_poz in range(int(self.y_section[y]), int(self.y_section[y + 1])):
                    self.drone_hover = [x, y]
                    if [x, y] == [opp_y, opp_x]:
                        self.drone_picked = [x, y]
                        self.opponent_x = False
                        self.opponent_y = False
                        
                     
    def launch_sonar(self):
        self.current_role = {"Captain" : False, "Radio operator" : True, "First mate" : False, "Engineer" : True}
        
        x = self.submarine_x
        y = self.submarine_y
        
        if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
            self.rain_poz = 1
        elif (x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1):
            self.rain_poz = 0
            
        self.rain_time = 20
        self.sonar_on = False
        
        
    def resurface(self):
        # Reset the path (Captain)
        self.startPicked = False
        self.boardh = [[False for x in range(self.map_points - 1)] for y in range(15)]
        self.boardv = [[False for x in range(15)] for y in range(self.map_points - 1)]
        # Reset the First Mate
        self.clock_score = [0, 0, 0, 0]
        self.clock_disabled = [False, False, False, False]
        self.clock_ready = [False, False, False, False]
        # Reset the Engineer
        for system in self.eng_system:
            system[1] = False
        self.deaths += 1
        self.Send({"action": "clear_radio", "player": self.player, "gameID": self.gameID})
        print "resurface"
        
        
    def check_explosion_damage(self):
        print "submarine location: ", self.submarine_y, self.submarine_x
        print "explosion coord: ", self.explosion_poz
        explosion_loc = self.get_map_loc_from_coord(self.explosion_poz)
        explosion_loc[0] += 1
        explosion_loc[1] += 1
        print "explosion location: ", explosion_loc
        
        if explosion_loc == [self.submarine_y, self.submarine_x]:
            self.deaths += 2
        elif abs(explosion_loc[0] - self.submarine_y) < 2 and abs(explosion_loc[1] - self.submarine_x) < 2:
            self.deaths += 1
    
    
    def update_index_location(self):
        x_poz = self.submarine_current_location[0]
        y_poz = self.submarine_current_location[1]
            
        x_square = int(math.floor((x_poz - 5.0 + self.side_size/2) / self.side_size))
        y_square = int(math.floor((y_poz - 5.0 + self.side_size/2) / self.side_size))
        
        self.submarine_current_index = [x_square, y_square]
        
        
    def get_map_loc_from_coord(self, c):
        x = c[0]
        y = c[1]
        x_square = int(math.floor((x - 5.0 + self.side_size/2) / self.side_size))
        y_square = int(math.floor((y - 5.0 + self.side_size/2) / self.side_size))
        
        return [x_square, y_square]
    
    
    def check_dead(self):
        if self.deaths >= 4:
            self.Send({"action": "lost", "player": self.player, "gameID": self.gameID})
            self.game_status = "Lost"
    
    
    def update(self):
        # clearing the screen
        self.screen.fill(0)
        self.clock.tick(60)
        self.drawBoard()
        
        if self.turn and self.game_status == "Running":
            # PICK START
            if not self.startPicked:
                self.pick_start()
            else:
                # DRAW THE PATH
                if self.current_role["Captain"] and not self.mine_on and not self.torpedo_on:
                    if self.moves != 0:
                        self.moves = 1
                    self.draw_path()
                    self.update_index_location()

            # FIRST MATE
            if self.current_role["First mate"]:
                self.moves = 2
                self.load_first_mate()
            self.fm_verify_disabled()
            self.fm_verify_ready()

            # ENGINEER
            if self.current_role["Engineer"]:
                self.moves = 3
                self.eng_pick_a_system()
                self.eng_auto_repair()
                self.check_damage()
                
            if self.torpedo_on:
                self.launch_torpedo()
                
            if self.mine_on:
                self.drop_mine()
                
            if self.drone_on:
                self.launch_drone()
                
            if self.sonar_on:
                self.launch_sonar()
                
            if self.moves == 1:
                self.Send({"action": "change_turn", "player": self.player, "gameID": self.gameID})
                self.moves = 0
        
        # RADIO OPERATOR
        if not self.drone_on:
            self.draw_opponent_path()
        if self.game_status == "Running":
            self.check_dead()
        elif self.game_status == "Lost":
            self.screen.blit(self.game_lost, [0, 0])
        elif self.game_status == "Won":
            self.screen.blit(self.game_won, [0, 0])
        # update the contents of the entire display
        pygame.display.flip()


    def finished(self):
        self.screen.blit(self.gameover if not self.didiwin else self.winningscreen, (0, 0))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.update()


    def Network(self, data):
        # The network events are received by Network_* callback methods (* = the action key you wat to catch)
        print("Network function in client")
        print("GOT THE DATA: ", data)


    def Network_connected(self, data):
        print "connected to the server"

    
    def Network_error(self, data):
        # data comes in the form of network exceptions like (111, 'Connection refused')
        # standard socket errors passed from the socket layer
        print "error:", data['error'][1]

    
    def Network_disconnected(self, data):
        print "disconnected from the server"

    
    def Network_smile(self, data):
        # custom method that will receive any data sent from the server with an "action" key
        # ex: channel.Send({"action": "numplayers", "players": 10})
        print "myaction:", data
        print "I'm the Captain"


    def Network_startgame(self, data):
        print "STARTGAME data: ", data
        self.player = data["player"]
        self.gameID = data["gameID"]
        print "this is the player: ", self.player
        if self.player == 0:
            self.turn = True
        if self.player == 1:
            self.turn = False


    def Network_position(self, data):
        print "NETWORK POSITION"
        self.action_list.append(data["way"])

        
    def Network_explode(self, data):
        print "Explosion data from the other player"
        self.attack_explosion = True
        self.explosion = 1
        self.explosion_poz = data["poz"]

        
    def Network_mine(self, data):
        x, y = data["location"]
        self.locations[x][y] = "hidden_mine"
        
        
    def Network_change_turn(self, data):
        if self.turn:
            self.turn = False
        else:
            self.turn = True
            
     
    def Network_robot_change_turn(self, data):
        self.turn = True
            
            
    def Network_give_location(self, data):
        self.Send({"action": "secret_location", "sub_x": self.submarine_x, "sub_y": self.submarine_y, "player": self.player, "gameID": self.gameID})
        
        
    def Network_get_secret_location(self, data):
        self.opponent_x = data["sub_x"]
        self.opponent_y = data["sub_y"]
        
        
    def Network_rain_attack(self, data):
        self.rain_time = 20
        self.rain_attack = True
        self.rain_poz = data["poz"]
        x = self.submarine_x
        y = self.submarine_y
        
        if self.rain_poz == 0 and ((x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1)):
            self.deaths += 1
        elif self.rain_poz == 1 and (x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1):
            self.deaths += 1
            
            
    def Network_clear_radio(self, data):
        self.action_list = []
            
            
    def Network_robot_notif(self, data):
        self.robot_opp = True
        
            
    def Network_won(self, data):
        self.game_status = "Won"
            
        
    def check_exit(self):
        #Create a function that lets us check whether the user has clicked to exit (required to avoid crash)
        #Check if the user exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                exit()


#Create a class to hold our character information
class Player(object):
    
    #Constructor
    def __init__(self, nr):
        # print("Player constructor. Created player with the number: ", nr)
        #Set our object fields
        self.nr = nr


bg = SonarGame('localhost', 1337)
# bg = SonarGame("35.204.129.136", 1337)

while True:
    bg.check_exit()
    connection.Pump()
    bg.Pump()
    bg.update()
    # if bg.update() == 1:
    #     break
bg.finished()
