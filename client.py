import pygame
from network import Network
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

result_text = ""
class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Arial", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((231,237,215))

    if not(game.connected()):
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("Waiting for Player...", 1, (255,118,130), (231,237,215))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("Your Move", 1, (90, 160, 141))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (90, 160, 141))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (255, 92, 0))
            text2 = font.render(move2, 1, (255, 92, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (172, 153, 193))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (172, 153, 193))
            else:
                text1 = font.render("Player 1", 1, (107, 167, 214))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (172, 153, 193))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (172, 153, 193))
            else:
                text2 = font.render("Player 2", 1, (107, 167, 214))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

        font = pygame.font.SysFont("Arial", 90)
        result = font.render(result_text, 1, (0, 0, 0))
        win.blit(result, (width/2 - result.get_width()/2, height/8 - result.get_height()/8))

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0,121, 231)), Button("Scissors", 250, 500, (255, 71, 92)), Button("Paper", 450, 500, (165,119,249))]
def main():
    global result_text
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print(f"You are player {player}")

    while run:
        clock.tick(60)
        try:
            game = n.send(("GET_GAME", None))
            print(f"Received game state: {game.__dict__}")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send(("RESET", None))
                print("Game reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("Arial", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (18, 247, 41))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 195, 77))
            else:
                text = font.render("You Lost", 1, (255, 64, 35))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 8 - text.get_height() / 8))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                n.send(("DISCONNECT", None))
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(("MOVE", btn.text))
                                print(f"Sent move: {btn.text}")
                        else:
                            if not game.p2Went:
                                n.send(("MOVE", btn.text))
                                print(f"Sent move: {btn.text}")

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((231, 237, 215))
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("Click to Play!", 1, (255, 255, 255))
        win.blit(text, (150, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()




