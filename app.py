import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (128, 128, 128)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BIG_FOOD_COLOR = (255, 255, 0)
BIG_FOOD_SIZE = GRID_SIZE * 2

# Snake class
class Snake:
    def __init__(self):
        self.body = [(100, 100)]
        self.direction = (1, 0)
        self.score = 0
        self.speed = 10
        self.last_move_time = 0

    def move(self, food):
        if pygame.time.get_ticks() - self.last_move_time < 1000 // self.speed:
            return True

        self.last_move_time = pygame.time.get_ticks()
        x, y = self.body[0]
        dx, dy = self.direction
        new_head = ((x + dx * GRID_SIZE) % WIDTH, (y + dy * GRID_SIZE) % HEIGHT)
        if new_head in self.body[1:]:
            return False  # Game over: Snake collided with itself
        self.body.insert(0, new_head)
        if new_head == food.position:
            food.regenerate()
            if food.is_big:
                self.score += 5
                self.grow()
            else:
                self.score += 1
            if self.speed < 20:
                self.speed += 1
        else:
            self.body.pop()
        return True

    def grow(self):
        x, y = self.body[-1]
        dx, dy = self.direction
        new_tail = ((x - dx * GRID_SIZE) % WIDTH, (y - dy * GRID_SIZE) % HEIGHT)
        self.body.append(new_tail)

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, SNAKE_COLOR, (segment[0], segment[1], GRID_SIZE, GRID_SIZE), border_radius=5)

# Food class
class Food:
    def __init__(self):
        self.position = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
        self.is_big = False

    def draw(self, surface):
        if self.is_big:
            pygame.draw.circle(surface, BIG_FOOD_COLOR, (self.position[0] + GRID_SIZE // 2, self.position[1] + GRID_SIZE // 2), BIG_FOOD_SIZE // 2)
        else:
            pygame.draw.circle(surface, FOOD_COLOR, (self.position[0] + GRID_SIZE // 2, self.position[1] + GRID_SIZE // 2), GRID_SIZE // 2)

    def regenerate(self):
        self.position = (random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE))
        self.is_big = (random.random() < 0.1)  # 10% chance of big food

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()

    # Load high score
    high_score = load_high_score()

    game_over = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))
                elif event.key == pygame.K_RETURN:
                    snake = Snake()
                    food = Food()
                    game_over = False
                    snake.speed = 10
                    snake.score = 0

        if not game_over:
            screen.fill(BACKGROUND_COLOR)
            if not snake.move(food):
                game_over = True
                if snake.score > high_score:
                    high_score = snake.score
                    save_high_score(high_score)
            snake.draw(screen)
            food.draw(screen)

            # Display score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {snake.score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            # Display high score
            high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
            screen.blit(high_score_text, (10, 40))
        else:
            # Game over message
            font = pygame.font.Font(None, 32)
            text = font.render("Game Over! Press ENTER to play again.", True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

if __name__ == "__main__":
    main()
