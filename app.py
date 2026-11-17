# -*- coding: utf-8 -*-
"""
Yangi O'zbek Alifbosi, PDF to Word va Tarjima Tizimi - Flask Veb Ilovasi
Word (.docx), Excel (.xlsx, .xls), PDF (.pdf) va Matnlarni qayta ishlash.
"""

import os
import sys
import uuid
import time
import shutil
import re
import json
import base64
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_file, abort, session, redirect, url_for

# Ma'lumotlar bazasi va Auth boshqaruvi
import db

# Windows cp1251 terminal encoding fix
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Modullarni import qilish
from converter_engine import UzbekTransliterator
from docx_processor import process_docx
from excel_processor import process_excel
from pdf_processor import convert_pdf_to_docx
from translator_engine import translate_text
import pdf_tools_engine

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'alifba_ai_studio_secret_2026_super_key')
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024  # 300 MB limit (ko'p fayllar va katta PDF lar uchun)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
CONVERTED_FOLDER = os.path.join(BASE_DIR, 'converted')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.docx', '.doc', '.xlsx', '.xls', '.txt', '.pdf'}


def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def get_safe_base_name(raw_base):
    """
    Kirill, o'zbek yoki boshqa alifbodagi nomlarni xavfsiz ASCII lotin fayl nomiga aylantirish.
    Masalan: 'Аъгзамов Ровшан' -> 'Agzamov_Rovshan'
    """
    if not raw_base:
        return f"hujjat_{int(time.time())}"
        
    cyr_to_ascii = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ў': 'o', 'қ': 'q',
        'ғ': 'g', 'ҳ': 'h'
    }
    cleaned_chars = []
    for ch in raw_base:
        lower_ch = ch.lower()
        if lower_ch in cyr_to_ascii:
            trans = cyr_to_ascii[lower_ch]
            cleaned_chars.append(trans.capitalize() if ch.isupper() else trans)
        elif ch.isalnum() or ch in ('-', '_'):
            cleaned_chars.append(ch)
        elif ch.isspace():
            cleaned_chars.append('_')
        else:
            cleaned_chars.append('_')
            
    safe_base = ''.join(cleaned_chars)
    safe_base = re.sub(r'_+', '_', safe_base).strip('_')
    if not safe_base:
        safe_base = f"hujjat_{int(time.time())}"
    return safe_base


# Global Task Progress Tracker
TASK_PROGRESS = {}


def update_task_progress(task_id, percent, status):
    if task_id:
        TASK_PROGRESS[task_id] = {
            'percent': min(100, max(0, int(percent))),
            'status': status,
            'time': time.time()
        }


def cleanup_old_files():
    """24 soatdan eski vaqtinchalik fayllarni va keshni tozalash"""
    try:
        now = time.time()
        for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER]:
            for f in os.listdir(folder):
                file_path = os.path.join(folder, f)
                if os.path.isfile(file_path):
                    if now - os.path.getmtime(file_path) > 86400:
                        os.remove(file_path)
        # Tozalash: 1 soatdan eski task progresslar
        expired_tasks = [tid for tid, data in TASK_PROGRESS.items() if now - data.get('time', 0) > 3600]
        for tid in expired_tasks:
            TASK_PROGRESS.pop(tid, None)
    except Exception:
        pass


@app.route('/api/task-progress/<task_id>')
def api_task_progress(task_id):
    """Real vaqtda konvertatsiya yoki tarjima foizini (0-100%) qaytarish"""
    prog = TASK_PROGRESS.get(task_id, {'percent': 0, 'status': 'Kutilmoqda...'})
    return jsonify({
        'success': True,
        'percent': prog.get('percent', 0),
        'status': prog.get('status', 'Kutilmoqda...')
    })


def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or '127.0.0.1'


def get_current_user():
    uid = session.get('user_id')
    if uid:
        return db.get_user_by_id(uid)
    return None


@app.route('/')
def index():
    client_ip = get_client_ip()
    ua = request.headers.get('User-Agent', '')
    db.log_page_visit(client_ip, ua)
    cleanup_old_files()
    return render_template('index.html')


