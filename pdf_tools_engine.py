# -*- coding: utf-8 -*-
"""
PDF Asboblari Majmuasi (PDF Studio Engine)
Muallif: Ismoilov Nodir
Funksiyalar:
- Merge (Birlashtirish)
- Split (Ajratish / Kesish)
- Compress (Siqish / Hajmni kamaytirish)
- Word to PDF (.docx, .doc -> .pdf)
- Excel to PDF (.xlsx, .xls -> .pdf)
- PowerPoint to PDF (.pptx, .ppt -> .pdf)
- PDF to Excel (.pdf -> .xlsx jadvallar)
- PDF to Images (.pdf -> .zip ichida PNG/JPG)
- Images to PDF (JPG/PNG -> .pdf)
- Rotate PDF (Sahifalarni 90, 180, 270 burish)
- Watermark (Matnli suv belgisi qo'yish)
- Page Numbers (Sahifa raqamlarini qo'yish)
- Protect PDF (Parol bilan himoyalash)
- Unlock PDF (Parolni yechish)
"""

import os
import io
import re
import time
import zipfile
import fitz  # PyMuPDF
import openpyxl
from PIL import Image

# Windows COM for Office documents
try:
    import pythoncom
    import win32com.client
    HAS_WIN32COM = True
except Exception:
    HAS_WIN32COM = False


def parse_page_range(range_str, total_pages):
    """
    Sahifalar oralig'ini parsing qilish: masalan "1-3, 5, 7-9" -> [0, 1, 2, 4, 6, 7, 8] (0-indexed)
    """
    if not range_str or range_str.strip().lower() in ['all', 'barchasi', 'все']:
        return list(range(total_pages))
    
    selected = set()
    parts = range_str.replace(';', ',').split(',')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            sub = part.split('-')
            if len(sub) == 2 and sub[0].strip().isdigit() and sub[1].strip().isdigit():
                start = max(1, int(sub[0].strip()))
                end = min(total_pages, int(sub[1].strip()))
                for p in range(start, end + 1):
                    selected.add(p - 1)
        elif part.isdigit():
            p = int(part)
            if 1 <= p <= total_pages:
                selected.add(p - 1)
                
    result = sorted(list(selected))
    return result if result else list(range(total_pages))


# ==============================================================================
# 1. MERGE PDF (Birlashtirish)
# ==============================================================================
def merge_pdfs(file_paths, output_path, progress_callback=None):
    """Bir nechta PDF fayllarni bitta yaxlit PDF hujjatga birlashtirish"""
    if progress_callback: progress_callback(10, "PDF fayllar tayyorlanmoqda...")
    merged_doc = fitz.open()
    total_files = len(file_paths)
    
    for idx, fpath in enumerate(file_paths, 1):
        if os.path.exists(fpath):
            src_doc = fitz.open(fpath)
            merged_doc.insert_pdf(src_doc)
            src_doc.close()
        if progress_callback:
            pct = 10 + int(70 * (idx / max(1, total_files)))
            progress_callback(pct, f"Birlashtirilmoqda: {idx}/{total_files}...")
            
    if progress_callback: progress_callback(85, "Yaxlit PDF fayl saqlanmoqda...")
    merged_doc.save(output_path, garbage=4, deflate=True)
    page_count = len(merged_doc)
    merged_doc.close()
    if progress_callback: progress_callback(100, "Tayyor! PDF lar birlashtirildi.")
    
    return {
        'success': True,
        'page_count': page_count,
        'file_count': total_files,
        'output_size': os.path.getsize(output_path)
    }


