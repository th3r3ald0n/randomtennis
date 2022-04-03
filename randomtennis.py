import random

def win_game_prob(p):
    """Map probability of winning a point to probability of winning a game"""
    return p**4 + 4*(p**4)*(1-p) + 10*(p**4)*(1-p)**2 + 20*(p**3)*(1-p)**3*((p**2)/((p**2) + (1-p)**2))

        
class Player:
    """For simulations with altering point winning chances
       p_as_server: Probability in interval [0,1] of winning a point when serving, 
                    including double faults, first, second service etc.
       p_game_as_server: Probability of winning a service game
       
       For simple simulations, p_as_server is the overall probability of winning a point
       """    
    def __init__(self, p):
        self.points = 0 
        self.games = 0 
        self.sets = 0
        self.matches = 0 
        self.serving = False
        self.p_as_server = p
        self.p_game_as_server = win_game_prob(p)
        # meta stats
        self.sets_total = 0 
        self.scoreboard = []
        
class Draw:
    def coinflip(p1, p2):
        if random.random() <= 0.5: 
            p1.serving = True
            p2.serving = False
        else: 
            p2.serving = True
            p1.serving = False
    
    def serving(p1, p2):
        if p1.serving and not p2.serving: return p1
        elif p2.serving and not p1.serving: return p2
        else: print("serve error")
            
    def returning(p1, p2):
        if p1.serving and not p2.serving: return p2
        elif p2.serving and not p1.serving: return p1
        else: print("return error")
    
    def score_game(p, p1, p2):
        if random.random() <= p: return p1
        else: return p2
    
    def add_game(player):
        player.games += 1
        
    def simple_scoring(p, p1, p2):
        Draw.add_game(Draw.score_game(p, p1, p2))
    
    def service_scoring(server, returner):
        Draw.add_game(Draw.score_service_game(server, returner))
        
    def score_service_game(server, returner):
        if random.random() <= server.p_game_as_server:
            return server
        else: return returner
        
        

class Score:
    def is_set(p1, p2):
        """return player if game score is set"""
        if ((p1.games == 6) and (p2.games <=4)) or (p1.games == 7):
            return p1
        elif ((p2.games == 6) and (p1.games <=4)) or (p2.games == 7):
            return p2
        else:
            return False  
        
    def is_match(p1, p2, winning_sets = 2):
        """return player if game score is match"""
        if p1.sets == winning_sets: return p1
        elif p2.sets == winning_sets: return p2
        else: return False

class Simple_tester:
    """Only simulate matches with one constant point winning probability"""
    def __init__(self, p, winning_sets=2):
        self.player1, self.player2 = Player(p), Player(1-p)
        self.winning_sets = winning_sets
        self.drawing_function = Draw.simple_scoring
        
    def loop(self, func, **kwargs):
        """func: function which draws points"""
        while True:
            if Score.is_match(self.player1, self.player2, winning_sets = self.winning_sets) != False:
                winner = Score.is_match(self.player1, self.player2, winning_sets = self.winning_sets)
                winner.matches += 1
                self.player1.sets, self.player2.sets = 0,0 
                break
            elif Score.is_set(self.player1, self.player2) != False:
                set_winner = Score.is_set(self.player1, self.player2)
                set_winner.sets += 1
                set_winner.sets_total += 1
                ##
                self.player1.scoreboard.append([self.player1.games, self.player2.games])
                self.player1.games, self.player2.games = 0, 0 
            else:
                func(**kwargs)
            
    def simulate_match(self):
        self.loop(Draw.simple_scoring, p = self.player1.p_game_as_server, p1 = self.player1, p2= self.player2)
        
    def multiple_runs(self, runs):
        self.runs = runs
        for i in range(self.runs):
            self.simulate_match()
        #print("Multiple runs DONE")
    

class Service_tester(Simple_tester):
    """Simulate matches with alternating point winning probabilities"""
    def __init__(self, p1_as_server, p2_as_server, winning_sets=2):
        self.player1, self.player2 = Player(p1_as_server), Player(p2_as_server)
        self.winning_sets = winning_sets
        self.drawing_function = Draw.service_scoring
        
    def loop(self, func, server, returner):
        """func: function which draws games"""
        while True:
            if Score.is_match(self.player1, self.player2, winning_sets = self.winning_sets) != False:
                winner = Score.is_match(self.player1, self.player2, winning_sets = self.winning_sets)
                winner.matches += 1
                self.player1.sets, self.player2.sets = 0,0 
                break
            elif Score.is_set(self.player1, self.player2) != False:
                set_winner = Score.is_set(self.player1, self.player2)
                set_winner.sets += 1
                self.player1.games, self.player2.games = 0, 0
            else:
                func(server, returner)
                server, returner = returner, server
        
    def simulate_match(self):
        Draw.coinflip(self.player1, self.player2)
        #print(self.player1.serving, self.player2.serving)
        server = Draw.serving(self.player1, self.player2)
        returner = Draw.returning(self.player1, self.player2)
        self.loop(self.drawing_function, server = server, returner=returner)



