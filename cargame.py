import pygame
import random

# Pygame'i başlatma
pygame.init()

# Ekran boyutları
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (120, 120, 120)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)

# Yol boyutları
road_width = 300
road_x = screen_width // 2 - road_width // 2

# Araba boyutları
car_width = 50
car_height = 100

# Duba boyutları
cone_width = 30
cone_height = 50

# Ağaç boyutları
# (gövde ve yaprak için)
tree_trunk_width = 20
tree_trunk_height = 40
tree_leaves_radius = 30

def draw_road(road_lines):
    pygame.draw.rect(screen, GRAY, (road_x, 0, road_width, screen_height))
    # Yol çizgileri
    for y in road_lines:
        pygame.draw.rect(screen, WHITE, (screen_width//2 - 5, y, 10, 40))

# Araba sınıfı
class Car:
    def __init__(self):
        self.x = screen_width // 2 - car_width // 2
        self.y = screen_height - car_height - 10
        self.speed = 5

    def draw(self):
        # Araba gövdesi
        pygame.draw.rect(screen, BLUE, (self.x, self.y + 20, car_width, car_height - 20), border_radius=12)
        # Cam
        pygame.draw.rect(screen, (180, 220, 255), (self.x + 8, self.y + 25, car_width - 16, 35), border_radius=8)
        # Tekerlekler
        pygame.draw.ellipse(screen, BLACK, (self.x + 5, self.y + car_height - 20, 15, 15))
        pygame.draw.ellipse(screen, BLACK, (self.x + car_width - 20, self.y + car_height - 20, 15, 15))
        pygame.draw.ellipse(screen, BLACK, (self.x + 5, self.y + 10, 15, 15))
        pygame.draw.ellipse(screen, BLACK, (self.x + car_width - 20, self.y + 10, 15, 15))
        # Farlar
        pygame.draw.circle(screen, (255, 255, 100), (self.x + 10, self.y + 20), 6)
        pygame.draw.circle(screen, (255, 255, 100), (self.x + car_width - 10, self.y + 20), 6)

    def move_left(self):
        if self.x > road_x:
            self.x -= self.speed

    def move_right(self):
        if self.x < road_x + road_width - car_width:
            self.x += self.speed

# Duba (engel) sınıfı
class Cone:
    def __init__(self):
        self.x = random.randint(road_x + 20, road_x + road_width - cone_width - 20)
        self.y = -cone_height
        self.width = cone_width
        self.height = cone_height
        self.speed = 7

    def move(self):
        self.y += self.speed

    def draw(self):
        # Duba gövdesi (turuncu üçgen)
        pygame.draw.polygon(screen, (255, 140, 0), [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])
        # Beyaz şerit
        pygame.draw.rect(screen, WHITE, (self.x + 5, self.y + self.height//2, self.width - 10, 8))

# Düşman araba sınıfı
class EnemyCar:
    def __init__(self):
        self.width = car_width
        self.height = car_height
        self.x = random.randint(road_x + 10, road_x + road_width - self.width - 10)
        self.y = -self.height
        self.speed = random.randint(6, 10)

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y + 20, self.width, self.height - 20), border_radius=12)
        pygame.draw.rect(screen, (255, 200, 200), (self.x + 8, self.y + 25, self.width - 16, 35), border_radius=8)
        pygame.draw.ellipse(screen, BLACK, (self.x + 5, self.y + self.height - 20, 15, 15))
        pygame.draw.ellipse(screen, BLACK, (self.x + self.width - 20, self.y + self.height - 20, 15, 15))
        pygame.draw.ellipse(screen, BLACK, (self.x + 5, self.y + 10, 15, 15))
        pygame.draw.ellipse(screen, BLACK, (self.x + self.width - 20, self.y + 10, 15, 15))

# Can bonusu sınıfı
class LifeBonus:
    def __init__(self):
        self.radius = 22
        self.x = random.randint(road_x + 20, road_x + road_width - self.radius*2 - 20)
        self.y = -self.radius*2
        self.speed = 7

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, (0, 200, 0), (self.x + self.radius, self.y + self.radius), self.radius)
        font = pygame.font.SysFont("Arial", 28, bold=True)
        heart = font.render("+1", True, WHITE)
        screen.blit(heart, (self.x + self.radius - heart.get_width()//2, self.y + self.radius - heart.get_height()//2))

# Ana oyun fonksiyonu
def game():
    while True:
        car = Car()
        cones = []
        enemy_cars = []
        bonuses = []
        road_lines = [i for i in range(0, screen_height, 80)]
        clock = pygame.time.Clock()
        running = True
        score = 0
        cone_timer = 0
        enemy_timer = 0
        bonus_timer = 0
        lives = 1
        cones_passed = 0
        bonus_pending = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Tuşlara basılma durumunu kontrol et
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                car.move_left()
            if keys[pygame.K_RIGHT]:
                car.move_right()

            # Yol çizgilerini hareket ettir
            for i in range(len(road_lines)):
                road_lines[i] += 7
                if road_lines[i] > screen_height:
                    road_lines[i] = road_lines[i] - screen_height - 40

            # Yeni duba oluşturma
            cone_timer += 1
            if cone_timer > 35:
                cones.append(Cone())
                cone_timer = 0

            # Yeni düşman araba oluşturma
            enemy_timer += 1
            if enemy_timer > 60:
                if random.random() < 0.5:
                    enemy_cars.append(EnemyCar())
                enemy_timer = 0

            # 15 duba geçilince can bonusu oluştur
            if cones_passed > 0 and cones_passed % 15 == 0 and not bonus_pending:
                bonuses.append(LifeBonus())
                bonus_pending = True
            if cones_passed % 15 != 0:
                bonus_pending = False

            # Dubaları hareket ettir
            for cone in cones[:]:
                cone.move()
                if cone.y > screen_height:
                    cones.remove(cone)
                    score += 2  # Her duba için 2 puan
                    cones_passed += 1

            # Düşman arabaları hareket ettir
            for enemy in enemy_cars[:]:
                enemy.move()
                if enemy.y > screen_height:
                    enemy_cars.remove(enemy)

            # Bonusları hareket ettir
            for bonus in bonuses[:]:
                bonus.move()
                if bonus.y > screen_height:
                    bonuses.remove(bonus)

            # Ekranı beyaz yap
            screen.fill(WHITE)
            # Yolu çiz
            draw_road(road_lines)

            # Arabayı çiz
            car.draw()

            # Dubaları çiz ve çarpışma kontrolü
            for cone in cones:
                cone.draw()
                # Çarpışma kontrolü
                car_rect = pygame.Rect(car.x, car.y, car_width, car_height)
                cone_rect = pygame.Rect(cone.x, cone.y, cone.width, cone.height)
                if car_rect.colliderect(cone_rect):
                    if lives > 0:
                        lives -= 1
                        cones.remove(cone)
                        continue
                    font_over = pygame.font.SysFont("Arial", 80, bold=True)
                    over_text = font_over.render("GAME OVER", True, RED)
                    font_score = pygame.font.SysFont("Arial", 40, bold=True)
                    score_text = font_score.render(f"Skorun: {score}", True, BLACK)
                    font_restart = pygame.font.SysFont("Arial", 30)
                    restart_text = font_restart.render("Yeniden başlatmak için bir tuşa bas!", True, BLACK)
                    screen.blit(over_text, (screen_width//2 - over_text.get_width()//2, screen_height//2 - 120))
                    screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2 - 30))
                    screen.blit(restart_text, (screen_width//2 - restart_text.get_width()//2, screen_height//2 + 40))
                    pygame.display.update()
                    # Tuş bekle
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return
                            if event.type == pygame.KEYDOWN:
                                waiting = False
                                running = False
                    break

            # Düşman arabaları çiz ve çarpışma kontrolü
            for enemy in enemy_cars:
                enemy.draw()
                car_rect = pygame.Rect(car.x, car.y, car_width, car_height)
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if car_rect.colliderect(enemy_rect):
                    if lives > 0:
                        lives -= 1
                        enemy_cars.remove(enemy)
                        continue
                    font_over = pygame.font.SysFont("Arial", 80, bold=True)
                    over_text = font_over.render("GAME OVER", True, RED)
                    font_score = pygame.font.SysFont("Arial", 40, bold=True)
                    score_text = font_score.render(f"Skorun: {score}", True, BLACK)
                    font_restart = pygame.font.SysFont("Arial", 30)
                    restart_text = font_restart.render("Yeniden başlatmak için bir tuşa bas!", True, BLACK)
                    screen.blit(over_text, (screen_width//2 - over_text.get_width()//2, screen_height//2 - 120))
                    screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2 - 30))
                    screen.blit(restart_text, (screen_width//2 - restart_text.get_width()//2, screen_height//2 + 40))
                    pygame.display.update()
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return
                            if event.type == pygame.KEYDOWN:
                                waiting = False
                                running = False
                    break

            # Bonusları çiz ve alma kontrolü
            for bonus in bonuses[:]:
                bonus.draw()
                car_rect = pygame.Rect(car.x, car.y, car_width, car_height)
                bonus_rect = pygame.Rect(bonus.x, bonus.y, bonus.radius*2, bonus.radius*2)
                if car_rect.colliderect(bonus_rect):
                    lives += 1
                    bonuses.remove(bonus)

            # Skoru ve canı yazdır
            font = pygame.font.SysFont("Arial", 30)
            score_text = font.render(f"Skor: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            life_text = font.render(f"Can: {lives+1}", True, (0, 180, 0))
            screen.blit(life_text, (10, 50))

            # Ekranı güncelle
            pygame.display.update()

            # FPS kontrolü
            clock.tick(60)

# Oyunu başlat
game()
