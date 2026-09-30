"""ÃœÃ§gen diken vs AABB â€” harici kÃ¼tÃ¼phane yok."""

from __future__ import annotations

import pygame


def _cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def point_in_triangle(px: float, py: float, a: tuple, b: tuple, c: tuple) -> bool:
    def orient(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]) -> float:
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    p = (px, py)
    d1 = orient(p, a, b)
    d2 = orient(p, b, c)
    d3 = orient(p, c, a)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)


def _seg_intersect(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> bool:
    r = (p2[0] - p1[0], p2[1] - p1[1])
    s = (p4[0] - p3[0], p4[1] - p3[1])
    denom = _cross(r[0], r[1], s[0], s[1])
    if abs(denom) < 1e-9:
        return False
    t = _cross(p3[0] - p1[0], p3[1] - p1[1], s[0], s[1]) / denom
    u = _cross(p3[0] - p1[0], p3[1] - p1[1], r[0], r[1]) / denom
    return 0 <= t <= 1 and 0 <= u <= 1


def triangle_hits_rect(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
    rect: pygame.Rect,
) -> bool:
    """Dik Ã¼Ã§gen (a sol-alt, b tepe, c saÄŸ-alt) ile oyuncu AABB."""
    margin = 3
    r = rect.inflate(-margin * 2, -margin * 2)
    if r.w < 4 or r.h < 4:
        r = rect

    corners = (
        (r.left, r.top),
        (r.right - 1, r.top),
        (r.right - 1, r.bottom - 1),
        (r.left, r.bottom - 1),
    )
    for p in corners:
        if point_in_triangle(p[0], p[1], a, b, c):
            return True
    for v in (a, b, c):
        if r.collidepoint(v[0], v[1]):
            return True
    tri_edges = ((a, b), (b, c), (c, a))
    rect_edges = (
        (corners[0], corners[1]),
        (corners[1], corners[2]),
        (corners[2], corners[3]),
        (corners[3], corners[0]),
    )
    for e1 in tri_edges:
        for e2 in rect_edges:
            if _seg_intersect(e1[0], e1[1], e2[0], e2[1]):
                return True
    return False