@app.route('/api/convert-text', methods=['POST'])
def api_convert_text():
    """Jonli matnni o'girish yoki tarjima qilish API"""
    user_id = session.get('user_id')
    client_ip = get_client_ip()
    can_proc, reason, left_count, is_vip = db.check_can_process(user_id=user_id, ip_address=client_ip)
    if not can_proc:
        return jsonify({
            'success': False,
            'limit_reached': True,
            'error': reason,
            'price': db.get_setting('vip_monthly_price', '25 000'),
            'card_number': db.get_setting('card_number', '5614 6819 0834 3415'),
            'card_holder': db.get_setting('card_holder', 'ISMOILOV NODIR'),
            'telegram_admin': db.get_setting('telegram_admin', 'alifbauz')
        }), 403

    data = request.get_json() or {}
    text = data.get('text', '')
    mode = data.get('mode', 'auto')
    o_variant = data.get('o_variant', 'ö')
    apostrophe = data.get('apostrophe', 'ʼ')

    if not text:
        return jsonify({'success': False, 'error': 'Matn kiritilmadi!'})

    transliterator = UzbekTransliterator(o_variant=o_variant, apostrophe_style=apostrophe)
    converted_text, stats = transliterator.convert(text, mode=mode, return_stats=True)

    db.log_usage(user_id=user_id, ip_address=client_ip, action_type='convert_text', file_name='Jonli matn')

    return jsonify({
        'success': True,
        'converted_text': converted_text,
        'stats': stats,
        'left_today': left_count - 1 if not is_vip else 999999
    })


