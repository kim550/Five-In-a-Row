import pygame
import random
import copy

screen = pygame.display.set_mode((600, 600))
pygame.init()
pygame.display.set_caption('五子棋')

fpsclock = pygame.time.Clock()

def fill_text(surface, font, text, pos, color=(0, 0, 0), shadow=False, center=False):
    text1 = font.render(text, True, color)
    text_rect = text1.get_rect()
    if shadow:
        text2 = font.render(text, True, (255 - color[0], 255 - color[1], 255 - color[2]))
        for p in [(pos[0] - 1, pos[1] - 1),
                  (pos[0] + 1, pos[1] - 1),
                  (pos[0] - 1, pos[1] + 1),
                  (pos[0] + 1, pos[1] + 1)]:
            if center:
                text_rect.center = p
            else:
                text_rect.x = p[0]
                text_rect.y = p[1]
            screen.blit(text2, text_rect)
    if center:
        text_rect.center = pos
    else:
        text_rect.x = pos[0]
        text_rect.y = pos[1]
    screen.blit(text1, text_rect)

class Chessman:
    def __init__(self, turn):
        self.turn = turn
        self.color = (255, 255, 255) if turn else (0, 0, 0)
        self.visible = True
        self.x = 0
        self.y = 0
        self.time = pygame.time.get_ticks()
        self.flash = 0 if turn == computer else 2
    def draw(self):
        if self.flash <= 1:
            current = pygame.time.get_ticks()
            if current - self.time >= 300:
                self.visible = not self.visible
                self.flash += 1
                self.time = current
        if self.visible:
            pygame.draw.circle(screen, self.color, (self.x, self.y), 13, 0)

class Entry:
    def __init__(self, chess, ix, iy, mode, num):
        self.chess = chess
        self.enemy = int(not self.chess)
        self.startix = ix
        self.startiy = iy
        self.mode = mode
        self.num = num
        if mode == 1:
            self.stopix = ix + num
            self.stopiy = iy
            self.stepix = 1
            self.stepiy = 0
        elif mode == 2:
            self.stopix = ix
            self.stopiy = iy + num
            self.stepix = 0
            self.stepiy = 1
        elif mode == 3:
            self.stopix = ix + num
            self.stopiy = iy + num
            self.stepix = 1
            self.stepiy = 1
        elif mode == 4:
            self.stopix = ix + num
            self.stopiy = iy - num
            self.stepix = 1
            self.stepiy = -1
        self.previx = self.startix - self.stepix
        self.previy = self.startiy - self.stepiy
        self.nextix = self.stopix + self.stepix
        self.nextiy = self.stopiy + self.stepiy
        self.pholeix = self.previx - self.stepix
        self.pholeiy = self.previy - self.stepiy
        self.nholeix = self.nextix + self.stepix
        self.nholeiy = self.nextiy + self.stepiy
    def check(self):
        res = [False, False]
        try:
            if chessboard[self.previx][self.previy] == self.enemy:
                res[0] = True
        except IndexError:
            pass
        try:
            if chessboard[self.nextix][self.nextiy] == self.enemy:
                res[1] = True
        except IndexError:
            pass
        return res
    def hole(self):
        res = [False, False]
        try:
            if chessboard[self.pholeix][self.pholeiy] == self.chess and chessboard[self.previx][self.previy] == -1:
                res[0] = True
        except IndexError:
            pass
        try:
            if chessboard[self.nholeix][self.nholeiy] == self.chess and chessboard[self.nextix][self.nextiy] == -1:
                res[1] = True
        except IndexError:
            pass
        return res

def draw_board():
    pygame.draw.rect(screen, (0, 0, 0), (20, 20, 560, 560), 2)
    for i in range(20, 580, 28):
        pygame.draw.line(screen, (0, 0, 0), (20, i), (580, i), 1)
        pygame.draw.line(screen, (0, 0, 0), (i, 20), (i, 580), 1)
    pygame.draw.circle(screen, (0, 0, 0), (300, 300), 3, 0)
    for chessman in chessmen:
        chessman.draw()

