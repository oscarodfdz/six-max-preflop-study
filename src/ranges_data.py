# -*- coding: utf-8 -*-
"""
Datos estructurados de rangos pre-flop para 6-Max Torneo (Sin Ante).
Incluye:
1. RFI (Raise First In ~100bb)
2. Defensa de Big Blind (vs Open Raise 2.5bb / 3.0bb)
3. 3-Bet IP / SB y Defensa contra 3-Bet (4-Bet / Call)
4. Matrices Nash Push / Fold (< 20bb Sin Ante)
"""

RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

RFI_LIST = [
    (
        "1. UTG (Lojack)",
        "Open: 2.0-2.5 bb · ~15.2%",
        ["55+", "ATs+", "A5s-A4s", "KTs+", "QTs+", "JTs", "T9s", "AJo+", "KQo"],
        ["44-22", "A9s", "A8s", "A3s-A2s", "K9s", "98s", "87s", "ATo", "KJo"],
        "Más cerrado: evita offsuit dominadas (KTo, QJo).",
    ),
    (
        "2. HJ (Hijack)",
        "Open: 2.0-2.5 bb · ~19.8%",
        ["22+", "A8s+", "A5s-A2s", "K9s+", "Q9s+", "J9s+", "T9s", "98s", "87s", "76s", "ATo+", "KJo+"],
        ["A7s-A6s", "K8s", "T8s", "65s", "QJo", "KTo"],
        "Entran todos los pares 22+ y más suited conectadas.",
    ),
    (
        "3. CO (Cutoff)",
        "Open: 2.0-2.5 bb · ~27.8%",
        ["22+", "A2s+", "K7s+", "Q8s+", "J8s+", "T8s+", "97s+", "87s", "76s", "65s", "54s", "A9o+", "KTo+", "QTo+", "JTo"],
        ["K6s-K5s", "96s", "86s", "75s", "A8o", "K9o", "Q9o", "J9o"],
        "Todos los Ases suited (A2s+) y broadways offsuit.",
    ),
    (
        "4. BTN (Botón)",
        "Open: 2.0-2.5 bb · ~44.5%",
        ["22+", "A2s+", "K2s+", "Q4s+", "J6s+", "T6s+", "96s+", "85s+", "75s+", "64s+", "53s+", "43s", "A7o+", "K8o+", "Q9o+", "J9o+", "T9o", "98o"],
        ["Q3s-Q2s", "J5s-J4s", "T5s", "95s", "84s", "74s", "63s", "52s", "A6o-A2o", "K7o", "Q8o", "J8o", "T8o", "87o"],
        "Posición ideal IP. Sin ante no abras basura offsuit.",
    ),
    (
        "5. SB vs BB",
        "Open: 3.0 bb (o Limp mix) · ~42.5%",
        ["22+", "A2s+", "K2s+", "Q4s+", "J6s+", "T6s+", "96s+", "85s+", "75s+", "64s+", "54s", "A7o+", "K8o+", "Q9o+", "J9o+", "T9o"],
        ["Q3s-Q2s", "J5s", "T5s", "95s", "53s", "43s", "A6o-A2o", "K7o", "Q8o", "J8o", "T8o", "98o", "87o"],
        "Fuera de posición: sube a 3 bb o mezcla con Limp.",
    ),
]

BB_LIST = [
    (
        "BB vs UTG Open (2.5 bb)",
        "3-Bet OOP: 10-11 bb · Defensa ~25%",
        ["JJ+", "AKs", "AQs", "AKo"],
        ["A5s-A4s", "KTs", "QTs", "JTs", "T9s"],
        ["TT-22", "AJs-A6s", "A3s-A2s", "KQs-KJs", "K9s", "QJs", "Q9s", "J9s", "98s", "87s", "76s", "65s", "54s", "AQo-AJo", "KQo"],
    ),
    (
        "BB vs HJ Open (2.5 bb)",
        "3-Bet OOP: 10-11 bb · Defensa ~29%",
        ["TT+", "AQs+", "AKo", "AQo"],
        ["A5s-A3s", "KTs", "QTs", "JTs", "T9s", "98s"],
        ["99-22", "AJs-A6s", "A2s", "KQs-KJs", "K9s-K8s", "QJs", "Q9s-Q8s", "J9s-J8s", "T8s", "87s", "76s", "65s", "54s", "AJo-ATo", "KQo-KJo"],
    ),
    (
        "BB vs CO Open (2.5 bb)",
        "3-Bet OOP: 10-11 bb · Defensa ~36%",
        ["99+", "AJs+", "KQs", "AKo-AQo"],
        ["A5s-A2s", "K9s", "Q9s", "J9s", "T8s", "97s", "87s", "76s", "ATo", "KJo"],
        ["88-22", "ATs-A6s", "KJs-KTs", "K8s-K5s", "QJs-QTs", "Q8s-Q7s", "JTs", "J8s", "T9s", "98s", "86s", "75s", "65s", "54s", "43s", "AJo", "A9o", "KQo", "QJo", "JTo"],
    ),
    (
        "BB vs BTN Open (2.5 bb)",
        "3-Bet OOP: 10.5-11.5 bb · Defensa ~49%",
        ["88+", "ATs+", "KJs+", "QJs", "AKo-AJo", "KQo"],
        ["A5s-A2s", "K7s-K5s", "Q8s", "J8s", "T7s", "97s", "86s", "75s", "64s", "54s", "A9o-A8o", "KTo", "QTo"],
        ["77-22", "A9s-A6s", "KTs-K8s", "K4s-K2s", "QTs-Q9s", "Q7s-Q4s", "JTs-J9s", "J7s-J6s", "T9s-T8s", "T6s", "98s", "96s", "87s", "85s", "76s", "65s", "53s", "43s", "ATo", "A7o-A4o", "KJo", "K9o", "QJo", "JTo", "T9o", "98o"],
    ),
    (
        "BB vs SB Open (3.0 bb) IP",
        "3-Bet IP: 8.5-9.0 bb · Defensa ~55%",
        ["88+", "ATs+", "KJs+", "QJs", "AKo-AJo", "KQo"],
        ["A5s-A2s", "K6s-K4s", "Q7s-Q6s", "J7s", "T7s", "96s", "85s", "75s", "64s", "53s", "A8o-A7o", "K9o", "Q9o", "J9o"],
        ["77-22", "A9s-A6s", "KTs-K7s", "K3s-K2s", "QTs-Q8s", "Q5s-Q2s", "JTs-J8s", "J6s-J5s", "T9s-T8s", "T6s", "98s-97s", "87s-86s", "76s", "65s", "54s", "43s", "ATo", "A9o", "A6o-A2o", "KJo-KTo", "K8o", "QJo-QTo", "JTo", "T9o", "98o", "87o"],
    ),
]