@app.route('/api/convert-file', methods=['POST'])
def api_convert_file():
    """Faylni (.docx, .xlsx, .xls, .pdf, .txt) o'girish yoki tarjima qilish API"""
    user_id = session.get('user_id')
    client_ip = get_client_ip()
    can_proc, reason, left_count, is_vip = db.check_can_process(user_id=user_id, ip_address=client_ip)
    if not can_proc:
        return jsonify({
            'success': False,
            'limit_reached': True,
            'error': reason,
            'price': db.get_setting('vip_monthly_price', '25 000'),
            'card_number': db.get_setting('card_number', '5614 6819 0834 3415'),
            'card_holder': db.get_setting('card_holder', 'ISMOILOV NODIR'),
            'telegram_admin': db.get_setting('telegram_admin', 'alifbauz')
        }), 403

    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Fayl tanlanmadi!'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Fayl nomi bo\'sh!'}), 400

    orig_name = file.filename
    raw_base, raw_ext = os.path.splitext(orig_name)
    ext = raw_ext.lower().strip()

    if ext not in ALLOWED_EXTENSIONS:
        fmt_str = ext if ext else "noma'lum"
        return jsonify({
            'success': False, 
            'error': f"Faqat Word (.docx, .doc), Excel (.xlsx, .xls), PDF (.pdf) va Matn (.txt) fayllari qabul qilinadi! (Yuklangan format: {fmt_str})"
        }), 400

    mode = request.form.get('mode', 'auto')
    o_variant = request.form.get('o_variant', 'ö')
    apostrophe = request.form.get('apostrophe', 'ʼ')
    task_id = request.form.get('task_id', '')

    def on_prog(percent, msg):
        update_task_progress(task_id, percent, msg)

    update_task_progress(task_id, 5, "Fayl serverga yuklandi...")

    transliterator = UzbekTransliterator(o_variant=o_variant, apostrophe_style=apostrophe)

    safe_base = get_safe_base_name(raw_base)
    unique_id = uuid.uuid4().hex[:8]

    upload_filename = f"{unique_id}_{safe_base}{ext}"
    upload_path = os.path.join(UPLOAD_FOLDER, upload_filename)
    file.save(upload_path)

    # Prefix nomlash
    mode_prefix = "Word_" if ext == '.pdf' and mode == 'pdf_to_word' else "Tayyor_"
    converted_ext = '.docx' if ext in ['.pdf', '.doc'] else ext
    converted_filename = f"{mode_prefix}{safe_base}_{unique_id}{converted_ext}"
    converted_path = os.path.join(CONVERTED_FOLDER, converted_filename)

    try:
        # 1. PDF Fayl
        if ext == '.pdf':
            start_t = time.perf_counter()
            temp_docx_path = os.path.join(UPLOAD_FOLDER, f"temp_{unique_id}_{safe_base}.docx")
            pdf_res = convert_pdf_to_docx(upload_path, temp_docx_path, progress_callback=on_prog)
            
            # Agar faqat PDF -> Word bo'lsa
            if mode == 'pdf_to_word':
                shutil.move(temp_docx_path, converted_path)
                on_prog(100, "Tayyor! Word hujjati tayyorlandi.")
                res = {
                    'success': True,
                    'word_count': 0,
                    'char_count': 0,
                    'preview_original': f"PDF fayl muvaffaqiyatli Word (.docx) formatiga o'tkazildi ({pdf_res['pages_count']} bet).",
                    'preview_converted': "Barcha jadvallar, matnlar va rasmlar tahrirlanuvchi Word formatida saqlandi.",
                    'duration_ms': pdf_res['duration_ms']
                }
            else:
                on_prog(50, "Word hujjati qayta ishlanmoqda...")
                res = process_docx(temp_docx_path, converted_path, transliterator=transliterator, mode=mode, progress_callback=on_prog)
                if os.path.exists(temp_docx_path):
                    os.remove(temp_docx_path)

        # 2. Word (.docx) Fayl
        elif ext == '.docx':
            res = process_docx(upload_path, converted_path, transliterator=transliterator, mode=mode, progress_callback=on_prog)

        # 2b. Eski Word (.doc) Fayl
        elif ext == '.doc':
            on_prog(10, "Eski .doc formati yangi .docx formatiga aylantirilmoqda...")
            temp_docx_path = os.path.join(UPLOAD_FOLDER, f"temp_{unique_id}_{safe_base}.docx")
            try:
                import pythoncom
                import win32com.client
                pythoncom.CoInitialize()
                word_app = win32com.client.Dispatch("Word.Application")
                word_app.Visible = False
                abs_doc = os.path.abspath(upload_path)
                abs_docx = os.path.abspath(temp_docx_path)
                doc_file = word_app.Documents.Open(abs_doc)
                doc_file.SaveAs2(abs_docx, FileFormat=16)
                doc_file.Close()
                word_app.Quit()
                res = process_docx(temp_docx_path, converted_path, transliterator=transliterator, mode=mode, progress_callback=on_prog)
                if os.path.exists(temp_docx_path):
                    os.remove(temp_docx_path)
            except Exception as doc_err:
                return jsonify({
                    'success': False, 
                    'error': f"Eski .doc faylni ochishda xatolik: {str(doc_err)}. Iltimos faylni Microsoft Word dasturida ochib .docx formatida saqlang va qayta yuklang."
                }), 400

        # 3. Excel (.xlsx, .xls) Fayl
        elif ext in ['.xlsx', '.xls']:
            res = process_excel(upload_path, converted_path, transliterator=transliterator, mode=mode, progress_callback=on_prog)
            if 'output_path' in res and res['output_path'] != converted_path:
                converted_filename = os.path.basename(res['output_path'])

        # 4. Matn (.txt) Fayl
        elif ext == '.txt':
            start_t = time.perf_counter()
            on_prog(10, "Matn o‘qilmoqda...")
            with open(upload_path, 'r', encoding='utf-8', errors='ignore') as rf:
                txt_content = rf.read()
            if mode in ['ru_to_uz', 'uz_to_ru', 'en_to_uz', 'uz_to_en']:
                lang_pairs = {'ru_to_uz': ('ru', 'uz'), 'uz_to_ru': ('uz', 'ru'), 'en_to_uz': ('en', 'uz'), 'uz_to_en': ('uz', 'en')}
                src, dest = lang_pairs.get(mode, ('uz', 'en'))
                lines = [l for l in txt_content.split('\n') if l.strip()]
                def on_txt_b(done_b, total_b):
                    pct = 20 + int(70 * (done_b / max(1, total_b)))
                    on_prog(pct, f"AI Tarjima qilmoqda: {done_b}/{total_b} ({pct}%)")
                from translator_engine import batch_translate_list
                trans_lines = batch_translate_list(lines, src=src, dest=dest, progress_callback=on_txt_b)
                line_map = dict(zip(lines, trans_lines))
                conv_content = "\n".join(line_map.get(l, l) for l in txt_content.split('\n'))
            else:
                on_prog(40, "Alifbo o‘girilmoqda...")
                conv_content = transliterator.convert(txt_content, mode=mode)
            on_prog(90, "Fayl saqlanmoqda...")
            with open(converted_path, 'w', encoding='utf-8') as wf:
                wf.write(conv_content)
            on_prog(100, "Tayyor! Muvaffaqiyatli yakunlandi.")
            res = {
                'success': True,
                'word_count': len(txt_content.split()),
                'char_count': len(txt_content),
                'preview_original': txt_content[:500],
                'preview_converted': conv_content[:500],
                'duration_ms': round((time.perf_counter() - start_t) * 1000.0, 2)
            }
        else:
            return jsonify({'success': False, 'error': f"Noma'lum format: {ext}"}), 400

        update_task_progress(task_id, 100, "Tayyor! Muvaffaqiyatli yakunlandi.")

        download_url = f"/download/{converted_filename}"

        db.log_usage(user_id=user_id, ip_address=client_ip, action_type=f'file_{target_direction}', file_name=orig_name)

        return jsonify({
            'success': True,
            'download_url': download_url,
            'filename': converted_filename,
            'original_filename': orig_name,
            'file_type': converted_ext[1:].upper(),
            'left_today': left_count - 1 if not is_vip else 999999,
            'stats': {
                'word_count': res.get('word_count', 0),
                'char_count': res.get('char_count', 0),
                'duration_ms': res.get('duration_ms', 0),
                'preview_original': res.get('preview_original', ''),
                'preview_converted': res.get('preview_converted', '')
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Faylni qayta ishlashda xatolik yuz berdi: {str(e)}"
        }), 500


@app.route('/api/pdf-tool', methods=['POST'])
def api_pdf_tool():
    """
    Kengaytirilgan PDF Asboblari API (15 ta zamonaviy PDF funksiyalari)
    """
    user_id = session.get('user_id')
    client_ip = get_client_ip()
    can_proc, reason, left_count, is_vip = db.check_can_process(user_id=user_id, ip_address=client_ip)
    if not can_proc:
        return jsonify({
            'success': False,
            'limit_reached': True,
            'error': reason,
            'price': db.get_setting('vip_monthly_price', '25 000'),
            'card_number': db.get_setting('card_number', '5614 6819 0834 3415'),
            'card_holder': db.get_setting('card_holder', 'ISMOILOV NODIR'),
            'telegram_admin': db.get_setting('telegram_admin', 'alifbauz')
        }), 403

    tool = request.form.get('tool', 'pdf_to_word')
    task_id = request.form.get('task_id', '')

    def finish_pdf_tool(payload):
        target_name = payload.get('filename') or tool
        db.log_usage(user_id=user_id, ip_address=client_ip, action_type=f'pdf_{tool}', file_name=target_name)
        payload['left_today'] = left_count - 1 if not is_vip else 999999
        return jsonify(payload)

    def on_prog(percent, msg):
        update_task_progress(task_id, percent, msg)

    update_task_progress(task_id, 5, "Fayllar qabul qilinmoqda...")
    unique_id = uuid.uuid4().hex[:8]

    # 1. Multi-file tools: 'merge', 'images_to_pdf'
    if tool in ['merge', 'images_to_pdf']:
        files = request.files.getlist('files')
        if not files or len(files) == 0:
            if 'file' in request.files:
                files = [request.files['file']]
            else:
                return jsonify({'success': False, 'error': 'Hech qanday fayl tanlanmadi!'}), 400

        saved_paths = []
        for f in files:
            if f.filename:
                raw_b, raw_e = os.path.splitext(f.filename)
                s_base = get_safe_base_name(raw_b)
                s_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{s_base}{raw_e.lower()}")
                f.save(s_path)
                saved_paths.append(s_path)

        if not saved_paths:
            return jsonify({'success': False, 'error': 'Fayllar saqlanmadi!'}), 400

        try:
            if tool == 'merge':
                out_filename = f"Birlashtirilgan_Hujjat_{unique_id}.pdf"
                out_path = os.path.join(CONVERTED_FOLDER, out_filename)
                res = pdf_tools_engine.merge_pdfs(saved_paths, out_path, progress_callback=on_prog)
                return finish_pdf_tool({
                "success": True,
                    'download_url': f"/download/{out_filename}",
                    'filename': out_filename,
                    'message': f"{len(saved_paths)} ta PDF muvaffaqiyatli birlashtirildi ({res.get('page_count', len(saved_paths))} bet)!"
                })
            elif tool == 'images_to_pdf':
                out_filename = f"Rasmlar_Kitobi_{unique_id}.pdf"
                out_path = os.path.join(CONVERTED_FOLDER, out_filename)
                res = pdf_tools_engine.images_to_pdf(saved_paths, out_path, progress_callback=on_prog)
                page_cnt = res.get('pages_count', res.get('page_count', len(saved_paths)))
                return finish_pdf_tool({
                "success": True,
                    'download_url': f"/download/{out_filename}",
                    'filename': out_filename,
                    'message': f"{len(saved_paths)} ta rasm PDF hujjatga aylantirildi ({page_cnt} bet)!"
                })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': f"Xatolik: {str(e)}"}), 500

    # 2. Single-file tools
    file = request.files.get('file')
    if not file:
        files = request.files.getlist('files')
        if files:
            file = files[0]

    if not file or file.filename == '':
        return jsonify({'success': False, 'error': 'Fayl tanlanmadi!'}), 400

    orig_name = file.filename
    raw_base, raw_ext = os.path.splitext(orig_name)
    ext = raw_ext.lower().strip()
    safe_base = get_safe_base_name(raw_base)

    upload_filename = f"{unique_id}_{safe_base}{ext}"
    upload_path = os.path.join(UPLOAD_FOLDER, upload_filename)
    file.save(upload_path)

    try:
        if tool == 'split':
            page_range = request.form.get('page_range', 'har_biri')
            out_filename = f"Ajratilgan_Sahifalar_{safe_base}_{unique_id}.zip"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.split_pdf(upload_path, out_path, page_range_str=page_range, progress_callback=on_prog)
            actual_file = os.path.basename(res['output_path'])
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{actual_file}",
                'filename': actual_file,
                'message': f"PDF sahifalari muvaffaqiyatli ajratildi va bitta ZIP arxivga joylandi ({res['page_count']} ta sahifa)!"
            })

        elif tool == 'compress':
            quality = request.form.get('quality', 'medium')
            out_filename = f"Siqilgan_{safe_base}_{unique_id}.pdf"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.compress_pdf(upload_path, out_path, level=quality, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': f"PDF hajmi {res['saved_percent']}% ga kamaytirildi ({res.get('pages_count', 0)} sahifa)!"
            })

        elif tool == 'rotate':
            angle = int(request.form.get('angle', 90))
            page_range = request.form.get('page_range', 'all')
            out_filename = f"Burilgan_{safe_base}_{unique_id}.pdf"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.rotate_pdf(upload_path, out_path, angle=angle, page_range_str=page_range, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': f"PDF sahifalari {angle}° ga muvaffaqiyatli burildi!"
            })

        elif tool == 'watermark':
            text = request.form.get('text', 'KONFIDENSIAL')
            fontsize = int(request.form.get('fontsize', 38))
            out_filename = f"Suv_Belgili_{safe_base}_{unique_id}.pdf"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.watermark_pdf(upload_path, out_path, watermark_text=text, fontsize=fontsize, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': f"PDF ga '{text}' suv belgisi muvaffaqiyatli qo‘yildi!"
            })

        elif tool == 'page_numbers':
            position = request.form.get('position', 'bottom-right')
            fmt = request.form.get('format', 'Sahifa {n} / {total}')
            out_filename = f"Raqamlangan_{safe_base}_{unique_id}.pdf"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.page_numbers_pdf(upload_path, out_path, position=position, format_str=fmt, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': f"Barcha {res['pages_count']} ta sahifaga tartib raqamlari qo‘yildi!"
            })

        elif tool == 'protect':
            password = request.form.get('password', '')
            if not password:
                return jsonify({'success': False, 'error': 'Parol kiritilmadi!'}), 400
            out_filename = f"Himoyalangan_{safe_base}_{unique_id}.pdf"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.protect_pdf(upload_path, out_path, password=password, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': "PDF fayl parol bilan ishonchli himoyalandi!"
            })

        elif tool == 'unlock':
            password = request.form.get('password', '')
            out_filename = f"Ochilgan_{safe_base}_{unique_id}.pdf"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.unlock_pdf(upload_path, out_path, password=password, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': "PDF fayl himoyasi muvaffaqiyatli olib tashlandi!"
            })

        elif tool == 'pdf_to_images':
            img_format = request.form.get('format', 'png').lower()
            dpi = int(request.form.get('dpi', 150))
            out_filename = f"Rasmlar_{safe_base}_{unique_id}.zip"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.pdf_to_images(upload_path, out_path, dpi=dpi, img_format=img_format, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': f"PDF ning barcha {res['pages_count']} sahifasi sifatli rasmlar sifatida ZIP ga yuklandi!"
            })

        elif tool == 'pdf_to_excel':
            out_filename = f"Jadval_{safe_base}_{unique_id}.xlsx"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.pdf_to_excel(upload_path, out_path, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': f"PDF dagi jadvallar Excel (.xlsx) ga muvaffaqiyatli ko‘chirildi!"
            })

        elif tool == 'word_to_pdf':
            out_filename = f"{safe_base}_{unique_id}.pdf"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.word_to_pdf(upload_path, out_path, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': "Word hujjati 100% original sifatda PDF ga aylantirildi!"
            })

        elif tool == 'excel_to_pdf':
            out_filename = f"{safe_base}_{unique_id}.pdf"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.excel_to_pdf(upload_path, out_path, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': "Excel jadvali sifatli PDF ga aylantirildi!"
            })

        elif tool == 'ppt_to_pdf':
            out_filename = f"{safe_base}_{unique_id}.pdf"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            res = pdf_tools_engine.powerpoint_to_pdf(upload_path, out_path, progress_callback=on_prog)
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': "PowerPoint taqdimoti PDF formatiga o‘tkazildi!"
            })

        elif tool == 'pdf_to_word':
            pdf_mode = request.form.get('pdf_mode', 'pdf_to_word')
            temp_docx_path = os.path.join(UPLOAD_FOLDER, f"temp_{unique_id}_{safe_base}.docx")
            out_filename = f"Word_{safe_base}_{unique_id}.docx"
            out_path = os.path.join(CONVERTED_FOLDER, out_filename)
            pdf_res = convert_pdf_to_docx(upload_path, temp_docx_path, progress_callback=on_prog)
            
            if pdf_mode == 'pdf_to_word':
                shutil.move(temp_docx_path, out_path)
            else:
                transliterator = UzbekTransliterator()
                process_docx(temp_docx_path, out_path, transliterator=transliterator, mode=pdf_mode, progress_callback=on_prog)
                if os.path.exists(temp_docx_path):
                    os.remove(temp_docx_path)
                
            return finish_pdf_tool({
                "success": True,
                'download_url': f"/download/{out_filename}",
                'filename': out_filename,
                'message': f"PDF muvaffaqiyatli Word (.docx) formatiga o‘tkazildi ({pdf_res['pages_count']} bet)!"
            })
        else:
            return jsonify({'success': False, 'error': f"Noma'lum asbob: {tool}"}), 400

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f"Xatolik yuz berdi: {str(e)}"}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """O'girilgan yoki tarjima qilingan tayyor faylni yuklab olish"""
    file_path = os.path.join(CONVERTED_FOLDER, filename)
    if not os.path.exists(file_path):
        abort(404, description="Fayl topilmadi yoki muddati o'tgan!")
    return send_file(file_path, as_attachment=True, download_name=filename)


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'app': 'Yangi Uzbek Alifbosi AI Konverter'})