def set_chessman(mx, my, ix, iy):
    global begin
    if ix is not None or 6 <= mx < 594 and 6 <= my < 594:
        chessman = Chessman(turn)
        if begin:
            ix = 10
            iy = 10
            x = 300
            y = 300
        else:
            if ix is None:
                mx -= 6
                my -= 6
                ix = mx // 28
                iy = my // 28
            x = 20 + ix * 28
            y = 20 + iy * 28
            for chess in chessmen:
                if chess.x == x and chess.y == y:
                    return 0
        chessman.x = x
        chessman.y = y
        chessmen.append(chessman)
        chessboard[ix][iy] = int(turn)
        begin = False
        return (ix, iy)
    return 0

def has2(chessboard, chs):
    _2 = []
    for ix, line in enumerate(chessboard):
        for iy, chess in enumerate(line):
            if chess == chs:
                try:
                    if chessboard[ix + 1][iy] == chess:
                        _2.append((ix, iy, 1))
                except:
                    pass
                try:
                    if chessboard[ix][iy + 1] == chess:
                        _2.append((ix, iy, 2))
                except:
                    pass
                try:
                    if chessboard[ix + 1][iy + 1] == chess:
                        _2.append((ix, iy, 3))
                except:
                    pass
                try:
                    if chessboard[ix + 1][iy - 1] == chess:
                        _2.append((ix, iy, 4))
                except:
                    pass
    return _2

def has3(chessboard, chs):
    _3 = []
    for ix, line in enumerate(chessboard):
        for iy, chess in enumerate(line):
            if chess == chs:
                try:
                    if (chessboard[ix + 1][iy] == chess and
                        chessboard[ix + 2][iy] == chess):
                        _3.append((ix, iy, 1))
                except:
                    pass
                try:
                    if (chessboard[ix][iy + 1] == chess and
                        chessboard[ix][iy + 2] == chess):
                        _3.append((ix, iy, 2))
                except:
                    pass
                try:
                    if (chessboard[ix + 1][iy + 1] == chess and
                        chessboard[ix + 2][iy + 2] == chess):
                        _3.append((ix, iy, 3))
                except:
                    pass
                try:
                    if (chessboard[ix + 1][iy - 1] == chess and
                        chessboard[ix + 2][iy - 2] == chess):
                        _3.append((ix, iy, 4))
                except:
                    pass
    return _3

def has4(chessboard, chs):
    _4 = []
    for ix, line in enumerate(chessboard):
        for iy, chess in enumerate(line):
            if chess == chs:
                try:
                    if (chessboard[ix + 1][iy] == chess and
                        chessboard[ix + 2][iy] == chess and
                        chessboard[ix + 3][iy] == chess):
                        _4.append((ix, iy, 1))
                except:
                    pass
                try:
                    if (chessboard[ix][iy + 1] == chess and
                        chessboard[ix][iy + 2] == chess and
                        chessboard[ix][iy + 3] == chess):
                        _4.append((ix, iy, 2))
                except:
                    pass
                try:
                    if (chessboard[ix + 1][iy + 1] == chess and
                        chessboard[ix + 2][iy + 2] == chess and
                        chessboard[ix + 3][iy + 3] == chess):
                        _4.append((ix, iy, 3))
                except:
                    pass
                try:
                    if (chessboard[ix + 1][iy - 1] == chess and
                        chessboard[ix + 2][iy - 2] == chess and
                        chessboard[ix + 3][iy - 3] == chess):
                        _4.append((ix, iy, 4))
                except:
                    pass
    return _4

def has5(chessboard, chs):
    _5 = []
    for ix, line in enumerate(chessboard):
        for iy, chess in enumerate(line):
            if chess == chs:
                try:
                    if (chessboard[ix + 1][iy] == chess and
                        chessboard[ix + 2][iy] == chess and
                        chessboard[ix + 3][iy] == chess and
                        chessboard[ix + 4][iy] == chess):
                        _5.append((ix, iy, 1))
                except:
                    pass
                try:
                    if (chessboard[ix][iy + 1] == chess and
                        chessboard[ix][iy + 2] == chess and
                        chessboard[ix][iy + 3] == chess and
                        chessboard[ix][iy + 4] == chess):
                        _5.append((ix, iy, 2))
                except:
                    pass
                try:
                    if (chessboard[ix + 1][iy + 1] == chess and
                        chessboard[ix + 2][iy + 2] == chess and
                        chessboard[ix + 3][iy + 3] == chess and
                        chessboard[ix + 4][iy + 4] == chess):
                        _5.append((ix, iy, 3))
                except:
                    pass
                try:
                    if (chessboard[ix + 1][iy - 1] == chess and
                        chessboard[ix + 2][iy - 2] == chess and
                        chessboard[ix + 3][iy - 3] == chess and
                        chessboard[ix + 4][iy - 4] == chess):
                        _5.append((ix, iy, 4))
                except:
                    pass
    return _5