TB_LIST = [
    (
        "BTN vs CO Open (2.5 bb) IP",
        "3-Bet IP: 7.5 bb",
        ["TT+", "AJs+", "KQs", "AKo-AQo"],
        ["A9s-A8s", "A5s-A2s", "KTs-K9s", "QTs", "J9s", "T8s", "87s", "76s", "AJo", "KQo"],
        ["99-44", "ATs", "A7s-A6s", "KJs", "QJs", "JTs", "T9s", "98s"],
    ),
    (
        "CO vs UTG/HJ Open (2.5 bb)",
        "3-Bet IP: 7.5 bb",
        ["JJ+", "AQs+", "AKo"],
        ["A5s-A4s", "KQs", "KTs", "QTs", "AQo"],
        ["TT-55", "AJs-ATs", "KJs", "QJs", "JTs", "T9s"],
    ),
    (
        "SB vs BTN Open (3-Bet o Fold)",
        "3-Bet OOP: 10-11 bb (Sin Cold Call)",
        ["77+", "A9s+", "KTs+", "QTs+", "JTs", "ATo+", "KQo"],
        ["66-55", "A8s-A2s", "K9s", "Q9s", "J9s", "T9s", "98s", "87s", "KJo"],
        [],
    ),
    (
        "SB vs UTG/HJ Open (3-Bet o Fold)",
        "3-Bet OOP: 10-11 bb",
        ["TT+", "AJs+", "KQs", "AKo-AQo"],
        ["99-88", "ATs", "A5s-A4s", "KJs", "QJs", "JTs"],
        [],
    ),
    (
        "Defensa: UTG/HJ vs 3-Bet",
        "Rojo=4B Valor · Morado=4B Bluff · Azul=Call",
        ["QQ+", "AKs", "AKo"],
        ["A5s-A4s", "AQs"],
        ["JJ-77", "AJs-ATs", "KQs-KJs", "QJs", "JTs", "T9s", "AQo"],
    ),
    (
        "Defensa: CO/BTN vs Blinds 3-Bet IP",
        "Rojo=4B Valor · Morado=4B Bluff · Azul=Call",
        ["JJ+", "AQs+", "AKo-AQo"],
        ["A5s-A3s", "K9s", "Q9s", "ATo", "KQo"],
        ["TT-44", "AJs-A7s", "KQs-KTs", "QJs-QTs", "JTs-J9s", "T9s-T8s", "98s", "87s", "76s", "65s", "AJo"],
    ),
]

UNCAPPED_SB_NASH = [
    [60, 60, 55, 50, 46, 38, 35, 33, 30, 32, 30, 28, 26],
    [60, 60, 48, 42, 36, 28, 22, 19, 17, 16, 14, 13, 12],
    [52, 38, 60, 36, 30, 21, 16, 13, 12, 11, 10,  9,  8],
    [44, 28, 22, 60, 28, 19, 15, 11,  9,  8,  7,  6,  6],
    [38, 22, 17, 16, 60, 22, 16, 12,  9,  7,  6,  5,  5],
    [26, 14, 11, 11, 12, 60, 19, 14, 10,  7,  5,  4,  0],
    [22, 11,  9,  8,  9,  9, 55, 17, 12,  9,  6,  4,  0],
    [19,  9,  7,  6,  7,  7,  7, 50, 15, 11,  7,  4,  0],
    [16,  8,  6,  4,  5,  6,  6,  6, 45, 13,  8,  5,  0],
    [16,  7,  5,  0,  0,  4,  5,  5,  5, 40, 11,  6,  4],
    [14,  6,  4,  0,  0,  0,  0,  4,  4,  4, 34,  7,  4],
    [13,  5,  0,  0,  0,  0,  0,  0,  0,  0,  0, 28,  4],
    [12,  5,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 24],
]


def nash_val(pos_idx, r, c):
    raw = UNCAPPED_SB_NASH[r][c]
    if raw == 0:
        return 0
    mults = [0.40, 0.52, 0.68, 0.86, 1.00, 0.72]
    shifts = [-2.2, -1.5, -0.8, -0.2, 0.0, -1.8]
    val = round(raw * mults[pos_idx] + shifts[pos_idx])
    if r == c and pos_idx <= 3:
        val = max(val, round(raw * (mults[pos_idx] + 0.08)))
    return 0 if val < 3 else min(20, val)