# ==============================================================================
# 2. SPLIT PDF (Ajratish / Kesish - barcha sahifalarni ZIP arxivda berish)
# ==============================================================================
def split_pdf(input_path, output_path, page_range_str="har_biri", progress_callback=None):
    """
    PDF fayldan sahifalarni ajratib, har bir sahifani alohida PDF qilib
    bitta ZIP arxiv faylga joylaydi.
    """
    if progress_callback: progress_callback(10, "PDF sahifalari tahlil qilinmoqda...")
    doc = fitz.open(input_path)
    total_pages = len(doc)
    
    # Chiqish fayli doimo .zip bo'lishini ta'minlash
    base_no_ext = os.path.splitext(output_path)[0]
    zip_output = base_no_ext + ".zip"
    
    clean_range = str(page_range_str).strip().lower()
    if clean_range in ['har_biri', 'all', 'barchasi', 'each', 'alohida', 'каждая', '']:
        indices = list(range(total_pages))
    else:
        indices = parse_page_range(clean_range, total_pages)
        if not indices:
            indices = list(range(total_pages))
            
    total_to_split = len(indices)
    if progress_callback: progress_callback(20, f"{total_to_split} ta sahifa alohida PDF larga ajratilmoqda...")
    
    with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zf:
        for step, idx in enumerate(indices, 1):
            sub_doc = fitz.open()
            sub_doc.insert_pdf(doc, from_page=idx, to_page=idx)
            pdf_bytes = sub_doc.tobytes(deflate=True, garbage=3)
            sub_doc.close()
            zf.writestr(f"sahifa_{idx+1}.pdf", pdf_bytes)
            
            if progress_callback:
                pct = 20 + int(75 * (step / max(1, total_to_split)))
                progress_callback(pct, f"Sahifa ajratilmoqda: {step}/{total_to_split} (sahifa {idx+1})...")
                
    doc.close()
    if progress_callback: progress_callback(100, f"Tayyor! {total_to_split} ta sahifa ZIP arxivga joylandi.")
    
    return {
        'success': True,
        'page_count': total_to_split,
        'pages_count': total_to_split,
        'output_path': zip_output,
        'is_zip': True
    }


# ==============================================================================
# 3. COMPRESS PDF (Siqish / Hajmni MB lardan sezilarli kamaytirish)
# ==============================================================================
def compress_pdf(input_path, output_path, level="medium", progress_callback=None):
    """
    PDF faylni sifatini saqlagan holda kuchli siqish (hajmini MB larni kamaytirish).
    level: 'extreme' (yuqori siquv), 'medium' (standart, sifatli), 'light' (yengil)
    """
    orig_size = os.path.getsize(input_path)
    if progress_callback: progress_callback(10, "PDF tarkibi va grafikasi tahlil qilinmoqda...")
    
    doc = fitz.open(input_path)
    total_pages = len(doc)
    
    # Har bir rejim uchun siquv parametrlari
    if level == 'extreme':
        max_dim = 900
        quality = 48
        scale_limit = 0.50
    elif level == 'light':
        max_dim = 1800
        quality = 78
        scale_limit = 0.85
    else:  # medium (standart)
        max_dim = 1300
        quality = 65
        scale_limit = 0.70
        
    processed_xrefs = set()
    total_images_found = 0
    
    for i, page in enumerate(doc, 1):
        image_list = page.get_images(full=True)
        for img_info in image_list:
            xref = img_info[0]
            if xref in processed_xrefs:
                continue
            processed_xrefs.add(xref)
            total_images_found += 1
            
            try:
                base_image = doc.extract_image(xref)
                if not base_image:
                    continue
                raw_bytes = base_image["image"]
                pil_img = Image.open(io.BytesIO(raw_bytes))
                
                # RGB ga o'tkazish (JPEG faqat RGB qabul qiladi)
                if pil_img.mode in ['RGBA', 'P', 'LA']:
                    pil_img = pil_img.convert('RGB')
                    
                w, h = pil_img.size
                # Agar rasm katta bo'lsa, mos ravishda kichraytirish
                if w > max_dim or h > max_dim:
                    scale = min(max_dim / max(1, w), max_dim / max(1, h))
                    new_w = max(100, int(w * scale))
                    new_h = max(100, int(h * scale))
                    pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                elif level == 'extreme' and (w > 600 or h > 600):
                    new_w = int(w * scale_limit)
                    new_h = int(h * scale_limit)
                    pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    
                buf = io.BytesIO()
                pil_img.save(buf, format='JPEG', quality=quality, optimize=True)
                new_bytes = buf.getvalue()
                
                # Agar yangi rasm hajmi kichikroq bo'lsa, sahifadagi rasmni almashtiramiz
                if len(new_bytes) < len(raw_bytes):
                    page.replace_image(xref, stream=new_bytes)
            except Exception:
                pass
                
        if progress_callback:
            pct = 15 + int(70 * (i / max(1, total_pages)))
            progress_callback(pct, f"Optimizatsiya qilinmoqda: {i}/{total_pages} bet...")
            
    if progress_callback: progress_callback(88, "Siqilgan PDF saqlanmoqda...")
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    
    new_size = os.path.getsize(output_path)
    
    # Agar fayl qandaydir sabab bilan kattalashgan bo'lsa (masalan, allaqachon siqilgan bo'lsa)
    if new_size > orig_size:
        import shutil
        shutil.copy2(input_path, output_path)
        new_size = os.path.getsize(output_path)
        
    saved_bytes = max(0, orig_size - new_size)
    saved_percent = round((saved_bytes / max(1, orig_size)) * 100, 1)
    
    if progress_callback: progress_callback(100, f"Tayyor! Hajmi {saved_percent}% ga kamaytirildi.")
    
    return {
        'success': True,
        'orig_size': orig_size,
        'new_size': new_size,
        'saved_percent': saved_percent,
        'pages_count': total_pages,
        'page_count': total_pages
    }


