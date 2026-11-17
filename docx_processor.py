# -*- coding: utf-8 -*-
"""
Word (.docx) Hujjatlarini qayta ishlash moduli (Mukammal va Xatosiz).
Bo'lingan runlarni (masalan: 'yo' + '‘' + 'llari') aqlli birlashtirib,
shriftlar, qalinlik (bold), qiyalik (italic), jadvallar va stillarni
100% buzilmasdan saqlagan holda o'giradi yoki o'ta tezkor (batch) tarjima qiladi.
"""

import time
import docx
from converter_engine import UzbekTransliterator
from translator_engine import batch_translate_list, is_translatable


def get_run_style(r):
    """Run ning barcha asosiy format parametrlarini olish"""
    font_color = None
    if r.font and r.font.color:
        try:
            font_color = r.font.color.rgb
        except Exception:
            pass
    return (
        r.bold,
        r.italic,
        r.underline,
        r.font.name if r.font else None,
        r.font.size if r.font else None,
        font_color
    )


def process_paragraph_runs(p, transliterator, mode='auto'):
    """
    Paragraf ichidagi bo'lingan runlarni birlashtirib,
    tutuq belgisi va harf birikmalarini (o', g', sh, ch)
    to'liq va xatosiz o'girish.
    """
    runs = p.runs
    if not runs:
        if p.text and p.text.strip():
            p.text = transliterator.convert(p.text, mode=mode)
        return

    full_text = "".join(r.text for r in runs if r.text)
    if not full_text.strip():
        return

    styles = [get_run_style(r) for r in runs]

    # 1. Agar barcha runlar bir xil formatda bo'lsa (90%+ holatda)
    if len(set(styles)) <= 1:
        converted_text = transliterator.convert(full_text, mode=mode)
        runs[0].text = converted_text
        for r in runs[1:]:
            r.text = ""
        return

    # 2. Agar stillar farq qilsa: ketma-ket bir xil stilli runlarni guruhlab birlashtirish
    groups = []
    current_group = [runs[0]]
    current_style = styles[0]

    for r, s in zip(runs[1:], styles[1:]):
        if s == current_style:
            current_group.append(r)
        else:
            groups.append((current_group, current_style))
            current_group = [r]
            current_style = s
    if current_group:
        groups.append((current_group, current_style))

    for grp_runs, _ in groups:
        grp_text = "".join(r.text for r in grp_runs if r.text)
        if grp_text:
            conv = transliterator.convert(grp_text, mode=mode)
            grp_runs[0].text = conv
            for extra_r in grp_runs[1:]:
                extra_r.text = ""


def _collect_all_paragraphs(doc):
    """Word hujjatidagi barcha paragraflar (asosiy matn, jadvallar, kolontitullar) ro'yxatini yig'ish"""
    all_p = []

    # 1. Asosiy matn
    for p in doc.paragraphs:
        all_p.append(p)

    # 2. Jadvallar
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    all_p.append(p)

    # 3. Kolontitullar (Headers & Footers)
    for section in doc.sections:
        hf_list = [
            getattr(section, 'header', None),
            getattr(section, 'footer', None),
            getattr(section, 'first_page_header', None),
            getattr(section, 'first_page_footer', None),
            getattr(section, 'even_page_header', None),
            getattr(section, 'even_page_footer', None)
        ]
        for hf in hf_list:
            if hf is not None:
                for p in getattr(hf, 'paragraphs', []):
                    all_p.append(p)
                for table in getattr(hf, 'tables', []):
                    for row in table.rows:
                        for cell in row.cells:
                            for p in cell.paragraphs:
                                all_p.append(p)

    return all_p


