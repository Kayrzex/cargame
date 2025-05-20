import pygame
import random
import asyncio

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
road_width = 800  # 4 şerit için genişlik artırıldı
road_x = screen_width // 2 - road_width // 2

# Araba boyutları
car_width = 84  # Oyuncu aracı genişliği büyütüldü
car_height = 130  # Oyuncu aracı uzunluğu büyütüldü
enemy_car_width = car_width  # Düşman aracı genişliği oyuncu ile aynı
enemy_car_height = car_height  # Düşman aracı uzunluğu oyuncu ile aynı

# Duba boyutları
cone_width = 30
cone_height = 50

# Ağaç boyutları
# (gövde ve yaprak için)
tree_trunk_width = 20
tree_trunk_height = 40
tree_leaves_radius = 30

car_img = pygame.image.load('srt.png')
car_img = pygame.transform.scale(car_img, (car_width, car_height))
# Düşman arabası için de dodge.png kullan
enemy_car_img = pygame.transform.scale(pygame.image.load('dodge.png'), (enemy_car_width, enemy_car_height))

def draw_road(road_lines):
    pygame.draw.rect(screen, GRAY, (road_x, 0, road_width, screen_height))
    lane_width = road_width // 4
    for y in road_lines:
        for i in range(1, 4+1):  # 4 şerit için 4 çizgi
            pygame.draw.rect(screen, WHITE, (road_x + i * lane_width - 5, y, 10, 40))

