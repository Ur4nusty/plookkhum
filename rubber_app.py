import base64
import os

import pandas as pd
import streamlit as st

st.set_page_config(page_title="ปลูกคุ้ม", page_icon="🌳", layout="centered")

LIME, BG, CARD, LINE, MUTED = "#8FAF4A", "#0E2419", "#163325", "#244A33", "#9FB3A5"
SQM_PER_RAI = 1600

# ---------------- สไตล์ ----------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai+Looped:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, button, input, textarea {
    font-family: 'Noto Sans Thai Looped', system-ui, sans-serif !important;
}
.stApp {
    background: radial-gradient(1100px 620px at 50% -8%, #214F35 0%, #0B1B12 62%) fixed;
    color: #fff;
}
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 460px; padding: 1rem 1.2rem 2.5rem; }
.block-container [data-testid="stVerticalBlock"] { gap: .75rem; }
@media (min-width: 700px) {
    .block-container {
        margin: 1.2rem auto; padding: 1.2rem 1.4rem 1.6rem; background: __BG__;
        border: 1px solid __LINE__; border-radius: 28px;
        box-shadow: 0 30px 80px rgba(0, 0, 0, .5);
    }
}

/* หัวเรื่อง */
.brand { font-size: clamp(2.6rem, 7.5vh, 3.4rem); font-weight: 700; line-height: 1.1; letter-spacing: -0.01em; margin: 0 0 .2rem; text-shadow: 0 2px 18px rgba(0,0,0,.5); }
.brand span { color: __LIME__; }
.bar { width: 64px; height: 4px; background: __LIME__; border-radius: 2px; margin: .4rem 0 1rem; }
.lead { color: #E9EFEA; font-size: .98rem; line-height: 1.55; margin-bottom: .2rem; }
.lead b { color: __LIME__; font-weight: 600; }
.meta { color: __MUTED__; font-size: .85rem; margin-bottom: .4rem; }
.page-title { font-size: 2rem; font-weight: 700; margin: .4rem 0 0; }
.page-title span { color: __LIME__; }
.hero { position: relative; border-radius: 20px; overflow: hidden; line-height: 0; height: clamp(120px, 20vh, 210px); }
.hero svg, .hero img { width: 100%; height: 100%; object-fit: cover; display: block; }
.hero::after { content: ""; position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(14,36,25,0) 35%, __BG__ 100%); }
.brand-wrap { position: relative; top: -2.9rem; margin-bottom: -2.9rem; }

