# -*- coding: utf-8 -*-
"""
End-to-End Test Suite for Alifbo AI Converter
Tests:
1. Text conversion API
2. Word document (.docx) generation, upload, conversion & verification
3. Excel document (.xlsx) generation, upload, conversion & verification
"""

import os
import io
import docx
import openpyxl
from openpyxl.styles import Font, PatternFill
from app import app

def run_tests():
    client = app.test_client()

    print("\n--- 1. Testing Text Conversion API ---")
    test_text = "Ўзбекистон Республикаси, g'alaba, shahar, chiroyli, Ер, поезд, цирк, Конституция, эълон"
    resp = client.post('/api/convert-text', json={'text': test_text, 'mode': 'auto', 'o_variant': 'ö'})
    assert resp.status_code == 200, f"Status code: {resp.status_code}"
    data = resp.get_json()
    assert data['success'] is True
    print("Original Text:", test_text)
    print("Converted:    ", data['converted_text'])
    print("Stats:        ", data['stats'])
    assert "Özbekiston" in data['converted_text']
    assert "ğalaba" in data['converted_text']
    assert "şahar" in data['converted_text']
    assert "çiroyli" in data['converted_text']
    assert "Yer" in data['converted_text']
    assert "poyezd" in data['converted_text']
    assert "sirk" in data['converted_text']
    assert "Konstitutsiya" in data['converted_text']
    assert "eʼlon" in data['converted_text']
    print(">>> Text Conversion API: PASSED! <<<")

    print("\n--- 2. Testing Word (.docx) Conversion ---")
    # Create sample docx
    sample_doc_path = os.path.join(os.path.dirname(__file__), 'sample_input.docx')
    doc = docx.Document()
    doc.add_heading('Ўзбекистон Тарихи ва Маданияти', level=1)
    
    p = doc.add_paragraph()
    r1 = p.add_run('O‘zbekiston Respublikasi ')
    r1.bold = True
    r2 = p.add_run('mustaqil va suveren davlatdir. ')
    r2.italic = True
    r3 = p.add_run('Шаҳар ва қишлоқлар обод бўлмоқда.')
    
    table = doc.add_table(rows=2, cols=3)
    table.cell(0, 0).text = '№'
    table.cell(0, 1).text = 'Шаҳар номи'
    table.cell(0, 2).text = 'Тавсифи'
    table.cell(1, 0).text = '1'
    table.cell(1, 1).text = 'Тошкент'
    table.cell(1, 2).text = 'Chiroyli poytaxt va yashil shahar'
    
    doc.save(sample_doc_path)
    
    with open(sample_doc_path, 'rb') as f:
        file_bytes = io.BytesIO(f.read())
        resp = client.post('/api/convert-file', data={
            'file': (file_bytes, 'sample_input.docx'),
            'mode': 'auto',
            'o_variant': 'ö'
        }, content_type='multipart/form-data')

    assert resp.status_code == 200, f"Docx error: {resp.status_code}"
    data = resp.get_json()
    assert data['success'] is True, data
    print("Docx converted successfully!")
    print("Download URL:", data['download_url'])
    print("Word count:", data['stats']['word_count'])

    # Verify download file content
    dl_resp = client.get(data['download_url'])
    assert dl_resp.status_code == 200
    converted_docx_bytes = io.BytesIO(dl_resp.data)
    conv_doc = docx.Document(converted_docx_bytes)
    
    full_text = " ".join([p.text for p in conv_doc.paragraphs])
    for table in conv_doc.tables:
        for row in table.rows:
            for cell in row.cells:
                full_text += " " + cell.text
                
    print("Converted Docx Text:", full_text)
    assert "Özbekiston Tarixi va Madaniyati" in full_text
    assert "Özbekiston Respublikasi" in full_text
    assert "Toşkent" in full_text
    assert "Çiroyli poytaxt va yaşil şahar" in full_text
    print(">>> Word (.docx) Conversion: PASSED! <<<")

    print("\n--- 3. Testing Excel (.xlsx) Conversion ---")
    sample_xlsx_path = os.path.join(os.path.dirname(__file__), 'sample_input.xlsx')
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ҳисобот_2026"

    ws['A1'] = "Маҳсулот номи"
    ws['A1'].font = Font(bold=True)
    ws['B1'] = "Нархи (сўм)"
    ws['C1'] = "Ҳолати"

    ws['A2'] = "Ғўза мойи"
    ws['B2'] = 25000
    ws['C2'] = "O'ta sifatli va shirin"

    ws['A3'] = "Чой (кўк)"
    ws['B3'] = 12000
    ws['C3'] = "Yangi hosil"

    ws['A4'] = "Жами:"
    ws['B4'] = "=SUM(B2:B3)"

    wb.save(sample_xlsx_path)

    with open(sample_xlsx_path, 'rb') as f:
        file_bytes = io.BytesIO(f.read())
        resp = client.post('/api/convert-file', data={
            'file': (file_bytes, 'sample_input.xlsx'),
            'mode': 'auto',
            'o_variant': 'ö'
        }, content_type='multipart/form-data')

    assert resp.status_code == 200, f"Xlsx error: {resp.status_code}"
    data = resp.get_json()
    assert data['success'] is True, data
    print("Excel converted successfully!")
    print("Download URL:", data['download_url'])

    # Verify download file content
    dl_resp = client.get(data['download_url'])
    assert dl_resp.status_code == 200
    conv_wb = openpyxl.load_workbook(io.BytesIO(dl_resp.data))
    conv_ws = conv_wb.active
    
    print("Sheet title:", conv_ws.title)
    print("A1:", conv_ws['A1'].value, "Bold:", conv_ws['A1'].font.bold)
    print("A2:", conv_ws['A2'].value)
    print("C2:", conv_ws['C2'].value)
    print("A3:", conv_ws['A3'].value)
    print("B4 (formula):", conv_ws['B4'].value)

    assert conv_ws.title == "Hisobot_2026"
    assert conv_ws['A1'].value == "Mahsulot nomi"
    assert conv_ws['A1'].font.bold is True
    assert conv_ws['A2'].value == "Ğöza moyi"
    assert conv_ws['C2'].value == "Öta sifatli va şirin"
    assert conv_ws['A3'].value == "Çoy (kök)"
    assert conv_ws['B4'].value == "=SUM(B2:B3)"  # Formula preserved!
    print(">>> Excel (.xlsx) Conversion: PASSED! <<<")

    print("\n==========================================")
    print("🎉 ALL TESTS PASSED SUCCESSFULLY! 100% OK")
    print("==========================================\n")

if __name__ == '__main__':
    run_tests()
