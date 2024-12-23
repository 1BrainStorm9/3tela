import pygame
import math

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция Солнечной системы")

# Константы
G = 0.1  # Гравитационная постоянная
TIME_STEP = 1  # Шаг времени

# Цвета
COLORS = {
    "background": (255, 255, 255),
    "sun": (255, 215, 0),
    "venus": (255, 182, 193),
    "earth": (0, 255, 0),
    "mars": (255, 69, 0),
}

# Класс небесного тела
class CelestialBody:
    def __init__(self, mass, x, y, vx, vy, color):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.trajectory = []

    def update(self, bodies):
        fx, fy = 0, 0
        for body in bodies:
            if body is not self:
                dx = body.x - self.x
                dy = body.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0:
                    force = G * self.mass * body.mass / distance**2
                    fx += force * dx / distance
                    fy += force * dy / distance

        # Обновление скорости и позиции
        self.vx += fx / self.mass * TIME_STEP
        self.vy += fy / self.mass * TIME_STEP
        self.x += self.vx * TIME_STEP
        self.y += self.vy * TIME_STEP

        # Сохранение траектории
        self.trajectory.append((int(self.x), int(self.y)))
        if len(self.trajectory) > 500:  # Ограничение длины траектории
            self.trajectory.pop(0)

    def draw(self):
        for point in self.trajectory:
            pygame.draw.circle(screen, self.color, point, 1)  # Траектория
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)  # Само тело

# Создание объектов
sun = CelestialBody(1000, WIDTH // 2, HEIGHT // 2, 0, 0, COLORS["sun"])

venus = CelestialBody(8, WIDTH // 2 + 100, HEIGHT // 2, 0, -math.sqrt(G * sun.mass / 100), COLORS["venus"])
earth = CelestialBody(10, WIDTH // 2 + 150, HEIGHT // 2, 0, -math.sqrt(G * sun.mass / 150), COLORS["earth"])
mars = CelestialBody(7, WIDTH // 2 + 228, HEIGHT // 2, 0, -math.sqrt(G * sun.mass / 228), COLORS["mars"])

bodies = [sun, venus, earth, mars]

# Основной цикл программы
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(COLORS["background"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление состояний и отрисовка
    for body in bodies:
        body.update(bodies)
        body.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