# Bariyer çizim fonksiyonu
def draw_barriers():
    barrier_width = 12
    # Sol bariyer: kahverengi, uzun ve ince çizgi
    pygame.draw.rect(screen, (139, 69, 19), (road_x - barrier_width//2, 0, barrier_width, screen_height))
    # Sağ bariyer: kahverengi, uzun ve ince çizgi
    pygame.draw.rect(screen, (139, 69, 19), (road_x + road_width - barrier_width//2, 0, barrier_width, screen_height))

# Araba sınıfı
class Car:
    def __init__(self):
        self.x = screen_width // 2 - car_width // 2
        self.y = screen_height - car_height - 10
        self.speed = 45  # Hız artırıldı
        self.normal_speed = 40  # Hız artırıldı
        self.slow_speed = 2
        self.turn_speed = 5  # Sağa/sola dönüş hızı azaltıldı

    def draw(self):
        screen.blit(car_img, (self.x, self.y))

    def move_left(self):
        if self.x > road_x:
            self.x -= self.turn_speed  # Sabit hız

    def move_right(self):
        if self.x < road_x + road_width - car_width:
            self.x += self.turn_speed  # Sabit hız

    def accelerate(self, accelerating):
        if accelerating:
            if self.speed < self.normal_speed:
                self.speed += 1
            if self.speed > self.normal_speed:
                self.speed = self.normal_speed

    def brake(self, braking):
        if braking:
            if self.speed > 3:
                self.speed -= 2  # Kademeli yavaşlama
            else:
                self.speed = 3  # Tamamen durmasın, minimum hızda gitsin

# Düşman araba sınıfı
class EnemyCar:
    def __init__(self):
        self.width = enemy_car_width
        self.height = enemy_car_height
        lane_width = road_width // 4
        lane = random.randint(0, 3)  # 4 şerit: 0,1,2,3
        self.x = road_x + lane * lane_width + (lane_width - self.width) // 2
        self.y = -self.height
        self.speed = random.randint(1, 2)
    def move(self):
        self.y += self.speed
    def draw(self):
        screen.blit(enemy_car_img, (self.x, self.y))

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

class FuelBonus:
    def __init__(self):
        self.width = 36
        self.height = 48
        self.x = random.randint(road_x + 20, road_x + road_width - self.width - 20)
        self.y = -self.height
        self.speed = 3  # Benzin bonusu hızı yavaşlatıldı
    def move(self):
        self.y += self.speed
    def draw(self):
        pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.width, self.height), border_radius=7)
        font = pygame.font.SysFont("Arial", 22, bold=True)
        text = font.render("FUEL", True, WHITE)
        screen.blit(text, (self.x + self.width//2 - text.get_width()//2, self.y + self.height//2 - text.get_height()//2))

class NosBonus:
    def __init__(self):
        self.width = 36
        self.height = 48
        self.x = random.randint(road_x + 20, road_x + road_width - self.width - 20)
        self.y = -self.height
        self.speed = 3
    def move(self):
        self.y += self.speed
    def draw(self):
        pygame.draw.rect(screen, (0, 120, 255), (self.x, self.y, self.width, self.height), border_radius=7)
        font = pygame.font.SysFont("Arial", 22, bold=True)
        text = font.render("NOS", True, WHITE)
        screen.blit(text, (self.x + self.width//2 - text.get_width()//2, self.y + self.height//2 - text.get_height()//2))

# Ana oyun fonksiyonu
async def main():
    while True:
        car = Car()
        enemy_cars = []
        bonuses = []
        road_lines = [i for i in range(0, screen_height, 80)]
        clock = pygame.time.Clock()
        running = True
        score = 0
        enemy_timer = 0
        bonus_timer = 0
        lives = 1
        max_lives = 4
        bonus_pending = False
        falling = False
        fall_y = 0
        brake_pressed = False
        enemies_passed = 0
        fuel = 5
        max_fuel = 5
        fuel_timer = 0
        fuel_bonuses = []
        nos_count = 0
        max_nos = 4
        nos_active = False
        nos_timer = 0
        nos_bonuses = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN and not brake_pressed:
                        car.brake(True)
                        brake_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        brake_pressed = False

            if not falling:
                keys = pygame.key.get_pressed()
                car.accelerate(keys[pygame.K_UP] or keys[pygame.K_w])
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    car.move_left()
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    car.move_right()
                # Space artık fren değil, NOS
                if keys[pygame.K_SPACE] and nos_count > 0 and not nos_active:
                    nos_active = True
                    nos_timer = 120  # 2 saniye turbo
                    nos_count -= 1
                if nos_active:
                    car.speed = car.normal_speed + 20  # Turbo hız
                    nos_timer -= 1
                    if nos_timer <= 0:
                        nos_active = False
                        car.speed = car.normal_speed
                elif keys[pygame.K_DOWN]:
                    car.speed = 1  # Aşağı ok ile neredeyse tamamen dur
                else:
                    car.speed = car.normal_speed

            # Yol çizgilerini hareket ettir
            for i in range(len(road_lines)):
                road_lines[i] += car.speed
                if road_lines[i] > screen_height:
                    road_lines[i] = road_lines[i] - screen_height - 40

            # Yeni düşman araba oluşturma
            enemy_timer += 1
            min_timer = max(30, 80 - score // 10 * 10)  # Daha sık düşman
            max_enemies = 7  # Aynı anda ekranda daha fazla düşman
            if enemy_timer > min_timer and len(enemy_cars) < max_enemies:
                spawn_chance = min(0.7 + score / 200, 0.95)
                if random.random() < spawn_chance:
                    new_enemy = EnemyCar()
                    overlap = False
                    for enemy in enemy_cars:
                        rect1 = pygame.Rect(new_enemy.x, new_enemy.y, new_enemy.width, new_enemy.height)
                        rect2 = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                        # Dikeyde çakışma olmasın diye daha sıkı kontrol
                        if rect1.colliderect(rect2):
                            overlap = True
                            break
                    if not overlap:
                        enemy_cars.append(new_enemy)
                enemy_timer = 0

            # Ara sıra can bonusu oluştur
            bonus_timer += 1
            if bonus_timer > 120:  # Daha sık bonus
                if random.random() < 0.5 and lives < max_lives:  # Çıkma olasılığı artırıldı
                    bonuses.append(LifeBonus())
                bonus_timer = 0

            # Ara sıra benzin bonusu oluştur
            if random.random() < 0.008 and len(fuel_bonuses) < 2 and fuel < max_fuel:
                fuel_bonuses.append(FuelBonus())

            # Ara sıra NOS bonusu oluştur
            if random.random() < 0.006 and len(nos_bonuses) < 2 and nos_count < max_nos:
                nos_bonuses.append(NosBonus())

            # Düşman arabaları hareket ettir
            for enemy in enemy_cars[:]:
                enemy.y += enemy.speed
                if enemy.y + enemy.height < 0:
                    enemy_cars.remove(enemy)
                    enemies_passed += 1
                    if enemies_passed >= 5:
                        lives += 1
                        enemies_passed = 0

            # Bonusları hareket ettir
            for bonus in bonuses[:]:
                bonus.y += bonus.speed
                if bonus.y > screen_height:
                    bonuses.remove(bonus)

            # Benzin bonuslarını hareket ettir
            for fbonus in fuel_bonuses[:]:
                fbonus.move()
                if fbonus.y > screen_height:
                    fuel_bonuses.remove(fbonus)

            # NOS bonuslarını hareket ettir
            for nbonus in nos_bonuses[:]:
                nbonus.move()
                if nbonus.y > screen_height:
                    nos_bonuses.remove(nbonus)

            # Ekranı beyaz yap
            screen.fill(WHITE)
            draw_road(road_lines)
            draw_barriers()

            # Arabayı çiz
            if not falling:
                car.draw()

            # Bariyer çarpışma kontrolü
            if not falling:
                if car.x <= road_x or car.x + car_width >= road_x + road_width:
                    if lives > 0:
                        lives -= 1

            # Düşme animasyonu
            if falling:
                fall_y += 15
                screen.blit(pygame.transform.scale(screen.subsurface(car.x, car.y, car_width, car_height), (car_width, car_height)), (car.x, fall_y))
                if fall_y > screen_height:
                    falling = False
                    if lives >= 0:
                        car.x = screen_width // 2 - car_width // 2
                        car.y = screen_height - car_height - 10
                    if lives < 0:
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

            # Düşman arabaları çiz ve çarpışma kontrolü
            for enemy in enemy_cars:
                enemy.draw()
                car_rect = pygame.Rect(car.x, car.y, car_width, car_height)
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if not falling and car_rect.colliderect(enemy_rect):
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
                    await asyncio.sleep(0)
                    break

            # Bonusları çiz ve alma kontrolü
            for bonus in bonuses[:]:
                bonus.draw()
                car_rect = pygame.Rect(car.x, car.y, car_width, car_height)
                bonus_rect = pygame.Rect(bonus.x, bonus.y, bonus.radius*2, bonus.radius*2)
                if not falling and car_rect.colliderect(bonus_rect):
                    if lives < max_lives:
                        lives += 1
                    bonuses.remove(bonus)

            # Benzin bonuslarını çiz ve alma kontrolü
            for fbonus in fuel_bonuses[:]:
                fbonus.draw()
                car_rect = pygame.Rect(car.x, car.y, car_width, car_height)
                fbonus_rect = pygame.Rect(fbonus.x, fbonus.y, fbonus.width, fbonus.height)
                if not falling and car_rect.colliderect(fbonus_rect):
                    if fuel < max_fuel:
                        fuel += 1
                    fuel_bonuses.remove(fbonus)

            # NOS bonuslarını çiz ve alma kontrolü
            for nbonus in nos_bonuses[:]:
                nbonus.draw()
                car_rect = pygame.Rect(car.x, car.y, car_width, car_height)
                nbonus_rect = pygame.Rect(nbonus.x, nbonus.y, nbonus.width, nbonus.height)
                if not falling and car_rect.colliderect(nbonus_rect):
                    if nos_count < max_nos:
                        nos_count += 1
                    nos_bonuses.remove(nbonus)

            # Skoru ve canı yazdır
            font = pygame.font.SysFont("Arial", 30)
            score_text = font.render(f"Skor: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            # Can simgelerini çiz
            for i in range(lives):
                pygame.draw.circle(screen, (220, 0, 0), (30 + i*35, 60), 15)

            # Hız ibresi ekle
            speed_font = pygame.font.SysFont("Arial", 28, bold=True)
            speed_box = pygame.Rect(screen_width - 150, screen_height - 80, 120, 60)
            pygame.draw.rect(screen, (230,230,230), speed_box, border_radius=12)
            pygame.draw.rect(screen, (100,100,100), speed_box, 2, border_radius=12)
            # Hız göstergesinde yanıltıcı değer (gerçek hız x4)
            speed_text = speed_font.render(f"Hız: {int(car.speed * 4)}", True, (0, 100, 0))
            screen.blit(speed_text, (screen_width - 140, screen_height - 60))

            # Benzin göstergesi (sağ üstte)
            fuel_icon_w = 28
            fuel_icon_h = 36
            for i in range(max_fuel):
                color = (200,0,0) if i < fuel else (80,80,80)
                pygame.draw.rect(screen, color, (screen_width-40, 20 + i*(fuel_icon_h+6), fuel_icon_w, fuel_icon_h), border_radius=6)

            # NOS göstergesi (sol üstte, mavi kutular)
            for i in range(nos_count):
                pygame.draw.rect(screen, (0,120,255), (20, 100 + i*30, 22, 22), border_radius=5)
            if nos_active:
                font_nos = pygame.font.SysFont("Arial", 28, bold=True)
                nos_text = font_nos.render("NOS!", True, (0,120,255))
                screen.blit(nos_text, (20, 80))

            # Benzin bitince oyun biter
            if fuel <= 0:
                font_over = pygame.font.SysFont("Arial", 80, bold=True)
                over_text = font_over.render("BENZİN BİTTİ", True, RED)
                font_restart = pygame.font.SysFont("Arial", 30)
                restart_text = font_restart.render("Yeniden başlatmak için bir tuşa bas!", True, BLACK)
                screen.blit(over_text, (screen_width//2 - over_text.get_width()//2, screen_height//2 - 80))
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

            # Ekranı güncelle
            pygame.display.update()

            # FPS kontrolü
            clock.tick(60)
            await asyncio.sleep(0)

        await asyncio.sleep(0)


# Oyunu başlat
asyncio.run(main())
