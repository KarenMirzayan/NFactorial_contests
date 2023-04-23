import pygame, math

class Firstcircle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = (0, 255, 0)
        self.image = pygame.surface.Surface((20, 20), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.color, self.rect.center, 10)
        self.rect.center = (1000, 1000)

    def draw(self, screen, x, y):
        self.rect.center = (x, y)
        screen.blit(self.image, (x-10, y-10))

class Lastcircle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface((10, 10), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = (900, 900)

    def draw(self, screen, x, y, color):
        pygame.draw.circle(self.image, color, self.rect.center, 5)
        self.rect.center = (x, y)
        screen.blit(self.image, (x-5, y-5))
        

WIDTH = 800
HEIGHT = 800

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Perfect Circle')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.surface.Surface((WIDTH, HEIGHT))
bg.fill("Black")
pygame.draw.circle(bg, "Grey", (400, 400), 10, 0)
pygame.draw.circle(bg, "Grey", (400, 400), 50, 1)
screen.blit(bg, (0, 0))

blackbg = pygame.surface.Surface((69, 20))
blackbg.fill("Black")
blackbg_rect = blackbg.get_rect().center

bigblackbg = pygame.surface.Surface((115, 34))
bigblackbg.fill("Black")
bigblackbg_rect = blackbg.get_rect().center

R = 0
G = 255
R_temp = R
G_temp = G
color = (R, G, 0)

r = 0
r_temp = 0
p = 0
list = [255]
coord_list = []
score = 0
highscore = 0

C_first = Firstcircle()
firstcircle = pygame.sprite.Group()
firstcircle.add(C_first)

C_last = Lastcircle()
lastcircle = pygame.sprite.Group()
lastcircle.add(C_last)

all_sprites = pygame.sprite.Group()
all_sprites.add([C_first, C_last])


tooclose = False
circleisclosed = False
press_space = True

font = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

percentage_txt = font_small.render("{}%".format(100.0), True, "Green", "Black")
percentage_txt_rect = percentage_txt.get_rect().center
screen.blit(percentage_txt, (400-percentage_txt_rect[0], 700-percentage_txt_rect[1]))

tooclose_txt = font.render("Too close!", True, "Red")
tooclose_txt_rect = tooclose_txt.get_rect().center

tooslow_txt = font.render("Too slow!", True, "Red")
tooslow_txt_rect = tooslow_txt.get_rect().center

circleisnot = font.render("Draw a full circle!", True, "Red")
circleisnot_rect = circleisnot.get_rect().center

space = font.render("Press SPACE to try again", True, "White")
space_rect = space.get_rect().center

running = True
is_mouse_down = False

TOOSLOW = pygame.USEREVENT + 1

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            for entity in all_sprites:
                entity.kill()
            running = False
            pygame.quit()
            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                for entity in all_sprites:
                    entity.kill()
                running = False
                pygame.quit()
            if event.key == pygame.K_SPACE:
                R = 0
                G = 255
                R_temp = R
                G_temp = G
                color = (R, G, 0)
                r = 0
                r_temp = 0
                p = 0
                score = 0
                tooclose = False
                circleisclosed = False
                is_mouse_down = False
                press_space = True
                highscore_txt = font.render("{0:.1f}%".format(highscore), True, (int(255*(1-(highscore/100))), int(255*(highscore/100)), 0), "Black")
                bg.blit(bigblackbg, (0, 0))
                bg.blit(highscore_txt, (0, 0))
                screen.blit(bg, (0, 0))
                list = [255]
                coord_list = []


        if event.type == pygame.MOUSEBUTTONDOWN and press_space:
            x = event.pos[0]
            y = event.pos[1]
            r = math.sqrt((abs(400-x))**2 + (abs(400-y))**2)
            if r <= 50:
                tooclose = True
            C_first.draw(screen, x, y)
            is_mouse_down = True
            pygame.time.set_timer(TOOSLOW, 8000, 1)

        if event.type == pygame.MOUSEBUTTONUP and press_space:
            x = event.pos[0]
            y = event.pos[1]
            C_last.draw(screen, x, y, color)
            is_mouse_down = False
            if pygame.sprite.spritecollideany(C_first, lastcircle) and len(coord_list) > 75:
                circleisclosed = True
                score = (sum(list)/len(list))/255 * 100
                if score > highscore:
                    highscore = score
                circleisclosed_txt = font.render("Your accuracy is {0:.1f}%".format(score), True, "White")
                circleisclosed_txt_rect = circleisclosed_txt.get_rect().center
                screen.fill("Black")
                screen.blit(circleisclosed_txt, (400-circleisclosed_txt_rect[0], 200-circleisclosed_txt_rect[1]))
                screen.blit(space, (400-space_rect[0], 235-space_rect[1]))
                C_first.rect.center = (1000, 1000)
                C_last.rect.center = (900, 900)
                press_space = False
            else:
                circleisclosed = False
                screen.fill("Black")
                screen.blit(circleisnot, (400-circleisnot_rect[0], 200-circleisnot_rect[1]))
                screen.blit(space, (400-space_rect[0], 235-space_rect[1]))
                C_first.rect.center = (1000, 1000)
                C_last.rect.center = (900, 900)
                press_space = False
            pygame.time.set_timer(TOOSLOW, 0)


        if event.type == pygame.MOUSEMOTION and press_space:
            if is_mouse_down == True:
                x = event.pos[0]
                y = event.pos[1]
                if (x, y) not in coord_list:
                    coord_list.append((x, y))
                    r_temp = math.sqrt((abs(400-x))**2 + (abs(400-y))**2)
                    if r_temp <= 50:
                        tooclose = True
                    p = (abs(r_temp - r))/(r/2)
                    percentage_txt = font_small.render("{0:.1f}%".format((sum(list)/len(list))/255 * 100), True, (int(255*(1 - (sum(list)/len(list))/255)), int(255*(sum(list)/len(list))/255), 0), "Black")
                    percentage_txt_rect = percentage_txt.get_rect().center
                    screen.blit(blackbg, (400-blackbg_rect[0], 700-blackbg_rect[1]))
                    screen.blit(percentage_txt, (400-percentage_txt_rect[0], 700-percentage_txt_rect[1]))
                    pygame.draw.circle(screen, color, (x, y), 5)


        if event.type == TOOSLOW:
            press_space = False
            screen.fill("Black")
            screen.blit(tooslow_txt, (400-tooslow_txt_rect[0], 200-tooslow_txt_rect[1]))
            screen.blit(space, (400-space_rect[0], 235-space_rect[1]))
            

    
    if r_temp != r:
        r_temp_prev = r_temp
        R_temp = int(round(G * (1.2*p)))
        G_temp = int(round(G * (1 - (1.2*p))))
        if G_temp >= 0 and G_temp <= 255 and R_temp >=0 and R_temp <= 255:
            color = (R_temp, G_temp, 0)
            list.append(G_temp)
        else:
            color = (255, 0, 0)
            list.append(0)
    
    if tooclose:
        screen.fill("Black")
        screen.blit(tooclose_txt, (400-tooclose_txt_rect[0], 200-tooclose_txt_rect[1]))
        screen.blit(space, (400-space_rect[0], 235-space_rect[1]))
        press_space = False
    
    pygame.display.update()
    clock.tick(144)
pygame.quit()
quit()