# ==============================================================================
# 4. ROTATE PDF (Sahifalarni burish)
# ==============================================================================
def rotate_pdf(input_path, output_path, angle=90, page_range_str="all", progress_callback=None):
    """PDF sahifalarini 90, 180 yoki 270 darajaga burish"""
    if progress_callback: progress_callback(20, "PDF yuklanmoqda...")
    doc = fitz.open(input_path)
    total_pages = len(doc)
    indices = parse_page_range(page_range_str, total_pages)
    
    angle = int(angle) % 360
    if angle not in [90, 180, 270]:
        angle = 90
        
    for idx in indices:
        page = doc[idx]
        cur_rot = page.rotation
        page.set_rotation((cur_rot + angle) % 360)
        
    if progress_callback: progress_callback(80, "Burilgan sahifalar saqlanmoqda...")
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    if progress_callback: progress_callback(100, "Tayyor! Sahifalar burildi.")
    
    return {'success': True, 'pages_rotated': len(indices), 'angle': angle}


# ==============================================================================
# 5. WATERMARK PDF (Matnli suv belgisi qo'yish)
# ==============================================================================
def watermark_pdf(input_path, output_path, watermark_text="KONFIDENSIAL", fontsize=38, opacity=0.35, progress_callback=None):
    """PDF sahifalariga diagonal matnli suv belgisi tushirish"""
    if progress_callback: progress_callback(20, "Suv belgisi tayyorlanmoqda...")
    doc = fitz.open(input_path)
    total_pages = len(doc)
    
    # Rangni kulrang-shaffof qilish
    c_val = 0.65
    font_size = int(fontsize) if fontsize else 38
    
    for i, page in enumerate(doc, 1):
        rect = page.rect
        center_x = rect.width / 2.0
        center_y = rect.height / 2.0
        
        # Matn uzunligini hisoblab markazga joylash
        p = fitz.Point(center_x - (len(watermark_text) * font_size * 0.25), center_y + (font_size * 0.35))
        # 45 daraja burchak ostida markazdan o'tkazish
        page.insert_text(p, watermark_text, fontsize=font_size, color=(c_val, c_val, c_val), morph=(p, fitz.Matrix(45)))
        
        if progress_callback:
            pct = 20 + int(65 * (i / total_pages))
            progress_callback(pct, f"Suv belgisi qo‘yilmoqda: {i}/{total_pages} bet...")
            
    if progress_callback: progress_callback(90, "Fayl saqlanmoqda...")
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    if progress_callback: progress_callback(100, "Tayyor! Suv belgisi muvaffaqiyatli qo‘yildi.")
    
    return {'success': True, 'pages_count': total_pages, 'watermark_text': watermark_text}


