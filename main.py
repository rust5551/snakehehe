import pygame
import pygame.freetype
import random
import math

class SnakeGame():
    def __init__(self):
        pygame.init()
        self.font = pygame.freetype.Font(None, 40)
        self.screen = pygame.display.set_mode((1000, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.my_image = pygame.Surface((1000, 720), pygame.SRCALPHA)
        pygame.draw.rect(self.my_image, (0, 0, 0, 200), self.my_image.get_rect())
        self.restart()
        self.spawn_apple()
        self.create_grid()
        self.game()

    def game(self):
        self.key = 'w'
        ticks = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key in [119, 97, 115, 100]:
                        self.key = chr(event.key)
                        self.keys.append(chr(event.key))
                    elif event.key == 114 and self.lost:
                        self.restart()
            
            if not self.lost:
                if ticks == 10:
                    ticks = 0
                    if self.keys:
                        self.key = self.keys.pop(0)
                    self.move(self.key)

                    self.drawing()
                    pygame.display.flip() 
                    self.screen.fill('black')
                else:
                    ticks += 1
            else:
                self.over_screen()

            self.clock.tick(60)

    def move(self, key):
        self.tail.insert(0, self.head[:])
        self.lasttail = self.tail.pop(-1)
        match key:
            case 'w': self.head[1] -= 1
            case 's': self.head[1] += 1
            case 'a': self.head[0] -= 1
            case 'd': self.head[0] += 1
        if self.gameover():
            #print('GANEIVER')
            self.lost = True
        else:
            self.apple_eat()
            self.create_grid()
            self.eyes()

    def restart(self):
        self.grid = [[''] * 20 for _ in range(20)]
        self.head = [9, 16]
        self.tail = [[9, 17], [9, 18]]
        self.apple = [0, 0]
        self.lost = False
        self.score = 0
        self.spawn_apple()
        self.create_grid()
        self.key = "w"
        self.keys = []

    def apple_eat(self):
        if self.head == self.apple:
            self.score += 1
            self.tail.append(self.lasttail)
            self.spawn_apple()

    def gameover(self):
        if (self.head[0] < 0 or self.head[0] > 19 or
            self.head[1] < 0 or self.head[1] > 19 or
            self.head in self.tail):
            return True
        return False
    
    def over_screen(self):
        self.screen.blit(self.my_image, self.my_image.get_rect())
        self.font.render_to(self.screen, (300, 150), f"Игра окончена", (255, 255, 255))
        self.font.render_to(self.screen, (150, 250), f"Нажмите R чтобы начать заново", (255, 255, 255))
        pygame.display.flip() 
        self.drawing()

    def create_grid(self):
        self.grid = [[''] * 20 for _ in range(20)]
        self.grid[self.head[1]][self.head[0]] = '@'
        for i in self.tail:
            self.grid[i[1]][i[0]] = '#'
        self.grid[self.apple[1]][self.apple[0]] = 'a'

    def spawn_apple(self):
        self.apple = [random.randint(0, 19), random.randint(0, 19)]
        while self.apple == self.head or self.apple in self.tail:
            self.apple = [random.randint(0, 19), random.randint(0, 19)]

    def eyes(self):
        a = self.head[0] - self.apple[0]
        b = self.head[1] - self.apple[1]

        c = (a * a + b * b) ** 0.5

        if b <= 0:
            angle = math.degrees(math.acos(a / c))
        else:
            angle = 360 - math.degrees(math.acos(a / c))
        
        eyespos = {180: (18, 32), 202.5: (18, 31), 225: (18, 30), 247.5: (17, 30),
                   270: (16, 30), 292.5: (15, 30), 315: (14, 30), 337.5: (14, 31),
                   0: (14, 32), 22.5: (14, 33), 45: (14, 34), 67.5: (15, 34),
                   90: (16, 34), 112.5: (17, 34), 135: (18, 34), 157.5: (18, 33),}


        self.eyedir = eyespos[min(eyespos, key=lambda x:abs(x-angle))]  
        

    def drawing(self):
        # Snake
        pygame.draw.rect(self.screen, '#393939', (9, 9, 32 * 20 + 1, 32 * 20 + 1))
        for linenum, line in enumerate(self.grid):
            for tilenum, tile in enumerate(line):
                if tile == '': # Grid tiles
                    pygame.draw.rect(self.screen, 'black', (10 + 32 * tilenum, 10 + 32 * linenum, 31, 31))
                elif tile == '@': # Snake head
                    pygame.draw.rect(self.screen, '#0bae00', (10 + 32 * tilenum, 10 + 32 * linenum, 31, 31))
                    # This is abomination and i'm not proud of it

                    if self.key == 'w':
                        pygame.draw.circle(self.screen, 'gray', (16 + 32 * tilenum, 16 + 32 * linenum), 4)
                        pygame.draw.circle(self.screen, 'gray', (32 + 32 * tilenum, 16 + 32 * linenum), 4)
                        pygame.draw.circle(self.screen, 'black', (self.eyedir[0] + 32 * tilenum, self.eyedir[1] - 16 + 32 * linenum), 3)
                        pygame.draw.circle(self.screen, 'black', (self.eyedir[0] + 16 + 32 * tilenum, self.eyedir[1] - 16 + 32 * linenum), 3)
                    elif self.key == 's':
                        pygame.draw.circle(self.screen, 'gray', (16 + 32 * tilenum, 32 + 32 * linenum), 4)
                        pygame.draw.circle(self.screen, 'gray', (32 + 32 * tilenum, 32 + 32 * linenum), 4)
                        pygame.draw.circle(self.screen, 'black', (self.eyedir[0] + 32 * tilenum, self.eyedir[1] + 32 * linenum), 3)
                        pygame.draw.circle(self.screen, 'black', (self.eyedir[0] + 16 + 32 * tilenum, self.eyedir[1] + 32 * linenum), 3)
                    elif self.key == 'a':
                        pygame.draw.circle(self.screen, 'gray', (16 + 32 * tilenum, 16 + 32 * linenum), 4)
                        pygame.draw.circle(self.screen, 'gray', (16 + 32 * tilenum, 32 + 32 * linenum), 4)
                        pygame.draw.circle(self.screen, 'black', (self.eyedir[0] + 32 * tilenum, self.eyedir[1] - 16 + 32 * linenum), 3)
                        pygame.draw.circle(self.screen, 'black', (self.eyedir[0] + 32 * tilenum, self.eyedir[1] + 32 * linenum), 3)
                    elif self.key == 'd':
                        pygame.draw.circle(self.screen, 'gray', (32 + 32 * tilenum, 16 + 32 * linenum), 4)
                        pygame.draw.circle(self.screen, 'gray', (32 + 32 * tilenum, 32 + 32 * linenum), 4)
                        pygame.draw.circle(self.screen, 'black', (self.eyedir[0] + 16 + 32 * tilenum, self.eyedir[1] - 16 + 32 * linenum), 3)
                        pygame.draw.circle(self.screen, 'black', (self.eyedir[0] + 16 + 32 * tilenum, self.eyedir[1] + 32 * linenum), 3)

                elif tile == '#': # Snake tail
                    pygame.draw.rect(self.screen, '#077300', (10 + 32 * tilenum, 10 + 32 * linenum, 31, 31))
                elif tile == 'a': # Aple hehe
                    pygame.draw.rect(self.screen, 'red', (10 + 32 * tilenum, 10 + 32 * linenum, 31, 31))

        # For debug

        #pygame.draw.line(self.screen, 'white', (self.head[0] * 32 + 26, self.head[1] * 32 + 26), (self.apple[0] * 32 + 26, self.apple[1] * 32 + 26))

        
        # UI
        self.font.render_to(self.screen, (700, 30), f"Счёт: {self.score}", (255, 255, 255))

a = SnakeGame()