# ---------------------------------------------------------------------------
# FOYDALANUVCHILAR AUTH API (Ro'yxatdan o'tish, Kirish, Chiqish)
# ---------------------------------------------------------------------------

@app.route('/api/auth/register', methods=['POST'])
def api_auth_register():
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()

    ok, res = db.register_user(name, username, password)
    if not ok:
        return jsonify({'success': False, 'error': res}), 400

    session['user_id'] = res['id']
    return jsonify({
        'success': True,
        'user': {
            'id': res['id'],
            'name': res['name'],
            'username': res['username'],
            'is_vip': res['is_vip']
        }
    })


@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()

    ok, res = db.authenticate_user(username, password)
    if not ok:
        return jsonify({'success': False, 'error': res}), 401

    session['user_id'] = res['id']
    return jsonify({
        'success': True,
        'user': {
            'id': res['id'],
            'name': res['name'],
            'username': res['username'],
            'is_vip': res['is_vip']
        }
    })


@app.route('/api/auth/logout', methods=['POST'])
def api_auth_logout():
    session.pop('user_id', None)
    return jsonify({'success': True})


@app.route('/api/auth/me', methods=['GET'])
def api_auth_me():
    user = get_current_user()
    client_ip = get_client_ip()
    settings = db.get_all_settings()

    daily_limit = int(settings.get('daily_free_limit', '5'))

    if user:
        used_today = db.get_today_usage_count(user_id=user['id'])
        left_today = 999999 if user.get('is_vip') == 1 else max(0, daily_limit - used_today)
        user_info = {
            'id': user['id'],
            'name': user['name'],
            'username': user['username'],
            'is_vip': user.get('is_vip', 0),
            'vip_until': user.get('vip_until'),
            'used_today': used_today,
            'left_today': left_today,
            'is_blocked': user.get('is_blocked', 0)
        }
    else:
        used_today = db.get_today_usage_count(ip_address=client_ip)
        left_today = max(0, daily_limit - used_today)
        user_info = None

    return jsonify({
        'success': True,
        'logged_in': user is not None,
        'user': user_info,
        'guest_used_today': used_today if not user else None,
        'guest_left_today': left_today if not user else None,
        'daily_limit': daily_limit,
        'require_login': settings.get('require_login', 'false').lower() == 'true',
        'settings': {
            'vip_monthly_price': settings.get('vip_monthly_price', '25 000'),
            'card_number': settings.get('card_number', '5614 6819 0834 3415'),
            'card_holder': settings.get('card_holder', 'ISMOILOV NODIR'),
            'telegram_admin': settings.get('telegram_admin', 'alifbauz'),
            'announcement_active': settings.get('announcement_active', 'false').lower() == 'true',
            'announcement_text': settings.get('announcement_text', '')
        }
    })


