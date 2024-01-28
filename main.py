import pygame
from fighter import Fighter


pygame.init()

#Create a game window

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("PROJECT SB")

#Create Framerate...
clock = pygame.time.Clock()
FPS = 60

#Define colors...
RED = (250, 0, 0)
YELLOW = (250, 250, 0)
WHITE = (250, 250, 250)
GREEN = (0, 255, 0)
CYAN = (0, 250, 250)
BLACK = (0, 0, 0)


#Define game varriables...
intro_count = 3
last_count_upadte = pygame.time.get_ticks()
score = [0,0] #Defines scores...[P1,P2]
round_over = False
ROUND_OVER_COOLDOWN = 3000

#Define fighter varriables...
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

#load sounds...
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#Load Background Image
bg_img = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

#Load Spritesheets...
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

#Load Victory...
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#Fighter Animation Steps...
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 2, 8, 8, 3, 7]

#Define fonts...
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
intro_font = pygame.font.Font("assets/fonts/turok.ttf", 50)

#function for drawing texts...
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x,y))

#Function for drawing background...
def draw_bg():
	scaled_bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH,SCREEN_HEIGHT))
	screen.blit(scaled_bg, (0,0))

#Function for drawing health bars..
def draw_health_bar(health,x,y):
	ratio = health / 100
	pygame.draw.rect(screen, WHITE, (x-2, y-2, 404, 34))
	pygame.draw.rect(screen, RED, (x, y, 400, 30))
	pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


#For two fighter instances
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#Game Loop
run = True

while run:

	clock.tick(FPS)

	#Draw Background
	draw_bg()

	#Showing Fighter Stats
	draw_health_bar(fighter_1.health, 20, 20)
	draw_health_bar(fighter_2.health, 580, 20)
	draw_text("P1: " + str(score[0]), score_font, CYAN, 20, 60)
	draw_text("P2: " + str(score[1]), score_font, CYAN, 580, 60)

	if intro_count <= 0:
	#movements
		fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT,fighter_2, round_over)
		fighter_2.move(SCREEN_WIDTH,SCREEN_HEIGHT,fighter_1, round_over)
	else:
		#diplay count timer
		draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
		#update count...
		if (pygame.time.get_ticks() - last_count_upadte) >= 1000:
			intro_count -= 1
			last_count_upadte = pygame.time.get_ticks()

	#Update fighter
	fighter_1.update()
	fighter_2.update()

	#Draw Fighters
	fighter_1.draw(screen)
	fighter_2.draw(screen)

	#check for player get defeated...
	if round_over == False:
		if fighter_1.alive == False and fighter_2.alive == False:
			round_over = True
			round_over_time = pygame.time.get_ticks()			
		elif fighter_2.alive == False:
			score[0] += 1
			round_over = True
			round_over_time = pygame.time.get_ticks()
			#print(score)
		elif fighter_1.alive == False:
			score[1] += 1
			round_over = True
			round_over_time = pygame.time.get_ticks()
			#print(score)
	else:
		#display vicotry...
		"""screen.blit(victory_img, (360, 150))"""
		if fighter_1.alive == False and fighter_2.alive == False:
			draw_text("DRAW!", intro_font, BLACK, SCREEN_WIDTH / 2.4, SCREEN_HEIGHT / 3)
		elif fighter_2.alive == False:
			draw_text("Player 1 wins!", intro_font, GREEN, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3)
		elif fighter_1.alive == False:
			draw_text("Player 2 wins!", intro_font, GREEN, SCREEN_WIDTH/ 3, SCREEN_HEIGHT / 3)

		#reset...
		if (pygame.time.get_ticks() - round_over_time) > ROUND_OVER_COOLDOWN:
			round_over = False
			intro_count = 3
			fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
			fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

	#Event Handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	#Update display
	pygame.display.update()


#EXIT PyGame...
pygame.quit()