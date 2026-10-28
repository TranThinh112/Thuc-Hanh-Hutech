# -*- coding: utf-8 -*-
import sys
import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

sys.stdout.reconfigure(encoding="utf-8")

SRC_PATH = r"C:/Users/Admin/Downloads/BAO_CAO_DO_AN_XAY_DUNG_WEBSITE_TMDT_PHONG_CHONG_GIAN_LAN_THANH_TOAN.docx"
OUT_DOWNLOAD = r"C:/Users/Admin/Downloads/BAO_CAO_DO_AN_XAY_DUNG_WEBSITE_TMDT_PHONG_CHONG_GIAN_LAN_THANH_TOAN_HOAN_CHINH.docx"
OUT_LOCAL = r"BAO_CAO_DO_AN_XAY_DUNG_WEBSITE_TMDT_PHONG_CHONG_GIAN_LAN_THANH_TOAN_HOAN_CHINH.docx"

print(f"Loading original document: {SRC_PATH}")
doc = docx.Document(SRC_PATH)

def format_run(run, font_name="Times New Roman", font_size=13, bold=False, italic=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color

def add_p(target_p, text="", bold=False, italic=False, size=13, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.3):
    p = target_p.insert_paragraph_before()
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        r = p.add_run(text)
        format_run(r, font_size=size, bold=bold, italic=italic)
    return p

def add_h1(target_p, text):
    return add_p(target_p, text, bold=True, size=15, space_before=18, space_after=10, align=WD_ALIGN_PARAGRAPH.LEFT)

def add_h2(target_p, text):
    return add_p(target_p, text, bold=True, size=13.5, space_before=14, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT)

def add_h3(target_p, text):
    return add_p(target_p, text, bold=True, size=13, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT)

def add_bullet(target_p, title, desc):
    p = target_p.insert_paragraph_before()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.left_indent = Inches(0.25)
    r_bullet = p.add_run("•  ")
    format_run(r_bullet, font_size=13, bold=True)
    if title:
        r_title = p.add_run(title + ": ")
        format_run(r_title, font_size=13, bold=True)
    r_desc = p.add_run(desc)
    format_run(r_desc, font_size=13, bold=False)
    return p

def set_cell_background(cell, fill_hex):
    w_ns = nsdecls("w")
    shd = parse_xml(f'<w:shd {w_ns} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def add_table_data(doc, target_p, headers, rows, col_widths, caption):
    if caption:
        p_cap = target_p.insert_paragraph_before()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(4)
        r_lbl = p_cap.add_run(caption)
        format_run(r_lbl, font_size=11, bold=True, italic=True)
        
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    w_ns = nsdecls("w")
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1F497D")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        for r in p.runs:
            format_run(r, font_size=10.5, bold=True, color=RGBColor(255, 255, 255))
            
    # Data rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        bg_col = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            if bg_col != "FFFFFF":
                set_cell_background(row_cells[c_idx], bg_col)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            if c_idx == 0 or len(str(val)) < 12:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                format_run(r, font_size=10, bold=(c_idx == 0 and len(row_data) > 3))
                
    # Borders
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {w_ns}><w:top w:val="single" w:sz="6" w:space="0" w:color="1F497D"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="1F497D"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/><w:left w:val="none"/><w:right w:val="none"/><w:insideV w:val="none"/></w:tblBorders>')
    tblPr.append(borders)
    
    # Column widths
    for row in table.rows:
        for c_idx, w in enumerate(col_widths):
            row.cells[c_idx].width = Inches(w)
            
    target_p._element.addprevious(table._element)
    
    # Spacing after
    p_sp = target_p.insert_paragraph_before()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(6)

def add_figure_item(target_p, img_path, fig_id, fig_title, commentary):
    p_img = target_p.insert_paragraph_before()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(10)
    p_img.paragraph_format.space_after = Pt(4)
    r_img = p_img.add_run()
    r_img.add_picture(img_path, width=Inches(5.95))
    
    p_cap = target_p.insert_paragraph_before()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    r_lbl = p_cap.add_run(f"Hình {fig_id}: ")
    format_run(r_lbl, font_size=11, bold=True, italic=True)
    r_txt = p_cap.add_run(fig_title)
    format_run(r_txt, font_size=11, bold=False, italic=True)
    
    if commentary:
        for c in commentary:
            add_p(target_p, c, size=13, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

print("Updating Danh mục hình ảnh...")
# Find paragraph with 'DANH MỤC HÌNH ẢNH'
fig_list_idx = None
for i, p in enumerate(doc.paragraphs):
    if "DANH MỤC HÌNH ẢNH" in p.text.upper():
        fig_list_idx = i
        break

if fig_list_idx is not None:
    # Delete empty lines between fig_list_idx and Chapter 1
    ch1_idx = None
    for i in range(fig_list_idx + 1, len(doc.paragraphs)):
        if "CHƯƠNG 1:" in doc.paragraphs[i].text.upper():
            ch1_idx = i
            break
    if ch1_idx is not None:
        p_ch1 = doc.paragraphs[ch1_idx]
        # Remove empty paragraphs in between
        for p in [doc.paragraphs[k] for k in range(fig_list_idx + 1, ch1_idx)]:
            p._element.getparent().remove(p._element)
            
        # Insert 14 figure entries
        with open("chapter3_sec4.json", "r", encoding="utf-8") as f:
            sec4_data = json.load(f)
            
        for sub in sec4_data["subsections"]:
            for fig in sub["figures"]:
                p_item = p_ch1.insert_paragraph_before()
                p_item.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p_item.paragraph_format.line_spacing = 1.3
                p_item.paragraph_format.space_before = Pt(2)
                p_item.paragraph_format.space_after = Pt(3)
                r_num = p_item.add_run(f"Hình {fig['id']}: ")
                format_run(r_num, font_size=12, bold=True)
                r_title = p_item.add_run(fig["title"])
                format_run(r_title, font_size=12, bold=False)

print("Locating Chapter 3 and Chapter 4...")
ch3_start = None
ch4_start = None
for i, p in enumerate(doc.paragraphs):
    if "CHƯƠNG 3:" in p.text.upper() and ch3_start is None:
        ch3_start = i
    elif "CHƯƠNG 4:" in p.text.upper() and ch4_start is None:
        ch4_start = i
        break

print(f"Found Chapter 3 at index {ch3_start}, Chapter 4 at index {ch4_start}")
p_target = doc.paragraphs[ch4_start]

# Load all 5 section data files
with open("chapter3_sec1.json", "r", encoding="utf-8") as f:
    sec1 = json.load(f)
with open("chapter3_sec2.json", "r", encoding="utf-8") as f:
    sec2 = json.load(f)
with open("chapter3_sec3.json", "r", encoding="utf-8") as f:
    sec3 = json.load(f)
with open("chapter3_sec4.json", "r", encoding="utf-8") as f:
    sec4 = json.load(f)
with open("chapter3_sec5.json", "r", encoding="utf-8") as f:
    sec5 = json.load(f)

# Insert Chapter 3 Heading 1
print("Inserting Chapter 3 Title and Section 3.1...")
add_h1(p_target, "CHƯƠNG 3: XÂY DỰNG WEBSITE THƯƠNG MẠI ĐIỆN TỬ VÀ THỰC NGHIỆM HỆ THỐNG PHÁT HIỆN, PHÒNG CHỐNG GIAN LẬN")

# SECTION 3.1
add_h2(p_target, sec1["title"])
add_p(p_target, sec1["intro"])
for sub in sec1["subsections"]:
    add_h3(p_target, sub["title"])
    for p_txt in sub.get("paragraphs", []):
        add_p(p_target, p_txt)
    for b_title, b_desc in sub.get("bullets", []):
        add_bullet(p_target, b_title, b_desc)

# SECTION 3.2
print("Inserting Section 3.2...")
add_h2(p_target, sec2["title"])
add_p(p_target, sec2["intro"])
for sub in sec2["subsections"]:
    add_h3(p_target, sub["title"])
    for p_txt in sub.get("paragraphs", []):
        add_p(p_target, p_txt)
    for b_title, b_desc in sub.get("bullets", []):
        add_bullet(p_target, b_title, b_desc)
    if "table" in sub:
        t = sub["table"]
        add_table_data(doc, p_target, t["headers"], t["rows"], t["widths"], t["caption"])

# SECTION 3.3
print("Inserting Section 3.3...")
add_h2(p_target, sec3["title"])
add_p(p_target, sec3["intro"])
for sub in sec3["subsections"]:
    add_h3(p_target, sub["title"])
    for p_txt in sub.get("paragraphs", []):
        add_p(p_target, p_txt)
    if "table_rules" in sub:
        t = sub["table_rules"]
        add_table_data(doc, p_target, t["headers"], t["rows"], t["widths"], t["caption"])
    for p_txt in sub.get("post_paragraphs", []):
        add_p(p_target, p_txt)
    if "table_decisions" in sub:
        t = sub["table_decisions"]
        add_table_data(doc, p_target, t["headers"], t["rows"], t["widths"], t["caption"])

# SECTION 3.4
print("Inserting Section 3.4 with 14 UI screenshots...")
add_h2(p_target, sec4["title"])
add_p(p_target, sec4["intro"])
for sub in sec4["subsections"]:
    add_h3(p_target, sub["title"])
    if "intro" in sub:
        add_p(p_target, sub["intro"])
    for fig in sub.get("figures", []):
        print(f"  Embedding Hình {fig['id']}: {fig['title']}")
        add_figure_item(p_target, fig["file"], fig["id"], fig["title"], fig["commentary"])

# SECTION 3.5
print("Inserting Section 3.5 with test scenarios and evaluation...")
add_h2(p_target, sec5["title"])
add_p(p_target, sec5["intro"])
for sub in sec5["subsections"]:
    add_h3(p_target, sub["title"])
    for p_txt in sub.get("paragraphs", []):
        add_p(p_target, p_txt)
    if "table" in sub:
        t = sub["table"]
        add_table_data(doc, p_target, t["headers"], t["rows"], t["widths"], t["caption"])
    if "table_confusion" in sub:
        t = sub["table_confusion"]
        add_table_data(doc, p_target, t["headers"], t["rows"], t["widths"], t["caption"])
    for p_txt in sub.get("post_paragraphs", []):
        add_p(p_target, p_txt)
    for p_txt in sub.get("post_conf_paragraphs", []):
        add_p(p_target, p_txt)
    if "table_metrics" in sub:
        t = sub["table_metrics"]
        add_table_data(doc, p_target, t["headers"], t["rows"], t["widths"], t["caption"])
    for p_txt in sub.get("final_paragraphs", []):
        add_p(p_target, p_txt)

# Spacing before Chapter 4
p_end = p_target.insert_paragraph_before()
p_end.paragraph_format.space_before = Pt(12)
p_end.paragraph_format.space_after = Pt(6)

print("Removing old placeholder paragraphs of Chapter 3...")
# Old paragraphs from ch3_start up to ch4_start
old_paragraphs = [doc.paragraphs[k] for k in range(ch3_start, ch4_start)]
for p in old_paragraphs:
    p._element.getparent().remove(p._element)

print(f"Saving final documents...")
print(f"  -> {OUT_LOCAL}")
doc.save(OUT_LOCAL)
print(f"  -> {OUT_DOWNLOAD}")
doc.save(OUT_DOWNLOAD)

print("SUCCESS: Complete report document successfully generated!")
