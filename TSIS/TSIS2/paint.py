# paint.py - main paint app TSIS2

import pygame
import sys
from datetime import datetime
import tools

pygame.init()

WIDTH, HEIGHT = 1100, 700
TOOLBAR_H     = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - TSIS2")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 13)

# white canvas
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill((255, 255, 255))

# color palette
PALETTE = [
    (0,0,0),(255,255,255),(255,0,0),(0,180,0),
    (0,0,255),(255,165,0),(128,0,128),(0,200,200),
    (255,20,147),(139,69,19),(128,128,128),(255,255,0)
]

# brush sizes mapped to keys 1 2 3
SIZES = {pygame.K_1: 2, pygame.K_2: 5, pygame.K_3: 10}

# all tools in order
TOOLS = [
    "Pencil", "Line", "Rect", "Square", "Circle",
    "R.Tri", "Eq.Tri", "Rhombus", "Eraser", "Fill", "Text"
]

# state
color      = (0, 0, 0)
brush_size = 2
tool_idx   = 0
drawing    = False
start_pos  = None
last_pos   = None

# text tool state
typing     = False
text_pos   = None
typed_text = ""

def draw_toolbar():
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, TOOLBAR_H))
    pygame.draw.line(screen, (170,170,170), (0, TOOLBAR_H), (WIDTH, TOOLBAR_H), 1)

    # row 1 - tool buttons
    btn_w = WIDTH // len(TOOLS) - 2
    for i, name in enumerate(TOOLS):
        r  = pygame.Rect(2 + i*(btn_w+2), 5, btn_w, 36)
        bg = (70, 120, 210) if i == tool_idx else (155, 155, 155)
        pygame.draw.rect(screen, bg, r, border_radius=5)
        lbl = font.render(name, True, (255,255,255))
        screen.blit(lbl, (r.centerx - lbl.get_width()//2,
                           r.centery - lbl.get_height()//2))

    # row 2 left - color swatches
    cx = 6
    for col in PALETTE:
        r = pygame.Rect(cx, 50, 28, 28)
        pygame.draw.rect(screen, col, r)
        if col == color:
            pygame.draw.rect(screen, (0,0,0), r, 3)
        else:
            pygame.draw.rect(screen, (100,100,100), r, 1)
        cx += 32

    # row 2 right - brush size buttons (clickable)
    sizes_info = [(1, 2), (2, 5), (3, 10)]
    for i, (key, size) in enumerate(sizes_info):
        r  = pygame.Rect(WIDTH - 310 + i*100, 50, 90, 28)
        bg = (70, 120, 210) if brush_size == size else (155,155,155)
        pygame.draw.rect(screen, bg, r, border_radius=4)
        lbl = font.render(f"[{key}] {size}px", True, (255,255,255))
        screen.blit(lbl, (r.centerx - lbl.get_width()//2,
                           r.centery - lbl.get_height()//2))

    # ctrl+s hint
    hint = font.render("Ctrl+S = save PNG", True, (80,80,80))
    screen.blit(hint, (WIDTH - 148, 10))

# map tool index to commit/preview functions
def do_preview(cur_pos):
    s = start_pos
    c = cur_pos
    if tool_idx == 1:  tools.line_preview(screen,     (s[0], s[1]+TOOLBAR_H), (c[0], c[1]+TOOLBAR_H), color, brush_size)
    elif tool_idx == 2: tools.rect_preview(screen,    (s[0], s[1]+TOOLBAR_H), (c[0], c[1]+TOOLBAR_H), color, brush_size)
    elif tool_idx == 3: tools.square_preview(screen,  (s[0], s[1]+TOOLBAR_H), (c[0], c[1]+TOOLBAR_H), color, brush_size)
    elif tool_idx == 4: tools.circle_preview(screen,  (s[0], s[1]+TOOLBAR_H), (c[0], c[1]+TOOLBAR_H), color, brush_size)
    elif tool_idx == 5: tools.right_triangle_preview(screen,  (s[0], s[1]+TOOLBAR_H), (c[0], c[1]+TOOLBAR_H), color, brush_size)
    elif tool_idx == 6: tools.eq_triangle_preview(screen,     (s[0], s[1]+TOOLBAR_H), (c[0], c[1]+TOOLBAR_H), color, brush_size)
    elif tool_idx == 7: tools.rhombus_preview(screen, (s[0], s[1]+TOOLBAR_H), (c[0], c[1]+TOOLBAR_H), color, brush_size)

def do_commit(end_pos):
    s = start_pos
    e = end_pos
    if tool_idx == 1:  tools.line_commit(canvas,     s, e, color, brush_size)
    elif tool_idx == 2: tools.rect_commit(canvas,    s, e, color, brush_size)
    elif tool_idx == 3: tools.square_commit(canvas,  s, e, color, brush_size)
    elif tool_idx == 4: tools.circle_commit(canvas,  s, e, color, brush_size)
    elif tool_idx == 5: tools.right_triangle_commit(canvas,  s, e, color, brush_size)
    elif tool_idx == 6: tools.eq_triangle_commit(canvas,     s, e, color, brush_size)
    elif tool_idx == 7: tools.rhombus_commit(canvas, s, e, color, brush_size)

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        elif event.type == pygame.KEYDOWN:
            # brush size keys
            if event.key in SIZES:
                brush_size = SIZES[event.key]

            # Ctrl+S - save canvas as PNG file
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"canvas_{ts}.png"
                pygame.image.save(canvas, filename)
                print(f"Saved: {filename}")

            # text tool typing
            elif typing:
                if event.key == pygame.K_RETURN:
                    tools.text_commit(canvas, text_pos, typed_text, color)
                    typing = False; typed_text = ""
                elif event.key == pygame.K_ESCAPE:
                    typing = False; typed_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]
                elif event.unicode.isprintable():
                    typed_text += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # clicked on toolbar
            if my < TOOLBAR_H:
                # tool buttons row 1
                btn_w = WIDTH // len(TOOLS) - 2
                for i in range(len(TOOLS)):
                    r = pygame.Rect(2 + i*(btn_w+2), 5, btn_w, 36)
                    if r.collidepoint(mx, my):
                        tool_idx = i

                # color swatches row 2
                cx2 = 6
                for col in PALETTE:
                    r = pygame.Rect(cx2, 50, 28, 28)
                    if r.collidepoint(mx, my):
                        color = col
                    cx2 += 32

                # size buttons row 2 right
                for i, (key, size) in enumerate([(1,2),(2,5),(3,10)]):
                    r = pygame.Rect(WIDTH - 310 + i*100, 50, 90, 28)
                    if r.collidepoint(mx, my):
                        brush_size = size
                continue

            # canvas click - translate y
            cy         = my - TOOLBAR_H
            canvas_pos = (mx, cy)

            if tool_idx == 10:   # text
                typing     = True
                text_pos   = canvas_pos
                typed_text = ""
            elif tool_idx == 9:  # fill
                tools.flood_fill(canvas, canvas_pos, color)
            elif tool_idx == 0:  # pencil
                drawing  = True
                last_pos = canvas_pos
            elif tool_idx == 8:  # eraser
                drawing  = True
                last_pos = canvas_pos
            else:                # all shape tools
                drawing   = True
                start_pos = canvas_pos

        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            if my < TOOLBAR_H: continue
            cy         = my - TOOLBAR_H
            canvas_pos = (mx, cy)

            if drawing:
                if tool_idx == 0:  # pencil
                    tools.pencil(canvas, last_pos, canvas_pos, color, brush_size)
                    last_pos = canvas_pos
                elif tool_idx == 8:  # eraser
                    tools.eraser(canvas, last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            mx, my = event.pos
            if my < TOOLBAR_H:
                drawing = False; continue
            cy         = my - TOOLBAR_H
            canvas_pos = (mx, cy)

            # commit shape to canvas on release
            if drawing and start_pos and tool_idx not in (0, 8, 9, 10):
                do_commit(canvas_pos)

            drawing   = False
            start_pos = None
            last_pos  = None

    # render frame
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, TOOLBAR_H))

    # live shape preview while dragging
    if drawing and start_pos and tool_idx not in (0, 8, 9, 10):
        cur = pygame.mouse.get_pos()
        cur_canvas = (cur[0], cur[1] - TOOLBAR_H)
        do_preview(cur_canvas)

    # text preview while typing
    if typing and text_pos:
        tools.text_preview(screen,
                           (text_pos[0], text_pos[1] + TOOLBAR_H),
                           typed_text, color)

    draw_toolbar()
    pygame.display.flip()
    clock.tick(60)