import pygame
import time

class GAME:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((450,450))

        self.debug = True

        return

    def draw_lines(self):

        #draw vertical lines
        white = (255, 255, 255)
        pygame.draw.line(self.screen, white, (150, 35), (150, 415))
        pygame.draw.line(self.screen, white, (300, 35), (300, 415))

        #draw horizontal lines
        pygame.draw.line(self.screen, white, (35, 150), (415, 150))
        pygame.draw.line(self.screen, white, (35, 300), (415, 300))

        return

    def setup(self):

        #set game title
        pygame.display.set_caption("Tic Tac Toe")

        #make the screen black
        black = (0, 0, 0)
        self.screen.fill(black)

        #draw lines
        self.draw_lines()

        #which positions are filled
        #0 means unfilled, 1 means X, 2 means O
        self.positions = [0 for _ in range(9)]

        #whose turn it is
        #0 means player's turn, 1 means the computer's
        self.turn = 0

        #if the player or the computer is playing X
        self.player_first = True

        self.victory = False
        self.victory_layout = None
        self.winner = 0

        #draw everything to the screen
        pygame.display.flip()
        

        return

    def get_pos(self, pos):
        #returns which square the mouse is in
        #
        # 1 | 2 | 3
        # ---------
        # 4 | 5 | 6
        # ---------
        # 7 | 8 | 9
        #

        x, y = pos

        horizontal = 0
        vertical = 0
        
        if x < 150:
            horizontal = 1
        elif 150 < x < 300:
            horizontal = 2
        elif x > 300:
            horizontal = 3

        if y < 150:
            vertical = 0
        elif 150 < y < 300:
            vertical = 3
        elif y > 300:
            vertical = 6

        return horizontal + vertical

    def convert_pos(self, pos):
        #convert a number between 1 and 9 to
        #screen cordinates

        #seperate out x and y
        x = (pos % 3)
        if x == 0: x = 3
        y = (pos+2) // 3

        #get the screen cordinates
        x = ((x-1) * 150) + 75
        y = ((y-1) * 150) + 75

        return x, y

    def draw_x(self, pos):

        if self.debug:
            print(f'Drawing X at position: {pos}')

        #mark the self.positions variable
        self.positions[pos-1] = 1

        x, y = self.convert_pos(pos)

        white = (255, 255, 255)

        #size of the X
        size = 60

        #first line
        pygame.draw.line(self.screen, white, (x-size, y-size), (x+size, y+size))
        #second line
        pygame.draw.line(self.screen, white, (x+size, y-size), (x-size, y+size))

        return

    def draw_o(self, pos):

        if self.debug:
            print(f'Drawing O at position: {pos}')

        #mark the self.positions variable
        self.positions[pos-1] = 2

        x, y = self.convert_pos(pos)

        white = (255, 255, 255)

        #size of the circle
        size = 60

        #draw cirlce
        pygame.draw.circle(self.screen, white, (x, y), size, 1)

        return

    def player_mark(self, pos):

        if self.turn == 0:
            if self.debug:
                print(f'attempting to mark board for the player on position: {pos}')
            if self.player_first and self.positions[pos-1] == 0:
                #then place an X
                self.draw_x(pos)
                self.turn = 1
            elif self.positions[pos-1] == 0:
                #place a O
                self.draw_o(pos)
                self.turn = 1
        elif self.turn == 1 and self.positions[pos-1] == 0:
            if self.player_first:
                self.draw_o(pos)
                self.turn = 0
            elif self.positions[pos-1] == 0:
                self.draw_x(pos)
                self.turn = 0

        return
    
    def computer_moves(self):

        if self.debug:
            print(f'positions: {self.positions}')

        #ai should evaluate self.positions
        


        #make it the player's turn
        self.turn = 0

        return

    def check_victory(self):

        if self.debug:
            print('checking for victory')

        #victory layouts
        v_layouts = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        #for each possible victory layout
        for layout in v_layouts:

            #store which mark to check for
            #it will be either
            #0 for nothing, 1 for X, or 2 or O
            mark = self.positions[layout[0]]

            #3 nothings in a row don't equal victory
            if mark == 0: continue

            #check each possible victory layout position
            #to see if it matches the mark
            for p in layout:
                if self.positions[p] != mark:
                    break
            else:
                #that means that there is a winner
                #and the mark at self.positions[p] won
                self.victory = True
                self.victory_layout = layout
                self.winner = self.positions[p]
                break

        if self.debug:
            print('all layouts checked')
            print(f'victory: {self.victory}')
        #all victory positions have been checked
        #and self.victory is either True or False now
        if self.victory:
            if self.winner == 1:
                show = 'X'
            else:
                show = 'O'
            pygame.display.set_caption(f"Tic Tac Toe - {show} won!")
            red = (170, 0, 0)
            start = self.convert_pos(self.victory_layout[0]+1)
            end = self.convert_pos(self.victory_layout[2]+1)
            pygame.draw.line(self.screen, red, start, end, 3)
            pygame.display.flip()
            time.sleep(4)
            self.setup()
        #check to see if there was a cat
        cat = True
        for position in range(len(self.positions)):
            #then there is still a position that hasn't been played
            if self.positions[position] == 0:
                cat = False
        if cat:
            pygame.display.set_caption(f"Tic Tac Toe - Cat!")
            time.sleep(4)
            self.setup()
            

        return

    def reset(self):

        return

    def run(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                    break
                #event hooks go here
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self.get_pos(event.pos)
                    self.player_mark(pos)
                    #self.computer_moves()
                    pygame.display.flip()
                    self.check_victory()


        return


if __name__ == "__main__":
    game = GAME()
    game.setup()
    game.run()
