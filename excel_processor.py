# -*- coding: utf-8 -*-
"""
Excel (.xlsx, .xls) Fayllarini qayta ishlash moduli.
Barcha varaqlar (Sheets), kataklar (Cells), formulalar, raqamlar,
shriftlar va ranglarni 100% buzmasdan Yangi Lotinga o'giradi yoki
ko'p oqimli (batch) tarjima qiladi.
"""

import os
import time
import openpyxl
import xlrd
from converter_engine import UzbekTransliterator
from translator_engine import batch_translate_list, is_translatable


def process_xlsx(input_path, output_path, transliterator=None, mode='auto', progress_callback=None):
    """
    .xlsx faylini formatlarini saqlagan holda o'giradi yoki tarjima qiladi.
    """
    if transliterator is None:
        transliterator = UzbekTransliterator()

    start_time = time.perf_counter()
    if progress_callback:
        progress_callback(5, "Excel hujjati ochilmoqda...")

    wb = openpyxl.load_workbook(input_path, data_only=False)

    is_translation = mode in ['ru_to_uz', 'uz_to_ru', 'en_to_uz', 'uz_to_en']
    lang_pairs = {
        'ru_to_uz': ('ru', 'uz'),
        'uz_to_ru': ('uz', 'ru'),
        'en_to_uz': ('en', 'uz'),
        'uz_to_en': ('uz', 'en')
    }

    total_words = 0
    total_chars = 0
    total_cells = 0
    preview_orig = []
    preview_conv = []

    # Barcha kataklarni saralash
    cells_to_process = []
    raw_texts = []

    for sheet in wb.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if isinstance(cell.value, str):
                    val = cell.value.strip()
                    if not val or val.startswith('='):
                        continue
                    total_cells += 1
                    total_chars += len(val)
                    total_words += len(val.split())
                    cells_to_process.append((sheet, cell, cell.value))
                    raw_texts.append(cell.value)

    if is_translation:
        src, dest = lang_pairs.get(mode, ('uz', 'en'))
        if progress_callback:
            progress_callback(15, "Excel matnlari tarjimaga tayyorlanmoqda...")

        def on_batch_prog(done_b, total_b):
            if progress_callback and total_b > 0:
                pct = 20 + int(65 * (done_b / total_b))
                progress_callback(pct, f"AI Kataklarni tarjima qilmoqda: {done_b}/{total_b} ({pct}%)")

        translated_texts = batch_translate_list(
            raw_texts,
            src=src,
            dest=dest,
            progress_callback=on_batch_prog,
            max_workers=6
        )

        for (sheet, cell, orig_val), trans_val in zip(cells_to_process, translated_texts):
            cell.value = trans_val
            if len(preview_orig) < 6 and orig_val:
                preview_orig.append(f"[{sheet.title} {cell.coordinate}]: {orig_val}")
            if len(preview_conv) < 6 and trans_val:
                preview_conv.append(f"[{sheet.title} {cell.coordinate}]: {trans_val}")

    else:
        # Transliteratsiya
        if progress_callback:
            progress_callback(25, "Excel kataklari yangi alifboga o‘girilmoqda...")

        step = max(1, len(cells_to_process) // 10) if cells_to_process else 1
        for idx, (sheet, cell, orig_val) in enumerate(cells_to_process):
            conv_val = transliterator.convert(orig_val, mode=mode)
            cell.value = conv_val

            if len(preview_orig) < 6:
                preview_orig.append(f"[{sheet.title} {cell.coordinate}]: {orig_val}")
            if len(preview_conv) < 6:
                preview_conv.append(f"[{sheet.title} {cell.coordinate}]: {conv_val}")

            if progress_callback and idx % step == 0:
                pct = 25 + int(60 * (idx / max(1, len(cells_to_process))))
                progress_callback(pct, f"Alifbo o‘girilmoqda ({pct}%)")

    if progress_callback:
        progress_callback(92, "Excel fayli saqlanmoqda...")

    wb.save(output_path)

    if progress_callback:
        progress_callback(100, "Tayyor! Muvaffaqiyatli yakunlandi.")

    duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

    return {
        'success': True,
        'word_count': total_words,
        'char_count': total_chars,
        'cells_count': total_cells,
        'preview_original': "\n".join(preview_orig),
        'preview_converted': "\n".join(preview_conv),
        'duration_ms': duration_ms
    }


def process_xls(input_path, output_path, transliterator=None, mode='auto', progress_callback=None):
    """
    Eski formatdagi .xls faylini o'qib, yangi .xlsx formatiga o'giradi yoki tarjima qiladi.
    """
    if transliterator is None:
        transliterator = UzbekTransliterator()

    start_time = time.perf_counter()
    if progress_callback:
        progress_callback(5, ".xls fayli ochilmoqda...")

    rb = xlrd.open_workbook(input_path)
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    total_words = 0
    total_chars = 0
    total_cells = 0
    preview_orig = []
    preview_conv = []

    for sheet_idx in range(rb.nsheets):
        rsheet = rb.sheet_by_index(sheet_idx)
        sheet_title = transliterator.convert(rsheet.name, mode=mode)
        ws = wb.create_sheet(title=sheet_title)

        for r_idx in range(rsheet.nrows):
            for c_idx in range(rsheet.ncols):
                cell_val = rsheet.cell_value(r_idx, c_idx)
                if isinstance(cell_val, str):
                    val = cell_val.strip()
                    total_cells += 1
                    total_chars += len(val)
                    total_words += len(val.split())

                    if len(preview_orig) < 6 and val:
                        preview_orig.append(f"[{sheet_title} R{r_idx+1}C{c_idx+1}]: {val}")

                    converted_val = transliterator.convert(cell_val, mode=mode)
                    ws.cell(row=r_idx + 1, column=c_idx + 1, value=converted_val)

                    if len(preview_conv) < 6 and val:
                        preview_conv.append(f"[{sheet_title} R{r_idx+1}C{c_idx+1}]: {converted_val}")
                else:
                    ws.cell(row=r_idx + 1, column=c_idx + 1, value=cell_val)

    if not output_path.endswith('.xlsx'):
        output_path = os.path.splitext(output_path)[0] + '.xlsx'

    if progress_callback:
        progress_callback(92, "Fayl saqlanmoqda...")

    wb.save(output_path)

    if progress_callback:
        progress_callback(100, "Tayyor! Muvaffaqiyatli yakunlandi.")

    duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

    return {
        'success': True,
        'word_count': total_words,
        'char_count': total_chars,
        'cells_count': total_cells,
        'output_path': output_path,
        'preview_original': "\n".join(preview_orig),
        'preview_converted': "\n".join(preview_conv),
        'duration_ms': duration_ms
    }


def process_excel(input_path, output_path, transliterator=None, mode='auto', progress_callback=None):
    """Fayl kengaytmasiga qarab tegishli o'giruvchini chaqiradi"""
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.xlsx':
        return process_xlsx(input_path, output_path, transliterator=transliterator, mode=mode, progress_callback=progress_callback)
    elif ext == '.xls':
        return process_xls(input_path, output_path, transliterator=transliterator, mode=mode, progress_callback=progress_callback)
    else:
        raise ValueError(f"Qo'llab-quvvatlanmaydigan Excel formati: {ext}")