# ---------------------------------------------------------------------------
# ADMIN PANEL ROUTES (/admin)
# ---------------------------------------------------------------------------

@app.route('/admin')
def admin_page():
    is_admin = session.get('is_admin', False)
    return render_template('admin.html', is_admin=is_admin)


@app.route('/api/admin/login', methods=['POST'])
def api_admin_login():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip().lower()
    password = (data.get('password') or '').strip()

    admin_user = (db.get_setting('admin_username', 'admin') or 'admin').strip().lower()
    admin_pass_hash = db.get_setting('admin_password_hash', db.hash_password('admin123'))

    pass_ok = (db.hash_password(password) == admin_pass_hash)
    user_ok = (not username) or (username == admin_user)

    if pass_ok and user_ok:
        session['is_admin'] = True
        session.permanent = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': "Admin login yoki parol noto'g'ri!"}), 401


@app.route('/api/admin/logout', methods=['POST'])
def api_admin_logout():
    session.pop('is_admin', None)
    return jsonify({'success': True})


@app.route('/api/admin/users', methods=['GET'])
def api_admin_users():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403
    q = request.args.get('q', '')
    filter_type = request.args.get('filter', 'all')
    users = db.search_users(query=q, filter_type=filter_type)
    return jsonify({'success': True, 'users': users})


