from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

from time import sleep


class ClientChannel(Channel):

    def Network(self, data): 
        # Whenever the client does connection.Send(mydata), the Network() method will be called
        print("Network function call")
        print(data)

        
    def Network_myaction(self, data):
        # called if the data has the key "action" with the value "my_action"
        print("my_action", data)

        
    def Network_move(self, data):
        print "NETWORK MOVE"
        way = data["way"]
        player = data["player"]
        gameID = data["gameID"]
        self._server.draw_path(way, player, gameID)
        
        
    def Network_explode(self, data):
        print "SERVER EXPLODE"
        poz = data["poz"]
        player = data["player"]
        gameID = data["gameID"]
        self._server.explosion(poz, player, gameID)
        
        
    def Network_mine(self, data):
        mine_location = data["location"]
        player = data["player"]
        gameID = data["gameID"]
        self._server.add_mine(mine_location, player, gameID)
        
        
    def Network_lost(self, data):
        print "SERVER LOST"
        player = data["player"]
        gameID = data["gameID"]
        self._server.game_done(player, gameID)
        
    def Network_askLoc(self, data):
        print "ASKED FOR LOCATION"
        player = data["player"]
        gameID = data["gameID"]
        self._server.ask_location(player, gameID)
        
        
    def Network_secret_location(self, data):
        print "RECEIVED SECRET LOCATION"
        player = data["player"]
        gameID = data["gameID"]
        sub_x = data["sub_x"]
        sub_y = data["sub_y"]
        self._server.give_location(sub_x, sub_y, player, gameID)
        
        
    def Network_rain(self, data):
        print "RAIN ATTACK"
        player = data["player"]
        gameID = data["gameID"]
        poz = data["poz"]
        self._server.rain_attack(poz, player, gameID)
        

    def Network_change_turn(self, data):
        print "CHANGE TURN"
        player = data["player"]
        gameID = data["gameID"]
        self._server.change_turn(player, gameID)
        
        
    def Network_robot_change_turn(self, data):
        print "ROBOT CHANGE TURN"
        player = data["player"]
        gameID = data["gameID"]
        self._server.robot_change_turn(player, gameID)
        
        
    def Network_clear_radio(self, data):
        print "CLEAR RADIO"
        player = data["player"]
        gameID = data["gameID"]
        self._server.clear_radio(player, gameID)

        
class GameServer(Server):

    channelClass = ClientChannel # the channel class created aboves

    def __init__(self, *args, **kwargs):

        Server.__init__(self, *args, **kwargs) # call the super constructor
        print "Created the game server"
        self.games = []
        self.queue = None # Every odd'th player will wait in the queue for a pair player
        self.gameIndex = 0 # how many games the server handles

    def Connected(self, channel, addr):
        # method called whenever a new client connects to the server

        if self.queue == None:
            # we have to create a new game
            channel.gameID = self.gameIndex
            self.queue = Game(channel, self.gameIndex)
        else:
            # there's a game in the queue (one player waiting)
            channel.gameID = self.gameIndex
            self.queue.player_channels.append(channel)

            #Send a message to the clients that the game is starting
            for i in range(0, len(self.queue.player_channels)):
                print("Both connected. The game can start")
                print("SENDING START DATA TO THE CHANNEL: ", self.queue.player_channels[i])
                self.queue.player_channels[i].Send({"action": "startgame", "player": i, "gameID": self.queue.gameID})

            self.games.append(self.queue)
            self.queue = None
            self.gameIndex += 1


    def draw_path(self, way, player, gameID):
        # get the game
        g = self.games[gameID]

        # tell the other player that this one moved
        for i in range(0, len(g.player_channels)):
            if not i == player:
                g.player_channels[i].Send({"action": "position", "way": way, "player": player})

                
    def explosion(self, poz, player, gameID):
        # get the game
        g = self.games[gameID]
        
        # tell the other player where the explosion happened
        for i in range(0, len(g.player_channels)):
            if not i == player:
                g.player_channels[i].Send({"action": "explode", "poz": poz, "player": player})
                
                
    def add_mine(self, mine_location, player, gameID):
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            if not i == player:
                g.player_channels[i].Send({"action": "mine", "location": mine_location, "player": player})
                
                
    def game_done(self, player, gameID):
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            if not i == player:
                g.player_channels[i].Send({"action": "won", "player": player})
                
                
    def change_turn(self, player, gameID):
        # Change turn for both players, including the one that requested 
        # turn = False for player, turn = True for the waiting opponent
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            g.player_channels[i].Send({"action": "change_turn", "player": player})
            
            
    def robot_change_turn(self, player, gameID):
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            if not i == player:
                g.player_channels[i].Send({"action": "robot_change_turn", "player": player})
            
            
    def ask_location(self, player, gameID):
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            if not i == player:
                g.player_channels[i].Send({"action": "give_location", "player": player})
                
                
    def give_location(self, sub_x, sub_y, player, gameID):
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            if not i == player:
                g.player_channels[i].Send({"action": "get_secret_location", "sub_x": sub_x, "sub_y": sub_y, "player": player})
                
                
    def rain_attack(self, poz, player, gameID):
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            if not i == player:
                g.player_channels[i].Send({"action": "rain_attack", "poz": poz, "player": player})

                
    def clear_radio(self, player, gameID):
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            if not i == player:
                g.player_channels[i].Send({"action": "clear_radio", "player": player})
                
                
# game class to hold info about a particular game
class Game(object):
    # Constructor
    def __init__(self, player, gameIndex):

        print("HERE WE CREATE THE GAME. player channel: ", player, " gameIndex: ", gameIndex)
        
        #Store the network channel of the first client
        self.player_channels = [player]

        #Set the game id
        self.gameID = gameIndex


# player class to hold information about a single player
# class Player(object):
    # Constructor
    # def __init__(self, x, y):
        
        # Set the x and y
        # self.x = x
        # self.y = y
        
    # Create a function to move this player
    # def move(self, x, y):
        # self.x += x
        # self.y += y


if __name__ == "__main__":

    print("Server starting on LOCALHOST...\n")
    myserver = GameServer(localaddr=('localhost', 1337))

    while True:
        myserver.Pump()
        sleep(0.0001)
