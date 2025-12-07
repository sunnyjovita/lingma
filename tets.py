import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]   # L
]

# Tetromino colors
COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.color = COLORS[self.shape_idx]
        self.rotation = 0

    def rotate(self):
        # Transpose the matrix and reverse each row for clockwise rotation
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = self.shape[r][c]
                
        return rotated

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()
        
    def reset_game(self):
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.fall_speed = 0.5  # seconds
        self.fall_time = 0
        
    def new_piece(self):
        return Tetromino(GRID_WIDTH // 2 - 1, 0)
        
    def valid_position(self, piece, x, y, shape=None):
        shape_to_check = shape if shape else piece.shape
        for r, row in enumerate(shape_to_check):
            for c, cell in enumerate(row):
                if cell:
                    pos_x, pos_y = x + c, y + r
                    if (pos_x < 0 or pos_x >= GRID_WIDTH or 
                        pos_y >= GRID_HEIGHT or 
                        (pos_y >= 0 and self.board[pos_y][pos_x])):
                        return False
        return True
        
    def merge_piece(self):
        for r, row in enumerate(self.current_piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    board_y = self.current_piece.y + r
                    board_x = self.current_piece.x + c
                    if 0 <= board_y < GRID_HEIGHT and 0 <= board_x < GRID_WIDTH:
                        self.board[board_y][board_x] = self.current_piece.color
                        
    def clear_lines(self):
        lines_cleared = 0
        for i in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.board[i]):
                del self.board[i]
                self.board.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared * 100
        
    def move(self, dx, dy):
        if not self.game_over:
            if self.valid_position(self.current_piece, 
                                 self.current_piece.x + dx, 
                                 self.current_piece.y + dy):
                self.current_piece.x += dx
                self.current_piece.y += dy
                return True
        return False
        
    def rotate_piece(self):
        if not self.game_over:
            rotated_shape = self.current_piece.rotate()
            if self.valid_position(self.current_piece, 
                                 self.current_piece.x, 
                                 self.current_piece.y, 
                                 rotated_shape):
                self.current_piece.shape = rotated_shape
                return True
        return False
        
    def drop(self):
        if not self.game_over:
            while self.move(0, 1):
                pass
            self.lock_piece()
            
    def lock_piece(self):
        self.merge_piece()
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        # Check if game is over
        if not self.valid_position(self.current_piece, 
                                 self.current_piece.x, 
                                 self.current_piece.y):
            self.game_over = True
            
    def draw_board(self):
        # Calculate position to center the grid
        grid_left = (SCREEN_WIDTH - SIDEBAR_WIDTH - GRID_WIDTH * GRID_SIZE) // 2
        grid_top = (SCREEN_HEIGHT - GRID_HEIGHT * GRID_SIZE) // 2
        
        # Draw background
        self.screen.fill(BLACK)
        
        # Draw grid border
        pygame.draw.rect(self.screen, WHITE, 
                        (grid_left - 1, grid_top - 1, 
                         GRID_WIDTH * GRID_SIZE + 2, 
                         GRID_HEIGHT * GRID_SIZE + 2), 2)
        
        # Draw placed blocks
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, cell,
                                   (grid_left + x * GRID_SIZE, 
                                    grid_top + y * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, WHITE,
                                   (grid_left + x * GRID_SIZE, 
                                    grid_top + y * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE), 1)
        
        # Draw current piece
        if not self.game_over:
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.current_piece.color,
                                       (grid_left + (self.current_piece.x + x) * GRID_SIZE,
                                        grid_top + (self.current_piece.y + y) * GRID_SIZE,
                                        GRID_SIZE, GRID_SIZE))
                        pygame.draw.rect(self.screen, WHITE,
                                       (grid_left + (self.current_piece.x + x) * GRID_SIZE,
                                        grid_top + (self.current_piece.y + y) * GRID_SIZE,
                                        GRID_SIZE, GRID_SIZE), 1)
        
        # Draw sidebar
        sidebar_left = SCREEN_WIDTH - SIDEBAR_WIDTH
        pygame.draw.line(self.screen, WHITE, (sidebar_left, 0), (sidebar_left, SCREEN_HEIGHT), 2)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (sidebar_left + 10, 50))
        
        # Draw next piece preview
        next_text = self.font.render("Next:", True, WHITE)
        self.screen.blit(next_text, (sidebar_left + 10, 150))
        
        # Draw next piece
        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece.color,
                                   (sidebar_left + 40 + x * GRID_SIZE,
                                    200 + y * GRID_SIZE,
                                    GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, WHITE,
                                   (sidebar_left + 40 + x * GRID_SIZE,
                                    200 + y * GRID_SIZE,
                                    GRID_SIZE, GRID_SIZE), 1)
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, 
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 10))
        
        # Draw controls help
        controls = [
            "Controls:",
            "← → : Move",
            "↑ : Rotate",
            "↓ : Soft Drop",
            "Space : Hard Drop",
            "R : Restart"
        ]
        
        for i, text in enumerate(controls):
            control_text = pygame.font.SysFont(None, 24).render(text, True, WHITE)
            self.screen.blit(control_text, (sidebar_left + 10, SCREEN_HEIGHT - 150 + i * 25))

    def run(self):
        last_time = pygame.time.get_ticks()
        
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move(0, 1)
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            self.drop()
                    
                    if event.key == pygame.K_r:
                        self.reset_game()
            
            # Game logic
            if not self.game_over:
                self.fall_time += delta_time
                if self.fall_time >= self.fall_speed:
                    self.fall_time = 0
                    if not self.move(0, 1):
                        self.lock_piece()
            
            # Drawing
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()