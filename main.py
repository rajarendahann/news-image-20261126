#!/usr/bin/env python3
import sys
import os
import zlib
import struct

# -----------------------------------------------------------------------------
# PNG Encoder (Pure Stdlib: zlib + struct)
# -----------------------------------------------------------------------------
def save_png(filepath, width, height, pixels):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0) # filter type 0 (none)
        for x in range(width):
            idx = y * width + x
            r, g, b = pixels[idx]
            raw_data.extend(bytes([r, g, b]))

    compressed = zlib.compress(bytes(raw_data), level=6)
    
    png = bytearray(b'\x89PNG\r\n\x1a\n')
    png.extend(chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)))
    png.extend(chunk(b'IDAT', compressed))
    png.extend(chunk(b'IEND', b''))
    
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(png)

# -----------------------------------------------------------------------------
# Built-in 5x7 Bitmap Font & Drawing Engine
# -----------------------------------------------------------------------------
FONT_5X7 = {
    ' ': [0,0,0,0,0,0,0],
    '!': [4,4,4,4,0,4,0],
    '"': [10,10,0,0,0,0,0],
    '#': [10,31,10,10,31,10,0],
    '$': [4,31,20,14,5,31,4],
    '%': [24,25,2,4,8,19,3],
    '&': [12,18,20,8,21,18,13],
    '\'': [4,4,0,0,0,0,0],
    '(': [8,4,2,2,2,4,8],
    ')': [2,4,8,8,8,4,2],
    '*': [0,4,21,14,21,4,0],
    '+': [0,4,4,31,4,4,0],
    ',': [0,0,0,0,0,4,8],
    '-': [0,0,0,31,0,0,0],
    '.': [0,0,0,0,0,4,0],
    '/': [1,2,4,8,16,32,0],
    '0': [14,17,19,21,25,17,14],
    '1': [4,12,4,4,4,4,14],
    '2': [14,17,1,2,4,8,31],
    '3': [31,1,2,14,1,1,30],
    '4': [2,6,10,18,31,2,2],
    '5': [31,16,30,1,1,17,14],
    '6': [14,16,30,17,17,17,14],
    '7': [31,1,2,4,8,8,8],
    '8': [14,17,17,14,17,17,14],
    '9': [14,17,17,15,1,1,14],
    ':': [0,4,0,0,4,0,0],
    ';': [0,4,0,0,4,8,0],
    '<': [2,4,8,16,8,4,2],
    '=': [0,0,31,0,31,0,0],
    '>': [8,4,2,1,2,4,8],
    '?': [14,17,1,2,4,0,4],
    '@': [14,17,21,21,23,16,14],
    'A': [14,17,17,31,17,17,17],
    'B': [30,17,17,30,17,17,30],
    'C': [14,17,16,16,16,17,14],
    'D': [30,17,17,17,17,17,30],
    'E': [31,16,16,30,16,16,31],
    'F': [31,16,16,30,16,16,16],
    'G': [14,17,16,23,17,17,15],
    'H': [17,17,17,31,17,17,17],
    'I': [14,4,4,4,4,4,14],
    'J': [7,2,2,2,2,18,12],
    'K': [17,18,20,24,20,18,17],
    'L': [16,16,16,16,16,16,31],
    'M': [17,27,21,21,17,17,17],
    'N': [17,25,21,19,17,17,17],
    'O': [14,17,17,17,17,17,14],
    'P': [30,17,17,30,16,16,16],
    'Q': [14,17,17,17,21,18,13],
    'R': [30,17,17,30,20,18,17],
    'S': [14,16,16,14,1,1,30],
    'T': [31,4,4,4,4,4,4],
    'U': [17,17,17,17,17,17,14],
    'V': [17,17,17,17,17,10,4],
    'W': [17,17,17,21,21,27,17],
    'X': [17,17,10,4,10,17,17],
    'Y': [17,17,10,4,4,4,4],
    'Z': [31,1,2,4,8,16,31],
    '[': [14,8,8,8,8,8,14],
    '\\': [16,8,4,2,1,0,0],
    ']': [14,2,2,2,2,2,14],
    '^': [4,10,17,0,0,0,0],
    '_': [0,0,0,0,0,0,31],
    '`': [8,4,0,0,0,0,0],
    'a': [0,0,14,1,15,17,15],
    'b': [16,16,22,25,17,17,30],
    'c': [0,0,14,16,16,17,14],
    'd': [1,1,15,17,17,17,15],
    'e': [0,0,14,17,31,16,14],
    'f': [6,9,8,28,8,8,8],
    'g': [0,15,17,17,15,1,14],
    'h': [16,16,22,25,17,17,17],
    'i': [4,0,12,4,4,4,14],
    'j': [2,0,6,2,2,18,12],
    'k': [16,16,18,20,24,20,18],
    'l': [12,4,4,4,4,4,14],
    'm': [0,0,26,21,21,21,21],
    'n': [0,0,22,25,17,17,17],
    'o': [0,0,14,17,17,17,14],
    'p': [0,30,17,17,30,16,16],
    'q': [0,15,17,17,15,1,1],
    'r': [0,0,22,25,16,16,16],
    's': [0,0,15,16,14,1,30],
    't': [8,8,30,8,8,9,6],
    'u': [0,0,17,17,17,19,13],
    'v': [0,0,17,17,17,10,4],
    'w': [0,0,17,21,21,21,14],
    'x': [0,0,17,10,4,10,17],
    'y': [0,17,17,17,15,1,14],
    'z': [0,0,31,2,4,8,31],
    '{': [2,4,4,24,4,4,2],
    '|': [4,4,4,4,4,4,4],
    '}': [8,4,4,3,4,4,8],
    '~': [0,8,21,2,0,0,0],
}