@app.route('/api/admin/set-vip', methods=['POST'])
def api_admin_set_vip():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403
    data = request.get_json() or {}
    user_id = data.get('user_id')
    months = data.get('months', 1)
    is_unlimited = data.get('unlimited', False)

    db.update_user_vip_months(user_id, months, is_unlimited=is_unlimited)
    return jsonify({'success': True})


@app.route('/api/admin/revoke-vip', methods=['POST'])
def api_admin_revoke_vip():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403
    data = request.get_json() or {}
    user_id = data.get('user_id')
    db.revoke_user_vip(user_id)
    return jsonify({'success': True})


@app.route('/api/admin/toggle-block', methods=['POST'])
def api_admin_toggle_block():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403
    data = request.get_json() or {}
    user_id = data.get('user_id')
    ok, new_state = db.toggle_user_block(user_id)
    return jsonify({'success': True, 'is_blocked': new_state})


@app.route('/api/admin/delete-user', methods=['POST'])
def api_admin_delete_user():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403
    data = request.get_json() or {}
    user_id = data.get('user_id')
    db.delete_user(user_id)
    return jsonify({'success': True})


@app.route('/api/admin/metrics', methods=['GET'])
def api_admin_metrics():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403
    metrics = db.get_admin_dashboard_metrics()
    return jsonify({'success': True, 'metrics': metrics})


