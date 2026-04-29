# tools.py - all drawing tools for paint app

import pygame
import math
from collections import deque

# pencil - draws along mouse path
def pencil(canvas, last_pos, current_pos, color, size):
    if last_pos:
        pygame.draw.line(canvas, color, last_pos, current_pos, size)
    else:
        pygame.draw.circle(canvas, color, current_pos, size // 2)

# eraser - same as pencil but white
def eraser(canvas, last_pos, current_pos, size):
    if last_pos:
        pygame.draw.line(canvas, (255,255,255), last_pos, current_pos, size * 4)
    else:
        pygame.draw.circle(canvas, (255,255,255), current_pos, size * 2)

# line preview on screen while dragging
def line_preview(surface, start, end, color, size):
    if start and end:
        pygame.draw.line(surface, color, start, end, size)

# commit line to canvas
def line_commit(canvas, start, end, color, size):
    if start and end:
        pygame.draw.line(canvas, color, start, end, size)

# rect preview
def rect_preview(surface, start, end, color, size):
    if start and end:
        pygame.draw.rect(surface, color, _make_rect(start, end), size)

# commit rect to canvas
def rect_commit(canvas, start, end, color, size):
    if start and end:
        pygame.draw.rect(canvas, color, _make_rect(start, end), size)

# square preview - forces equal width and height
def square_preview(surface, start, end, color, size):
    if start and end:
        pygame.draw.rect(surface, color, _make_square(start, end), size)

# commit square to canvas
def square_commit(canvas, start, end, color, size):
    if start and end:
        pygame.draw.rect(canvas, color, _make_square(start, end), size)

# circle preview
def circle_preview(surface, start, end, color, size):
    if start and end:
        rad = _radius(start, end)
        if rad > 0:
            pygame.draw.circle(surface, color, start, rad, size)

# commit circle to canvas
def circle_commit(canvas, start, end, color, size):
    if start and end:
        rad = _radius(start, end)
        if rad > 0:
            pygame.draw.circle(canvas, color, start, rad, size)

# right triangle preview (right angle at bottom left)
def right_triangle_preview(surface, start, end, color, size):
    if start and end:
        pts = _right_triangle_pts(start, end)
        pygame.draw.polygon(surface, color, pts, size)

# commit right triangle
def right_triangle_commit(canvas, start, end, color, size):
    if start and end:
        pts = _right_triangle_pts(start, end)
        pygame.draw.polygon(canvas, color, pts, size)

# equilateral triangle preview
def eq_triangle_preview(surface, start, end, color, size):
    if start and end:
        pts = _eq_triangle_pts(start, end)
        pygame.draw.polygon(surface, color, pts, size)

# commit equilateral triangle
def eq_triangle_commit(canvas, start, end, color, size):
    if start and end:
        pts = _eq_triangle_pts(start, end)
        pygame.draw.polygon(canvas, color, pts, size)

# rhombus preview
def rhombus_preview(surface, start, end, color, size):
    if start and end:
        pts = _rhombus_pts(start, end)
        pygame.draw.polygon(surface, color, pts, size)

# commit rhombus
def rhombus_commit(canvas, start, end, color, size):
    if start and end:
        pts = _rhombus_pts(start, end)
        pygame.draw.polygon(canvas, color, pts, size)

# flood fill using BFS
def flood_fill(surface, pos, fill_color):
    surface.lock()
    tx, ty  = pos
    target  = surface.get_at((tx, ty))[:3]
    if target == fill_color[:3]:
        surface.unlock()
        return
    w, h    = surface.get_size()
    queue   = deque([pos])
    visited = {pos}
    while queue:
        x, y = queue.popleft()
        if surface.get_at((x, y))[:3] != target:
            continue
        surface.set_at((x, y), fill_color)
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and (nx,ny) not in visited:
                visited.add((nx,ny))
                queue.append((nx,ny))
    surface.unlock()

# text preview while typing
def text_preview(surface, pos, text, color):
    if pos:
        f    = pygame.font.SysFont("Arial", 22)
        surf = f.render(text + "|", True, color)
        surface.blit(surf, pos)

# commit text to canvas on Enter
def text_commit(canvas, pos, text, color):
    if pos and text:
        f    = pygame.font.SysFont("Arial", 22)
        surf = f.render(text, True, color)
        canvas.blit(surf, pos)

# ── private helpers ───────────────────────────────────────────────────────────

def _make_rect(start, end):
    return pygame.Rect(
        min(start[0], end[0]),
        min(start[1], end[1]),
        abs(end[0] - start[0]),
        abs(end[1] - start[1])
    )

def _make_square(start, end):
    # use the smaller side so it stays square
    side = min(abs(end[0]-start[0]), abs(end[1]-start[1]))
    sx   = start[0] if end[0] >= start[0] else start[0] - side
    sy   = start[1] if end[1] >= start[1] else start[1] - side
    return pygame.Rect(sx, sy, side, side)

def _radius(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    return int((dx**2 + dy**2) ** 0.5)

def _right_triangle_pts(start, end):
    # right angle at bottom-left
    return [
        (start[0], end[1]),   # bottom left (right angle)
        (end[0],   end[1]),   # bottom right
        (start[0], start[1]), # top left
    ]

def _eq_triangle_pts(start, end):
    # base goes from start to end, third point above center
    bx    = (start[0] + end[0]) / 2
    h     = abs(end[0] - start[0]) * math.sqrt(3) / 2
    top_y = min(start[1], end[1]) - h
    return [
        (start[0], end[1]),
        (end[0],   end[1]),
        (bx,       top_y),
    ]

def _rhombus_pts(start, end):
    # diamond shape from bounding box
    mx = (start[0] + end[0]) // 2
    my = (start[1] + end[1]) // 2
    return [
        (mx,       start[1]),  # top
        (end[0],   my),        # right
        (mx,       end[1]),    # bottom
        (start[0], my),        # left
    ]