# ==============================================================================
# 6. PAGE NUMBERS (Sahifa raqamlarini qo'yish)
# ==============================================================================
def page_numbers_pdf(input_path, output_path, position="bottom-right", format_str="Sahifa {n} / {total}", progress_callback=None):
    """PDF sahifalarining ostki yoki ustki qismiga sahifa raqamlarini qo'yish"""
    if progress_callback: progress_callback(20, "Sahifalar raqamlanmoqda...")
    doc = fitz.open(input_path)
    total_pages = len(doc)
    
    for idx, page in enumerate(doc, 1):
        rect = page.rect
        num_text = format_str.replace("{n}", str(idx)).replace("{total}", str(total_pages))
        
        if position == 'bottom-center':
            tb_rect = fitz.Rect(rect.width / 2 - 120, rect.height - 35, rect.width / 2 + 120, rect.height - 15)
            align = fitz.TEXT_ALIGN_CENTER
        elif position == 'bottom-left':
            tb_rect = fitz.Rect(35, rect.height - 35, 235, rect.height - 15)
            align = fitz.TEXT_ALIGN_LEFT
        elif position == 'top-right':
            tb_rect = fitz.Rect(rect.width - 235, 15, rect.width - 35, 35)
            align = fitz.TEXT_ALIGN_RIGHT
        else:  # bottom-right (standart)
            tb_rect = fitz.Rect(rect.width - 235, rect.height - 35, rect.width - 35, rect.height - 15)
            align = fitz.TEXT_ALIGN_RIGHT
            
        page.insert_textbox(tb_rect, num_text, fontsize=10, color=(0.35, 0.35, 0.35), align=align)
        
    if progress_callback: progress_callback(90, "Raqamlangan PDF saqlanmoqda...")
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    if progress_callback: progress_callback(100, "Tayyor! Sahifalar raqamlandi.")
    
    return {'success': True, 'pages_count': total_pages}


# ==============================================================================
# 7. PROTECT PDF (Parol qo'yish)
# ==============================================================================
def protect_pdf(input_path, output_path, password, progress_callback=None):
    """PDF faylni parol bilan AES-256 shifrlash"""
    if not password:
        raise ValueError("Parol kiritilmadi!")
        
    if progress_callback: progress_callback(30, "PDF shifrlanmoqda...")
    doc = fitz.open(input_path)
    pages_count = len(doc)
    
    # AES-256 bilan himoyalash
    doc.save(
        output_path,
        encryption=fitz.PDF_ENCRYPT_AES_256,
        user_pw=password,
        owner_pw=password + "_admin"
    )
    doc.close()
    if progress_callback: progress_callback(100, "Tayyor! PDF parol bilan himoyalandi.")
    return {'success': True, 'pages_count': pages_count}


# ==============================================================================
# 8. UNLOCK PDF (Parolni yechish)
# ==============================================================================
def unlock_pdf(input_path, output_path, password="", progress_callback=None):
    """Parolli PDF faylning parolini tekshirib, himoyasini olib tashlash"""
    if progress_callback: progress_callback(20, "Parol tekshirilmoqda...")
    doc = fitz.open(input_path)
    
    if doc.is_encrypted:
        auth_success = doc.authenticate(password)
        if not auth_success:
            doc.close()
            raise ValueError("Kiritilgan parol noto‘g‘ri!")
            
    if progress_callback: progress_callback(60, "Himoyasiz PDF nusxasi yaratilmoqda...")
    new_doc = fitz.open()
    new_doc.insert_pdf(doc)
    new_doc.save(output_path, garbage=4, deflate=True)
    pages_count = len(new_doc)
    new_doc.close()
    doc.close()
    
    if progress_callback: progress_callback(100, "Tayyor! PDF himoyasi olib tashlandi.")
    return {'success': True, 'pages_count': pages_count}


# ==============================================================================
# 9. PDF TO IMAGES (PDF -> Rasmlar ZIP)
# ==============================================================================
def pdf_to_images(input_path, output_zip_path, dpi=150, img_format="png", progress_callback=None):
    """PDF ning barcha sahifalarini rasm qilib ZIP arxivga joylash"""
    if progress_callback: progress_callback(10, "PDF sahifalari rasmga aylantirilmoqda...")
    doc = fitz.open(input_path)
    total_pages = len(doc)
    
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for i, page in enumerate(doc, 1):
            pix = page.get_pixmap(dpi=dpi)
            img_bytes = pix.tobytes(img_format.lower())
            zf.writestr(f"sahifa_{i}.{img_format.lower()}", img_bytes)
            if progress_callback:
                pct = 10 + int(80 * (i / total_pages))
                progress_callback(pct, f"Rasm tayyorlanmoqda: {i}/{total_pages} bet...")
                
    doc.close()
    if progress_callback: progress_callback(100, "Tayyor! Barcha sahifalar rasmga o‘tkazildi.")
    return {'success': True, 'pages_count': total_pages, 'zip_size': os.path.getsize(output_zip_path)}