def get_char_glyph(ch):
    if ch in FONT_5X7:
        return FONT_5X7[ch]
    upper = ch.upper()
    if upper in FONT_5X7:
        return FONT_5X7[upper]
    return FONT_5X7['?']

class Canvas:
    def __init__(self, width=1024, height=1024, bg_color=(253, 251, 247)):
        self.width = width
        self.height = height
        self.pixels = [bg_color] * (width * height)

    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y * self.width + x] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + w)
        y1 = min(self.height, y + h)
        for py in range(y0, y1):
            row_offset = py * self.width
            for px in range(x0, x1):
                self.pixels[row_offset + px] = color

    def draw_rect(self, x, y, w, h, color, thickness=1):
        self.fill_rect(x, y, w, thickness, color) # top
        self.fill_rect(x, y + h - thickness, w, thickness, color) # bottom
        self.fill_rect(x, y, thickness, h, color) # left
        self.fill_rect(x + w - thickness, y, thickness, h, color) # right

    def draw_line(self, x0, y0, x1, y1, color, thickness=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        cx, cy = x0, y0
        while True:
            self.fill_rect(cx, cy, thickness, thickness, color)
            if cx == x1 and cy == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                cx += sx
            if e2 < dx:
                err += dx
                cy += sy

    def draw_char(self, ch, x, y, color, scale=1):
        glyph = get_char_glyph(ch)
        for row_idx, row_val in enumerate(glyph):
            for col_idx in range(5):
                if (row_val >> (4 - col_idx)) & 1:
                    px = x + col_idx * scale
                    py = y + row_idx * scale
                    if scale == 1:
                        self.set_pixel(px, py, color)
                    else:
                        self.fill_rect(px, py, scale, scale, color)

    def draw_text(self, text, x, y, color, scale=1):
        cx = x
        char_w = 6 * scale # 5 pixels + 1 spacing
        for ch in text:
            if ch != '\n':
                self.draw_char(ch, cx, y, color, scale)
            cx += char_w

    def measure_text(self, text, scale=1):
        return len(text) * 6 * scale

    def wrap_text(self, text, max_width, scale=1):
        words = text.split(' ')
        lines = []
        current_line = []
        char_w = 6 * scale
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) * char_w <= max_width or not current_line:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines

