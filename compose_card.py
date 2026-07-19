import html

FRAG_PATH = "/home/claude/portrait_fragment.svg"
OUT_PATH = "/home/claude/profile_card.svg"

with open(FRAG_PATH) as f:
    portrait_fragment = f.read()

CARD_BG = "#f6f8fa"
CARD_BORDER = "#e1e4e8"
PORTRAIT_BG = "#0d1117"
KEY_COLOR = "#22863a"     # green
VAL_COLOR = "#0366d6"     # blue
HEAD_COLOR = "#24292e"    # near-black
DOT_COLOR = "#c9d1d9"

FONT = "Consolas, Menlo, monospace"
FS = 15.5
LH = 24

W = 1220
PORTRAIT_W = 420
PORTRAIT_H = 560
PAD = 26
TEXT_X = PORTRAIT_W + 60

rows = []  # (kind, ...)
rows.append(("header", "OmShukla"))
rows.append(("kv", "OS", "Linux, Windows"))
rows.append(("kv", "Dev Uptime", "3 years, 6 months"))
rows.append(("kv", "GitHub Uptime", "1 year, 8 months"))
rows.append(("kv", "Host", "Planet Earth (Remote OK)"))
rows.append(("kv", "Kernel", "cloud-native-amd64"))
rows.append(("kv", "IDE", "VS Code, Cursor"))
rows.append(("blank",))
rows.append(("kv", "Languages.Programming", "C++, Python, JavaScript/TypeScript"))
rows.append(("kv", "Languages.Frameworks", "React, Node.js, FastAPI"))
rows.append(("blank",))
rows.append(("kv", "Hobbies", "Competitive Programming, Music"))
rows.append(("kv", "Interests", "Cloud Computing, Open Source Dev"))
rows.append(("blank",))
rows.append(("header", "Contact"))
rows.append(("kv", "Location", "Lucknow, India"))
rows.append(("kv", "Email", "omshukla2028@gmail.com"))
rows.append(("kv", "GitHub", "github.com/om-shukla-cld"))
rows.append(("kv", "LinkedIn", "linkedin.com/in/om-shukla-cld"))
rows.append(("kv", "Portfolio", "om-shukla.dev"))
rows.append(("blank",))
rows.append(("header", "GitHub Stats"))
rows.append(("kv", "Repos", "-- (auto-fills once repo is public)"))
rows.append(("kv", "Stars", "--"))
rows.append(("kv", "Followers", "--"))

def esc(s):
    return html.escape(s)

max_key_len = max(len(row[1]) for row in rows if row[0] == "kv")
DOT_COL = max_key_len + 2  # column (in chars) where dot leaders start
VAL_COL = DOT_COL + 14     # column where values start

svg_rows = []
y = PAD + FS
for row in rows:
    if row[0] == "header":
        text = row[1]
        line = f"{text} "
        dashes = "-" * (48 - len(line))
        svg_rows.append(
            f'<text x="{TEXT_X}" y="{y}" font-family="{FONT}" font-size="{FS}" '
            f'font-weight="700" fill="{HEAD_COLOR}" xml:space="preserve">'
            f'{esc(text)} <tspan fill="{DOT_COLOR}">{esc(dashes)}</tspan></text>'
        )
        y += LH
    elif row[0] == "blank":
        y += LH * 0.5
    else:
        _, key, val = row
        n_dots = max(2, DOT_COL - len(key))
        pad_before_val = max(1, VAL_COL - (len(key) + n_dots))
        dots = "." * n_dots
        spacer = " " * pad_before_val
        svg_rows.append(
            f'<text x="{TEXT_X}" y="{y}" font-family="{FONT}" font-size="{FS}" '
            f'xml:space="preserve">'
            f'<tspan fill="{KEY_COLOR}" font-weight="600">{esc(key)}</tspan>'
            f'<tspan fill="{DOT_COLOR}">{esc(dots)}{esc(spacer)}</tspan>'
            f'<tspan fill="{VAL_COLOR}">{esc(val)}</tspan>'
            f'</text>'
        )
        y += LH

H = max(PORTRAIT_H + PAD * 2, y + PAD)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}">
  <rect x="0" y="0" width="{W}" height="{H:.0f}" rx="14" fill="{CARD_BG}" stroke="{CARD_BORDER}" stroke-width="1.5"/>
  <rect x="{PAD}" y="{PAD}" width="{PORTRAIT_W - PAD}" height="{PORTRAIT_H}" rx="10" fill="{PORTRAIT_BG}"/>
  <g transform="translate({PAD}, {PAD})">
    {portrait_fragment}
  </g>
  {''.join(svg_rows)}
</svg>'''

with open(OUT_PATH, "w") as f:
    f.write(svg)

print("wrote", OUT_PATH, "height", H)
