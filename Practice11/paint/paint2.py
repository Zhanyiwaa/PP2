import pygame

# =========================
# INITIALIZATION
# =========================
pygame.init()

# --- Constants (window + layout sizes) ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 500
PALETTE_WIDTH = 150

# --- Colors (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# =========================
# TOOLS ENUM (IDs)
# =========================
PEN = 0
RECTANGLE = 1
CIRCLE = 2
ERASER = 3
SQUARE = 4
RIGHT_TRIANGLE = 5
EQUILATERAL_TRIANGLE = 6
RHOMBUS = 7

# =========================
# WINDOW SETUP
# =========================
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Program Extended")
clock = pygame.time.Clock()

# =========================
# CANVAS (drawing surface)
# =========================
canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

# =========================
# STATE VARIABLES
# =========================
current_tool = PEN
current_color = BLACK
drawing = False
start_pos = None
end_pos = None

brush_size = 5
eraser_size = 20

# =========================
# COLOR PALETTE UI
# =========================
palette = [
    {"color": BLACK, "rect": pygame.Rect(620, 60, 30, 30)},
    {"color": RED, "rect": pygame.Rect(660, 60, 30, 30)},
    {"color": GREEN, "rect": pygame.Rect(700, 60, 30, 30)},
    {"color": BLUE, "rect": pygame.Rect(740, 60, 30, 30)},
    {"color": YELLOW, "rect": pygame.Rect(620, 100, 30, 30)},
    {"color": PURPLE, "rect": pygame.Rect(660, 100, 30, 30)},
    {"color": ORANGE, "rect": pygame.Rect(700, 100, 30, 30)},
    {"color": WHITE, "rect": pygame.Rect(740, 100, 30, 30)}
]

# =========================
# TOOL BUTTONS UI
# =========================
tool_buttons = [
    {"tool": PEN, "rect": pygame.Rect(620, 150, 60, 30), "text": "Pen"},
    {"tool": RECTANGLE, "rect": pygame.Rect(690, 150, 60, 30), "text": "Rect"},
    {"tool": CIRCLE, "rect": pygame.Rect(620, 190, 60, 30), "text": "Circle"},
    {"tool": ERASER, "rect": pygame.Rect(690, 190, 60, 30), "text": "Eraser"},
    {"tool": SQUARE, "rect": pygame.Rect(620, 230, 60, 30), "text": "Square"},
    {"tool": RIGHT_TRIANGLE, "rect": pygame.Rect(690, 230, 60, 30), "text": "R-Tri"},
    {"tool": EQUILATERAL_TRIANGLE, "rect": pygame.Rect(620, 270, 60, 30), "text": "E-Tri"},
    {"tool": RHOMBUS, "rect": pygame.Rect(690, 270, 60, 30), "text": "Rhomb"}
]

font = pygame.font.SysFont("Arial", 14)

# =========================
# DRAW UI
# =========================
def draw_ui():
    pygame.draw.rect(screen, GRAY, (CANVAS_WIDTH, 0, PALETTE_WIDTH, SCREEN_HEIGHT))

    # colors
    for c in palette:
        pygame.draw.rect(screen, c["color"], c["rect"])
        pygame.draw.rect(screen, BLACK, c["rect"], 2)

    # tools
    for b in tool_buttons:
        pygame.draw.rect(screen, GRAY, b["rect"])
        pygame.draw.rect(screen, BLACK, b["rect"], 2)
        text = font.render(b["text"], True, BLACK)
        screen.blit(text, text.get_rect(center=b["rect"].center))


# =========================
# DRAW SHAPES (CORE LOGIC)
# =========================
def draw_shape(surface, tool, color, start, end):

    # --- Rectangle ---
    if tool == RECTANGLE:
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        w = abs(start[0] - end[0])
        h = abs(start[1] - end[1])
        pygame.draw.rect(surface, color, (x, y, w, h), 2)

    # --- Square (equal sides) ---
    elif tool == SQUARE:
        size = min(abs(start[0] - end[0]), abs(start[1] - end[1]))
        x = start[0]
        y = start[1]
        pygame.draw.rect(surface, color, (x, y, size, size), 2)

    # --- Circle ---
    elif tool == CIRCLE:
        center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        radius = max(abs(start[0] - end[0]), abs(start[1] - end[1])) // 2
        pygame.draw.circle(surface, color, center, radius, 2)

    # --- Right Triangle ---
    elif tool == RIGHT_TRIANGLE:
        points = [
            start,
            (start[0], end[1]),
            end
        ]
        pygame.draw.polygon(surface, color, points, 2)

    # --- Equilateral Triangle ---
    elif tool == EQUILATERAL_TRIANGLE:
        x1, y1 = start
        x2, y2 = end

        # base width
        base = abs(x2 - x1)

        # height formula √3/2 * side
        height = int(base * (3 ** 0.5) / 2)

        points = [
            (x1, y1),
            (x2, y1),
            ((x1 + x2) // 2, y1 - height)
        ]
        pygame.draw.polygon(surface, color, points, 2)

    # --- Rhombus ---
    elif tool == RHOMBUS:
        cx = (start[0] + end[0]) // 2
        cy = (start[1] + end[1]) // 2

        dx = abs(start[0] - end[0]) // 2
        dy = abs(start[1] - end[1]) // 2

        points = [
            (cx, cy - dy),
            (cx + dx, cy),
            (cx, cy + dy),
            (cx - dx, cy)
        ]
        pygame.draw.polygon(surface, color, points, 2)

    # --- Pen ---
    elif tool == PEN:
        pygame.draw.line(surface, color, start, end, brush_size)

    # --- Eraser ---
    elif tool == ERASER:
        pygame.draw.circle(surface, WHITE, end, eraser_size)


# =========================
# MAIN LOOP
# =========================
running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # --- Mouse Down ---
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos

                # color select
                for c in palette:
                    if c["rect"].collidepoint(x, y):
                        current_color = c["color"]
                        if current_color == WHITE:
                            current_tool = ERASER

                # tool select
                for b in tool_buttons:
                    if b["rect"].collidepoint(x, y):
                        current_tool = b["tool"]

                # start drawing
                if x < CANVAS_WIDTH and y < CANVAS_HEIGHT:
                    drawing = True
                    start_pos = event.pos
                    end_pos = event.pos

        # --- Mouse Move ---
        elif event.type == pygame.MOUSEMOTION and drawing:
            x, y = event.pos
            if x < CANVAS_WIDTH and y < CANVAS_HEIGHT:
                end_pos = event.pos

                if current_tool in [PEN, ERASER]:
                    draw_shape(canvas, current_tool, current_color, start_pos, end_pos)
                    start_pos = end_pos

        # --- Mouse Up ---
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                if current_tool not in [PEN, ERASER]:
                    draw_shape(canvas, current_tool, current_color, start_pos, end_pos)

    # =========================
    # DRAW EVERYTHING
    # =========================
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    draw_ui()

    # preview shapes
    if drawing and current_tool not in [PEN, ERASER]:
        temp = canvas.copy()
        draw_shape(temp, current_tool, current_color, start_pos, end_pos)
        screen.blit(temp, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()