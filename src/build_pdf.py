# -*- coding: utf-8 -*-
"""
Generador vectorial PDF (sin dependencias externas) para el Estudio Pre-Flop 6-Max Torneo (Sin Ante).
Ejecución:
    python3 src/build_pdf.py
Salida:
    docs/Six-Max_Torneo_Estudio_PreFlop.pdf
"""
import os
import zlib
from pathlib import Path
from ranges_data import RANKS, RFI_LIST, BB_LIST, TB_LIST, nash_val


def parse_range(tokens):
    s = set()
    if not tokens:
        return s
    for raw in tokens:
        t = raw.strip()
        if not t:
            continue
        plus = t.endswith("+")
        if plus:
            t = t[:-1]
        if "-" in t:
            a, b = t.split("-")
            if len(a) == 2 and a[0] == a[1]:
                i1, i2 = RANKS.index(a[0]), RANKS.index(b[0])
                for i in range(min(i1, i2), max(i1, i2) + 1):
                    s.add(RANKS[i] + RANKS[i])
            else:
                kind = a[2]
                hi = a[0]
                i1, i2 = RANKS.index(a[1]), RANKS.index(b[1])
                for i in range(min(i1, i2), max(i1, i2) + 1):
                    s.add(hi + RANKS[i] + kind)
            continue
        if len(t) == 2 and t[0] == t[1]:
            if plus:
                idx = RANKS.index(t[0])
                for i in range(0, idx + 1):
                    s.add(RANKS[i] + RANKS[i])
            else:
                s.add(t)
        else:
            hi, lo, kind = t[0], t[1], t[2]
            if plus:
                hi_idx, lo_idx = RANKS.index(hi), RANKS.index(lo)
                for i in range(hi_idx + 1, lo_idx + 1):
                    s.add(hi + RANKS[i] + kind)
            else:
                s.add(t)
    return s


def hand_at(r, c):
    if r == c:
        return RANKS[r] + RANKS[c]
    if r < c:
        return RANKS[r] + RANKS[c] + "s"
    return RANKS[c] + RANKS[r] + "o"


def pdf_escape(txt):
    b = txt.encode("cp1252", errors="replace")
    out = bytearray()
    for ch in b:
        if ch in (40, 41, 92):
            out.append(92)
            out.append(ch)
        elif 32 <= ch <= 126:
            out.append(ch)
        else:
            out.extend(f"\\{ch:03o}".encode("ascii"))
    return out.decode("ascii")