def main():
    canvas = Canvas(1024, 1024, bg_color=(250, 247, 240)) # Warm premium newsprint background
    
    INK = (20, 20, 20)
    MUTED = (100, 95, 90)
    LINE_COLOR = (185, 175, 160)
    ACCENT_DARK = (40, 45, 55)
    
    # Section accent colors
    ACCENTS = {
        'ASIA': (180, 40, 40),       # Crimson Red
        'MIDDLE EAST': (30, 130, 60),  # Deep Emerald
        'EUROPE': (25, 100, 190),    # Classic Blue
        'AFRICA': (190, 110, 20),    # Warm Ochre
        'AMERICAS': (35, 60, 110),   # Navy Blue
        'OCEANIA': (20, 140, 130),   # Teal
        'GLOBAL': (70, 75, 85)       # Slate Gray
    }

    # 1. Masthead Header
    canvas.draw_text("THE WORLD IN ONE DAY • GLOBAL CHRONICLE EDITION", 16, 12, MUTED, scale=1)
    canvas.draw_line(16, 24, 1008, 24, LINE_COLOR, thickness=1)
    
    # Huge headline date banner
    canvas.draw_text("Thursday 26 November 2026", 16, 30, INK, scale=4)
    
    # Lede summary
    lede_text = "Trump tariffs unveiled; Nvidia reinstates Huang; 26 die in Indonesian factory fire."
    canvas.draw_text(lede_text, 16, 74, INK, scale=1)
    
    # Double rule header divider
    canvas.draw_line(16, 92, 1008, 92, INK, thickness=2)
    canvas.draw_line(16, 96, 1008, 96, LINE_COLOR, thickness=1)

    # 2. Region counters row
    counters_text = "ASIA (7)  |  MIDDLE EAST (1)  |  EUROPE (3)  |  AFRICA (0)  |  AMERICAS (5)  |  OCEANIA (2)  |  GLOBAL (6)"
    canvas.draw_text(counters_text, 16, 105, ACCENT_DARK, scale=1)
    canvas.draw_line(16, 117, 1008, 117, LINE_COLOR, thickness=1)

    # 3. Row of 3 BIG story cards (y = 133 to 408)
    big_stories = [
        ("GLOBAL", "Trump Unveils Fresh Tariff Suite", 
         "Proposed duties range from 10% to 40% targeting over a dozen major trading partners.",
         "Capped by negotiated trade agreements."),
        ("AMERICAS", "Nvidia Board Under Fire After Huang Return", 
         "Huang addressed employees less than a week after an all-hands held without him.",
         "Firm previously weighed a successor."),
        ("ASIA", "Indonesian Factory Fire Kills 26 Workers", 
         "26 workers killed with 8 still missing in blaze. US proposes up to 25% tariff on India.",
         "Offers 17% if trade deal is done.")
    ]
    
    card_w = 324
    card_gap = 18
    start_x = 16
    card_y = 133
    card_h = 275

    for i, (reg, head, l1, l2) in enumerate(big_stories):
        cx = start_x + i * (card_w + card_gap)
        accent = ACCENTS.get(reg, INK)
        # Card background box with subtle tint
        canvas.fill_rect(cx, card_y, card_w, card_h, (255, 253, 248))
        canvas.draw_rect(cx, card_y, card_w, card_h, LINE_COLOR, thickness=1)
        # Inner accent border line at top
        canvas.fill_rect(cx, card_y, card_w, 3, accent)
        
        # Region tag banner
        canvas.fill_rect(cx + 8, card_y + 8, card_w - 16, 24, accent)
        canvas.draw_text(reg, cx + 16, card_y + 12, (255, 255, 255), scale=2)
        
        # Headline (wrapped)
        head_lines = canvas.wrap_text(head, card_w - 24, scale=2)
        hy = card_y + 42
        for hl in head_lines[:2]:
            canvas.draw_text(hl, cx + 12, hy, INK, scale=2)
            hy += 18
            
        canvas.draw_line(cx + 12, hy + 2, cx + card_w - 12, hy + 2, LINE_COLOR, thickness=1)
        
        # Body lines
        by = hy + 12
        for bl in [l1, l2]:
            wrapped_bl = canvas.wrap_text(bl, card_w - 24, scale=1)
            for wbl in wrapped_bl:
                canvas.draw_text(wbl, cx + 12, by, INK, scale=1)
                by += 11
            by += 4

    canvas.draw_line(16, 418, 1008, 418, INK, thickness=2)

    # 4. 3x3 Grid of Medium Cards (y = 428 to 688)
    medium_stories = [
        ("GLOBAL", "Houthi Attack on Saudi PIF Tower", "Houthi attack on Saudi Public Investment Fund Tower injures 11."),
        ("EUROPE", "Norway Raises Cargo Ship Concerns", "Norway raises concerns after Ukraine strikes a Russian cargo ship."),
        ("EUROPE", "H5N1 Avian Influenza Hits Flocks", "H5N1 avian influenza is hitting Europe's poultry flocks hard."),
        ("ASIA", "China Extends Mineral Export Relief", "China extends key mineral export relief in the US trade dispute."),
        ("ASIA", "China Joins Cambodia Drills", "China joins Cambodia's Golden Dragon drills with ~3,000 personnel."),
        ("MIDDLE EAST", "UK Sanctions Yemen Houthis", "UK sanctions Yemen's Houthis and four senior officials over rights abuses."),
        ("ASIA", "South Korea Flags Russian Jets", "South Korea says Russian jets entered its air defence zone."),
        ("AMERICAS", "11 Killed in UAE Bus-Truck Crash", "11 killed when bus and truck collide in UAE's Ras Al Khaimah."),
        ("OCEANIA", "Two Charged Over Sandringham Break-In", "Two charged after break-in at the Prince and Princess of Wales' home.")
    ]

    grid_y = 428
    m_card_w = 324
    m_card_h = 76
    m_gap_x = 18
    m_gap_y = 8

    for idx, (reg, head, desc) in enumerate(medium_stories):
        col = idx % 3
        row = idx // 3
        mx = start_x + col * (m_card_w + m_gap_x)
        my = grid_y + row * (m_card_h + m_gap_y)
        accent = ACCENTS.get(reg, INK)
        
        canvas.fill_rect(mx, my, m_card_w, m_card_h, (255, 253, 248))
        canvas.draw_rect(mx, my, m_card_w, m_card_h, LINE_COLOR, thickness=1)
        canvas.fill_rect(mx, my, 3, m_card_h, accent) # Left accent tab
        
        # Region tag small
        canvas.fill_rect(mx + 8, my + 6, 64, 14, accent)
        canvas.draw_text(reg, mx + 11, my + 9, (255, 255, 255), scale=1)
        
        # Headline
        head_wrapped = canvas.wrap_text(head, m_card_w - 82, scale=1)
        if head_wrapped:
            canvas.draw_text(head_wrapped[0], mx + 76, my + 9, INK, scale=1)
        
        # Description
        desc_wrapped = canvas.wrap_text(desc, m_card_w - 16, scale=1)
        dy = my + 24
        for dw in desc_wrapped[:2]:
            canvas.draw_text(dw, mx + 10, dy, INK, scale=1)
            dy += 10

    canvas.draw_line(16, 698, 1008, 698, INK, thickness=2)

    # 5. Bottom Section: Map (left) + Two-column list (right) (y = 708 to 948)
    map_x = 16
    map_y = 708
    map_w = 336
    map_h = 240
    
    canvas.fill_rect(map_x, map_y, map_w, map_h, (255, 253, 248))
    canvas.draw_rect(map_x, map_y, map_w, map_h, LINE_COLOR, thickness=1)
    
    # Map header bar
    canvas.fill_rect(map_x, map_y, map_w, 24, ACCENT_DARK)
    canvas.draw_text("WHERE IT HAPPENED", map_x + 8, map_y + 8, (255, 255, 255), scale=2)
    
    # Legible dot-map grid and cities
    for dot_x in range(map_x + 20, map_x + map_w - 20, 24):
        for dot_y in range(map_y + 36, map_y + map_h - 15, 24):
            canvas.set_pixel(dot_x, dot_y, (200, 190, 175))

    cities = [
        ("Washington", 60, 95),
        ("Norfolk", 115, 75),
        ("Moscow", 185, 55),
        ("Riyadh", 170, 120),
        ("Sanaa", 190, 155),
        ("Ras Al Khaimah", 220, 135),
        ("Jakarta", 265, 185),
        ("Phnom Penh", 255, 175),
        ("Taipei", 280, 125),
        ("Seoul", 285, 90),
    ]
    
    for city, cx_off, cy_off in cities:
        px = map_x + cx_off
        py = map_y + cy_off
        canvas.fill_rect(px - 3, py - 3, 7, 7, (180, 40, 40))
        canvas.draw_text(city, px + 6, py - 3, INK, scale=1)

    # Right: Two-column list "ALSO ON THURSDAY 26 NOVEMBER 2026"
    list_x = 368
    list_y = 708
    list_w = 640
    list_h = 240
    
    canvas.fill_rect(list_x, list_y, list_w, list_h, (255, 253, 248))
    canvas.draw_rect(list_x, list_y, list_w, list_h, LINE_COLOR, thickness=1)
    
    # List header bar
    canvas.fill_rect(list_x, list_y, list_w, 24, ACCENT_DARK)
    canvas.draw_text("ALSO ON THURSDAY 26 NOVEMBER 2026", list_x + 8, list_y + 8, (255, 255, 255), scale=2)

    also_items = [
        ("Russia plans to launch a nuclear-armed satellite this year, reports say", "GLOBAL"),
        ("Sheikh Hasina seeks December 16 return aboard Bangladesh's state carrier", "ASIA"),
        ("US blocks restoring the WTO appeals system for the 102nd time", "GLOBAL"),
        ("Alice Huang-linked firms listed $270M in AI servers in China amid probe", "GLOBAL"),
        ("Trump's talks with NATO chief Rutte come amid alliance strains", "GLOBAL"),
        ("Miss Universe 2026 won by Jennifer Barreto of Puerto Rico", "AMERICAS"),
        ("Sweden pauses some deportations of young adults who arrived as children", "EUROPE"),
        ("GTRI: proposed 17% US tariff under trade pact gives India edge", "ASIA"),
        ("Trump proposes new tariffs including on China and India, 10%-40% range", "AMERICAS"),
        ("Hong Kong wildlife: ~80 exotic animals/hr, groups urge positive list", "ASIA"),
        ("Australia: woman charged over 300-chicken farm theft in NSW", "OCEANIA"),
        ("Nvidia co-founder spoke to employees as board faces fire", "AMERICAS")
    ]

    col1_x = list_x + 8
    col2_x = list_x + 328
    col_w_text = 304
    
    y_left = list_y + 32
    y_right = list_y + 32
    
    for idx, (item, reg) in enumerate(also_items):
        target_x = col1_x if idx < 6 else col2_x
        target_y_ptr = [y_left] if idx < 6 else [y_right]
        
        wrapped = canvas.wrap_text(f"[{reg}] {item}", col_w_text, scale=1)
        for line in wrapped:
            canvas.draw_text(line, target_x, target_y_ptr[0], INK, scale=1)
            target_y_ptr[0] += 10
        target_y_ptr[0] += 3
        
        if idx < 6:
            y_left = target_y_ptr[0]
        else:
            y_right = target_y_ptr[0]

    canvas.draw_line(16, 956, 1008, 956, INK, thickness=2)

    # 6. Footer (y = 962 to 1024)
    footer_lines = [
        "DATE CHECK: every story on this page happened, or was first reported, on Thursday 26 November 2026",
        "Sources: Reuters, AP, AFP, BBC, Al Jazeera, RNZ, Taipei Times, Business Standard, NZ Herald. Errors are not intentional.",
        "Stories are attributed, not stated as facts. Numbers are approximate."
    ]
    
    fy = 964
    for fl in footer_lines:
        canvas.draw_text(fl, 16, fy, MUTED, scale=1)
        fy += 11

    # Output path resolution according to rules
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR')
    if output_dir:
        try:
            os.makedirs(output_dir, exist_ok=True)
            out_path = os.path.join(output_dir, 'entry.png')
        except Exception:
            out_path = os.path.join(os.getcwd(), 'entry.png')
    else:
        try:
            os.makedirs('/output', exist_ok=True)
            out_path = '/output/entry.png'
        except Exception:
            out_path = os.path.join(os.getcwd(), 'entry.png')

    try:
        save_png(out_path, 1024, 1024, canvas.pixels)
        print(f"Successfully generated {out_path}")
    except Exception as e:
        fallback_path = os.path.join(os.getcwd(), 'entry.png')
        save_png(fallback_path, 1024, 1024, canvas.pixels)
        print(f"Fallback: successfully generated {fallback_path} due to error: {e}")

if __name__ == '__main__':
    main()