def process(num, turn, resn, hole):
    s = [has2, has3, has4][num - 2](chessboard, turn)
    for n in s:
        entry = Entry(turn, *n, num - 1)
        if hole:
            res = entry.hole()
            if res[0]:
                if set_chessman(None, None, entry.previx, entry.previy):
                    return 1
            if res[1]:
                if set_chessman(None, None, entry.nextix, entry.nextiy):
                    return 1
        else:
            res = entry.check()
            s = sum(res)
            if s == 2 - resn:
                if set_chessman(None, None, entry.previx, entry.previy):
                    return 1
                if set_chessman(None, None, entry.nextix, entry.nextiy):
                    return 1

def computer_turn1():
    scores = {}
    last5 = len(has5(chessboard, computer))
    cb = copy.deepcopy(chessboard)
    for ix, line in enumerate(cb):
        for iy, chess in enumerate(line):
            if chess == -1:
                cb[ix][iy] = computer
                now5 = len(has5(cb, computer))
                cb[ix][iy] = -1
                if now5 - last5 > 0:
                    return set_chessman(None, None, ix, iy)

def computer_turn2():
    scores = {}
    last5 = len(has5(chessboard, player))
    cb = copy.deepcopy(chessboard)
    for ix, line in enumerate(cb):
        for iy, chess in enumerate(line):
            if chess == -1:
                cb[ix][iy] = player
                now5 = len(has5(cb, player))
                cb[ix][iy] = -1
                if now5 - last5 > 0:
                    return set_chessman(None, None, ix, iy)

def computer_turn3():
    if (process(4, computer, 2, False) or process(4, computer, 1, False) or
        process(3, computer, 2, True) or process(3, player, 2, True) or
        process(4, player, 2, False) or process(4, player, 1, False) or
        process(3, computer, 2, False) or process(3, player, 2, False) or
        process(3, computer, 1, True) or process(3, player, 1, True) or
        process(3, computer, 1, False) or process(2, computer, 2, True) or
        process(2, player, 2, True) or process(3, player, 1, False)):
        return 1

def computer_turn4():
    scores = {}
    last2 = len(has2(chessboard, player))
    last3 = len(has3(chessboard, player))
    last4 = len(has4(chessboard, player))
    cb = copy.deepcopy(chessboard)
    for ix, line in enumerate(cb):
        for iy, chess in enumerate(line):
            if chess == -1:
                cb[ix][iy] = player
                now2 = len(has2(cb, player))
                now3 = len(has3(cb, player))
                now4 = len(has4(cb, player))
                score = (now2 - last2) + (now3 - last3) * 2 + (now4 - last4) * 4
                if score > 2:
                    scores[score] = (ix, iy)
                cb[ix][iy] = -1
    for score in sorted(scores.keys(), reverse=True):
        if set_chessman(None, None, scores[score][0], scores[score][1]):
            return 1

def computer_turn5():
    scores = {}
    last2 = len(has2(chessboard, computer))
    last3 = len(has3(chessboard, computer))
    last4 = len(has4(chessboard, computer))
    cb = copy.deepcopy(chessboard)
    for ix, line in enumerate(cb):
        for iy, chess in enumerate(line):
            if chess == -1:
                cb[ix][iy] = computer
                now2 = len(has2(cb, computer))
                now3 = len(has3(cb, computer))
                now4 = len(has4(cb, computer))
                score = (now2 - last2) + (now3 - last3) * 2 + (now4 - last4) * 4
                if score > 3:
                    scores[score] = (ix, iy)
                cb[ix][iy] = -1
    for score in sorted(scores.keys(), reverse=True):
        if set_chessman(None, None, scores[score][0], scores[score][1]):
            return 1

def computer_turn6():
    if (process(2, computer, 2, False) or process(2, player, 2, False) or
        process(2, computer, 1, False) or process(2, player, 1, False)):
        return 1

