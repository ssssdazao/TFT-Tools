import json
import random
import streamlit as st
from pathlib import Path


st.set_page_config(page_title="战斗模拟", page_icon="⚔️", layout="wide", initial_sidebar_state="expanded")


def get_base64_of_bin_file(bin_file):
    import base64
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_bg_and_style():
    import os

    bg_style = ""
    try:
        bg_path = Path(__file__).resolve().parents[1] / "bg.jpg"
        if bg_path.exists():
            bg_base64 = get_base64_of_bin_file(str(bg_path))
            bg_style = f"""
            background-image: url("data:image/jpeg;base64,{bg_base64}");
            """
        else:
            bg_style = """
            background-image: url("https://images.wallpapersden.com/image/download/anime-school-classroom-sunset_bGdnaGuUmZqaraWkpJRmbmdlrWZlbWU.jpg");
            """
    except Exception:
        bg_style = """
        background-color: #2e3047;
        """

    st.markdown(
        f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Zcool+KuaiLe&family=Nunito:wght@400;700&display=swap');
        
        /* 增强全局字体清晰度 - 强制浅色 */
        body, p, li, span, div {{
            color: #ffffff;
        }}
        
        /* 针对 Streamlit Markdown 文本的增强 */
        .stMarkdown p, .stMarkdown li {{
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.8);
            font-weight: 500;
        }}
        
        /* 输入框 Label 增强 */
        .stSelectbox label, .stNumberInput label, .stTextInput label, .stSlider label {{
            color: #ffffff !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.9);
            font-weight: 600 !important;
            font-size: 1rem !important;
        }}

        /* 侧边栏文字增强 */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {{
            color: #ffffff !important;
        }}

        .stApp {{
            {bg_style}
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            font-family: 'Nunito', sans-serif;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        section[data-testid="stSidebar"] {{
            visibility: visible !important;
            display: block !important;
            background: rgba(18, 18, 30, 0.52) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.10) !important;
        }}
        section[data-testid="stSidebar"] > div {{
            background: transparent !important;
        }}
        div[data-testid="stSidebarNav"] {{
            display: none !important;
        }}
        div[data-testid="stSidebarNav"] a {{
            border-radius: 12px !important;
        }}
        div[data-testid="stSidebarNav"] a:hover {{
            background: rgba(255, 255, 255, 0.08) !important;
        }}
        div[data-testid="stSidebarNav"] span {{
            font-weight: 700 !important;
        }}

        .main-glass {{
            position: fixed;
            top: 10vh;
            left: 2vw;
            width: 96vw;
            height: 80vh;
            background: rgba(20, 20, 35, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            z-index: 0;
            pointer-events: none;
            animation: fadeIn 0.8s ease-in-out;
        }}

        [data-testid="block-container"] {{
            z-index: 1;
            position: relative;
            padding-top: 40px !important;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .main-title {{
            font-family: 'Zcool KuaiLe', sans-serif;
            font-size: 2.6rem;
            background: linear-gradient(120deg, #7dd3fc 0%, #fda4af 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 4px 15px rgba(100, 180, 255, 0.25);
            text-align: left;
            margin-bottom: 0.2rem;
        }}

        .subtitle {{
            font-family: 'Nunito', sans-serif;
            font-size: 1.0rem;
            color: rgba(255, 255, 255, 0.85);
            letter-spacing: 1px;
            margin-bottom: 18px;
        }}

        .panel {{
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 16px 18px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }}

        /* 按钮背景透明化 */
        .stButton > button {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            background-image: none !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: #ffffff !important;
            backdrop-filter: blur(5px);
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            background-color: rgba(255, 255, 255, 0.25) !important;
            border-color: rgba(255, 255, 255, 0.4) !important;
            transform: translateY(-2px);
        }}
        .stButton > button:active {{
            background-color: rgba(255, 255, 255, 0.3) !important;
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )


set_bg_and_style()
st.markdown('<div class="main-glass"></div>', unsafe_allow_html=True)

st.markdown(
    """
<div style="display:flex; justify-content: space-between; align-items:flex-end; gap: 16px; margin-bottom: 8px;">
  <div>
    <div class="main-title">战斗模拟器</div>
    <div class="subtitle">可视化模拟 Tank / Carry 资源集中与集火效果</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


def role_block(prefix: str, label: str, defaults: dict):
    with st.sidebar.expander(label, expanded=False):
        count = st.number_input(f"{label} 数量", min_value=0, max_value=50, value=int(defaults["count"]), step=1, key=f"{prefix}_count")
        hp = st.number_input(f"{label} 生命值", min_value=1.0, max_value=20000.0, value=float(defaults["hp"]), step=50.0, key=f"{prefix}_hp")
        ad = st.number_input(f"{label} 攻击力", min_value=0.0, max_value=5000.0, value=float(defaults["ad"]), step=5.0, key=f"{prefix}_ad")
        atk_spd = st.number_input(f"{label} 攻速(次/秒)", min_value=0.1, max_value=10.0, value=float(defaults["as"]), step=0.05, key=f"{prefix}_as")
        armor = st.number_input(f"{label} 护甲", min_value=0.0, max_value=500.0, value=float(defaults["armor"]), step=5.0, key=f"{prefix}_armor")
        atk_range = st.number_input(f"{label} 射程(像素)", min_value=10.0, max_value=600.0, value=float(defaults["range"]), step=10.0, key=f"{prefix}_range")
        speed = st.number_input(f"{label} 移速(像素/秒)", min_value=10.0, max_value=600.0, value=float(defaults["speed"]), step=10.0, key=f"{prefix}_speed")
        taunt = st.slider(f"{label} 嘲讽/仇恨加成", min_value=-200.0, max_value=600.0, value=float(defaults["taunt"]), step=5.0, key=f"{prefix}_taunt")
        burst_cd = st.number_input(f"{label} 爆发间隔(秒)", min_value=0.0, max_value=20.0, value=float(defaults["burst_cd"]), step=0.5, key=f"{prefix}_burst_cd")
        burst_dmg = st.number_input(f"{label} 爆发伤害", min_value=0.0, max_value=5000.0, value=float(defaults["burst_dmg"]), step=10.0, key=f"{prefix}_burst_dmg")
    return {
        "count": int(count),
        "hp": float(hp),
        "ad": float(ad),
        "as": float(atk_spd),
        "armor": float(armor),
        "range": float(atk_range),
        "speed": float(speed),
        "taunt": float(taunt),
        "burst_cd": float(burst_cd),
        "burst_dmg": float(burst_dmg),
    }

def _app_dir_name():
    p = Path(__file__).resolve()
    if p.parent.name.lower() == "pages":
        return p.parents[1].name
    return p.parent.name


def _nav_link(path: str, label: str, icon: str):
    app_dir = _app_dir_name()
    candidates = [path, f"{app_dir}/{path}"]
    for c in candidates:
        try:
            st.page_link(c, label=label, icon=icon)
            return
        except Exception:
            pass
    if st.button(f"{icon} {label}", use_container_width=True):
        for c in candidates:
            try:
                st.switch_page(c)
                return
            except Exception:
                pass


with st.sidebar:
    st.markdown("### 导航")
    _nav_link("main.py", label="装备助手", icon="🛠️")
    _nav_link("pages/1_Battle_Simulator.py", label="战斗模拟", icon="⚔️")

st.sidebar.markdown("### 参数面板")
seed = st.sidebar.number_input("随机种子", min_value=0, max_value=2_147_483_647, value=12345, step=1)
arena_w = st.sidebar.number_input("战场宽度(像素)", min_value=640, max_value=1600, value=1100, step=10)
arena_h = st.sidebar.number_input("战场高度(像素)", min_value=360, max_value=1200, value=640, step=10)
focus = st.sidebar.slider("集火偏好(0=最近, 1=最高价值)", min_value=0.0, max_value=1.0, value=0.55, step=0.01)
distance_weight = st.sidebar.slider("距离权重", min_value=0.1, max_value=6.0, value=2.2, step=0.1)
value_dps_w = st.sidebar.slider("价值权重: DPS", min_value=0.0, max_value=6.0, value=2.0, step=0.1)
value_hp_w = st.sidebar.slider("价值权重: HP", min_value=0.0, max_value=2.0, value=0.25, step=0.05)
st.sidebar.divider()

blue_tank = role_block(
    "blue_tank",
    "蓝方 Tank",
    {"count": 3, "hp": 2200, "ad": 55, "as": 0.85, "armor": 70, "range": 52, "speed": 155, "taunt": 220, "burst_cd": 7.0, "burst_dmg": 90},
)
blue_carry = role_block(
    "blue_carry",
    "蓝方 Carry",
    {"count": 2, "hp": 1150, "ad": 95, "as": 1.25, "armor": 25, "range": 230, "speed": 165, "taunt": -30, "burst_cd": 4.0, "burst_dmg": 140},
)
blue_support = role_block(
    "blue_support",
    "蓝方 Support",
    {"count": 1, "hp": 1350, "ad": 45, "as": 1.0, "armor": 35, "range": 180, "speed": 165, "taunt": 40, "burst_cd": 6.0, "burst_dmg": 80},
)

st.sidebar.divider()

red_tank = role_block(
    "red_tank",
    "红方 Tank",
    {"count": 3, "hp": 2200, "ad": 55, "as": 0.85, "armor": 70, "range": 52, "speed": 155, "taunt": 220, "burst_cd": 7.0, "burst_dmg": 90},
)
red_carry = role_block(
    "red_carry",
    "红方 Carry",
    {"count": 2, "hp": 1150, "ad": 95, "as": 1.25, "armor": 25, "range": 230, "speed": 165, "taunt": -30, "burst_cd": 4.0, "burst_dmg": 140},
)
red_support = role_block(
    "red_support",
    "红方 Support",
    {"count": 1, "hp": 1350, "ad": 45, "as": 1.0, "armor": 35, "range": 180, "speed": 165, "taunt": 40, "burst_cd": 6.0, "burst_dmg": 80},
)

cols = st.columns([1, 1, 1])
with cols[0]:
    if st.button("开始模拟", use_container_width=True):
        st.session_state["sim_nonce"] = random.randint(1, 1_000_000_000)
with cols[1]:
    if st.button("随机种子", use_container_width=True):
        st.session_state["sim_nonce"] = random.randint(1, 1_000_000_000)
        st.session_state["sim_seed"] = random.randint(0, 2_147_483_647)
with cols[2]:
    st.markdown('<div class="panel">建议：先调整两方 Tank/Carry 数量，再改 Carry DPS 与集火偏好</div>', unsafe_allow_html=True)

if "sim_seed" in st.session_state:
    seed = int(st.session_state["sim_seed"])

nonce = int(st.session_state.get("sim_nonce", 1))

config = {
    "arena": {"w": int(arena_w), "h": int(arena_h)},
    "seed": int(seed),
    "model": {
        "focus": float(focus),
        "distance_weight": float(distance_weight),
        "value_dps_w": float(value_dps_w),
        "value_hp_w": float(value_hp_w),
    },
    "teams": {
        "blue": {"tank": blue_tank, "carry": blue_carry, "support": blue_support},
        "red": {"tank": red_tank, "carry": red_carry, "support": red_support},
    },
}

config_json = json.dumps(config, ensure_ascii=False)

html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    html, body {{ margin:0; padding:0; background: transparent; }}
    .wrap {{
      display: grid;
      grid-template-columns: 1fr 330px;
      gap: 14px;
      align-items: start;
    }}
    .card {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 14px;
    }}
    #arena {{
      width: 100%;
      height: auto;
      border-radius: 14px;
      background: rgba(10, 12, 22, 0.55);
      border: 1px solid rgba(255, 255, 255, 0.12);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    }}
    .hud {{
      color: rgba(255,255,255,0.92);
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
      line-height: 1.35;
    }}
    .row {{ display:flex; gap:10px; align-items:center; justify-content: space-between; margin: 10px 0; }}
    .pill {{
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.15);
      background: rgba(255,255,255,0.06);
      display: inline-flex;
      gap: 8px;
      align-items: center;
      justify-content: center;
      user-select: none;
    }}
    .btn {{
      cursor: pointer;
      border-radius: 12px;
      padding: 9px 12px;
      border: 1px solid rgba(255,255,255,0.16);
      background: rgba(255,255,255,0.08);
      color: rgba(255,255,255,0.92);
      font-weight: 650;
      user-select: none;
    }}
    .btn:hover {{ background: rgba(255,255,255,0.12); }}
    input[type="range"] {{ width: 100%; }}
    .small {{ font-size: 12px; color: rgba(255,255,255,0.78); }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <canvas id="arena" width="{config['arena']['w']}" height="{config['arena']['h']}"></canvas>
    </div>
    <div class="card hud">
      <div style="font-size: 16px; font-weight: 800; margin-bottom: 8px;">战斗回放</div>
      <div class="row">
        <button class="btn" id="btnToggle">暂停</button>
        <button class="btn" id="btnReset">重置</button>
      </div>
      <div class="row">
        <div class="pill"><span>时间</span><span class="mono" id="t">0.00</span></div>
        <div class="pill"><span>速度</span><span class="mono" id="spdLbl">1.0×</span></div>
      </div>
      <div style="margin: 8px 0;">
        <input id="spd" type="range" min="0.25" max="2.5" value="1.0" step="0.05"/>
      </div>
      <div class="row">
        <div class="pill">蓝方存活 <span class="mono" id="bAlive">0</span></div>
        <div class="pill">红方存活 <span class="mono" id="rAlive">0</span></div>
      </div>
      <div class="row">
        <div class="pill">蓝方总血 <span class="mono" id="bHp">0</span></div>
        <div class="pill">红方总血 <span class="mono" id="rHp">0</span></div>
      </div>
      <div style="margin-top: 12px; font-size: 15px; font-weight: 800;" id="winner"></div>
      <div style="margin-top: 8px;" class="small">
        模型：基础攻击 + 护甲减伤 + 距离/价值混合选目标 + 角色仇恨。Carry/Support 带周期性爆发。
      </div>
    </div>
  </div>

  <script>
    const CFG = {config_json};
    const NONCE = {nonce};

    function mulberry32(a) {{
      return function() {{
        let t = a += 0x6D2B79F5;
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      }}
    }}

    function clamp(v, a, b) {{ return Math.max(a, Math.min(b, v)); }}
    function len(x, y) {{ return Math.hypot(x, y); }}

    const canvas = document.getElementById("arena");
    const ctx = canvas.getContext("2d");

    const ui = {{
      t: document.getElementById("t"),
      bAlive: document.getElementById("bAlive"),
      rAlive: document.getElementById("rAlive"),
      bHp: document.getElementById("bHp"),
      rHp: document.getElementById("rHp"),
      winner: document.getElementById("winner"),
      spd: document.getElementById("spd"),
      spdLbl: document.getElementById("spdLbl"),
      btnToggle: document.getElementById("btnToggle"),
      btnReset: document.getElementById("btnReset"),
    }};

    const COLORS = {{
      blue: {{
        tank: "#2563eb",
        carry: "#22d3ee",
        support: "#a78bfa",
        hit: "rgba(125, 211, 252, 0.65)"
      }},
      red: {{
        tank: "#ef4444",
        carry: "#fb923c",
        support: "#f472b6",
        hit: "rgba(253, 164, 175, 0.65)"
      }},
    }};

    const ROLE_R = {{ tank: 11, carry: 9, support: 10 }};
    const HIT_PARTICLES_MAX = 240;

    function armorMul(armor) {{
      return 100.0 / (100.0 + Math.max(0.0, armor));
    }}

    function makeUnit(id, team, role, stats, x, y, rnd) {{
      const jitter = (rnd() - 0.5) * 8.0;
      const r = ROLE_R[role] || 10;
      const as = Math.max(0.1, stats.as);
      return {{
        id,
        team,
        role,
        x: x + jitter,
        y: y - jitter,
        vx: 0,
        vy: 0,
        r,
        hp: stats.hp,
        maxHp: stats.hp,
        ad: stats.ad,
        as,
        armor: stats.armor,
        range: stats.range,
        speed: stats.speed,
        taunt: stats.taunt,
        atkCd: 1.0 / as,
        atkLeft: rnd() * (1.0 / as),
        burstCd: stats.burst_cd,
        burstDmg: stats.burst_dmg,
        burstLeft: stats.burst_cd > 0 ? rnd() * stats.burst_cd : 0,
        target: null,
        dmgDone: 0,
        alive: true
      }};
    }}

    function buildTeam(teamName, teamCfg, leftSide, rnd) {{
      const units = [];
      const w = CFG.arena.w;
      const h = CFG.arena.h;
      const padX = 72;
      const padY = 70;
      const baseX = leftSide ? padX : (w - padX);
      const lanes = 4;

      function spawnRole(role, stats) {{
        const n = Math.max(0, stats.count || 0);
        for (let i = 0; i < n; i++) {{
          const lane = i % lanes;
          const y = padY + (lane + 0.5) * ((h - 2 * padY) / lanes) + (rnd() - 0.5) * 30;
          const x = baseX + (leftSide ? 1 : -1) * (30 + (i / lanes) * 18) + (rnd() - 0.5) * 20;
          units.push(makeUnit(`${{teamName}}_${{role}}_${{i}}`, teamName, role, stats, x, y, rnd));
        }}
      }}

      spawnRole("tank", teamCfg.tank);
      spawnRole("carry", teamCfg.carry);
      spawnRole("support", teamCfg.support);
      return units;
    }}

    function recomputeTarget(attacker, enemies, rnd) {{
      const focus = CFG.model.focus;
      const dw = CFG.model.distance_weight;
      const dpsW = CFG.model.value_dps_w;
      const hpW = CFG.model.value_hp_w;

      let best = null;
      let bestScore = -1e18;
      for (const e of enemies) {{
        if (!e.alive) continue;
        const dx = e.x - attacker.x;
        const dy = e.y - attacker.y;
        const d = Math.max(1.0, len(dx, dy));
        const nearestScore = 1.0 / Math.pow(d, dw);
        const dps = e.ad * e.as;
        const valueScore = (dpsW * dps + hpW * e.maxHp + e.taunt) / Math.pow(d, 0.35);
        const score = (1.0 - focus) * nearestScore + focus * valueScore;
        const jitter = (rnd() - 0.5) * 0.002;
        const s = score + jitter;
        if (s > bestScore) {{
          bestScore = s;
          best = e;
        }}
      }}
      attacker.target = best;
    }}

    function stepWorld(world, dt, rnd) {{
      if (world.done) return;

      const all = world.units;
      const blueAlive = [];
      const redAlive = [];
      for (const u of all) {{
        if (!u.alive) continue;
        if (u.team === "blue") blueAlive.push(u);
        else redAlive.push(u);
      }}
      if (blueAlive.length === 0 || redAlive.length === 0) {{
        world.done = true;
        world.winner = blueAlive.length === 0 ? "红方获胜" : "蓝方获胜";
        return;
      }}

      function enemiesOf(team) {{
        return team === "blue" ? redAlive : blueAlive;
      }}

      for (const u of all) {{
        if (!u.alive) continue;
        const enemies = enemiesOf(u.team);
        if (!u.target || !u.target.alive) recomputeTarget(u, enemies, rnd);
        if (!u.target) continue;

        const dx = u.target.x - u.x;
        const dy = u.target.y - u.y;
        const d = Math.max(0.001, len(dx, dy));
        const inRange = d <= u.range;

        if (!inRange) {{
          const nx = dx / d;
          const ny = dy / d;
          u.x += nx * u.speed * dt;
          u.y += ny * u.speed * dt;
          u.x = clamp(u.x, 20, CFG.arena.w - 20);
          u.y = clamp(u.y, 20, CFG.arena.h - 20);
        }}

        u.atkLeft -= dt;
        if (inRange && u.atkLeft <= 0) {{
          const raw = u.ad;
          const dmg = raw * armorMul(u.target.armor);
          u.target.hp -= dmg;
          u.dmgDone += dmg;
          world.hits.push({{
            x1: u.x, y1: u.y, x2: u.target.x, y2: u.target.y,
            c: u.team === "blue" ? COLORS.blue.hit : COLORS.red.hit,
            t: 0.22
          }});
          u.atkLeft = u.atkCd;
          if (u.target.hp <= 0 && u.target.alive) {{
            u.target.alive = false;
            u.target.hp = 0;
            u.target.target = null;
            u.target = null;
          }}
        }}

        if (u.burstCd > 0 && u.burstDmg > 0) {{
          u.burstLeft -= dt;
          if (u.burstLeft <= 0) {{
            recomputeTarget(u, enemies, rnd);
            if (u.target && u.target.alive) {{
              const bdx = u.target.x - u.x;
              const bdy = u.target.y - u.y;
              const bd = len(bdx, bdy);
              if (bd <= u.range * 1.25) {{
                const dmg = u.burstDmg * armorMul(u.target.armor * 0.35);
                u.target.hp -= dmg;
                u.dmgDone += dmg;
                world.hits.push({{
                  x1: u.x, y1: u.y, x2: u.target.x, y2: u.target.y,
                  c: "rgba(255,255,255,0.45)",
                  t: 0.28
                }});
                if (u.target.hp <= 0 && u.target.alive) {{
                  u.target.alive = false;
                  u.target.hp = 0;
                  u.target.target = null;
                  u.target = null;
                }}
              }}
            }}
            u.burstLeft = u.burstCd;
          }}
        }}
      }}

      for (const h of world.hits) h.t -= dt;
      world.hits = world.hits.filter(h => h.t > 0).slice(-HIT_PARTICLES_MAX);
    }}

    function drawWorld(world) {{
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const g = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      g.addColorStop(0, "rgba(15, 18, 35, 0.9)");
      g.addColorStop(1, "rgba(10, 12, 22, 0.85)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.save();
      ctx.globalAlpha = 0.22;
      ctx.strokeStyle = "rgba(255,255,255,0.18)";
      ctx.lineWidth = 1;
      for (let x = 0; x < canvas.width; x += 55) {{
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
      }}
      for (let y = 0; y < canvas.height; y += 55) {{
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
      }}
      ctx.restore();

      for (const h of world.hits) {{
        const a = clamp(h.t / 0.28, 0, 1);
        ctx.save();
        ctx.globalAlpha = 0.35 * a;
        ctx.strokeStyle = h.c;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(h.x1, h.y1);
        ctx.lineTo(h.x2, h.y2);
        ctx.stroke();
        ctx.restore();
      }}

      for (const u of world.units) {{
        if (!u.alive) continue;
        const c = COLORS[u.team][u.role] || (u.team === "blue" ? "#60a5fa" : "#f87171");

        ctx.save();
        ctx.shadowColor = "rgba(0,0,0,0.35)";
        ctx.shadowBlur = 12;
        ctx.fillStyle = c;
        ctx.beginPath();
        ctx.arc(u.x, u.y, u.r, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        const hpPct = u.maxHp > 0 ? clamp(u.hp / u.maxHp, 0, 1) : 0;
        const barW = 26;
        const barH = 4;
        const bx = u.x - barW / 2;
        const by = u.y - u.r - 10;
        ctx.save();
        ctx.globalAlpha = 0.9;
        ctx.fillStyle = "rgba(255,255,255,0.22)";
        ctx.fillRect(bx, by, barW, barH);
        ctx.fillStyle = hpPct > 0.5 ? "rgba(34,197,94,0.95)" : (hpPct > 0.25 ? "rgba(251,191,36,0.95)" : "rgba(239,68,68,0.95)");
        ctx.fillRect(bx, by, barW * hpPct, barH);
        ctx.restore();
      }}

      if (world.done) {{
        ctx.save();
        ctx.fillStyle = "rgba(255,255,255,0.92)";
        ctx.font = "800 34px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial";
        ctx.textAlign = "center";
        ctx.fillText(world.winner, canvas.width / 2, 52);
        ctx.restore();
      }}
    }}

    function computeHud(world) {{
      let bAlive = 0, rAlive = 0, bHp = 0, rHp = 0;
      for (const u of world.units) {{
        if (!u.alive) continue;
        if (u.team === "blue") {{
          bAlive += 1;
          bHp += u.hp;
        }} else {{
          rAlive += 1;
          rHp += u.hp;
        }}
      }}
      ui.bAlive.textContent = bAlive;
      ui.rAlive.textContent = rAlive;
      ui.bHp.textContent = Math.round(bHp);
      ui.rHp.textContent = Math.round(rHp);
      ui.t.textContent = world.t.toFixed(2);
      ui.winner.textContent = world.done ? world.winner : "";
    }}

    function reset() {{
      const rnd = mulberry32(CFG.seed ^ (NONCE * 2654435761 >>> 0));
      const blue = buildTeam("blue", CFG.teams.blue, true, rnd);
      const red = buildTeam("red", CFG.teams.red, false, rnd);
      const units = blue.concat(red);
      return {{
        t: 0,
        units,
        hits: [],
        done: false,
        winner: "",
        paused: false,
        spd: 1.0,
        acc: 0,
        rnd,
      }};
    }}

    let world = reset();
    ui.spd.addEventListener("input", () => {{
      world.spd = parseFloat(ui.spd.value);
      ui.spdLbl.textContent = `${{world.spd.toFixed(2)}}×`;
    }});
    ui.btnToggle.addEventListener("click", () => {{
      world.paused = !world.paused;
      ui.btnToggle.textContent = world.paused ? "继续" : "暂停";
    }});
    ui.btnReset.addEventListener("click", () => {{
      world = reset();
      ui.btnToggle.textContent = "暂停";
      ui.spd.value = "1.0";
      world.spd = 1.0;
      ui.spdLbl.textContent = "1.0×";
    }});

    let last = null;
    function loop(ts) {{
      if (last === null) last = ts;
      const rawDt = Math.min(0.05, (ts - last) / 1000.0);
      last = ts;
      const dt = world.paused ? 0 : rawDt * world.spd;

      world.acc += dt;
      const fixed = 1.0 / 60.0;
      let it = 0;
      while (world.acc >= fixed && it < 6) {{
        stepWorld(world, fixed, world.rnd);
        world.t += fixed;
        world.acc -= fixed;
        it += 1;
      }}

      drawWorld(world);
      computeHud(world);
      requestAnimationFrame(loop);
    }}
    requestAnimationFrame(loop);
  </script>
</body>
</html>
"""

st.markdown("### 画面")
st.components.v1.html(html, height=int(config["arena"]["h"] + 40), scrolling=False)
