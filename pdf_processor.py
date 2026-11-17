# -*- coding: utf-8 -*-
"""
PDF Fayllarini Word (.docx) formatiga xatosiz va toza o'tkazish moduli.
1. pdf2docx orqali to'liq jadvallar, sarlavha va rasmlarni saqlash
2. Post-processing: null baytlar (\x00), buzilgan shrift belgilari (», £, `)
   va qatorlar bir-biriga minishini to'liq tozalash
3. Buzilmaydigan toza oqim (Clean Flow Mode) fallback
"""

import os
import re
import time
import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_LINE_SPACING
from pdf2docx import Converter
import fitz  # PyMuPDF

# =========================================================================
# SMART PDF PATCH: Prevent rasterized SVG bitmaps from overlapping real text
# In invoices and styled PDFs, vector shapes/backgrounds around text are
# clipped as bitmap images by default. Filtering out bitmaps that contain
# text characters prevents duplicate text and unreadable overlaps.
# =========================================================================
try:
    from pdf2docx.page.RawPageFitz import RawPageFitz
    _orig_preprocess_shapes = RawPageFitz._preprocess_shapes

    def _safe_preprocess_shapes(self, **settings):
        paths = self._init_paths(**settings)
        shapes, images = paths.to_shapes_and_images(
            settings['min_svg_gap_dx'], 
            settings['min_svg_gap_dy'], 
            settings['min_svg_w'], 
            settings['min_svg_h'], 
            settings['clip_image_res_ratio']
        )
        filtered_images = []
        for img in images:
            bbox = fitz.Rect(img.get('bbox', [0, 0, 0, 0]))
            text_inside = self.page_engine.get_text('text', clip=bbox).strip()
            # If bitmap contains text, discard it so Word only receives the editable text
            if not text_inside:
                filtered_images.append(img)
        return shapes, filtered_images

    RawPageFitz._preprocess_shapes = _safe_preprocess_shapes
except Exception as patch_err:
    print("PDF smart patch notice:", patch_err)


def sanitize_docx_text(docx_path):
    """
    Word hujjatidagi buzilgan PDF shrift belgilarini tozalash
    va qatorlar minishini bartaraf etish
    """
    try:
        doc = docx.Document(docx_path)
        char_cleanup = {
            '\x00': '',
            '»': '‘',
            '«': '‘',
            '£': 'g‘',
            '`': '‘',
            '´': '‘',
            '’': '‘',
            'ʻ': '‘'
        }

        # 1. Paragraflarni tozalash
        for p in doc.paragraphs:
            if p.runs:
                for r in p.runs:
                    if r.text:
                        rt = r.text
                        for bad_char, good_char in char_cleanup.items():
                            rt = rt.replace(bad_char, good_char)
                        r.text = rt
            elif p.text:
                new_text = p.text
                for bad_char, good_char in char_cleanup.items():
                    new_text = new_text.replace(bad_char, good_char)
                p.text = new_text

            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(4)

        # 2. Jadvallarni tozalash
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        if p.runs:
                            for r in p.runs:
                                if r.text:
                                    rt = r.text
                                    for bad_char, good_char in char_cleanup.items():
                                        rt = rt.replace(bad_char, good_char)
                                    r.text = rt
                        elif p.text:
                            new_text = p.text
                            for bad_char, good_char in char_cleanup.items():
                                new_text = new_text.replace(bad_char, good_char)
                            p.text = new_text
                        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
                pass
        doc.save(docx_path)
    except Exception as e:
        print("Sanitize docx error:", e)


def convert_pdf_clean_flow(input_pdf_path, output_docx_path):
    """
    PyMuPDF orqali matn va jadvallarni oqim bo'yicha (Clean Flow) Wordga o'tkazish.
    Bu usulda hech qanday floating qutilar yoki ustma-ust tushishlar bo'lmaydi.
    """
    pdf_doc = fitz.open(input_pdf_path)
    doc = docx.Document()

    # Sahifa chekka masofalarini sozlash
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    for page_num in range(len(pdf_doc)):
        page = pdf_doc[page_num]
        blocks = page.get_text('blocks')
        
        # Bloklarni vertikal (y0) bo'yicha tartiblash
        blocks.sort(key=lambda b: (b[1], b[0]))

        for b in blocks:
            b_text = b[4].strip()
            if not b_text:
                continue

            # Tozalash
            b_text = b_text.replace('\x00', '').replace('»', '‘').replace('£', 'g‘').replace('`', '‘')

            lines = [l.strip() for l in b_text.split('\n') if l.strip()]
            for line in lines:
                p = doc.add_paragraph()
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(3)
                run = p.add_run(line)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(11)

        # Sahifalar orasiga bo'linma qo'shish (oxirgisidan tashqari)
        if page_num < len(pdf_doc) - 1:
            doc.add_page_break()

    pdf_doc.close()
    doc.save(output_docx_path)


def convert_pdf_to_docx(input_pdf_path, output_docx_path, progress_callback=None):
    """
    PDF faylni Word (.docx) formatiga xatosiz aylantiradi.
    Avval pdf2docx orqali to'liq struktura o'tkaziladi va xatolari tozalanadi.
    Agar kutilmagan xatolik yuz bersa, toza oqim (Clean Flow) orqali saqlanadi.
    """
    start_time = time.perf_counter()

    if not os.path.exists(input_pdf_path):
        raise FileNotFoundError(f"PDF fayl topilmadi: {input_pdf_path}")

    if progress_callback:
        progress_callback(10, "PDF fayli tahlil qilinmoqda...")

    pages_count = 1
    try:
        # 1-usul: pdf2docx (multi_processing=False Windows uchun eng xavfsiz va aniq)
        cv = Converter(input_pdf_path)
        pages_count = len(cv.pages)
        if progress_callback:
            progress_callback(35, f"PDF sahifalari ({pages_count} bet) Wordga o‘tkazilmoqda...")

        cv.convert(output_docx_path, multi_processing=False)
        cv.close()

        if progress_callback:
            progress_callback(85, "Word jadvallari va shriftlari tozalanmoqda...")

        # Hosil bo'lgan Word faylni tozalash (null baytlar, buzilgan apostroflar, qator oralig'i)
        sanitize_docx_text(output_docx_path)

    except Exception as e:
        print("pdf2docx fallback to clean flow:", e)
        # 2-usul (Fallback): PyMuPDF Clean Flow
        convert_pdf_clean_flow(input_pdf_path, output_docx_path)
        sanitize_docx_text(output_docx_path)

    duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

    return {
        'success': True,
        'output_path': output_docx_path,
        'duration_ms': duration_ms,
        'pages_count': pages_count
    }