# ==============================================================================
# 10. IMAGES TO PDF (Rasmlar -> PDF)
# ==============================================================================
def images_to_pdf(image_paths, output_path, progress_callback=None):
    """Bir yoki bir nechta JPG/PNG/WebP/BMP rasmlarni bitta sifatli PDF kitobga aylantirish"""
    if progress_callback: progress_callback(10, "Rasmlar tahlil qilinmoqda...")
    pdf_doc = fitz.open()
    total_imgs = len(image_paths)
    
    for idx, img_p in enumerate(image_paths, 1):
        if os.path.exists(img_p):
            added = False
            # 1. Tezkor PyMuPDF orqali urinish
            try:
                img = fitz.open(img_p)
                pdf_bytes = img.convert_to_pdf()
                img.close()
                img_pdf = fitz.open("pdf", pdf_bytes)
                pdf_doc.insert_pdf(img_pdf)
                img_pdf.close()
                added = True
            except Exception:
                pass
                
            # 2. Agar o'xshamasa (masalan, WebP yoki maxsus PNG), PIL orqali konvertatsiya qilish
            if not added:
                try:
                    pil_img = Image.open(img_p)
                    if pil_img.mode in ['RGBA', 'P', 'LA']:
                        pil_img = pil_img.convert('RGB')
                    buf = io.BytesIO()
                    pil_img.save(buf, format='JPEG', quality=95, optimize=True)
                    img_f = fitz.open("jpeg", buf.getvalue())
                    img_pdf = fitz.open("pdf", img_f.convert_to_pdf())
                    pdf_doc.insert_pdf(img_pdf)
                    img_pdf.close()
                    img_f.close()
                    added = True
                except Exception as ex:
                    print(f"Rasm yuklashda xatolik ({img_p}): {ex}")
                    
        if progress_callback:
            pct = 10 + int(75 * (idx / max(1, total_imgs)))
            progress_callback(pct, f"Rasm PDF ga qo‘shilmoqda: {idx}/{total_imgs}...")
            
    pages_count = len(pdf_doc)
    if pages_count == 0:
        pdf_doc.close()
        raise ValueError("Tanlangan rasmlarni PDF ga aylantirib bo‘lmadi! Fayllar buzilgan yoki mos kelmadi.")
        
    if progress_callback: progress_callback(90, "PDF fayl saqlanmoqda...")
    pdf_doc.save(output_path, garbage=4, deflate=True)
    pdf_doc.close()
    if progress_callback: progress_callback(100, f"Tayyor! {pages_count} ta rasm PDF hujjatga aylantirildi.")
    
    return {
        'success': True,
        'pages_count': pages_count,
        'page_count': pages_count
    }


# ==============================================================================
# 11. WORD TO PDF (Word -> PDF)
# ==============================================================================
def word_to_pdf(input_path, output_path, progress_callback=None):
    """Word (.docx, .doc) hujjatini 100% original ko'rinishida sifatli PDF qilish"""
    if progress_callback: progress_callback(20, "Microsoft Word ishga tushirilmoqda...")
    abs_in = os.path.abspath(input_path)
    abs_out = os.path.abspath(output_path)
    
    if HAS_WIN32COM:
        pythoncom.CoInitialize()
        word_app = win32com.client.Dispatch("Word.Application")
        word_app.Visible = False
        try:
            if progress_callback: progress_callback(45, "Hujjat PDF formatiga eksport qilinmoqda...")
            doc_file = word_app.Documents.Open(abs_in)
            # 17 = wdFormatPDF
            doc_file.SaveAs2(abs_out, FileFormat=17)
            doc_file.Close()
            word_app.Quit()
        except Exception as e:
            try: word_app.Quit()
            except Exception: pass
            raise e
    else:
        # Fallback if no win32com
        raise RuntimeError("Windows Word komponenti mavjud emas!")
        
    if progress_callback: progress_callback(100, "Tayyor! Word hujjati PDF ga o‘tkazildi.")
    return {'success': True, 'output_size': os.path.getsize(output_path)}


