from PIL import Image, ImageOps
import html

SRC = "/mnt/user-data/uploads/1784449681281_image.png"  # will be swapped for the real photo below
PHOTO = "/mnt/user-data/uploads/Screenshot_2025-12-24_155848.png"

RAMP = "@%#*+=-:. "
COLS = 46
CHAR_ASPECT = 0.5

def image_to_colored_ascii(path, cols=COLS):
    img = Image.open(path).convert("RGB")
    img = ImageOps.autocontrast(img, cutoff=1)
    w, h = img.size
    rows = int((h / w) * cols * CHAR_ASPECT)
    small = img.resize((cols, rows))
    gray = small.convert("L")

    px_rgb = list(small.getdata())
    px_gray = list(gray.getdata())

    cells = []  # list of rows, each a list of (char, hexcolor)
    for r in range(rows):
        row = []
        for c in range(cols):
            i = r * cols + c
            v = px_gray[i]
            ch = RAMP[int(v / 256 * len(RAMP))]
            rr, gg, bb = px_rgb[i]
            row.append((ch, f"#{rr:02x}{gg:02x}{bb:02x}"))
        cells.append(row)
    return cells

def portrait_svg_fragment(cells, x0, y0, font_size=6.2, line_h=6.6):
    parts = []
    for r, row in enumerate(cells):
        y = y0 + r * line_h + font_size
        x = x0
        # group consecutive same-color chars for compactness
        buf = ""
        cur_color = None
        run = []
        for ch, color in row:
            if color == cur_color:
                buf += ch
            else:
                if buf:
                    run.append((buf, cur_color))
                buf = ch
                cur_color = color
        if buf:
            run.append((buf, cur_color))
        tspans = "".join(
            f'<tspan fill="{color}">{html.escape(seg)}</tspan>' for seg, color in run
        )
        parts.append(
            f'<text x="{x}" y="{y}" font-family="Consolas, Menlo, monospace" '
            f'font-size="{font_size}" xml:space="preserve">{tspans}</text>'
        )
    return "\n".join(parts)

if __name__ == "__main__":
    cells = image_to_colored_ascii(PHOTO)
    frag = portrait_svg_fragment(cells, x0=24, y0=24)
    with open("/home/claude/portrait_fragment.svg", "w") as f:
        f.write(frag)
    print("rows:", len(cells), "cols:", len(cells[0]))