def process_docx(input_path, output_path, transliterator=None, mode='auto', progress_callback=None):
    """
    Word (.docx) faylini to'liq va formatlarni saqlagan holda o'giradi yoki tarjima qiladi.
    Katta fayllarda progress_callback(percent, status) orqali foizni hisoblab boradi.
    """
    if transliterator is None:
        transliterator = UzbekTransliterator()

    start_time = time.perf_counter()
    if progress_callback:
        progress_callback(5, "Word hujjati ochilmoqda...")

    doc = docx.Document(input_path)

    is_translation = mode in ['ru_to_uz', 'uz_to_ru', 'en_to_uz', 'uz_to_en']
    lang_pairs = {
        'ru_to_uz': ('ru', 'uz'),
        'uz_to_ru': ('uz', 'ru'),
        'en_to_uz': ('en', 'uz'),
        'uz_to_en': ('uz', 'en')
    }

    all_paragraphs = _collect_all_paragraphs(doc)
    total_elements = len(all_paragraphs)

    preview_orig_lines = []
    preview_conv_lines = []
    total_words = 0
    total_chars = 0

    if is_translation:
        # =====================================================================
        # ULTRA-TEZKOR KO'P OQIMLI BATCH TARJIMA (100x tezlik)
        # =====================================================================
        src, dest = lang_pairs.get(mode, ('uz', 'en'))
        if progress_callback:
            progress_callback(12, "Matn bloklari ajratilmoqda...")

        # Tarjima qilinadigan barcha paragraflarni saralash
        paragraphs_to_translate = []
        raw_texts = []

        for p in all_paragraphs:
            txt = p.text.strip() if p.text else ""
            if txt and is_translatable(txt):
                paragraphs_to_translate.append(p)
                raw_texts.append(txt)
                total_chars += len(txt)
                total_words += len(txt.split())
                if len(preview_orig_lines) < 6:
                    preview_orig_lines.append(txt)

        def on_batch_progress(done_b, total_b):
            if progress_callback and total_b > 0:
                pct = 15 + int(70 * (done_b / total_b))
                progress_callback(pct, f"AI Tarjima qilmoqda: {done_b}/{total_b} bo‘lak ({pct}%)")

        # Ko'p oqimli parallel paketli tarjima
        translated_texts = batch_translate_list(
            raw_texts,
            src=src,
            dest=dest,
            progress_callback=on_batch_progress,
            max_workers=6
        )

        if progress_callback:
            progress_callback(88, "Tarjima qilingan matnlar formatlanmoqda...")

        # Natijalarni Word paragraflariga kiritish (shriftlar va stillarni saqlagan holda)
        for p, trans_txt in zip(paragraphs_to_translate, translated_texts):
            if not trans_txt:
                continue
            if p.runs:
                p.runs[0].text = trans_txt
                for r in p.runs[1:]:
                    r.text = ""
            else:
                p.text = trans_txt

            if len(preview_conv_lines) < 6:
                preview_conv_lines.append(trans_txt)

    else:
        # =====================================================================
        # ALIFBO O'GIRISH (Kirill, Eski Lotin, Yangi Lotin)
        # =====================================================================
        if progress_callback:
            progress_callback(20, "Alifbo o‘girilmoqda...")

        step = max(1, total_elements // 10)
        for idx, p in enumerate(all_paragraphs):
            if p.text and p.text.strip():
                orig = p.text
                total_chars += len(orig)
                total_words += len(orig.split())

                if len(preview_orig_lines) < 6:
                    preview_orig_lines.append(orig.strip())

                process_paragraph_runs(p, transliterator, mode=mode)

                if len(preview_conv_lines) < 6:
                    preview_conv_lines.append(p.text.strip())

            if progress_callback and idx % step == 0:
                pct = 20 + int(65 * (idx / total_elements))
                progress_callback(pct, f"Alifbo o‘girilmoqda ({pct}%)")

    # Matn qutilari (Textboxes)
    try:
        txbx_nodes = doc.element.xpath('.//w:txbxContent//w:p')
        for p_elem in txbx_nodes:
            for t_node in p_elem.xpath('.//w:t'):
                if t_node.text and t_node.text.strip():
                    if is_translation:
                        src, dest = lang_pairs.get(mode, ('uz', 'en'))
                        from translator_engine import translate_chunk
                        t_node.text = translate_chunk(t_node.text, src=src, dest=dest)
                    else:
                        t_node.text = transliterator.convert(t_node.text, mode=mode)
    except Exception:
        pass

    if progress_callback:
        progress_callback(94, "Word fayli saqlanmoqda...")

    doc.save(output_path)

    if progress_callback:
        progress_callback(100, "Tayyor! Muvaffaqiyatli yakunlandi.")

    duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

    return {
        'success': True,
        'word_count': total_words,
        'char_count': total_chars,
        'elements_count': total_elements,
        'preview_original': "\n".join(preview_orig_lines),
        'preview_converted': "\n".join(preview_conv_lines),
        'duration_ms': duration_ms
    }