def computer_turn7():
    scores = {}
    last2 = len(has2(chessboard, computer))
    last3 = len(has3(chessboard, computer))
    last4 = len(has4(chessboard, computer))
    cb = copy.deepcopy(chessboard)
    for ix, line in enumerate(cb):
        for iy, chess in enumerate(line):
            if chess == -1:
                cb[ix][iy] = computer
                now2 = len(has2(cb, computer))
                now3 = len(has3(cb, computer))
                now4 = len(has4(cb, computer))
                score = (now2 - last2) + (now3 - last3) * 2 + (now4 - last4) * 4
                if score > 0:
                    scores[score] = (ix, iy)
                cb[ix][iy] = -1
    for score in sorted(scores.keys(), reverse=True):
        if set_chessman(None, None, scores[score][0], scores[score][1]):
            return 1

def computer_turn8():
    ixiys = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x != 0 or y != 0:
                ixiys.append((playerix + x, playeriy + y))
    i = random.randrange(0, len(ixiys))
    ix, iy = ixiys[i]
    while not set_chessman(None, None, ix, iy):
        del ixiys[i]
        if not ixiys:
            return 0
        i = random.randrange(0, len(ixiys))
        ix, iy = ixiys[i]
    return 1

def computer_turn():
    if computer_turn1():
        return
    if computer_turn2():
        return
    if computer_turn3():
        return
    if computer_turn4():
        return
    if computer_turn5():
        return
    if computer_turn6():
        return
    if computer_turn7():
        return
    if computer_turn8():
        return
    while not set_chessman(random.randint(6, 595), random.randint(6, 595), None, None):
        pass

def check_win():
    global win
    for ix, line in enumerate(chessboard):
        for iy, chess in enumerate(line):
            if chess != -1:
                try:
                    if (chessboard[ix + 1][iy] == chess and
                        chessboard[ix + 2][iy] == chess and
                        chessboard[ix + 3][iy] == chess and
                        chessboard[ix + 4][iy] == chess):
                        win = chess
                        return
                except:
                    pass
                try:
                    if (chessboard[ix][iy + 1] == chess and
                        chessboard[ix][iy + 2] == chess and
                        chessboard[ix][iy + 3] == chess and
                        chessboard[ix][iy + 4] == chess):
                        win = chess
                        return
                except:
                    pass
                try:
                    if (chessboard[ix + 1][iy + 1] == chess and
                        chessboard[ix + 2][iy + 2] == chess and
                        chessboard[ix + 3][iy + 3] == chess and
                        chessboard[ix + 4][iy + 4] == chess):
                        win = chess
                        return
                except:
                    pass
                try:
                    if (chessboard[ix + 1][iy - 1] == chess and
                        chessboard[ix + 2][iy - 2] == chess and
                        chessboard[ix + 3][iy - 3] == chess and
                        chessboard[ix + 4][iy - 4] == chess):
                        win = chess
                        return
                except:
                    pass

chessmen = []
chessboard = [[-1] * 21 for i in range(21)]
turn = False
computer = True
player = False
win = -1
begin = True
playerix = -1
playeriy = -1
lastplayer = pygame.time.get_ticks()

font = pygame.font.SysFont('fangsong', 30)
shadow = pygame.Surface((600, 40)).convert_alpha()
shadow.fill((0, 0, 0, 100))

while True:
    screen.fill((180, 150, 0))
    draw_board()
    if win == -1:
        if turn == computer:
            current = pygame.time.get_ticks()
            if current - lastplayer >= 200:
                computer_turn()
                turn = not turn
                check_win()
    elif win == computer:
        screen.blit(shadow, (0, 280))
        fill_text(screen, font, '哦，电脑赢了。', (300, 300), shadow=True, center=True)
    elif win == player:
        screen.blit(shadow, (0, 280))
        fill_text(screen, font, '你赢了！', (300, 300), shadow=True, center=True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if win == -1 and turn == player:
                    res = set_chessman(*event.pos, None, None)
                    if res:
                        playerix, playeriy = res
                        turn = not turn
                        lastplayer = pygame.time.get_ticks()
                        check_win()
    pygame.display.update()
    fpsclock.tick(30)
