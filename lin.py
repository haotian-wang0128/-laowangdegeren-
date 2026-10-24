"""
贪吃蛇小游戏 (Snake)
--------------------------
依赖: pygame   ->   安装命令:  pip install pygame
运行: python snake.py

操作说明:
    方向键 / WASD   控制蛇的移动方向
    R               游戏结束后重新开始
    ESC             退出游戏
"""

import random
import sys

import pygame  # 需要先安装: pip install pygame

# ==================== 常量配置 ====================
CELL_SIZE = 20                                    # 每个格子的边长(像素)
GRID_WIDTH = 30                                   # 横向格子数
GRID_HEIGHT = 20                                  # 纵向格子数
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH             # 窗口宽度
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT           # 窗口高度

BASE_FPS = 10                                     # 蛇的初始速度(格/秒)
MAX_FPS = 25                                      # 蛇的最大速度

# 颜色定义 (R, G, B)
BLACK = (18, 18, 18)
GRID_COLOR = (35, 35, 35)
SNAKE_HEAD_COLOR = (80, 220, 100)
SNAKE_BODY_COLOR = (40, 160, 70)
FOOD_COLOR = (230, 70, 70)
TEXT_COLOR = (240, 240, 240)


def draw_grid(surface):
    """绘制背景网格，方便观察蛇所在的格子"""
    for x in range(0, WINDOW_WIDTH + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))


def random_food(snake):
    """
    在所有空格子中随机选一个作为食物。
    如果没有空格子了(棋盘被填满)，返回 None。
    """
    occupied = set(snake)                 # 用集合查找，效率更高
    empty_cells = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in occupied
    ]
    return random.choice(empty_cells) if empty_cells else None


def create_new_game():
    """创建一局新游戏的初始状态，返回一个状态元组"""
    center_x, center_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
    # 蛇用列表表示，索引 0 是蛇头，后面依次是身体
    snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
    direction = (1, 0)          # 当前移动方向：向右 (dx, dy)
    pending_direction = direction
    food = random_food(snake)
    score = 0
    speed = BASE_FPS
    game_over = False
    return snake, direction, pending_direction, food, score, speed, game_over


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("贪吃蛇 Snake")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 64)

    # 初始化游戏状态
    snake, direction, pending_direction, food, score, speed, game_over = create_new_game()

    running = True
    while running:
        # ---------------- 1. 事件处理 ----------------
        turned_this_frame = False   # 保证同一帧内最多转向一次，防止“自杀式掉头”
        for event in pygame.event.get():
            if event.type == pygame.QUIT:              # 点击窗口右上角关闭
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:       # ESC 退出
                    running = False

                elif game_over:
                    if event.key == pygame.K_r:        # R 重新开始
                        (snake, direction, pending_direction,
                         food, score, speed, game_over) = create_new_game()

                else:
                    # 把按键转换成方向向量
                    new_dir = None
                    if event.key in (pygame.K_UP, pygame.K_w):
                        new_dir = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        new_dir = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        new_dir = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        new_dir = (1, 0)

                    # 过滤无效/反向操作：方向不同、不是 180° 掉头、本帧还没转过向
                    if (new_dir is not None
                            and new_dir != pending_direction
                            and not turned_this_frame
                            and new_dir != (-pending_direction[0], -pending_direction[1])):
                        pending_direction = new_dir
                        turned_this_frame = True

        # ---------------- 2. 更新游戏逻辑 ----------------
        if not game_over:
            direction = pending_direction
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # 撞墙判定
            hit_wall = not (0 <= new_head[0] < GRID_WIDTH and
                            0 <= new_head[1] < GRID_HEIGHT)
            # 撞自己判定：蛇尾这一帧会移开，所以排除最后一节
            hit_self = new_head in snake[:-1]

            if hit_wall or hit_self:
                game_over = True
            else:
                snake.insert(0, new_head)          # 蛇头前进

                if food is not None and new_head == food:
                    # 吃到食物：加分、加速、生成新食物，并且不删尾巴（蛇变长）
                    score += 1
                    speed = min(BASE_FPS + score // 5, MAX_FPS)   # 每吃 5 个加速一点
                    food = random_food(snake)
                    if food is None:               # 棋盘被填满 => 通关
                        game_over = True
                else:
                    snake.pop()                    # 没吃到食物就删掉尾巴，保持长度

        # ---------------- 3. 绘制画面 ----------------
        screen.fill(BLACK)
        draw_grid(screen)

        # 画食物
        if food is not None:
            food_rect = pygame.Rect(
                food[0] * CELL_SIZE + 2, food[1] * CELL_SIZE + 2,
                CELL_SIZE - 4, CELL_SIZE - 4
            )
            pygame.draw.rect(screen, FOOD_COLOR, food_rect)

        # 画蛇（蛇头颜色更亮）
        for index, (x, y) in enumerate(snake):
            color = SNAKE_HEAD_COLOR if index == 0 else SNAKE_BODY_COLOR
            body_rect = pygame.Rect(
                x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                CELL_SIZE - 2, CELL_SIZE - 2
            )
            pygame.draw.rect(screen, color, body_rect)

        # 显示分数
        score_surface = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_surface, (12, 10))

        # 游戏结束遮罩
        if game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))          # 半透明黑色
            screen.blit(overlay, (0, 0))

            title = big_font.render("Game Over", True, TEXT_COLOR)
            tip = font.render("Press R to Restart  |  ESC to Quit", True, TEXT_COLOR)
            screen.blit(title, title.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)))
            screen.blit(tip, tip.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)))

        pygame.display.flip()

        # ---------------- 4. 控制帧率（即蛇的移动速度） ----------------
        clock.tick(speed)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()