@app.route('/api/admin/clean-storage', methods=['POST'])
def api_admin_clean_storage():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403
    count, freed_mb = db.clean_storage_files()
    return jsonify({'success': True, 'cleaned_count': count, 'freed_mb': freed_mb})


@app.route('/api/admin/settings', methods=['GET', 'POST'])
def api_admin_settings():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403

    if request.method == 'GET':
        return jsonify({'success': True, 'settings': db.get_all_settings()})

    data = request.get_json() or {}
    updates = {}

    for k in ['require_login', 'daily_free_limit', 'vip_monthly_price', 'card_number', 'card_holder', 'telegram_admin', 'admin_username', 'announcement_active', 'announcement_text']:
        if k in data:
            updates[k] = data[k]

    new_pass = (data.get('new_password') or '').strip()
    if new_pass:
        updates['admin_password_hash'] = db.hash_password(new_pass)

    db.update_settings_dict(updates)
    return jsonify({'success': True})


@app.route('/api/admin/logs', methods=['GET'])
def api_admin_logs():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403
    logs = db.get_recent_usage_logs(limit=50)
    return jsonify({'success': True, 'logs': logs})


@app.route('/api/admin/visits', methods=['GET'])
def api_admin_visits():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi'}), 403
    visits = db.get_recent_visits(limit=50)
    return jsonify({'success': True, 'visits': visits})