/* เมนูหลัก (แถวแบบในแบบร่าง) */
.st-key-menu, .st-key-menu2, .st-key-menu [data-testid="stElementContainer"], .st-key-menu2 [data-testid="stElementContainer"],
.st-key-menu .stButton, .st-key-menu2 .stButton { width: 100% !important; }
.st-key-menu .stButton, .st-key-menu2 .stButton { display: flex; justify-content: center; }
.st-key-menu [data-testid="stVerticalBlock"], .st-key-menu2 [data-testid="stVerticalBlock"] { gap: .55rem; }
.st-key-menu button, .st-key-menu2 button {
    width: 100% !important; height: auto; position: relative; justify-content: center;
    background: __CARD__; border: 1px solid __LINE__; border-radius: 14px;
    padding: clamp(.5rem, 1.6vh, .9rem) 1.2rem; color: #fff; margin-bottom: 0;
}
.st-key-menu button, .st-key-menu2 button { transition: transform .12s ease, border-color .12s ease, background .12s ease; }
.st-key-menu button:hover, .st-key-menu2 button:hover { border-color: __LIME__; color: #fff; transform: translateY(-1px); background: #1A3B2A; }
.st-key-menu button:active, .st-key-menu2 button:active { transform: scale(.985); }
.st-key-menu button > div, .st-key-menu2 button > div { gap: .9rem; align-items: center; justify-content: center; width: auto; }
.st-key-menu [data-testid="stIconMaterial"] { color: __LIME__; font-size: 1.5rem; margin-right: .8rem; flex: none; background: rgba(143,175,74,.14);
    border-radius: 12px; padding: .5rem; width: 2.6rem; height: 2.6rem; display: flex; align-items: center; justify-content: center; }
.st-key-menu2 [data-testid="stIconMaterial"] { color: __MUTED__; }
@media (prefers-reduced-motion: reduce) { .st-key-menu button, .st-key-menu2 button { transition: none; } }
.st-key-menu button p, .st-key-menu2 button p { text-align: center; margin: 0; font-size: 1.05rem; line-height: 1.45; }
.st-key-menu2 button { background: transparent; border-style: dashed; color: __MUTED__; padding: .5rem 1.2rem; }
[data-testid="stMarkdownColoredText"] { color: __LIME__ !important; font-size: .9rem; font-weight: 400; }

/* ปุ่มกลับ */
.stDownloadButton, .stDownloadButton button { width: 100% !important; }
.stDownloadButton { display: flex; justify-content: center; }
.st-key-back button { background: transparent; border: none; color: __LIME__; padding: 0; font-size: 1rem; }
.st-key-back button:hover { color: #fff; background: transparent; }

/* ตัวเลขสรุป */
.big-label { color: __MUTED__; font-size: .92rem; }
.big-num { font-size: 3.1rem; font-weight: 600; color: __LIME__; line-height: 1.1; }
.big-num small { font-size: 1rem; color: __MUTED__; margin-left: .4rem; font-weight: 400; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: .7rem; margin: 1.2rem 0; }
.tile { background: linear-gradient(160deg, #1B3D2B, #12291D); border: 1px solid __LINE__; border-radius: 16px; padding: .9rem 1rem; }
.tile .v { font-size: 1.3rem; font-weight: 600; }
.tile .l { font-size: .82rem; color: __MUTED__; }
.kv { display: flex; justify-content: space-between; align-items: baseline; padding: .75rem 0; border-bottom: 1px solid __LINE__; }
.kv .k { color: #E9EFEA; }
.kv .p { color: __MUTED__; font-size: .85rem; margin-left: .5rem; }
.kv .v { font-weight: 600; }
.note { color: __MUTED__; font-size: .82rem; margin: .5rem 0 0; line-height: 1.55; }
h3 { font-size: 1.05rem !important; font-weight: 600 !important; margin-top: 1.8rem !important;
     border-left: 3px solid __LIME__; padding: 0 0 0 .6rem !important; }
label p, [data-testid="stWidgetLabel"] p { color: #CFE0D3 !important; font-size: .92rem !important; }
[data-baseweb="input"], [data-baseweb="base-input"] { background: __CARD__ !important; border-radius: 12px !important; }
[data-baseweb="input"] { border: 1px solid __LINE__ !important; }
[data-testid="stNumberInput"] button { background: transparent !important; color: __LIME__ !important; }
[data-testid="stDataFrame"] { border: 1px solid __LINE__; border-radius: 14px; overflow: hidden; }
[data-testid="stCaptionContainer"] { color: __MUTED__; }

:focus-visible { outline: 2px solid __LIME__ !important; outline-offset: 2px; }
</style>
"""
for k, v in {"__BG__": BG, "__LIME__": LIME, "__CARD__": CARD, "__LINE__": LINE, "__MUTED__": MUTED}.items():
    CSS = CSS.replace(k, v)
st.markdown(CSS, unsafe_allow_html=True)

HERO_SVG = f"""
<svg viewBox="0 0 400 200" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="สวนยางพารา">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2C5B3A"/><stop offset="1" stop-color="#0E2419"/>
    </linearGradient>
    <radialGradient id="s" cx="50%" cy="38%" r="40%">
      <stop offset="0" stop-color="{LIME}" stop-opacity=".55"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="400" height="200" fill="url(#g)"/>
  <rect width="400" height="200" fill="url(#s)"/>
  <polygon points="170,200 230,200 205,95 195,95" fill="#3E6B45" opacity=".55"/>
  <g fill="#0A1A12">
    <polygon points="0,0 22,0 14,200 -10,200" opacity=".95"/>
    <polygon points="70,0 88,0 82,200 52,200" opacity=".85"/>
    <polygon points="128,0 140,0 138,200 114,200" opacity=".7"/>
    <polygon points="378,0 400,0 410,200 386,200" opacity=".95"/>
    <polygon points="312,0 330,0 342,200 318,200" opacity=".85"/>
    <polygon points="262,0 274,0 288,200 266,200" opacity=".7"/>
  </g>
</svg>
"""

# ---------------- สถานะ ----------------
DEFAULTS = dict(
    rai=10.0, trees_per_rai=70, start_age=7, horizon=10, tap_days=130,
    rubber_price=50.0, price_growth=0.0, fert_price_kg=18.0, fert_labor_rai=150.0,
    fert_times=2, tap_share=40, other_cost_rai=800.0,
    use_irrigation=True, et0=4.0, kc=0.9, rain_mm_yr=1800.0, eff_rain=70, water_price_m3=3.0,
    apply_fert=True, fert_effect=10,
)
DEFAULT_RATES = pd.DataFrame({
    "อายุ (ปี)": list(range(1, 26)),
    "ปุ๋ย (กรัม/ต้น/ครั้ง)": [100] * 3 + [150] * 3 + [200] * 3 + [250] * 16,
    "ผลผลิต (กรัม/ต้น/วันกรีด)": [0] * 6 + [30, 38, 45, 50, 55, 58, 60] + [60] * 12,
})

ss = st.session_state
ss.setdefault("page", "home")
ss.setdefault("cfg", dict(DEFAULTS))
ss.setdefault("rates", DEFAULT_RATES.copy())
cfg = ss["cfg"]


def go(page):
    ss["page"] = page


def num(label, key, lo, hi, step):
    cfg[key] = st.number_input(label, lo, hi, cfg[key], step, key="w_" + key)


def sld(label, key, lo, hi):
    cfg[key] = st.slider(label, lo, hi, cfg[key], key="w_" + key)


def chk(label, key):
    cfg[key] = st.checkbox(label, cfg[key], key="w_" + key)


def fmt(x, d=0):
    return f"{x:,.{d}f}"


def tiles(items):
    html = "".join(f'<div class="tile"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in items)
    st.markdown(f'<div class="grid">{html}</div>', unsafe_allow_html=True)


def big(label, value, unit):
    st.markdown(
        f'<div class="big-label">{label}</div><div class="big-num">{value}<small>{unit}</small></div>',
        unsafe_allow_html=True,
    )


def kv_rows(rows):
    html = "".join(
        f'<div class="kv"><div class="k">{k}<span class="p">{p}</span></div><div class="v">{v}</div></div>'
        for k, v, p in rows
    )
    st.markdown(html, unsafe_allow_html=True)


def header(white, lime):
    with st.container(key="back"):
        st.button("กลับ", icon=":material/arrow_back_ios_new:", on_click=go, args=("home",))
    st.markdown(f'<div class="page-title">{white}<span>{lime}</span></div><div class="bar"></div>', unsafe_allow_html=True)


# ---------------- คำนวณ ----------------
def compute():
    c, rates = cfg, ss["rates"].set_index("อายุ (ปี)")
    trees = c["rai"] * c["trees_per_rai"]
    rows = []
    for i in range(int(c["horizon"])):
        age = int(min(c["start_age"] + i, 25))
        n = i + 1
        fert_g = float(rates.loc[age, "ปุ๋ย (กรัม/ต้น/ครั้ง)"])
        yld_g = float(rates.loc[age, "ผลผลิต (กรัม/ต้น/วันกรีด)"])

        fert_kg = fert_g * trees * c["fert_times"] / 1000 if c["apply_fert"] else 0.0
        fert_cost = fert_kg * c["fert_price_kg"]
        labor_cost = c["fert_labor_rai"] * c["rai"] * c["fert_times"] if c["apply_fert"] else 0.0

        etc_mm = c["et0"] * c["kc"] * 365  # 1 มม. บน 1 ตร.ม. = 1 ลิตร
        deficit = max(0.0, etc_mm - c["rain_mm_yr"] * c["eff_rain"] / 100) if c["use_irrigation"] else 0.0
        water_m3 = deficit * c["rai"] * SQM_PER_RAI / 1000
        water_cost = water_m3 * c["water_price_m3"]

        boost = 1 + (c["fert_effect"] / 100 if c["apply_fert"] and yld_g > 0 else 0)
        yield_kg = yld_g * boost * trees * c["tap_days"] / 1000
        price = c["rubber_price"] * (1 + c["price_growth"] / 100) ** n
        revenue = yield_kg * price
        tapper = revenue * c["tap_share"] / 100
        other = c["other_cost_rai"] * c["rai"]
        total = fert_cost + labor_cost + water_cost + tapper + other

        rows.append({
            "ปีที่": n, "อายุสวน": age,
            "ผลผลิต (กก.)": yield_kg, "ปุ๋ย (กก.)": fert_kg, "น้ำเสริม (ลบ.ม.)": water_m3,
            "ราคา (บาท/กก.)": price, "รายได้": revenue,
            "ค่าปุ๋ย": fert_cost, "ค่าแรงใส่ปุ๋ย": labor_cost, "ค่าน้ำ": water_cost,
            "ส่วนแบ่งคนกรีด": tapper, "ต้นทุนอื่น": other,
            "ต้นทุนรวม": total, "กำไรสุทธิ": revenue - total,
        })
    return trees, pd.DataFrame(rows)


trees, df = compute()
tot_rev, tot_cost, tot_net = df["รายได้"].sum(), df["ต้นทุนรวม"].sum(), df["กำไรสุทธิ"].sum()

# ---------------- หน้าแรก ----------------
def page_home():
    hero = next((p for p in ("hero.jpg", "hero.jpeg", "hero.png") if os.path.exists(p)), None)
    if hero:
        mime = "image/png" if hero.endswith(".png") else "image/jpeg"
        with open(hero, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        art = f'<img src="data:{mime};base64,{b64}" alt="สวนยางพารา">'
    else:
        art = HERO_SVG
    st.markdown(f'<div class="hero">{art}</div>', unsafe_allow_html=True)

    st.markdown('<div class="brand-wrap"><div class="brand">ปลูก<span>คุ้ม</span></div><div class="bar"></div></div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="lead">แอปคำนวณปริมาณน้ำและปุ๋ย ค่าใช้จ่าย <b>ความคุ้มค่า</b> '
        'และ<b>คาดการณ์ผลผลิต</b>ในสวนยางพารา</div>'
        f'<div class="meta">{fmt(cfg["rai"])} ไร่ · {fmt(trees)} ต้น · อายุ {int(cfg["start_age"])} ปี</div>',
        unsafe_allow_html=True,
    )

    menu = [
        ("น้ำและปุ๋ย", "คำนวณปริมาณ", "water", ":material/water_drop:"),
        ("ค่าใช้จ่าย", "ประเมินต้นทุน", "cost", ":material/payments:"),
        ("ความคุ้มค่า", "วิเคราะห์ความคุ้มค่า", "value", ":material/savings:"),
        ("ผลผลิต", "คาดการณ์ผลผลิต", "yield", ":material/forest:"),
    ]
    with st.container(key="menu"):
        for title, sub, page, icon in menu:
            st.button(f"**{title}**  \n:green[{sub}]", key=f"m_{page}", icon=icon, on_click=go, args=(page,))
    with st.container(key="menu2"):
        st.button("ข้อมูลสวน", key="m_garden", icon=":material/tune:", on_click=go, args=("garden",))
    st.markdown('<div class="note">ตัวเลขทั้งหมดเป็นค่าตัวอย่าง ปรับให้ตรงกับสวนของคุณก่อนใช้ตัดสินใจ</div>',
                unsafe_allow_html=True)


# ---------------- ข้อมูลสวน ----------------
def page_garden():
    header("ข้อมูล", "สวน")
    num("เนื้อที่ (ไร่)", "rai", 1.0, 10000.0, 1.0)
    num("จำนวนต้นต่อไร่", "trees_per_rai", 20, 100, 1)
    num("อายุสวนตอนนี้ (ปี)", "start_age", 1, 25, 1)
    sld("คาดการณ์ล่วงหน้า (ปี)", "horizon", 1, 20)
    num("วันกรีดต่อปี", "tap_days", 50, 220, 1)
    st.markdown(f'<div class="note">รวม {fmt(trees)} ต้น</div>', unsafe_allow_html=True)


# ---------------- น้ำและปุ๋ย ----------------
def page_water():
    header("น้ำและ", "ปุ๋ย")
    first = df.iloc[0]
    water_l_tree_day = first["น้ำเสริม (ลบ.ม.)"] * 1000 / trees / 365 if trees else 0
    tiles([
        (f"{fmt(first['ปุ๋ย (กก.)'])} กก.", f"ปุ๋ยปีแรก (≈ {first['ปุ๋ย (กก.)'] / 50:.1f} ถุง 50 กก.)"),
        (f"{fmt(first['น้ำเสริม (ลบ.ม.)'])} ลบ.ม.", "น้ำเสริมปีแรก"),
        (f"{fmt(first['ปุ๋ย (กก.)'] * 1000 / trees / max(cfg['fert_times'], 1), 0) if trees else 0} กรัม", "ปุ๋ยต่อต้นต่อครั้ง"),
        (f"{water_l_tree_day:.1f} ลิตร", "น้ำเสริมต่อต้นต่อวัน"),
    ])

    st.markdown("### ปุ๋ย")
    chk("ใส่ปุ๋ยตามแผน", "apply_fert")
    num("ใส่ปุ๋ยกี่ครั้งต่อปี", "fert_times", 1, 4, 1)
    st.caption("อัตรากรัมต่อต้นตามอายุ แก้ได้ที่หน้า ผลผลิต")

    st.markdown("### น้ำ")
    chk("ให้น้ำเสริม", "use_irrigation")
    num("ET0 (มม./วัน)", "et0", 1.0, 8.0, 0.1)
    num("Kc ของยาง", "kc", 0.5, 1.3, 0.05)
    num("ฝนรายปี (มม.)", "rain_mm_yr", 500.0, 4500.0, 50.0)
    sld("ฝนที่ใช้ได้จริง (%)", "eff_rain", 30, 90)

    st.markdown("### รายปี")
    st.dataframe(
        df[["ปีที่", "อายุสวน", "ปุ๋ย (กก.)", "น้ำเสริม (ลบ.ม.)"]].style.format("{:,.0f}", subset=["ปุ๋ย (กก.)", "น้ำเสริม (ลบ.ม.)"]),
        hide_index=True, use_container_width=True,
    )


# ---------------- ค่าใช้จ่าย ----------------
def page_cost():
    header("ค่า", "ใช้จ่าย")
    big("ต้นทุนรวม", fmt(tot_cost), "บาท")
    st.markdown(f'<div class="note">ใน {int(cfg["horizon"])} ปี · เฉลี่ย {fmt(tot_cost / max(cfg["rai"], 1) / max(cfg["horizon"], 1))} บาท/ไร่/ปี</div>', unsafe_allow_html=True)

    items = [
        ("ปุ๋ย", df["ค่าปุ๋ย"].sum()), ("ค่าแรงใส่ปุ๋ย", df["ค่าแรงใส่ปุ๋ย"].sum()),
        ("น้ำ", df["ค่าน้ำ"].sum()), ("ส่วนแบ่งคนกรีด", df["ส่วนแบ่งคนกรีด"].sum()),
        ("ต้นทุนอื่น", df["ต้นทุนอื่น"].sum()),
    ]
    kv_rows([(k, fmt(v) + " บาท", f"{v / tot_cost * 100:.0f}%" if tot_cost else "") for k, v in items])

    st.markdown("### ปรับราคา")
    num("ราคาปุ๋ย (บาท/กก.)", "fert_price_kg", 1.0, 100.0, 0.5)
    num("ค่าแรงใส่ปุ๋ย (บาท/ไร่/ครั้ง)", "fert_labor_rai", 0.0, 2000.0, 10.0)
    num("ต้นทุนน้ำ (บาท/ลบ.ม.)", "water_price_m3", 0.0, 100.0, 0.5)
    sld("ส่วนแบ่งคนกรีด (%)", "tap_share", 0, 60)
    num("ต้นทุนอื่น (บาท/ไร่/ปี)", "other_cost_rai", 0.0, 20000.0, 100.0)

    st.markdown("### ต้นทุนรายปี (บาท)")
    st.bar_chart(df.set_index("ปีที่")["ต้นทุนรวม"], color=LIME, height=220)


# ---------------- ความคุ้มค่า ----------------
def page_value():
    header("ความ", "คุ้มค่า")
    big("กำไรสุทธิรวม", fmt(tot_net), "บาท")
    bc = tot_rev / tot_cost if tot_cost else 0
    per_rai_year = tot_net / max(cfg["rai"], 1) / max(cfg["horizon"], 1)

    fert_spend = df["ค่าปุ๋ย"].sum() + df["ค่าแรงใส่ปุ๋ย"].sum()
    fert_ret = None
    if cfg["apply_fert"] and cfg["fert_effect"] > 0 and fert_spend > 0:
        extra = (df["รายได้"] - df["รายได้"] / (1 + cfg["fert_effect"] / 100)).sum()
        fert_ret = extra / fert_spend

    tiles([
        (fmt(tot_rev), "รายได้รวม (บาท)"),
        (f"{bc:.2f}", "รายได้ต่อต้นทุน (B/C)"),
        (fmt(per_rai_year), "กำไรต่อไร่ต่อปี (บาท)"),
        (f"{fert_ret:.1f} เท่า" if fert_ret is not None else "-", "ปุ๋ยคืนรายได้"),
    ])

    st.markdown("### ราคายาง")
    num("ราคายาง (บาท/กก.)", "rubber_price", 1.0, 500.0, 1.0)
    num("ราคายางเปลี่ยนต่อปี (%)", "price_growth", -20.0, 20.0, 0.5)

    st.markdown("### ถ้าราคายางเปลี่ยน")
    fixed = tot_cost - df["ส่วนแบ่งคนกรีด"].sum()
    sens = []
    for p in [30, 40, 50, 60, 70, 80]:
        rev = (df["ผลผลิต (กก.)"] * p).sum()
        cost = fixed + rev * cfg["tap_share"] / 100
        sens.append({"ราคา (บาท/กก.)": p, "กำไรสุทธิ": rev - cost, "B/C": rev / cost if cost else 0})
    st.dataframe(
        pd.DataFrame(sens).style.format({"กำไรสุทธิ": "{:,.0f}", "B/C": "{:.2f}"}),
        hide_index=True, use_container_width=True,
    )

    st.markdown("### รายได้ ต้นทุน และกำไร (บาท)")
    st.line_chart(df.set_index("ปีที่")[["รายได้", "ต้นทุนรวม", "กำไรสุทธิ"]], color=[LIME, "#6F8F78", "#FFFFFF"], height=240)


# ---------------- ผลผลิต ----------------
def page_yield():
    header("ผล", "ผลิต")
    big("ผลผลิตรวมที่คาดการณ์", fmt(df["ผลผลิต (กก.)"].sum()), "กก.")
    first = df.iloc[0]
    tiles([
        (fmt(first["ผลผลิต (กก.)"]), "ปีแรก (กก.)"),
        (fmt(df["ผลผลิต (กก.)"].iloc[-1]), f"ปีที่ {int(cfg['horizon'])} (กก.)"),
        (fmt(first["ผลผลิต (กก.)"] / max(cfg["rai"], 1)), "ปีแรก ต่อไร่ (กก.)"),
        (fmt(df["ผลผลิต (กก.)"].mean()), "เฉลี่ยต่อปี (กก.)"),
    ])
    st.bar_chart(df.set_index("ปีที่")["ผลผลิต (กก.)"], color=LIME, height=240)

    st.markdown("### ปรับตัวแปร")
    sld("ปุ๋ยเพิ่มผลผลิต (%)", "fert_effect", 0, 30)

    st.markdown("### อัตราตามอายุ")
    st.caption("ค่าตัวอย่าง แก้ในตารางได้ ผลคำนวณใหม่ทันที")
    edited = st.data_editor(ss["rates"], hide_index=True, use_container_width=True, key="rates_editor")
    if not edited.equals(ss["rates"]):
        ss["rates"] = edited
        st.rerun()

    st.download_button("ดาวน์โหลดตารางรายปี (CSV)", df.to_csv(index=False).encode("utf-8-sig"), "plookkhum.csv", "text/csv")


PAGES = {"home": page_home, "garden": page_garden, "water": page_water,
         "cost": page_cost, "value": page_value, "yield": page_yield}
PAGES[ss["page"]]()