# ==============================================================================
# 12. EXCEL TO PDF (Excel -> PDF)
# ==============================================================================
def excel_to_pdf(input_path, output_path, progress_callback=None):
    """Excel (.xlsx, .xls) jadvallarini sifatli PDF ga aylantirish"""
    if progress_callback: progress_callback(20, "Microsoft Excel ishga tushirilmoqda...")
    abs_in = os.path.abspath(input_path)
    abs_out = os.path.abspath(output_path)
    
    if HAS_WIN32COM:
        pythoncom.CoInitialize()
        excel_app = win32com.client.Dispatch("Excel.Application")
        excel_app.Visible = False
        try:
            if progress_callback: progress_callback(45, "Jadval PDF formatiga eksport qilinmoqda...")
            wb = excel_app.Workbooks.Open(abs_in)
            # 0 = xlTypePDF
            wb.ExportAsFixedFormat(0, abs_out)
            wb.Close(False)
            excel_app.Quit()
        except Exception as e:
            try: excel_app.Quit()
            except Exception: pass
            raise e
    else:
        raise RuntimeError("Windows Excel komponenti mavjud emas!")
        
    if progress_callback: progress_callback(100, "Tayyor! Excel jadvali PDF ga o‘tkazildi.")
    return {'success': True, 'output_size': os.path.getsize(output_path)}


# ==============================================================================
# 13. POWERPOINT TO PDF (PowerPoint -> PDF)
# ==============================================================================
def powerpoint_to_pdf(input_path, output_path, progress_callback=None):
    """PowerPoint (.pptx, .ppt) taqdimotlarini sifatli PDF ga aylantirish"""
    if progress_callback: progress_callback(20, "PowerPoint ishga tushirilmoqda...")
    abs_in = os.path.abspath(input_path)
    abs_out = os.path.abspath(output_path)
    
    if HAS_WIN32COM:
        pythoncom.CoInitialize()
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        try:
            if progress_callback: progress_callback(45, "Slaydlar PDF formatiga eksport qilinmoqda...")
            prs = ppt_app.Presentations.Open(abs_in, WithWindow=False)
            # 32 = ppSaveAsPDF
            prs.SaveAs(abs_out, 32)
            prs.Close()
            ppt_app.Quit()
        except Exception as e:
            try: ppt_app.Quit()
            except Exception: pass
            raise e
    else:
        raise RuntimeError("Windows PowerPoint komponenti mavjud emas!")
        
    if progress_callback: progress_callback(100, "Tayyor! Taqdimot PDF ga o‘tkazildi.")
    return {'success': True, 'output_size': os.path.getsize(output_path)}


# ==============================================================================
# 14. PDF TO EXCEL (PDF -> Excel jadvallar)
# ==============================================================================
def pdf_to_excel(input_path, output_path, progress_callback=None):
    """PDF dagi barcha jadvallarni ajratib olib Excel (.xlsx) ga yozish"""
    if progress_callback: progress_callback(15, "PDF jadvallari qidirilmoqda...")
    doc = fitz.open(input_path)
    total_pages = len(doc)
    
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # standart bo'sh varaqni o'chirish
    
    tables_found_total = 0
    
    for page_num, page in enumerate(doc, 1):
        tabs = page.find_tables()
        if tabs.tables:
            tables_found_total += len(tabs.tables)
            ws = wb.create_sheet(title=f"Varaq_{page_num}")
            for t_idx, table in enumerate(tabs.tables, 1):
                extracted = table.extract()
                for row in extracted:
                    ws.append([str(c).strip() if c is not None else '' for c in row])
                ws.append([])  # jadvallar orasiga bo'sh qator
        if progress_callback:
            pct = 15 + int(70 * (page_num / total_pages))
            progress_callback(pct, f"Jadvallar tahlili: {page_num}/{total_pages} bet...")
            
    if tables_found_total == 0:
        # Agar qat'iy jadval chiziqlari topilmasa, matn qatorlarini tartib bilan yozish
        ws = wb.create_sheet(title="Hujjat_Matni")
        for page in doc:
            for line in page.get_text().splitlines():
                if line.strip():
                    ws.append([line.strip()])
                    
    if progress_callback: progress_callback(90, "Excel fayli saqlanmoqda...")
    wb.save(output_path)
    doc.close()
    if progress_callback: progress_callback(100, "Tayyor! Jadvallar Excel ga ko‘chirildi.")
    
    return {
        'success': True,
        'tables_count': tables_found_total,
        'pages_count': total_pages,
        'output_size': os.path.getsize(output_path)
    }