@app.route('/api/admin/change-password', methods=['POST'])
def api_admin_change_password():
    if not session.get('is_admin'):
        return jsonify({'success': False, 'error': 'Ruxsat berilmadi! Avval admin panelga kiring.'}), 403

    data = request.get_json() or {}
    new_user = (data.get('new_username') or '').strip().lower()
    new_pass = (data.get('new_password') or '').strip()
    confirm_pass = (data.get('confirm_password') or '').strip()

    updates = {}
    if new_user:
        if len(new_user) < 3:
            return jsonify({'success': False, 'error': "Admin logini kamida 3 ta belgidan iborat bo‘lishi kerak!"}), 400
        updates['admin_username'] = new_user

    if new_pass:
        if len(new_pass) < 4:
            return jsonify({'success': False, 'error': "Yangi parol kamida 4 ta belgidan iborat bo‘lishi kerak!"}), 400
        if confirm_pass and new_pass != confirm_pass:
            return jsonify({'success': False, 'error': "Yangi parol va tasdiqlovchi parol bir-biriga mos kelmadi!"}), 400
        updates['admin_password_hash'] = db.hash_password(new_pass)

    if not updates:
        return jsonify({'success': False, 'error': "O‘zgartirish uchun ma’lumot kiritilmadi!"}), 400

    db.update_settings_dict(updates)
    return jsonify({'success': True, 'message': "Admin logini va paroli muvaffaqiyatli yangilandi!"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print("\n" + "=" * 55)
    print(">>> Yangi O'zbek Alifbosi AI Konverter ishga tushdi!")
    print(f">>> Brauzerda ochish: http://127.0.0.1:{port}")
    print("=" * 55 + "\n")
    app.run(host='0.0.0.0', port=port, debug=False)