class PDFCanvas:
    def __init__(self, width=841.89, height=595.28):  # A4 Landscape
        self.width = width
        self.height = height
        self.pages = []
        self.cur = []

    def new_page(self):
        if self.cur:
            self.pages.append("\n".join(self.cur))
        self.cur = []
        self.rect(0, 0, self.width, self.height, fill=(0.05, 0.07, 0.11))

    def rect(self, x, y_top, w, h, fill=None, stroke=None, lw=0.5):
        y = self.height - y_top - h
        cmds = []
        if lw:
            cmds.append(f"{lw:.2f} w")
        if fill and stroke:
            cmds.append(f"{fill[0]:.3f} {fill[1]:.3f} {fill[2]:.3f} rg")
            cmds.append(f"{stroke[0]:.3f} {stroke[1]:.3f} {stroke[2]:.3f} RG")
            cmds.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re B")
        elif fill:
            cmds.append(f"{fill[0]:.3f} {fill[1]:.3f} {fill[2]:.3f} rg")
            cmds.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")
        elif stroke:
            cmds.append(f"{stroke[0]:.3f} {stroke[1]:.3f} {stroke[2]:.3f} RG")
            cmds.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re S")
        self.cur.append(" ".join(cmds))

    def text(self, x, y_top, txt, size=10, bold=False, color=(1, 1, 1)):
        y = self.height - y_top - size * 0.82
        font = "/F2" if bold else "/F1"
        esc = pdf_escape(txt)
        self.cur.append(
            f"BT {font} {size:.2f} Tf {color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg {x:.2f} {y:.2f} Td ({esc}) Tj ET"
        )

    def save(self, path):
        if self.cur:
            self.pages.append("\n".join(self.cur))
            self.cur = []

        objs = []

        def add_obj(content_bytes):
            objs.append(content_bytes)
            return len(objs)

        add_obj(b"<< /Type /Catalog /Pages 2 0 R >>")
        add_obj(b"")
        add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")

        page_ids = []
        for p_str in self.pages:
            raw = p_str.encode("latin1")
            comp = zlib.compress(raw)
            stream_obj = (
                f"<< /Length {len(comp)} /Filter /FlateDecode >>\nstream\n".encode("latin1")
                + comp
                + b"\nendstream"
            )
            s_id = add_obj(stream_obj)
            page_dict = (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width:.2f} {self.height:.2f}] "
                f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {s_id} 0 R >>"
            ).encode("latin1")
            p_id = add_obj(page_dict)
            page_ids.append(p_id)

        kids = " ".join(f"{pid} 0 R" for pid in page_ids)
        objs[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("latin1")

        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = []
        for idx, body in enumerate(objs, start=1):
            offsets.append(len(out))
            out.extend(f"{idx} 0 obj\n".encode("latin1"))
            out.extend(body)
            out.extend(b"\nendobj\n")

        xref_pos = len(out)
        out.extend(f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode("latin1"))
        for off in offsets:
            out.extend(f"{off:010d} 00000 n \n".encode("latin1"))
        out.extend(
            f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("latin1")
        )
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(out)


C_BG_CARD = (0.08, 0.11, 0.17)
C_BORDER = (0.16, 0.22, 0.33)
C_FOLD = (0.10, 0.14, 0.21)
C_RAISE = (0.06, 0.72, 0.50)
C_MIX = (0.96, 0.62, 0.04)
C_3B_VAL = (0.93, 0.26, 0.26)
C_3B_BLUFF = (0.65, 0.33, 0.96)
C_CALL = (0.05, 0.65, 0.91)
C_WHITE = (0.96, 0.98, 1.0)
C_MUTED = (0.58, 0.64, 0.72)
C_DARK = (0.03, 0.12, 0.10)


def draw_header(pdf, title, subtitle, legend_items):
    pdf.rect(24, 18, pdf.width - 48, 38, fill=C_BG_CARD, stroke=C_BORDER, lw=0.8)
    pdf.text(36, 25, title, size=11.0, bold=True, color=C_WHITE)
    pdf.text(36, 41, subtitle, size=8.0, bold=False, color=C_MUTED)
    lx = pdf.width - 34
    for label, col in reversed(legend_items):
        tw = len(label) * 4.3 + 22
        lx -= tw
        pdf.rect(lx, 26, 9, 9, fill=col, stroke=(1, 1, 1), lw=0.3)
        pdf.text(lx + 13, 27, label, size=7.8, bold=True, color=C_WHITE)


def draw_matrix(pdf, x, y, size, title, sub, cell_fn):
    pdf.rect(x, y, size, size + 36, fill=C_BG_CARD, stroke=C_BORDER, lw=0.7)
    pdf.text(x + 8, y + 6, title, size=9.2, bold=True, color=C_WHITE)
    pdf.text(x + 8, y + 18, sub, size=7.2, bold=False, color=C_MUTED)

    grid_x = x + 6
    grid_y = y + 28
    grid_sz = size - 12
    cell_w = grid_sz / 13.0

    for r in range(13):
        for c in range(13):
            h = hand_at(r, c)
            bg, fg, sub_lbl = cell_fn(r, c, h)
            cx = grid_x + c * cell_w
            cy = grid_y + r * cell_w
            stroke_c = (0.35, 0.45, 0.60) if r == c else (0.14, 0.19, 0.28)
            pdf.rect(cx + 0.4, cy + 0.4, cell_w - 0.8, cell_w - 0.8, fill=bg, stroke=stroke_c, lw=0.35)
            pdf.text(cx + 1.8, cy + 2.0, h, size=5.5 if len(h) == 3 else 5.8, bold=True, color=fg)
            if sub_lbl:
                pdf.text(cx + 1.8, cy + cell_w - 6.2, sub_lbl, size=4.5, bold=False, color=fg)


def generate_pdf(pdf_path):
    pdf = PDFCanvas()
    coords = [(24, 66), (294, 66), (564, 66), (24, 330), (294, 330)]
    coords6 = [(24, 66), (294, 66), (564, 66), (24, 330), (294, 330), (564, 330)]
    bx, by, bw, bh = 564, 330, 252, 246

    # PAGE 1: RFI
    pdf.new_page()
    draw_header(
        pdf,
        "ESTUDIO PRE-FLOP: 6-MAX TORNEO (SIN ANTE) — 1. RANGOS DE APERTURA (RFI ~100 BB)",
        "Diagonal = Pares · Arriba derecha = Suited (s) · Abajo izquierda = Offsuit (o) · Bote inicial = 1.5 bb",
        [("Abrir 100%", C_RAISE), ("Mixta (~50%)", C_MIX), ("Fold", C_FOLD)],
    )
    for idx, (title, sub, r_tok, m_tok, _) in enumerate(RFI_LIST):
        s_r, s_m = parse_range(r_tok), parse_range(m_tok)
        def fn(r, c, h, sr=s_r, sm=s_m):
            if h in sr: return (C_RAISE, C_DARK, "")
            if h in sm: return (C_MIX, C_DARK, "50%")
            return (C_FOLD, C_MUTED, "")
        draw_matrix(pdf, coords[idx][0], coords[idx][1], 252, title, sub, fn)

    pdf.rect(bx, by, bw, bh, fill=C_BG_CARD, stroke=C_BORDER, lw=0.7)
    pdf.text(bx + 12, by + 12, "CLAVES RFI Y AJUSTE POR STACK", size=9.5, bold=True, color=C_WHITE)
    lines = [
        ("Sin ante robar vale menos:", True, C_MIX),
        ("Solo hay 1.5 bb en el centro (frente a ~2.25 bb", False, C_WHITE),
        ("con ante). No abras basura offsuit en CO/BTN.", False, C_WHITE),
        ("Por qué abrir A5s-A2s:", True, C_RAISE),
        ("Bloquean AA/AK del rival y tienen proyecto", False, C_WHITE),
        ("de color al As + escalera (rueda A-2-3-4-5).", False, C_WHITE),
        ("Ajuste por Stack Efectivo:", True, C_CALL),
        ("• > 60 bb: Tablas estándar; alto valor suited.", False, C_WHITE),
        ("• 30-45 bb: Quita suited débiles (54s, 64s).", False, C_WHITE),
        ("• 18-28 bb: Abre 2bb; prepara respuesta a shove.", False, C_WHITE),
        ("• < 15 bb: Usa las tablas Push/Fold (Pág. 4).", False, C_WHITE),
        ("Factor Burbuja / ICM:", True, C_3B_VAL),
        ("Con saltos de premio estrecha UTG/HJ y evita", False, C_WHITE),
        ("pagar 3-bets fuera de posición.", False, C_WHITE),
    ]
    ly = by + 32
    for txt, is_b, col in lines:
        pdf.text(bx + 12, ly, txt, size=7.6, bold=is_b, color=col)
        ly += 14.5 if is_b else 12.5

    # PAGE 2: BB DEFENSE
    pdf.new_page()
    draw_header(
        pdf,
        "2. DEFENSA DE BIG BLIND (SIN ANTE, VS OPEN RAISE DE 2.5 BB / 3.0 BB)",
        "Pot Odds sin ante vs 2.5bb = 27.3% (1.5 bb para ganar 5.5 bb) · Defiende más estrecho que en torneos con ante",
        [("3-Bet Valor", C_3B_VAL), ("3-Bet Bluff", C_3B_BLUFF), ("Call", C_CALL), ("Fold", C_FOLD)],
    )
    for idx, (title, sub, v_tok, b_tok, c_tok) in enumerate(BB_LIST):
        sv, sb, sc = parse_range(v_tok), parse_range(b_tok), parse_range(c_tok)
        def fn(r, c, h, sv=sv, sb=sb, sc=sc):
            if h in sv: return (C_3B_VAL, C_WHITE, "3BV")
            if h in sb: return (C_3B_BLUFF, C_WHITE, "3BB")
            if h in sc: return (C_CALL, C_WHITE, "")
            return (C_FOLD, C_MUTED, "")
        draw_matrix(pdf, coords[idx][0], coords[idx][1], 252, title, sub, fn)

    pdf.rect(bx, by, bw, bh, fill=C_BG_CARD, stroke=C_BORDER, lw=0.7)
    pdf.text(bx + 12, by + 12, "REGLAS DE DEFENSA EN BIG BLIND", size=9.5, bold=True, color=C_WHITE)
    bb_lines = [
        ("1. Matemática Sin Ante:", True, C_CALL),
        ("Contra un open a 2.5 bb necesitas 27.3% de", False, C_WHITE),
        ("equity bruta (con ante solo necesitas ~21%).", False, C_WHITE),
        ("Por eso foldeas manos offsuit débiles.", False, C_WHITE),
        ("2. Cuidado con la Dominación:", True, C_3B_VAL),
        ("Contra UTG/HJ foldea ATo, KJo, QJo: cuando", False, C_WHITE),
        ("ligas pareja alta sueles ir dominado.", False, C_WHITE),
        ("3. Estructura del 3-Bet OOP:", True, C_3B_BLUFF),
        ("Usa un tamaño de 10-11 bb (4x-4.4x) fuera de", False, C_WHITE),
        ("posición para negar la ventaja posicional.", False, C_WHITE),
        ("4. Si el rival abre a 2.0 bb (Min-Raise):", True, C_RAISE),
        ("Tus Pot Odds bajan al 22.2%: añade un 8% más", False, C_WHITE),
        ("de Calls con manos suited y conectores.", False, C_WHITE),
    ]
    ly = by + 32
    for txt, is_b, col in bb_lines:
        pdf.text(bx + 12, ly, txt, size=7.6, bold=is_b, color=col)
        ly += 14.5 if is_b else 12.5

    # PAGE 3: 3-BET & DEFENSE VS 3-BET
    pdf.new_page()
    draw_header(
        pdf,
        "3. RANGOS DE 3-BET (IP Y SB) Y DEFENSA CONTRA 3-BET (~100 BB SIN ANTE)",
        "En SB sin ante se juega estrategia pura de '3-Bet o Fold' · En defensa vs 3-Bet: Rojo = 4-Bet Valor, Morado = 4-Bet Bluff, Azul = Call",
        [("3B/4B Valor", C_3B_VAL), ("3B/4B Bluff", C_3B_BLUFF), ("Call", C_CALL), ("Fold", C_FOLD)],
    )
    for idx, (title, sub, v_tok, b_tok, c_tok) in enumerate(TB_LIST):
        sv, sb, sc = parse_range(v_tok), parse_range(b_tok), parse_range(c_tok)
        def fn(r, c, h, sv=sv, sb=sb, sc=sc):
            if h in sv: return (C_3B_VAL, C_WHITE, "")
            if h in sb: return (C_3B_BLUFF, C_WHITE, "")
            if h in sc: return (C_CALL, C_WHITE, "")
            return (C_FOLD, C_MUTED, "")
        draw_matrix(pdf, coords6[idx][0], coords6[idx][1], 252, title, sub, fn)

    # PAGE 4: PUSH / FOLD NASH
    pdf.new_page()
    draw_header(
        pdf,
        "4. TABLAS PUSH / FOLD NASH (SIN ANTE, STACK CORTO < 20 BB)",
        "El número dentro de cada celda indica el STACK MÁXIMO (en BB) con el que esa mano es All-In (o Call en BB) rentable",
        [("Push >14bb", C_RAISE), ("Push 8-14bb", C_MIX), ("Push 4-7bb", C_3B_VAL), ("Fold", C_FOLD)],
    )
    pf_titles = [
        ("UTG Push (Sin Ante)", "All-In directo desde UTG"),
        ("HJ Push (Sin Ante)", "All-In directo desde HJ"),
        ("CO Push (Sin Ante)", "All-In directo desde CO"),
        ("BTN Push (Sin Ante)", "All-In directo desde BTN"),
        ("SB Push vs BB (Sin Ante)", "All-In directo desde SB"),
        ("BB Call vs SB Push (Sin Ante)", "Stack máx. para pagar All-In de SB"),
    ]
    for idx, (title, sub) in enumerate(pf_titles):
        def fn(r, c, h, p_idx=idx):
            v = nash_val(p_idx, r, c)
            if v >= 15:
                return (C_RAISE, C_DARK, "20+" if v == 20 else f"{v}b")
            elif v >= 8:
                return (C_MIX, C_DARK, f"{v}b")
            elif v >= 3:
                return (C_3B_VAL, C_WHITE, f"{v}b")
            return (C_FOLD, C_MUTED, "")
        draw_matrix(pdf, coords6[idx][0], coords6[idx][1], 252, title, sub, fn)

    pdf.save(pdf_path)


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    out_pdf = root_dir / "docs" / "Six-Max_Torneo_Estudio_PreFlop.pdf"
    generate_pdf(str(out_pdf))
    print(f"PDF generado correctamente en: {out_pdf.relative_to(root_dir)} ({os.path.getsize(out_pdf)} bytes)")
