# -*- coding: utf-8 -*-
"""
Generador de la aplicación interactiva HTML (index.html) para Six-Max Torneo (Sin Ante).
Carga variables sensibles (como GEMINI_API_KEY si se integra IA) exclusivamente desde
variables de entorno (.env ignorado por Git), nunca en el código fuente.

Ejecución:
    python3 src/build_html.py
Salida:
    index.html
"""
import os
from pathlib import Path

# Lectura segura de clave API desde el entorno (nunca expuesta en el repositorio)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Estudio Pre-Flop: 6-Max Torneo (Sin Ante) — Guía Interactiva GTO</title>
<style>
  :root {
    --bg-main: #0b0f17;
    --bg-card: #131b29;
    --bg-card-alt: #182234;
    --bg-cell-fold: #1a2333;
    --border-color: #26334d;
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
    --accent-gold: #f59e0b;
    --accent-blue: #3b82f6;
    
    /* Action Colors (Solver Style) */
    --col-raise: #10b981;       /* Pure Open / Value */
    --col-raise-dark: #065f46;
    --col-mix: #f59e0b;         /* Mixed / 50% Frequency */
    --col-mix-dark: #78350f;
    --col-3bet-val: #ef4444;    /* 3-Bet / 4-Bet Value / Push */
    --col-3bet-val-dark: #7f1d1d;
    --col-3bet-bluff: #a855f7;  /* 3-Bet / 4-Bet Bluff / Polar */
    --col-3bet-bluff-dark: #581c87;
    --col-call: #0ea5e9;        /* Cold Call / Defend / Limp */
    --col-call-dark: #0c4a6e;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Helvetica, Arial, sans-serif;
    background: radial-gradient(circle at top, #152036 0%, var(--bg-main) 65%);
    color: var(--text-main);
    line-height: 1.5;
    min-height: 100vh;
    padding-bottom: 60px;
  }

  /* Header */
  header {
    background: rgba(19, 27, 41, 0.9);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    padding: 20px 28px;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .header-inner {
    max-width: 1440px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .brand-badge {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #10b981, #059669);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.2rem;
    color: #fff;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
  }

  .brand-title h1 {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #fff;
  }

  .brand-title p {
    font-size: 0.85rem;
    color: var(--text-muted);
  }

  .header-actions {
    display: flex;
    gap: 10px;
    align-items: center;
  }

  .btn-action {
    background: var(--bg-card-alt);
    color: var(--text-main);
    border: 1px solid var(--border-color);
    padding: 9px 15px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .btn-action:hover {
    border-color: var(--accent-blue);
    background: #1e2c45;
  }

  .btn-action.primary {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    border-color: #3b82f6;
    color: #fff;
  }

  .btn-action.primary:hover {
    filter: brightness(1.1);
  }

  /* Navigation Tabs */
  .nav-tabs {
    max-width: 1440px;
    margin: 22px auto 0;
    padding: 0 28px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .tab-btn {
    background: var(--bg-card);
    color: var(--text-muted);
    border: 1px solid var(--border-color);
    padding: 12px 18px;
    border-radius: 10px;
    font-size: 0.92rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.18s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .tab-btn:hover {
    color: var(--text-main);
    border-color: #3b4d71;
  }

  .tab-btn.active {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    color: #fff;
    border-color: var(--col-raise);
    box-shadow: 0 0 0 1px var(--col-raise), 0 6px 20px rgba(16, 185, 129, 0.15);
  }

  .tab-pill {
    font-size: 0.72rem;
    padding: 2px 7px;
    border-radius: 99px;
    background: rgba(255, 255, 255, 0.08);
    color: #cbd5e1;
  }

  /* Main Container */
  main {
    max-width: 1440px;
    margin: 20px auto 0;
    padding: 0 28px;
  }

  .tab-section {
    display: none;
  }

  .tab-section.active {
    display: block;
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Sub-navigation / Position Selector */
  .sub-bar {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
  }

  .pos-group {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
  }

  .pos-btn {
    background: var(--bg-card-alt);
    color: var(--text-muted);
    border: 1px solid var(--border-color);
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.88rem;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .pos-btn:hover {
    color: #fff;
    border-color: #475569;
  }

  .pos-btn.active {
    background: var(--col-raise);
    color: #042f2e;
    border-color: #34d399;
    box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
  }

  /* Legend */
  .legend {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    align-items: center;
    font-size: 0.82rem;
    color: #cbd5e1;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .swatch {
    width: 14px;
    height: 14px;
    border-radius: 4px;
    display: inline-block;
  }

  /* Workspace Grid: Left Matrix + Right Details */
  .workspace {
    display: grid;
    grid-template-columns: minmax(480px, 680px) 1fr;
    gap: 24px;
    align-items: start;
  }

  @media (max-width: 1080px) {
    .workspace {
      grid-template-columns: 1fr;
    }
  }

  /* 13x13 Hand Matrix */
  .matrix-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
  }

  .matrix-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 12px;
    padding: 0 4px;
  }

  .matrix-header h2 {
    font-size: 1.15rem;
    font-weight: 800;
    color: #fff;
  }

  .matrix-header .subtitle {
    font-size: 0.84rem;
    color: var(--text-muted);
    font-weight: 600;
  }

  .matrix-grid {
    display: grid;
    grid-template-columns: repeat(13, 1fr);
    gap: 3px;
    user-select: none;
  }

  .hand-cell {
    aspect-ratio: 1 / 0.92;
    border-radius: 5px;
    background: var(--bg-cell-fold);
    border: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 3px 4px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: transform 0.08s ease, box-shadow 0.08s ease;
  }

  .hand-cell:hover {
    transform: scale(1.12);
    z-index: 10;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.65);
    border-color: #fff;
  }

  .hand-cell.pair {
    border-color: rgba(255, 255, 255, 0.16);
  }

  .hand-label {
    font-size: 0.76rem;
    font-weight: 800;
    line-height: 1;
    z-index: 2;
    letter-spacing: -0.02em;
  }

  .hand-sub {
    font-size: 0.62rem;
    font-weight: 700;
    opacity: 0.88;
    z-index: 2;
    text-align: right;
    line-height: 1;
  }

  /* Action Styles for Cells */
  .act-fold {
    background: #161f2e;
    color: #64748b;
  }

  .act-raise {
    background: linear-gradient(145deg, #10b981, #059669);
    color: #022c22;
    border-color: rgba(255,255,255,0.22);
  }
  .act-raise .hand-sub { color: #064e3b; }

  .act-mix {
    background: linear-gradient(90deg, #10b981 50%, #1e293b 50%);
    color: #fff;
    border-color: #f59e0b;
  }
  .act-mix .hand-label {
    text-shadow: 0 1px 3px rgba(0,0,0,0.9);
  }
  .act-mix .hand-sub {
    color: #fde68a;
    text-shadow: 0 1px 2px rgba(0,0,0,0.9);
  }

  .act-limp {
    background: linear-gradient(135deg, #0ea5e9, #0284c7);
    color: #082f49;
  }

  .act-3bet-val {
    background: linear-gradient(145deg, #ef4444, #dc2626);
    color: #fff;
    border-color: rgba(255,255,255,0.25);
  }

  .act-3bet-bluff {
    background: linear-gradient(145deg, #a855f7, #7e22ce);
    color: #fff;
    border-color: rgba(255,255,255,0.22);
  }

  .act-call {
    background: linear-gradient(145deg, #0ea5e9, #0369a1);
    color: #fff;
    border-color: rgba(255,255,255,0.2);
  }

  .act-call-mix {
    background: linear-gradient(90deg, #0ea5e9 55%, #1e293b 55%);
    color: #fff;
    border-color: #38bdf8;
  }

  /* Right Side Info Panel */
  .info-panel {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .info-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 18px 20px;
  }

  .info-card h3 {
    font-size: 1rem;
    font-weight: 800;
    margin-bottom: 12px;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  /* Stats Bars */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px;
    margin-bottom: 14px;
  }

  .stat-box {
    background: var(--bg-card-alt);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 10px 12px;
  }

  .stat-box .stat-label {
    font-size: 0.74rem;
    color: var(--text-muted);
    text-transform: uppercase;
    font-weight: 700;
  }

  .stat-box .stat-val {
    font-size: 1.3rem;
    font-weight: 800;
    margin-top: 2px;
  }

  .stat-box .stat-sub {
    font-size: 0.74rem;
    color: var(--text-muted);
  }

  .freq-bar {
    height: 12px;
    border-radius: 99px;
    background: #1e293b;
    overflow: hidden;
    display: flex;
    margin-top: 6px;
  }

  .freq-seg {
    height: 100%;
    transition: width 0.25s ease;
  }

  /* Notes list */
  .notes-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 9px;
    font-size: 0.9rem;
    color: #cbd5e1;
  }

  .notes-list li {
    position: relative;
    padding-left: 18px;
  }

  .notes-list li::before {
    content: "▸";
    position: absolute;
    left: 0;
    color: var(--col-raise);
    font-weight: bold;
  }

  /* Inspector Box */
  .inspector-box {
    background: linear-gradient(135deg, #182235, #111827);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .inspector-badge {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    background: #1e293b;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    font-weight: 900;
    flex-shrink: 0;
    border: 2px solid rgba(255,255,255,0.15);
  }

  /* Multi-Grid Overview (All Positions at once) */
  .overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }

  .overview-grid .hand-label {
    font-size: 0.62rem;
  }
  .overview-grid .hand-sub {
    display: none;
  }

  /* Slider for Push/Fold */
  .slider-wrap {
    display: flex;
    align-items: center;
    gap: 14px;
    background: var(--bg-card-alt);
    padding: 10px 16px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
  }

  .slider-wrap input[type=range] {
    width: 190px;
    accent-color: var(--col-raise);
    cursor: pointer;
  }

  .stack-pill {
    background: var(--col-3bet-val);
    color: #fff;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 0.95rem;
    min-width: 68px;
    text-align: center;
  }

  /* Guide Tables */
  .guide-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 20px;
  }

  table.clean-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    margin-top: 8px;
  }

  table.clean-table th,
  table.clean-table td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border-color);
    text-align: left;
  }

  table.clean-table th {
    color: var(--text-muted);
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  /* Print / PDF Stylesheet */
  @media print {
    body {
      background: #fff !important;
      color: #000 !important;
      padding: 0;
    }
    header, .nav-tabs, .sub-bar, .no-print {
      display: none !important;
    }
    main {
      max-width: 100%;
      padding: 0;
      margin: 0;
    }
    #print-all-container {
      display: block !important;
    }
    .tab-section {
      display: none !important;
    }
    .print-page {
      page-break-after: always;
      padding: 10px;
    }
    .print-grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    .matrix-card {
      background: #fff !important;
      border: 1px solid #cbd5e1 !important;
      box-shadow: none !important;
      padding: 10px !important;
      break-inside: avoid;
    }
    .matrix-header h2 {
      color: #0f172a !important;
      font-size: 0.95rem !important;
    }
    .hand-cell {
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
      border: 1px solid #cbd5e1 !important;
    }
    .act-fold {
      background: #f1f5f9 !important;
      color: #64748b !important;
    }
  }

  #print-all-container {
    display: none;
  }
</style>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="brand">
      <div class="brand-badge">6M</div>
      <div class="brand-title">
        <h1>Estudio Pre-Flop: Six-Max Torneo (Sin Ante)</h1>
        <p>Rangos GTO (Chip-EV) · Apertura (RFI), Defensa de BB, 3-Bet / 4-Bet y Tablas Push/Fold Nash</p>
      </div>
    </div>
    <div class="header-actions no-print">
      <button class="btn-action" onclick="toggleCompareAllRFI()">
        <span>⊞</span> Ver las 5 Aperturas Juntas
      </button>
      <button class="btn-action primary" onclick="printFullStudy()">
        <span>🖨️</span> Guardar / Imprimir PDF Completo
      </button>
    </div>
  </div>
</header>

<nav class="nav-tabs no-print">
  <button class="tab-btn active" onclick="switchTab('rfi', this)">
    1. Apertura (RFI) <span class="tab-pill">100 bb</span>
  </button>
  <button class="tab-btn" onclick="switchTab('bbdef', this)">
    2. Defensa de BB <span class="tab-pill">vs Open</span>
  </button>
  <button class="tab-btn" onclick="switchTab('threebet', this)">
    3. 3-Bet y Respuesta <span class="tab-pill">IP / SB / vs 3B</span>
  </button>
  <button class="tab-btn" onclick="switchTab('pushfold', this)">
    4. Push / Fold Nash <span class="tab-pill">&lt; 20 bb</span>
  </button>
  <button class="tab-btn" onclick="switchTab('strategy', this)">
    5. Ajustes, ICM y Teoría <span class="tab-pill">Guía</span>
  </button>
</nav>

<main>
  <!-- ==================== TAB 1: RFI ==================== -->
  <section id="tab-rfi" class="tab-section active">
    <div class="sub-bar">
      <div class="pos-group" id="rfi-pos-buttons">
        <button class="pos-btn active" onclick="selectRFI(0, this)">UTG (LJ)</button>
        <button class="pos-btn" onclick="selectRFI(1, this)">HJ (Hijack)</button>
        <button class="pos-btn" onclick="selectRFI(2, this)">CO (Cutoff)</button>
        <button class="pos-btn" onclick="selectRFI(3, this)">BTN (Botón)</button>
        <button class="pos-btn" onclick="selectRFI(4, this)">SB vs BB</button>
      </div>
      <div class="legend">
        <div class="legend-item"><span class="swatch" style="background:#10b981"></span> Abrir 100% (Raise)</div>
        <div class="legend-item"><span class="swatch" style="background:linear-gradient(90deg,#10b981 50%,#f59e0b 50%)"></span> Mixta (~50%)</div>
        <div class="legend-item"><span class="swatch" style="background:#0ea5e9"></span> Limp / Mix (SB)</div>
        <div class="legend-item"><span class="swatch" style="background:#161f2e;border:1px solid #334155"></span> Fold</div>
      </div>
    </div>

    <div id="rfi-single-view" class="workspace">
      <div class="matrix-card">
        <div class="matrix-header">
          <h2 id="rfi-title">UTG (Lojack) — Raise First In</h2>
          <span class="subtitle" id="rfi-sizing">Tamaño: 2.0 – 2.5 bb</span>
        </div>
        <div id="rfi-grid" class="matrix-grid"></div>
      </div>

      <div class="info-panel">
        <div class="info-card">
          <h3>
            <span>Resumen del Rango</span>
            <span id="rfi-total-badge" style="color:var(--col-raise)">15.2%</span>
          </h3>
          <div class="stats-grid" id="rfi-stats"></div>
          <div class="freq-bar" id="rfi-freq-bar"></div>
        </div>

        <div class="inspector-box" id="rfi-inspector">
          <div class="inspector-badge" id="rfi-insp-hand">AKs</div>
          <div>
            <div style="font-weight:800;color:#fff" id="rfi-insp-action">Pasa el ratón por cualquier mano de la tabla</div>
            <div style="font-size:0.84rem;color:var(--text-muted)" id="rfi-insp-desc">Verás la frecuencia exacta, número de combinaciones y consejo estratégico.</div>
          </div>
        </div>

        <div class="info-card">
          <h3>Claves Estratégicas de la Posición (Sin Ante)</h3>
          <ul class="notes-list" id="rfi-notes"></ul>
        </div>
      </div>
    </div>

    <!-- All 5 RFI Grids side by side (toggleable) -->
    <div id="rfi-all-view" class="overview-grid" style="display:none"></div>
  </section>

  <!-- ==================== TAB 2: BB DEFENSE ==================== -->
  <section id="tab-bbdef" class="tab-section">
    <div class="sub-bar">
      <div class="pos-group" id="bb-pos-buttons">
        <button class="pos-btn active" onclick="selectBB(0, this)">BB vs UTG (2.5bb)</button>
        <button class="pos-btn" onclick="selectBB(1, this)">BB vs HJ (2.5bb)</button>
        <button class="pos-btn" onclick="selectBB(2, this)">BB vs CO (2.5bb)</button>
        <button class="pos-btn" onclick="selectBB(3, this)">BB vs BTN (2.5bb)</button>
        <button class="pos-btn" onclick="selectBB(4, this)">BB vs SB (3.0bb)</button>
      </div>
      <div class="legend">
        <div class="legend-item"><span class="swatch" style="background:#ef4444"></span> 3-Bet Valor</div>
        <div class="legend-item"><span class="swatch" style="background:#a855f7"></span> 3-Bet Bluff / Polar</div>
        <div class="legend-item"><span class="swatch" style="background:#0ea5e9"></span> Call (Defensa)</div>
        <div class="legend-item"><span class="swatch" style="background:#161f2e;border:1px solid #334155"></span> Fold</div>
      </div>
    </div>

    <div class="workspace">
      <div class="matrix-card">
        <div class="matrix-header">
          <h2 id="bb-title">Defensa de BB vs UTG Open (2.5 bb)</h2>
          <span class="subtitle" id="bb-sizing">Tamaño 3-Bet OOP: 10 – 11 bb</span>
        </div>
        <div id="bb-grid" class="matrix-grid"></div>
      </div>

      <div class="info-panel">
        <div class="info-card">
          <h3>
            <span>Desglose de Defensa en BB</span>
            <span id="bb-total-badge" style="color:#38bdf8">26%</span>
          </h3>
          <div class="stats-grid" id="bb-stats"></div>
          <div class="freq-bar" id="bb-freq-bar"></div>
        </div>

        <div class="inspector-box">
          <div class="inspector-badge" id="bb-insp-hand">QQ</div>
          <div>
            <div style="font-weight:800;color:#fff" id="bb-insp-action">Inspecciona cualquier celda</div>
            <div style="font-size:0.84rem;color:var(--text-muted)" id="bb-insp-desc">Sin ante, tus Pot Odds ante un open de 2.5bb son del 27.3% (1.5bb para ganar 5.5bb). Debes defender mucho más estrecho que en torneos con ante.</div>
          </div>
        </div>

        <div class="info-card">
          <h3>Ajustes de Defensa en BB (Sin Ante)</h3>
          <ul class="notes-list" id="bb-notes"></ul>
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== TAB 3: 3-BET & VS 3-BET ==================== -->
  <section id="tab-threebet" class="tab-section">
    <div class="sub-bar">
      <div class="pos-group" id="tb-pos-buttons">
        <button class="pos-btn active" onclick="selectTB(0, this)">BTN vs CO Open</button>
        <button class="pos-btn" onclick="selectTB(1, this)">CO vs UTG/HJ Open</button>
        <button class="pos-btn" onclick="selectTB(2, this)">SB vs BTN Open</button>
        <button class="pos-btn" onclick="selectTB(3, this)">SB vs UTG/HJ Open</button>
        <button class="pos-btn" onclick="selectTB(4, this)">Defensa: UTG/HJ vs 3-Bet</button>
        <button class="pos-btn" onclick="selectTB(5, this)">Defensa: CO/BTN vs 3-Bet</button>
      </div>
      <div class="legend">
        <div class="legend-item"><span class="swatch" style="background:#ef4444"></span> 3-Bet / 4-Bet Valor</div>
        <div class="legend-item"><span class="swatch" style="background:#a855f7"></span> 3-Bet / 4-Bet Bluff</div>
        <div class="legend-item"><span class="swatch" style="background:#0ea5e9"></span> Call</div>
        <div class="legend-item"><span class="swatch" style="background:#161f2e;border:1px solid #334155"></span> Fold</div>
      </div>
    </div>

    <div class="workspace">
      <div class="matrix-card">
        <div class="matrix-header">
          <h2 id="tb-title">BTN vs CO Open (2.5 bb)</h2>
          <span class="subtitle" id="tb-sizing">Tamaño 3-Bet IP: 7.5 bb</span>
        </div>
        <div id="tb-grid" class="matrix-grid"></div>
      </div>

      <div class="info-panel">
        <div class="info-card">
          <h3>
            <span>Distribución de Acciones</span>
            <span id="tb-total-badge" style="color:#ef4444">22%</span>
          </h3>
          <div class="stats-grid" id="tb-stats"></div>
          <div class="freq-bar" id="tb-freq-bar"></div>
        </div>

        <div class="inspector-box">
          <div class="inspector-badge" id="tb-insp-hand">A5s</div>
          <div>
            <div style="font-weight:800;color:#fff" id="tb-insp-action">Inspecciona una mano</div>
            <div style="font-size:0.84rem;color:var(--text-muted)" id="tb-insp-desc">En torneos sin ante el Cold Call en posiciones medias y SB se reduce drásticamente porque hay menos dinero muerto y alto riesgo de Squeeze.</div>
          </div>
        </div>

        <div class="info-card">
          <h3>Claves del Escenario</h3>
          <ul class="notes-list" id="tb-notes"></ul>
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== TAB 4: PUSH / FOLD NASH ==================== -->
  <section id="tab-pushfold" class="tab-section">
    <div class="sub-bar">
      <div class="pos-group" id="pf-pos-buttons">
        <button class="pos-btn active" onclick="selectPF(0, this)">UTG Push</button>
        <button class="pos-btn" onclick="selectPF(1, this)">HJ Push</button>
        <button class="pos-btn" onclick="selectPF(2, this)">CO Push</button>
        <button class="pos-btn" onclick="selectPF(3, this)">BTN Push</button>
        <button class="pos-btn" onclick="selectPF(4, this)">SB Push vs BB</button>
        <button class="pos-btn" onclick="selectPF(5, this)">BB Call vs SB Push</button>
      </div>

      <div class="slider-wrap">
        <span style="font-size:0.85rem;font-weight:700;color:#cbd5e1">Tu Stack Efectivo:</span>
        <input type="range" id="pf-stack-slider" min="4" max="20" step="1" value="12" oninput="updatePFSlider(this.value)">
        <span class="stack-pill" id="pf-stack-label">12 bb</span>
      </div>
    </div>

    <div class="workspace">
      <div class="matrix-card">
        <div class="matrix-header">
          <h2 id="pf-title">Tabla Nash Push/Fold (Sin Ante) — UTG</h2>
          <span class="subtitle">Número en celda = Máximo de BB para ir All-In</span>
        </div>
        <div id="pf-grid" class="matrix-grid"></div>
      </div>

      <div class="info-panel">
        <div class="info-card">
          <h3>
            <span>Rango con el Stack Seleccionado</span>
            <span id="pf-total-badge" style="color:var(--col-raise)">19.5%</span>
          </h3>
          <div class="stats-grid" id="pf-stats"></div>
          <p style="font-size:0.83rem;color:var(--text-muted);margin-top:8px">
            <strong>Cómo leer la matriz:</strong> Cada casilla indica el <strong>stack máximo (en BB)</strong> con el que esa mano es All-In directo rentable sin ante. Mueve el deslizador de arriba para iluminar exactamente qué manos empujar con tu stack actual.
          </p>
        </div>

        <div class="info-card">
          <h3>Guía de Stack Corto y Re-Shove (12 – 22 bb)</h3>
          <ul class="notes-list" id="pf-notes">
            <li><strong>Sin ante los rangos de Push son más cerrados:</strong> En un torneo con ante hay ~2.5 bb muertas en el centro; sin ante solo hay <strong>1.5 bb</strong> (SB + BB). Por eso necesitas manos más fuertes para ir all-in.</li>
            <li><strong>Zona de 14 a 20 bb (Min-Raise vs Open Push):</strong> Con manos monstruo (<code>AA–TT, AKs</code>) en BTN/CO y >14 bb suele ser más rentable abrir a <code>2 bb</code> para inducir 3-bet shoves, mientras que pares medios-bajos (<code>22–77</code>) y <code>Ax</code> débiles prefieren el <strong>Open Shove directo</strong>.</li>
            <li><strong>Re-Shove (3-Bet All-In con 15–22 bb):</strong> Ante un open de CO o BTN a 2–2.2 bb, tus mejores manos para re-empujar desde SB/BB son <code>55+, A7s+, ATo+, KJs+, KQo</code>.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- ==================== TAB 5: STRATEGY & ICM ==================== -->
  <section id="tab-strategy" class="tab-section">
    <div class="guide-grid">
      <div class="info-card">
        <h3>1. Matemática del Torneo Sin Ante vs Con Ante</h3>
        <table class="clean-table">
          <thead>
            <tr>
              <th>Métrica (Open a 2.5 bb)</th>
              <th>Sin Ante (Tu Formato)</th>
              <th>Con Ante (12.5% BB)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Bote inicial (Dead Money)</strong></td>
              <td>1.5 bb (0.5 SB + 1.0 BB)</td>
              <td>2.25 bb (1.5 + 0.75 antes)</td>
            </tr>
            <tr>
              <td><strong>Fold Equity necesaria (Steal)</strong></td>
              <td><strong>62.5%</strong> (2.5 / 4.0)</td>
              <td><strong>52.6%</strong> (2.5 / 4.75)</td>
            </tr>
            <tr>
              <td><strong>Pot Odds de la BB (Call 1.5bb)</strong></td>
              <td><strong>27.3%</strong> (1.5 / 5.5)</td>
              <td><strong>23.8%</strong> (1.5 / 6.25)</td>
            </tr>
            <tr>
              <td><strong>Impacto Estratégico</strong></td>
              <td>Robar vale menos; BB defiende ~12-15% menos manos</td>
              <td>Robos muy agresivos y defensas de BB muy amplias</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="info-card">
        <h3>2. Hoja de Ruta por Profundidad de Stack</h3>
        <table class="clean-table">
          <thead>
            <tr>
              <th>Stack Efectivo</th>
              <th>Tamaño Open</th>
              <th>Ajuste Principal en 6-Max Sin Ante</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>&gt; 60 bb (Deep)</strong></td>
              <td>2.2 – 2.5 bb (SB: 3bb)</td>
              <td>Usa las tablas RFI estándar. Alto valor en manos suited conectadas y pares bajos por implícitas.</td>
            </tr>
            <tr>
              <td><strong>30 – 50 bb (Medio)</strong></td>
              <td>2.0 – 2.2 bb (SB: 2.5-3bb)</td>
              <td>Recorta los conectores suited más bajos (<code>54s, 64s</code>) en posiciones tempranas; prioriza cartas altas y blockers.</td>
            </tr>
            <tr>
              <td><strong>18 – 28 bb (Incómodo)</strong></td>
              <td>2.0 bb (Min-raise)</td>
              <td>Toda mano que abras debe tener claro si paga o foldea ante un 3-bet all-in. Activa tus 3-bet re-shoves desde ciegas.</td>
            </tr>
            <tr>
              <td><strong>&lt; 15 bb (Short)</strong></td>
              <td>All-In (o 2bb en BTN)</td>
              <td>Pasa a la pestaña <strong>4. Push / Fold Nash</strong>. No regales fichas haciendo raise/fold con más del 15% de tu stack.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="info-card">
        <h3>3. Ajustes por ICM (Burbuja y Mesa Final)</h3>
        <ul class="notes-list">
          <li><strong>Factor Burbuja (Bubble Factor):</strong> En premios o burbuja, perder tus fichas duele más que lo que vale doblarte. Necesitas entre un <strong>5% y un 12% más de equity</strong> para pagar un all-in.</li>
          <li><strong>Si eres Stack Medio (el más presionado):</strong> Estrecha tus aperturas en UTG/HJ y evita pagar 3-bets fuera de posición contra los líderes en fichas.</li>
          <li><strong>Si eres Chip Leader:</strong> En BTN y CO puedes abrir aún más ancho si los stacks medios detrás de ti están jugando a sobrevivir el salto de premios.</li>
          <li><strong>Bloqueadores (Blockers) ganan valor en ICM:</strong> Manos como <code>A5s–A2s</code> y <code>KQo/ATo</code> suben de valor para abrir o 3-betear porque bloquean los rangos de continuación (<code>AA, AK, KK, QQ</code>) de tus rivales.</li>
        </ul>
      </div>

      <div class="info-card">
        <h3>4. Explotación Rápida según el Perfil de tu Mesa</h3>
        <ul class="notes-list">
          <li><strong>Mesa pasiva (pocos 3-bets):</strong> Convierte todas las manos mixtas (amarillas) en apertura al 100% y paga más en posición para jugar botes post-flop baratos.</li>
          <li><strong>Ciegas que foldean de más (&gt; 65% fold a steal):</strong> En torneos sin ante muchos jugadores sobre-foldean la BB sin darse cuenta; abre un 5–8% extra desde BTN y SB con tamaño mínimo (2 bb).</li>
          <li><strong>Rivales agresivos con 3-bet en ciegas:</strong> Elimina de tu rango de apertura las manos offsuit débiles (<code>KTo, QTo, A9o</code>) y quédate con manos que soportan bien un 3-bet (suited conectadas altas, pares y <code>Ax</code> suited).</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- ==================== PRINTABLE ALL-IN-ONE CONTAINER ==================== -->
  <div id="print-all-container"></div>
</main>

<script>
const RANKS = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"];

// Helper to expand range notation into Set of hand strings
function parseRange(tokens) {
  const set = new Set();
  if (!tokens) return set;
  for (let raw of tokens) {
    let t = raw.trim();
    if (!t) continue;
    const plus = t.endsWith("+");
    if (plus) t = t.slice(0, -1);
    if (t.includes("-")) {
      const [a, b] = t.split("-");
      if (a.length === 2 && a[0] === a[1]) {
        const i1 = RANKS.indexOf(a[0]);
        const i2 = RANKS.indexOf(b[0]);
        for (let i = Math.min(i1, i2); i <= Math.max(i1, i2); i++) {
          set.add(RANKS[i] + RANKS[i]);
        }
      } else {
        const kind = a[2];
        const hi = a[0];
        const i1 = RANKS.indexOf(a[1]);
        const i2 = RANKS.indexOf(b[1]);
        for (let i = Math.min(i1, i2); i <= Math.max(i1, i2); i++) {
          set.add(hi + RANKS[i] + kind);
        }
      }
      continue;
    }
    if (t.length === 2 && t[0] === t[1]) {
      if (plus) {
        const idx = RANKS.indexOf(t[0]);
        for (let i = 0; i <= idx; i++) set.add(RANKS[i] + RANKS[i]);
      } else {
        set.add(t);
      }
    } else {
      const hi = t[0], lo = t[1], kind = t[2];
      if (plus) {
        const hiIdx = RANKS.indexOf(hi);
        const loIdx = RANKS.indexOf(lo);
        for (let i = hiIdx + 1; i <= loIdx; i++) {
          set.add(hi + RANKS[i] + kind);
        }
      } else {
        set.add(t);
      }
    }
  }
  return set;
}

function handNameAt(r, c) {
  if (r === c) return RANKS[r] + RANKS[c];
  if (r < c) return RANKS[r] + RANKS[c] + "s";
  return RANKS[c] + RANKS[r] + "o";
}

function combosForHand(h) {
  if (h.length === 2) return 6;
  return h.endsWith("s") ? 4 : 12;
}

// ==================== DATA: 1. RFI (100bb No Ante) ====================
const RFI_DATA = [
  {
    name: "UTG (Lojack) — Primero en hablar",
    shortName: "UTG (LJ)",
    sizing: "Tamaño: 2.0 – 2.5 bb",
    raise: ["55+","ATs+","A5s-A4s","KTs+","QTs+","JTs","T9s","AJo+","KQo"],
    mix: ["44-22","A9s","A8s","A3s-A2s","K9s","98s","87s","ATo","KJo"],
    limp: [],
    notes: [
      "Quedan 5 jugadores por actuar y sin ante solo hay 1.5 bb en el centro: la disciplina aquí ahorra muchas fichas.",
      "Los Ases bajos suited (A5s–A4s) abren al 100% porque bloquean AA/AK y tienen jugada hacia color y escalera (rueda).",
      "Evita abrir manos offsuit fácilmente dominadas como KTo, QJo o A9o: cuando te pagan o 3-betean en posición pierden mucho EV.",
      "Pares pequeños (22–44) son mixtos: ábrelos al 100% en mesas pasivas y foldéalos si hay jugadores muy agresivos con el 3-bet detrás."
    ]
  },
  {
    name: "HJ (Hijack)",
    shortName: "HJ",
    sizing: "Tamaño: 2.0 – 2.5 bb",
    raise: ["22+","A8s+","A5s-A2s","K9s+","Q9s+","J9s+","T9s","98s","87s","76s","ATo+","KJo+"],
    mix: ["A7s-A6s","K8s","T8s","65s","QJo","KTo"],
    limp: [],
    notes: [
      "Con un jugador menos por hablar ya entran todos los pares (22+) y todos los A5s–A2s además de A8s+.",
      "Se incorporan conectores del mismo palo medios (98s, 87s, 76s) que juegan muy bien con stacks de >50 bb.",
      "ATo y KJo pasan a ser aperturas estándar; KTo y QJo se abren a media frecuencia dependiendo de lo agresivo que sea el Botón."
    ]
  },
  {
    name: "CO (Cutoff)",
    shortName: "CO",
    sizing: "Tamaño: 2.0 – 2.5 bb",
    raise: ["22+","A2s+","K7s+","Q8s+","J8s+","T8s+","97s+","87s","76s","65s","54s","A9o+","KTo+","QTo+","JTo"],
    mix: ["K6s-K5s","96s","86s","75s","A8o","K9o","Q9o","J9o"],
    limp: [],
    notes: [
      "Desde el Cutoff ya abres todos los Ases suited (A2s+) y todas las figuras offsuit de diez o más (KTo+, QTo+, JTo).",
      "El peligro principal es el 3-bet del Botón: si el BTN es muy agresivo, cierra las manos amarillas (mixtas).",
      "Si el Botón es pasivo o foldea mucho, puedes abrir prácticamente como si estuvieras en el propio Botón."
    ]
  },
  {
    name: "BTN (Botón) — Mejor Posición",
    shortName: "BTN",
    sizing: "Tamaño: 2.0 – 2.5 bb",
    raise: ["22+","A2s+","K2s+","Q4s+","J6s+","T6s+","96s+","85s+","75s+","64s+","53s+","43s","A7o+","K8o+","Q9o+","J9o+","T9o","98o"],
    mix: ["Q3s-Q2s","J5s-J4s","T5s","95s","84s","74s","63s","52s","A6o-A2o","K7o","Q8o","J8o","T8o","87o"],
    limp: [],
    notes: [
      "Hablarás el último en todas las calles post-flop (IP). Puedes abrir alrededor del 43–48% de la baraja.",
      "Importante sin ante: en torneos con ante el BTN abre ~55%, pero sin ante el bote es más pequeño y debes foldear las peores offsuit (A2o–A6o son solo mixtas).",
      "Usa un tamaño pequeño (2.0–2.2 bb): arriesgas menos para robar las ciegas y obligas a la BB a defender fuera de posición."
    ]
  },
  {
    name: "SB (Ciega Pequeña) vs BB",
    shortName: "SB vs BB",
    sizing: "Tamaño Raise: 3.0 bb (o Estrategia Mixta con Limp)",
    raise: ["22+","A2s+","K2s+","Q4s+","J6s+","T6s+","96s+","85s+","75s+","64s+","54s","A7o+","K8o+","Q9o+","J9o+","T9o"],
    mix: ["Q3s-Q2s","J5s","T5s","95s","53s","43s","A6o-A2o","K7o","Q8o","J8o","T8o","98o","87o"],
    limp: ["K4s-K2s","Q5s-Q4s","J7s-J6s","T7s-T6s","97s-96s","86s-85s","76s-75s","65s-64s","54s","A5o-A2o","K8o","Q9o","J9o","T9o"],
    notes: [
      "Solo queda la BB por hablar, pero estarás fuera de posición (OOP) todo el post-flop.",
      "Sube más grande (3.0 bb) para quitarle buenas Pot Odds a la BB y maximizar tu Fold Equity.",
      "Las celdas marcadas con sub-etiqueta 'Limp' pueden jugarse subiendo a 3 bb o completando (limp 0.5 bb) para realizar su equity sin inflar el bote OOP."
    ]
  }
];

// ==================== DATA: 2. BB DEFENSE (vs 2.5bb Open, No Ante) ====================
const BB_DATA = [
  {
    name: "Defensa de BB vs UTG Open (2.5 bb)",
    sizing: "Tamaño 3-Bet: 10 – 11 bb",
    val3b: ["JJ+","AKs","AQs","AKo"],
    bluff3b: ["A5s-A4s","KTs","QTs","JTs","T9s"],
    call: ["TT-22","AJs-A6s","A3s-A2s","KQs-KJs","K9s","QJs","Q9s","J9s","98s","87s","76s","65s","54s","AQo-AJo","KQo"],
    notes: [
      "Contra UTG en un torneo sin ante tu defensa total ronda solo el 24–27% (mucho más estrecha que con ante).",
      "Foldea manos offsuit dominadas como ATo, KJo o QJo: cuando ligas top pair contra el rango fuerte de UTG sueles estar dominado.",
      "Tu rango de 3-bet es polarizado: valor muy fuerte (JJ+, AK, AQs) acompañado de suited con blockers y gran jugabilidad (A5s, A4s, broadways suited)."
    ]
  },
  {
    name: "Defensa de BB vs HJ Open (2.5 bb)",
    sizing: "Tamaño 3-Bet: 10 – 11 bb",
    val3b: ["TT+","AQs+","AKo","AQo"],
    bluff3b: ["A5s-A3s","KTs","QTs","JTs","T9s","98s"],
    call: ["99-22","AJs-A6s","A2s","KQs-KJs","K9s-K8s","QJs","Q9s-Q8s","J9s-J8s","T8s","87s","76s","65s","54s","AJo-ATo","KQo-KJo"],
    notes: [
      "Amplías ligeramente tanto el rango de Call (entran ATo, KJo, K8s, Q8s) como el de 3-bet por valor (TT+, AQo).",
      "Todos los pares medios y bajos (22–99) pagan para buscar set o flotar en flops bajos donde el HJ conecta poco."
    ]
  },
  {
    name: "Defensa de BB vs CO Open (2.5 bb)",
    sizing: "Tamaño 3-Bet: 10 – 11 bb",
    val3b: ["99+","AJs+","KQs","AKo-AQo"],
    bluff3b: ["A5s-A2s","K9s","Q9s","J9s","T8s","97s","87s","76s","ATo","KJo"],
    call: ["88-22","ATs-A6s","KJs-KTs","K8s-K5s","QJs-QTs","Q8s-Q7s","JTs","J8s","T9s","98s","86s","75s","65s","54s","43s","AJo","A9o","KQo","QJo","JTo"],
    notes: [
      "El CO abre ~27%, por lo que ya defiendes alrededor del 36% de tus manos en BB.",
      "Tus 3-bets de farol usan dos tipos de manos: Ases suited bajos (A5s–A2s) que bloquean AA/AK, y conectores/gappers suited que juegan bien si el CO paga el 3-bet."
    ]
  },
  {
    name: "Defensa de BB vs BTN Open (2.5 bb)",
    sizing: "Tamaño 3-Bet: 10.5 – 11.5 bb",
    val3b: ["88+","ATs+","KJs+","QJs","AKo-AJo","KQo"],
    bluff3b: ["A5s-A2s","K7s-K5s","Q8s","J8s","T7s","97s","86s","75s","64s","54s","A9o-A8o","KTo","QTo"],
    call: ["77-22","A9s-A6s","KTs-K8s","K4s-K2s","QTs-Q9s","Q7s-Q4s","JTs-J9s","J7s-J6s","T9s-T8s","T6s","98s","96s","87s","85s","76s","65s","53s","43s","ATo","A7o-A4o","KJo","K9o","QJo","JTo","T9o","98o"],
    notes: [
      "El BTN abre muy amplio (~45%), así que la BB defiende cerca del 48–52% incluso sin ante.",
      "Aumenta tu frecuencia de 3-bet (~13–14%): como estás fuera de posición, 3-betear niega la realización de equity gratuita del Botón.",
      "Si el BTN abre a 2.0 bb (min-raise) en lugar de 2.5 bb, tus Pot Odds mejoran al 22.2% y debes añadir un 8–10% más de Calls con manos suited."
    ]
  },
  {
    name: "Defensa de BB vs SB Open (3.0 bb) — ¡Con Posición!",
    sizing: "Tamaño 3-Bet IP: 8.5 – 9.0 bb",
    val3b: ["88+","ATs+","KJs+","QJs","AKo-AJo","KQo"],
    bluff3b: ["A5s-A2s","K6s-K4s","Q7s-Q6s","J7s","T7s","96s","85s","75s","64s","53s","A8o-A7o","K9o","Q9o","J9o"],
    call: ["77-22","A9s-A6s","KTs-K7s","K3s-K2s","QTs-Q8s","Q5s-Q2s","JTs-J8s","J6s-J5s","T9s-T8s","T6s","98s-97s","87s-86s","76s","65s","54s","43s","ATo","A9o","A6o-A2o","KJo-KTo","K8o","QJo-QTo","JTo","T9o","98o","87o"],
    notes: [
      "Contra la SB tienes posición (IP) durante todo el post-flop: es el escenario donde más manos puedes defender rentablemente (~55%).",
      "Tu tamaño de 3-bet es más pequeño (8.5–9 bb frente a su subida a 3 bb) porque hablas después de él post-flop.",
      "Si la SB hace Limp (completa 0.5 bb), sube a 3.5 bb con tus manos fuertes (88+, ATs+, KJs+, AJo+, KQo) acompañadas de faroles como K5s, Q6s o 97s."
    ]
  }
];

// ==================== DATA: 3. 3-BET & VS 3-BET ====================
const TB_DATA = [
  {
    name: "BTN vs CO Open (2.5 bb) — En Posición",
    sizing: "Tamaño 3-Bet IP: 7.5 bb",
    val3b: ["TT+","AJs+","KQs","AKo-AQo"],
    bluff3b: ["A9s-A8s","A5s-A2s","KTs-K9s","QTs","J9s","T8s","87s","76s","AJo","KQo"],
    call: ["99-44","ATs","A7s-A6s","KJs","QJs","JTs","T9s","98s"],
    notes: [
      "Sin ante, el rango de Cold Call incluso en el Botón es selectivo y condensado en pares medios (44–99) y broadways suited.",
      "Manos como AJo o KQo prefieren 3-betear (bloquean AK/AQ/KQ del rival) antes que pagar y exponerse a un Squeeze de las ciegas."
    ]
  },
  {
    name: "CO vs UTG/HJ Open (2.5 bb)",
    sizing: "Tamaño 3-Bet IP: 7.5 bb",
    val3b: ["JJ+","AQs+","AKo"],
    bluff3b: ["A5s-A4s","KQs","KTs","QTs","AQo"],
    call: ["TT-55","AJs-ATs","KJs","QJs","JTs","T9s"],
    notes: [
      "Contra posiciones tempranas tu rango es mucho más estrecho y lineal.",
      "Evita pagar con manos offsuit o pares muy pequeños (22–44) con menos de 60 bb cuando quedan el BTN y ambas ciegas por hablar."
    ]
  },
  {
    name: "SB vs BTN Open (2.5 bb) — Estrategia 3-Bet o Fold",
    sizing: "Tamaño 3-Bet OOP: 10 – 11 bb",
    val3b: ["77+","A9s+","KTs+","QTs+","JTs","ATo+","KQo"],
    bluff3b: ["66-55","A8s-A2s","K9s","Q9s","J9s","T9s","98s","87s","KJo"],
    call: [],
    notes: [
      "En torneos sin ante, la SB prácticamente NO hace Cold Call: juegas una estrategia pura de '3-Bet o Fold' (~15–17%).",
      "¿Por qué no pagar en SB? Si solo pagas estarás fuera de posición post-flop y le das a la BB unas Pot Odds excelentes para pagar o hacer Squeeze.",
      "Tu rango de 3-bet aquí es lineal (fusionado): metes todas tus buenas cartas altas, pares 55+ y conectores suited."
    ]
  },
  {
    name: "SB vs UTG/HJ Open (2.5 bb)",
    sizing: "Tamaño 3-Bet OOP: 10 – 11 bb",
    val3b: ["TT+","AJs+","KQs","AKo-AQo"],
    bluff3b: ["99-88","ATs","A5s-A4s","KJs","QJs","JTs"],
    call: [],
    notes: [
      "De nuevo aplicamos '3-Bet o Fold' desde la SB, pero con un rango mucho más fuerte (~8–9%) porque el abridor viene de UTG o HJ.",
      "A5s y A4s funcionan como tus mejores 3-bet bluffs gracias al blocker del As y su capacidad de ligar color máximo o escalera."
    ]
  },
  {
    name: "Defensa: Abres en UTG/HJ y recibes un 3-Bet",
    sizing: "Tamaño 4-Bet: 2.2x el 3-Bet (~18–21 bb)",
    val3b: ["QQ+","AKs","AKo"],
    bluff3b: ["A5s-A4s","AQs"],
    call: ["JJ-77","AJs-ATs","KQs-KJs","QJs","JTs","T9s","AQo"],
    notes: [
      "Rojo = 4-Bet por Valor · Morado = 4-Bet Bluff · Azul = Call al 3-Bet.",
      "Cuando abres desde UTG/HJ y te hacen 3-bet, debes foldear la parte baja de tu rango (pares 22–66, AJo, KQo y conectores bajos).",
      "Si el stack efectivo es de 25–35 bb, tu 4-bet pasa a ser directamente All-In con QQ+, AK y A5s/A4s como faroles con blocker."
    ]
  },
  {
    name: "Defensa: Abres en CO/BTN y recibes 3-Bet de las Ciegas",
    sizing: "Tamaño 4-Bet IP: 2.1x el 3-Bet (~21–23 bb)",
    val3b: ["JJ+","AQs+","AKo-AQo"],
    bluff3b: ["A5s-A3s","K9s","Q9s","ATo","KQo"],
    call: ["TT-44","AJs-A7s","KQs-KTs","QJs-QTs","JTs-J9s","T9s-T8s","98s","87s","76s","65s","AJo"],
    notes: [
      "Rojo = 4-Bet por Valor · Morado = 4-Bet Bluff · Azul = Call al 3-Bet en Posición.",
      "Al tener posición (IP) contra la SB o la BB que 3-betea grande (10–11 bb), puedes pagar con muchos pares (44–TT), Ases suited y conectores suited.",
      "Evita pagar el 3-bet con manos offsuit débiles; usa alguna como ATo o KQo como 4-bet bluff ocasional y foldea el resto."
    ]
  }
];

// ==================== DATA: 4. PUSH / FOLD NASH (No Ante, Max BB per cell) ====================
// Base matrix of Nash No-Ante Push thresholds for SB vs BB (13x13).
// For earlier positions (BTN, CO, HJ, UTG), thresholds scale down realistically for No-Ante 6-Max.
const UNCAPPED_SB_NASH = [
  // A   K   Q   J   T   9   8   7   6   5   4   3   2
  [60, 60, 55, 50, 46, 38, 35, 33, 30, 32, 30, 28, 26], // A (s)
  [60, 60, 48, 42, 36, 28, 22, 19, 17, 16, 14, 13, 12], // K
  [52, 38, 60, 36, 30, 21, 16, 13, 12, 11, 10,  9,  8], // Q
  [44, 28, 22, 60, 28, 19, 15, 11,  9,  8,  7,  6,  6], // J
  [38, 22, 17, 16, 60, 22, 16, 12,  9,  7,  6,  5,  5], // T
  [26, 14, 11, 11, 12, 60, 19, 14, 10,  7,  5,  4,  0], // 9
  [22, 11,  9,  8,  9,  9, 55, 17, 12,  9,  6,  4,  0], // 8
  [19,  9,  7,  6,  7,  7,  7, 50, 15, 11,  7,  4,  0], // 7
  [16,  8,  6,  4,  5,  6,  6,  6, 45, 13,  8,  5,  0], // 6
  [16,  7,  5,  0,  0,  4,  5,  5,  5, 40, 11,  6,  4], // 5
  [14,  6,  4,  0,  0,  0,  0,  4,  4,  4, 34,  7,  4], // 4
  [13,  5,  0,  0,  0,  0,  0,  0,  0,  0,  0, 28,  4], // 3
  [12,  5,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 24]  // 2
];

function computeNashThreshold(posIndex, r, c) {
  const raw = UNCAPPED_SB_NASH[r][c];
  if (raw === 0) return 0;
  // Multipliers for UTG(0), HJ(1), CO(2), BTN(3), SB(4), BB Call vs SB(5)
  const mults = [0.40, 0.52, 0.68, 0.86, 1.00, 0.72];
  const shifts = [-2.2, -1.5, -0.8, -0.2, 0.0, -1.8];
  let val = Math.round(raw * mults[posIndex] + shifts[posIndex]);
  if (r === c && posIndex <= 3) {
    // Pocket pairs hold higher push equity from early/mid positions
    val = Math.max(val, Math.round(raw * (mults[posIndex] + 0.08)));
  }
  if (val < 3) return 0;
  return Math.min(20, val);
}

const PF_POS_INFO = [
  { name: "UTG (Lojack) — Push Directo (Sin Ante)", short: "UTG Push" },
  { name: "HJ (Hijack) — Push Directo (Sin Ante)", short: "HJ Push" },
  { name: "CO (Cutoff) — Push Directo (Sin Ante)", short: "CO Push" },
  { name: "BTN (Botón) — Push Directo (Sin Ante)", short: "BTN Push" },
  { name: "SB vs BB — Push Directo (Sin Ante)", short: "SB Push" },
  { name: "BB Call vs SB All-In (Sin Ante)", short: "BB Call vs SB" }
];

// ==================== RENDERING FUNCTIONS ====================
function switchTab(tabId, btn) {
  document.querySelectorAll(".tab-section").forEach(s => s.classList.remove("active"));
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  document.getElementById("tab-" + tabId).classList.add("active");
  btn.classList.add("active");
}

// 1. Render RFI
let currentRFI = 0;
function selectRFI(idx, btn) {
  currentRFI = idx;
  if (btn) {
    document.querySelectorAll("#rfi-pos-buttons .pos-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
  }
  const d = RFI_DATA[idx];
  document.getElementById("rfi-title").textContent = d.name;
  document.getElementById("rfi-sizing").textContent = d.sizing;

  const sRaise = parseRange(d.raise);
  const sMix = parseRange(d.mix);
  const sLimp = parseRange(d.limp);

  const gridEl = document.getElementById("rfi-grid");
  gridEl.innerHTML = "";

  let raiseCombos = 0, mixCombos = 0, pairC = 0, suitedC = 0, offsuitC = 0;

  for (let r = 0; r < 13; r++) {
    for (let c = 0; c < 13; c++) {
      const h = handNameAt(r, c);
      const combos = combosForHand(h);
      const isRaise = sRaise.has(h);
      const isMix = sMix.has(h);
      const isLimp = sLimp.has(h);

      let cls = "act-fold";
      let subText = "";
      let w = 0;

      if (isRaise) {
        cls = "act-raise";
        subText = isLimp ? "R/L" : "100%";
        w = 1;
        raiseCombos += combos;
      } else if (isMix) {
        cls = "act-mix";
        subText = isLimp ? "Limp" : "50%";
        w = 0.5;
        mixCombos += combos;
      }

      if (w > 0) {
        if (r === c) pairC += combos * w;
        else if (r < c) suitedC += combos * w;
        else offsuitC += combos * w;
      }

      const cell = document.createElement("div");
      cell.className = `hand-cell ${cls} ${r === c ? "pair" : ""}`;
      cell.innerHTML = `<span class="hand-label">${h}</span><span class="hand-sub">${subText}</span>`;
      cell.onmouseenter = () => inspectRFIHand(h, isRaise, isMix, isLimp, combos);
      gridEl.appendChild(cell);
    }
  }

  const effCombos = raiseCombos + mixCombos * 0.5;
  const totalPct = (effCombos / 1326 * 100).toFixed(1);
  const raisePct = (raiseCombos / 1326 * 100).toFixed(1);
  const mixPct = (mixCombos / 1326 * 100).toFixed(1);

  document.getElementById("rfi-total-badge").textContent = `${totalPct}% (${Math.round(effCombos)} combos)`;
  document.getElementById("rfi-stats").innerHTML = `
    <div class="stat-box">
      <div class="stat-label">Abrir Puro</div>
      <div class="stat-val" style="color:var(--col-raise)">${raisePct}%</div>
      <div class="stat-sub">${raiseCombos} combos</div>
    </div>
    <div class="stat-box">
      <div class="stat-label">Mixtas (50%)</div>
      <div class="stat-val" style="color:var(--col-mix)">${mixPct}%</div>
      <div class="stat-sub">${mixCombos} combos</div>
    </div>
    <div class="stat-box">
      <div class="stat-label">Suited / Pares</div>
      <div class="stat-val" style="color:#38bdf8">${Math.round(suitedC)} / ${Math.round(pairC)}</div>
      <div class="stat-sub">Offsuit: ${Math.round(offsuitC)} c.</div>
    </div>
  `;

  document.getElementById("rfi-freq-bar").innerHTML = `
    <div class="freq-seg" style="width:${raisePct}%;background:var(--col-raise)"></div>
    <div class="freq-seg" style="width:${mixPct}%;background:var(--col-mix)"></div>
  `;

  const notesEl = document.getElementById("rfi-notes");
  notesEl.innerHTML = d.notes.map(n => `<li>${n}</li>`).join("");
}

function inspectRFIHand(h, isRaise, isMix, isLimp, combos) {
  const badge = document.getElementById("rfi-insp-hand");
  const act = document.getElementById("rfi-insp-action");
  const desc = document.getElementById("rfi-insp-desc");
  badge.textContent = h;
  if (isRaise) {
    badge.style.background = "var(--col-raise)";
    badge.style.color = "#022c22";
    act.textContent = `${h} (${combos} combos) — ABRIR 100% (Raise First In)`;
    desc.textContent = isLimp
      ? "Apertura estándar en SB; también puedes mezclar algún Limp contra rivales muy agresivos en BB."
      : "Apertura rentable en cualquier mesa estándar con >35 bb.";
  } else if (isMix) {
    badge.style.background = "var(--col-mix)";
    badge.style.color = "#000";
    act.textContent = `${h} (${combos} combos) — MANO MIXTA (~50% Frecuencia)`;
    desc.textContent = "En el borde del rango: ábrela siempre si los jugadores detrás son pasivos o foldean de más; foldéala si hay 3-bettors agresivos.";
  } else {
    badge.style.background = "#1e293b";
    badge.style.color = "#94a3b8";
    act.textContent = `${h} (${combos} combos) — FOLD`;
    desc.textContent = "En torneos sin ante no hay suficiente dinero muerto en el bote para compensar las veces que te pagan o 3-betean con mejores manos.";
  }
}

function toggleCompareAllRFI() {
  const single = document.getElementById("rfi-single-view");
  const all = document.getElementById("rfi-all-view");
  if (all.style.display === "none") {
    all.innerHTML = "";
    RFI_DATA.forEach(d => {
      const sRaise = parseRange(d.raise);
      const sMix = parseRange(d.mix);
      let eff = 0;
      let cellsHtml = "";
      for (let r = 0; r < 13; r++) {
        for (let c = 0; c < 13; c++) {
          const h = handNameAt(r, c);
          const cb = combosForHand(h);
          let cls = "act-fold";
          if (sRaise.has(h)) { cls = "act-raise"; eff += cb; }
          else if (sMix.has(h)) { cls = "act-mix"; eff += cb * 0.5; }
          cellsHtml += `<div class="hand-cell ${cls}"><span class="hand-label">${h}</span></div>`;
        }
      }
      const pct = (eff / 1326 * 100).toFixed(1);
      all.innerHTML += `
        <div class="matrix-card">
          <div class="matrix-header">
            <h2>${d.shortName} · <span style="color:var(--col-raise)">${pct}%</span></h2>
            <span class="subtitle">${d.sizing}</span>
          </div>
          <div class="matrix-grid">${cellsHtml}</div>
        </div>
      `;
    });
    single.style.display = "none";
    all.style.display = "grid";
  } else {
    all.style.display = "none";
    single.style.display = "grid";
  }
}

// 2. Render BB Defense & 3. 3-Bet
function renderMultiActionGrid(dataList, idx, prefix) {
  const d = dataList[idx];
  document.getElementById(`${prefix}-title`).textContent = d.name;
  document.getElementById(`${prefix}-sizing`).textContent = d.sizing;

  const sVal = parseRange(d.val3b);
  const sBluff = parseRange(d.bluff3b);
  const sCall = parseRange(d.call);

  const gridEl = document.getElementById(`${prefix}-grid`);
  gridEl.innerHTML = "";

  let cVal = 0, cBluff = 0, cCall = 0;

  for (let r = 0; r < 13; r++) {
    for (let c = 0; c < 13; c++) {
      const h = handNameAt(r, c);
      const cb = combosForHand(h);
      let cls = "act-fold", sub = "", actionLabel = "Fold";

      if (sVal.has(h)) {
        cls = "act-3bet-val"; sub = "3B-V"; cVal += cb;
        actionLabel = "3-Bet / 4-Bet por Valor";
      } else if (sBluff.has(h)) {
        cls = "act-3bet-bluff"; sub = "3B-B"; cBluff += cb;
        actionLabel = "3-Bet / 4-Bet Bluff / Polarizado";
      } else if (sCall.has(h)) {
        cls = "act-call"; sub = "Call"; cCall += cb;
        actionLabel = "Call (Defensa Pasiva)";
      }

      const cell = document.createElement("div");
      cell.className = `hand-cell ${cls} ${r === c ? "pair" : ""}`;
      cell.innerHTML = `<span class="hand-label">${h}</span><span class="hand-sub">${sub}</span>`;
      cell.onmouseenter = () => {
        document.getElementById(`${prefix}-insp-hand`).textContent = h;
        document.getElementById(`${prefix}-insp-action`).textContent = `${h} (${cb} combos) — ${actionLabel}`;
      };
      gridEl.appendChild(cell);
    }
  }

  const totC = cVal + cBluff + cCall;
  const totPct = (totC / 1326 * 100).toFixed(1);
  const valPct = (cVal / 1326 * 100).toFixed(1);
  const bluffPct = (cBluff / 1326 * 100).toFixed(1);
  const callPct = (cCall / 1326 * 100).toFixed(1);

  document.getElementById(`${prefix}-total-badge`).textContent = `${totPct}% (${totC} combos)`;
  document.getElementById(`${prefix}-stats`).innerHTML = `
    <div class="stat-box">
      <div class="stat-label">Resubida Valor</div>
      <div class="stat-val" style="color:var(--col-3bet-val)">${valPct}%</div>
      <div class="stat-sub">${cVal} combos</div>
    </div>
    <div class="stat-box">
      <div class="stat-label">Resubida Bluff</div>
      <div class="stat-val" style="color:var(--col-3bet-bluff)">${bluffPct}%</div>
      <div class="stat-sub">${cBluff} combos</div>
    </div>
    <div class="stat-box">
      <div class="stat-label">Call</div>
      <div class="stat-val" style="color:var(--col-call)">${callPct}%</div>
      <div class="stat-sub">${cCall} combos</div>
    </div>
  `;

  document.getElementById(`${prefix}-freq-bar`).innerHTML = `
    <div class="freq-seg" style="width:${valPct}%;background:var(--col-3bet-val)"></div>
    <div class="freq-seg" style="width:${bluffPct}%;background:var(--col-3bet-bluff)"></div>
    <div class="freq-seg" style="width:${callPct}%;background:var(--col-call)"></div>
  `;

  document.getElementById(`${prefix}-notes`).innerHTML = d.notes.map(n => `<li>${n}</li>`).join("");
}

function selectBB(idx, btn) {
  if (btn) {
    document.querySelectorAll("#bb-pos-buttons .pos-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
  }
  renderMultiActionGrid(BB_DATA, idx, "bb");
}

function selectTB(idx, btn) {
  if (btn) {
    document.querySelectorAll("#tb-pos-buttons .pos-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
  }
  renderMultiActionGrid(TB_DATA, idx, "tb");
}

// 4. Render Push / Fold Nash
let currentPFPos = 0;
let currentPFStack = 12;

function selectPF(idx, btn) {
  currentPFPos = idx;
  if (btn) {
    document.querySelectorAll("#pf-pos-buttons .pos-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
  }
  renderPFGrid();
}

function updatePFSlider(val) {
  currentPFStack = parseInt(val, 10);
  document.getElementById("pf-stack-label").textContent = currentPFStack + " bb";
  renderPFGrid();
}

function renderPFGrid() {
  const info = PF_POS_INFO[currentPFPos];
  document.getElementById("pf-title").textContent = `${info.name} (Con ${currentPFStack} bb)`;
  const gridEl = document.getElementById("pf-grid");
  gridEl.innerHTML = "";

  let pushCombos = 0;
  for (let r = 0; r < 13; r++) {
    for (let c = 0; c < 13; c++) {
      const h = handNameAt(r, c);
      const cb = combosForHand(h);
      const maxBB = computeNashThreshold(currentPFPos, r, c);
      const isPush = maxBB >= currentPFStack;

      let cls = "act-fold";
      if (isPush) {
        pushCombos += cb;
        cls = (maxBB >= currentPFStack + 4) ? "act-raise" : "act-3bet-val";
      }

      const labelBB = maxBB === 20 ? "20+" : (maxBB > 0 ? maxBB + "bb" : "—");
      const cell = document.createElement("div");
      cell.className = `hand-cell ${cls} ${r === c ? "pair" : ""}`;
      cell.innerHTML = `<span class="hand-label">${h}</span><span class="hand-sub">${labelBB}</span>`;
      gridEl.appendChild(cell);
    }
  }

  const pct = (pushCombos / 1326 * 100).toFixed(1);
  document.getElementById("pf-total-badge").textContent = `${pct}% (${pushCombos} combos)`;
  document.getElementById("pf-stats").innerHTML = `
    <div class="stat-box">
      <div class="stat-label">Stack Seleccionado</div>
      <div class="stat-val" style="color:#f59e0b">${currentPFStack} bb</div>
      <div class="stat-sub">Torneo Sin Ante</div>
    </div>
    <div class="stat-box">
      <div class="stat-label">${currentPFPos === 5 ? "Manos de Call" : "Manos de All-In"}</div>
      <div class="stat-val" style="color:var(--col-raise)">${pct}%</div>
      <div class="stat-sub">${pushCombos} de 1,326 combos</div>
    </div>
  `;
}

// 5. Full Printable Report Generator (for Cmd+P / Save as PDF)
function buildSmallStaticGrid(sGreen, sYellow, sRed, sPurple, sBlue) {
  let html = '<div class="matrix-grid">';
  for (let r = 0; r < 13; r++) {
    for (let c = 0; c < 13; c++) {
      const h = handNameAt(r, c);
      let cls = "act-fold";
      if (sGreen && sGreen.has(h)) cls = "act-raise";
      else if (sYellow && sYellow.has(h)) cls = "act-mix";
      else if (sRed && sRed.has(h)) cls = "act-3bet-val";
      else if (sPurple && sPurple.has(h)) cls = "act-3bet-bluff";
      else if (sBlue && sBlue.has(h)) cls = "act-call";
      html += `<div class="hand-cell ${cls}"><span class="hand-label" style="font-size:0.58rem">${h}</span></div>`;
    }
  }
  html += '</div>';
  return html;
}

function printFullStudy() {
  const container = document.getElementById("print-all-container");
  let html = `<div class="print-page">
    <h1 style="margin-bottom:8px">Guía Pre-Flop: Six-Max Torneo (Sin Ante) — 1. Rangos de Apertura (RFI ~100bb)</h1>
    <p style="margin-bottom:12px;font-size:0.85rem">Verde = Abrir 100% · Amarillo = Mixta (~50%) · Gris = Fold</p>
    <div class="print-grid-2">`;
  RFI_DATA.forEach(d => {
    html += `<div class="matrix-card">
      <div class="matrix-header"><h2>${d.name}</h2><span class="subtitle">${d.sizing}</span></div>
      ${buildSmallStaticGrid(parseRange(d.raise), parseRange(d.mix), null, null, null)}
    </div>`;
  });
  html += `</div></div>`;

  html += `<div class="print-page">
    <h1 style="margin-bottom:8px">2. Defensa de Big Blind (Sin Ante, vs 2.5bb / 3bb)</h1>
    <p style="margin-bottom:12px;font-size:0.85rem">Rojo = 3-Bet Valor · Morado = 3-Bet Bluff · Azul = Call · Gris = Fold</p>
    <div class="print-grid-2">`;
  BB_DATA.forEach(d => {
    html += `<div class="matrix-card">
      <div class="matrix-header"><h2>${d.name}</h2><span class="subtitle">${d.sizing}</span></div>
      ${buildSmallStaticGrid(null, null, parseRange(d.val3b), parseRange(d.bluff3b), parseRange(d.call))}
    </div>`;
  });
  html += `</div></div>`;

  html += `<div class="print-page">
    <h1 style="margin-bottom:8px">3. Rangos de 3-Bet y Defensa vs 3-Bet (Sin Ante)</h1>
    <p style="margin-bottom:12px;font-size:0.85rem">Rojo = 3-Bet/4-Bet Valor · Morado = 3-Bet/4-Bet Bluff · Azul = Call · Gris = Fold</p>
    <div class="print-grid-2">`;
  TB_DATA.forEach(d => {
    html += `<div class="matrix-card">
      <div class="matrix-header"><h2>${d.name}</h2><span class="subtitle">${d.sizing}</span></div>
      ${buildSmallStaticGrid(null, null, parseRange(d.val3b), parseRange(d.bluff3b), parseRange(d.call))}
    </div>`;
  });
  html += `</div></div>`;

  container.innerHTML = html;
  window.print();
}

// Initialize all views on load
window.addEventListener("DOMContentLoaded", () => {
  selectRFI(0);
  selectBB(0);
  selectTB(0);
  renderPFGrid();
});
</script>
</body>
</html>
"""


def build():
    root_dir = Path(__file__).resolve().parent.parent
    out_file = root_dir / "index.html"
    out_file.write_text(HTML_TEMPLATE, encoding="utf-8")
    print(f"HTML generado en: {out_file.relative_to(root_dir)} ({out_file.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
