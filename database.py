import sqlite3

class ScoreSaver:
    def __init__(self):
        self.con = sqlite3.connect('database.db')
        self.create_score_Table();

    def create_score_Table(self):
        cur = self.con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS scores
               (player text, score real)''')
        
        self.con.commit()
    
    def does_player_exists(self,player):
        if self.get_player_highscore(player) > 0:
            return True
        else:
            return False
    
    def get_player_highscore(self,player):
        cur = self.con.cursor()
        cur.execute("SELECT MAX(score) FROM scores WHERE player = '"+player+"'")

        rows = cur.fetchall()
        if len(rows) > 0 and rows[0] != (None,):
            return int(rows[0][0])
        else:
            return 0
    
    def save_player_highscore(self,player,score):
        cur = self.con.cursor()
        query = ""
        if self.does_player_exists(player):
            query = "UPDATE scores SET score = "+str(score)+" WHERE player = '"+player+"'"
        else:
            query = "INSERT INTO scores VALUES('"+player+"','"+str(score)+"')"
        
        cur.execute(query)
        self.con.commit()