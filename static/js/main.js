// ==========================================================================
// HUJJAT & ALIFBO AI STUDIO - MULTI-LANGUAGE CONTROLLER & ENGINE
// Author: Ismoilov Nodir
// ==========================================================================

const CARD_NUMBER = "5614681908343415";

// 3 Tillardagi to'liq lug'at (Uzbek, Russian, English)
const I18N = {
  uz: {
    brandSub: "PDF to Word, Yangi Alifbo va AI Tarjima Tizimi",
    tabPdf: "📑 PDF Studio (15-in-1)",
    tabPdfDesc: "Birlashtirish, Word, Excel, Siqish...",
    pdfStudioTitle: "📑 PDF Asboblari Majmuasi (PDF Studio)",
    pdfStudioDesc: "Barcha zaruriy PDF amallari: Word, Excel, PowerPoint, birlashtirish, siqish, burish, suv belgisi va himoyalash.",
    toolPdfWordTitle: "PDF ➔ Word",
    toolPdfWordDesc: "Word (.docx) ga xatosiz o‘tkazish",
    toolWordPdfTitle: "Word ➔ PDF",
    toolWordPdfDesc: "DOCX hujjatlarni PDF qilish",
    toolMergeTitle: "Birlashtirish (Merge)",
    toolMergeDesc: "Bir nechta PDF ni bitta qilish",
    toolSplitTitle: "Ajratish (Split)",
    toolSplitDesc: "Sahifalarni kesib olish",
    toolCompressTitle: "Siqish (Compress)",
    toolCompressDesc: "Fayl hajmini kamaytirish",
    toolPdfExcelTitle: "PDF ➔ Excel",
    toolPdfExcelDesc: "Jadvallarni XLSX ga ajratish",
    toolExcelPdfTitle: "Excel ➔ PDF",
    toolExcelPdfDesc: "XLSX jadvallarni PDF qilish",
    toolPptPdfTitle: "PowerPoint ➔ PDF",
    toolPptPdfDesc: "PPTX taqdimotni PDF qilish",
    toolPdfImgTitle: "PDF ➔ JPG/PNG",
    toolPdfImgDesc: "Sahifalarni rasmga o‘tkazish",
    toolImgPdfTitle: "JPG/PNG ➔ PDF",
    toolImgPdfDesc: "Rasmlardan PDF yaratish",
    toolRotateTitle: "Burish (Rotate)",
    toolRotateDesc: "90°, 180°, 270° ga burish",
    toolWatermarkTitle: "Suv Belgisi",
    toolWatermarkDesc: "Matnli belgi tushirish",
    toolPageNumTitle: "Sahifa Raqamlari",
    toolPageNumDesc: "1, 2, 3... tartib raqam",
    toolProtectTitle: "Himoyalash (Parol)",
    toolProtectDesc: "Parol bilan shifrlash",
    toolUnlockTitle: "Parolni Yechish",
    toolUnlockDesc: "Himoyani olib tashlash",
    labelSplitMode: "Ajratish usuli:",
    splitAllPages: "📦 Barcha sahifalarni alohida PDF qilib ZIP ga joylash",
    splitCustomPages: "✂️ Tanlangan sahifalar (oraliqlar bo‘yicha)",
    themeDark: "🌙 Tungi",
    themeLight: "☀️ Kunduzgi",
    tabAlifbo: "🔤 Alifbo Konverteri",
    tabAlifboDesc: "Kirill, Lotin, Yangi Lotin",
    tabTranslate: "🌐 AI Tarjima",
    tabTranslateDesc: "Rus, O‘zbek, Ingliz tillari",
    tabAbout: "ℹ️ Dastur Haqida",
    tabAboutDesc: "Muallif & Donat (Karta, QR)",

    pdfHeaderTitle: "📑 PDF Hujjatlarni Word (.docx) Formatiga Xatosiz O‘tkazish",
    pdfHeaderDesc: "Barcha jadvallar, sarlavhalar, matn shriftlari va rasmlar 100% aniq saqlanadi.",
    pdfModeDirect: "Faqat Word (.docx) ga o‘tkazish",
    pdfModeDirectSub: "Alifbo va matnni o‘zgartirmasdan tahrirlanuvchi Word qilish",
    pdfModeNewLat: "Wordga o‘tkazish + Yangi Lotin",
    pdfModeNewLatSub: "PDF ni Word qilib, birdaniga Ö, Ğ, Ş, Ç ga o‘giradi",
    pdfModeRuUz: "Wordga o‘tkazish + O‘zbekchaga Tarjima",
    pdfModeRuUzSub: "Ruscha PDF ni Word qilib, o‘zbek tiliga tarjima qiladi",
    pdfDropTitle: "PDF faylingizni bu yerga tashlang",
    pdfDropSub: "yoki quyidagi tugmani bosib tanlang",
    btnSelectPdf: "📂 PDF Faylni Tanlash",
    pdfNote: "🔒 Katta hajmdagi ko‘p sahifali PDF fayllar ham bir necha soniyada Word formatiga o‘tkaziladi.",
    btnConvertPdf: "Word (.docx) ga O‘tkazish",
    btnDownloadDocx: "Word Hujjatini Yuklab Olish (.docx)",

    alifboHeaderTitle: "🔤 O‘zbek Alifbosi Konverteri (Word, Excel va Matn)",
    alifboHeaderDesc: "Kirill, Eski Lotin va Yangi Lotin (Ö, Ğ, Ş, Ç) alifbolari o‘rtasida formatni buzmasdan o‘girish.",
    dirCyrToNew: "Кирилл ➔ Yangi Lotin",
    dirOldToNew: "Eski Lotin ➔ Yangi Lotin",
    dirCyrToOld: "Кирилл ➔ Amaldagi Lotin",
    dirLatToCyr: "Lotin ➔ Кирилл",
    fileDropTitle: "Word (.docx) yoki Excel (.xlsx) faylingizni bu yerga tashlang",
    fileDropSub: "yoki quyidagi tugmani bosib tanlang",
    btnSelectDoc: "📂 Word / Excel Faylni Tanlash",
    formatNote: "🔒 Shriftlar, ranglar, jadvallar va Excel formulalari 100% buzilmasdan saqlanadi!",
    btnConvertAlifbo: "Alifboga O‘girish",
    alifboSuccessTitle: "Hujjat Yangi Alifboga Muvaffaqiyatli O‘tkazildi!",
    btnDownloadResult: "Yangi Hujjatni Yuklab Olish",

    liveEditorTitle: "✍️ Jonli Matn Muharriri (Tezkor o‘girish)",
    inputOriginalText: "Asl Matn",
    outputConvertedText: "O‘girilgan Matn",
    btnSample: "💡 Namuna",
    btnClear: "🗑 Tozalash",
    btnCopy: "📋 Nusxa Olish",
    btnRunConvert: "⚡ O‘girish",

    transHeaderTitle: "🌐 AI Hujjat va Matn Tarjimoni (Rus, O‘zbek, Ingliz)",
    transHeaderDesc: "Word, Excel, PDF va matnlarni tillar o‘rtasida xatosiz va ravon tarjima qilish.",
    transRuUzDesc: "Rus tilidagi hujjatlarni o‘zbekchaga tarjima qilish",
    transUzRuDesc: "O‘zbekcha hujjatlarni rus tiliga tarjima qilish",
    transEnUzDesc: "Ingliz tilidagi fayllarni o‘zbekchaga tarjima qilish",
    transUzEnDesc: "O‘zbekcha fayllarni ingliz tiliga tarjima qilish",
    transDropTitle: "Tarjima qilinadigan faylni bu yerga tashlang",
    transDropSub: "yoki quyidagi tugmani bosib tanlang",
    btnSelectTrans: "📂 Hujjatni Tanlash",
    transNote: "🔒 Hujjatdagi jadvallar va shriftlar tartibi saqlangan holda to‘liq tarjima qilib beriladi.",
    btnRunTranslateDoc: "Hujjatni Tarjima Qilish",
    transSuccessTitle: "Hujjat Muvaffaqiyatli Tarjima Qilindi!",
    transSuccessDesc: "Tarjima qilingan faylni yuklab olishingiz mumkin",
    btnDownloadTrans: "Tarjima Qilingan Hujjatni Yuklab Olish",
    transLiveTitle: "✍️ Jonli Matn Tarjimoni",
    transInputLabel: "Asl Matn",
    transOutputLabel: "Tarjima Natijasi",
    btnRunTranslate: "⚡ Tarjima Qilish",

    aboutTitle: "ℹ️ Dastur Haqida va Loyihani Qo‘llab-quvvatlash",
    aboutSub: "Dastur yaratuvchisi va loyiha rivoji uchun donat (hissa qo‘shish).",
    cardCreatorLabel: "Dastur Yaratuvchisi",
    btnCopyCard: "Karta Raqamidan Nusxa Olish (5614 6819 0834 3415)",
    donateHint: "Dastur rivojini istalgan bank ilovasi (Click, Payme, Zoomrad, Anorbank, Uzum va boshqalar) orqali qo‘llab-quvvatlashingiz mumkin.",
    cardRawText: "Karta raqami:",
    missionTitle: "🎯 Dasturning Maqsadi va Missiyasi",
    missionDesc: "Ushbu dasturiy majmua O‘zbekiston fuqarolari, o‘qituvchilar, talabalar va davlat/xususiy sektor xodimlari uchun hujjatlar aylanishini osonlashtirish, PDF larni Word formatiga xatosiz o‘tkazish, yangi alifbo islohotiga qulay moslashish hamda Rus va Ingliz tillaridagi hujjatlarni tezkor va xatosiz tarjima qilish maqsadida Ismoilov Nodir tomonidan yaratilgan.",
    footerCreator: "Dastur yaratuvchisi:",
    btnCancel: "✖ Bekor qilish",
    resSuccessTitle: "Word Hujjati Muvaffaqiyatli Tayyorlandi!",
    resSuccessDesc: "Barcha jadvallar va matnlar tahrirlanuvchi Word formatida saqlandi.",

    loadingTitle: "Hujjat Qayta Ishlanmoqda...",
    loadingSub: "AI matnlar, shriftlar va jadvallarni xatosiz tayyorlamoqda",
    loadingPdfTitle: "PDF Wordga O‘tkazilmoqda...",
    loadingPdfSub: "Barcha jadvallar, matnlar va rasmlar xatosiz tartiblanmoqda",
    loadingTransTitle: "AI Hujjatni Tarjima Qilmoqda...",
    loadingTransSub: "Sun'iy intellekt matn mazmunini ravon va xatosiz tarjima qilmoqda",
    loadingAlifboTitle: "Hujjat Yangi Alifboga O‘girilmoqda...",
    loadingAlifboSub: "Harflar, jadvallar va shriftlar Yangi Lotin formatiga o‘tkazilmoqda",
    loadingTimerPrefix: "Jarayon davom etmoqda: "
  },

  ru: {
    brandSub: "Конвертер PDF в Word, Новый Алфавит и AI Переводчик",
    tabPdf: "📑 PDF Studio (15-в-1)",
    tabPdfDesc: "Объединение, Word, Excel, Сжатие...",
    pdfStudioTitle: "📑 Набор инструментов PDF (PDF Studio)",
    pdfStudioDesc: "Все необходимые инструменты: Word, Excel, PowerPoint, объединение, сжатие, поворот, водяной знак и защита.",
    toolPdfWordTitle: "PDF в Word",
    toolPdfWordDesc: "Конвертация в DOCX без ошибок",
    toolWordPdfTitle: "Word в PDF",
    toolWordPdfDesc: "Преобразовать DOCX в PDF",
    toolMergeTitle: "Объединить PDF",
    toolMergeDesc: "Соединить несколько PDF файлов",
    toolSplitTitle: "Разделить PDF",
    toolSplitDesc: "Извлечь нужные страницы",
    toolCompressTitle: "Сжать PDF",
    toolCompressDesc: "Уменьшить размер файла",
    toolPdfExcelTitle: "PDF в Excel",
    toolPdfExcelDesc: "Экспорт таблиц в XLSX",
    toolExcelPdfTitle: "Excel в PDF",
    toolExcelPdfDesc: "Преобразовать XLSX в PDF",
    toolPptPdfTitle: "PowerPoint в PDF",
    toolPptPdfDesc: "Преобразовать PPTX в PDF",
    toolPdfImgTitle: "PDF в JPG/PNG",
    toolPdfImgDesc: "Страницы PDF в картинки",
    toolImgPdfTitle: "JPG/PNG в PDF",
    toolImgPdfDesc: "Создать PDF из изображений",
    toolRotateTitle: "Повернуть PDF",
    toolRotateDesc: "Поворот на 90°, 180°, 270°",
    toolWatermarkTitle: "Водяной знак",
    toolWatermarkDesc: "Добавить текст на страницы",
    toolPageNumTitle: "Номера страниц",
    toolPageNumDesc: "Нумерация страниц PDF",
    toolProtectTitle: "Защита PDF",
    toolProtectDesc: "Зашифровать паролем",
    toolUnlockTitle: "Снять защиту",
    toolUnlockDesc: "Удалить пароль с PDF",
    labelSplitMode: "Режим разделения:",
    splitAllPages: "📦 Разделить все страницы на отдельные PDF в ZIP",
    splitCustomPages: "✂️ Выбранные страницы (по диапазону)",
    themeDark: "🌙 Тёмная",
    themeLight: "☀️ Светлая",
    tabAlifbo: "🔤 Конвертер Алфавита",
    tabAlifboDesc: "Кириллица, Латиница, Новая",
    tabTranslate: "🌐 AI Переводчик",
    tabTranslateDesc: "Русский, Узбекский, Английский",
    tabAbout: "ℹ️ О Программе",
    tabAboutDesc: "Автор и Донат (Карта, QR)",

    pdfHeaderTitle: "📑 Конвертация PDF в редактируемый Word (.docx)",
    pdfHeaderDesc: "Все таблицы, заголовки, шрифты и изображения сохраняются на 100%.",
    pdfModeDirect: "Только конвертация в Word (.docx)",
    pdfModeDirectSub: "Создать редактируемый Word без изменения алфавита",
    pdfModeNewLat: "В Word + Новый Латинский алфавит",
    pdfModeNewLatSub: "Конвертирует PDF в Word и сразу переводит в Ö, Ğ, Ş, Ç",
    pdfModeRuUz: "В Word + Перевод на Узбекский",
    pdfModeRuUzSub: "Конвертирует русский PDF в Word и переводит на узбекский",
    pdfDropTitle: "Перетащите PDF файл сюда",
    pdfDropSub: "или нажмите кнопку ниже для выбора",
    btnSelectPdf: "📂 Выбрать PDF файл",
    pdfNote: "🔒 Многостраничные PDF документы конвертируются всего за пару секунд.",
    btnConvertPdf: "Конвертировать в Word (.docx)",
    btnDownloadDocx: "Скачать Word Документ (.docx)",

    alifboHeaderTitle: "🔤 Конвертер Узбекского Алфавита (Word, Excel и Текст)",
    alifboHeaderDesc: "Перевод между Кириллицей, Латиницей и Новой Латиницей (Ö, Ğ, Ş, Ç).",
    dirCyrToNew: "Кириллица ➔ Новая Латиница",
    dirOldToNew: "Старая Латиница ➔ Новая Латиница",
    dirCyrToOld: "Кириллица ➔ Действующая Латиница",
    dirLatToCyr: "Латиница ➔ Кириллица",
    fileDropTitle: "Перетащите файл Word (.docx) или Excel (.xlsx) сюда",
    fileDropSub: "или нажмите кнопку ниже для выбора",
    btnSelectDoc: "📂 Выбрать Word / Excel файл",
    formatNote: "🔒 Шрифты, цвета, таблицы и формулы Excel сохраняются на 100%!",
    btnConvertAlifbo: "Конвертировать Алфавит",
    alifboSuccessTitle: "Документ успешно переведен на новый алфавит!",
    btnDownloadResult: "Скачать готовый документ",

    liveEditorTitle: "✍️ Онлайн Редактор Текста (Быстрый перевод)",
    inputOriginalText: "Исходный Текст",
    outputConvertedText: "Результат",
    btnSample: "💡 Пример",
    btnClear: "🗑 Очистить",
    btnCopy: "📋 Копировать",
    btnRunConvert: "⚡ Конвертировать",

    transHeaderTitle: "🌐 AI Переводчик Документов и Текста (RU / UZ / EN)",
    transHeaderDesc: "Качественный перевод файлов Word, Excel, PDF и текстов между языками.",
    transRuUzDesc: "Перевод документов с русского на узбекский язык",
    transUzRuDesc: "Перевод документов с узбекского на русский язык",
    transEnUzDesc: "Перевод документов с английского на узбекский язык",
    transUzEnDesc: "Перевод документов с узбекского на английский язык",
    transDropTitle: "Перетащите файл для перевода сюда",
    transDropSub: "или нажмите кнопку ниже для выбора",
    btnSelectTrans: "📂 Выбрать Документ",
    transNote: "🔒 Сохраняются все таблицы, форматирование и стили документа.",
    btnRunTranslateDoc: "Перевести Документ",
    transSuccessTitle: "Документ успешно переведен!",
    transSuccessDesc: "Вы можете скачать переведенный файл",
    btnDownloadTrans: "Скачать переведенный документ",
    transLiveTitle: "✍️ Онлайн Переводчик Текста",
    transInputLabel: "Исходный Текст",
    transOutputLabel: "Результат Перевода",
    btnRunTranslate: "⚡ Перевести",

    aboutTitle: "ℹ️ О Программе и Поддержка Проекта",
    aboutSub: "Создатель программы и добровольный донат на развитие проекта.",
    cardCreatorLabel: "Автор Программы",
    btnCopyCard: "Скопировать номер карты (5614 6819 0834 3415)",
    donateHint: "Вы можете поддержать развитие программы через любое банковское приложение (Click, Payme, Zoomrad, Anorbank, Uzum и др.).",
    cardRawText: "Номер карты:",
    missionTitle: "🎯 Цель и Миссия Проекта",
    missionDesc: "Данный программный комплекс разработан Исмоиловым Нодиром с целью облегчения документооборота, качественной конвертации PDF в Word, перехода на новый узбекский алфавит и точного перевода документов с русского и английского языков.",
    footerCreator: "Создатель программы:",
    btnCancel: "✖ Отмена",
    resSuccessTitle: "Документ Word успешно подготовлен!",
    resSuccessDesc: "Все таблицы и тексты сохранены в редактируемом формате Word.",

    loadingTitle: "Документ обрабатывается...",
    loadingSub: "AI форматирует текст, шрифты и таблицы без ошибок",
    loadingPdfTitle: "PDF конвертируется в Word...",
    loadingPdfSub: "Все таблицы, тексты и изображения сохраняются на 100%",
    loadingTransTitle: "AI переводит документ...",
    loadingTransSub: "Искусственный интеллект выполняет качественный и связный перевод",
    loadingAlifboTitle: "Документ переводится на новый алфавит...",
    loadingAlifboSub: "Шрифты и таблицы переводятся на новый узбекский алфавит",
    loadingTimerPrefix: "Идет обработка: "
  },

  en: {
    brandSub: "PDF to Word, New Alphabet & AI Translation Studio",
    tabPdf: "📑 PDF Studio (15-in-1)",
    tabPdfDesc: "Merge, Word, Excel, Compress...",
    pdfStudioTitle: "📑 PDF Tools Suite (PDF Studio)",
    pdfStudioDesc: "All essential PDF tools: Word, Excel, PowerPoint, Merge, Compress, Rotate, Watermark and Protect.",
    toolPdfWordTitle: "PDF to Word",
    toolPdfWordDesc: "Convert to DOCX accurately",
    toolWordPdfTitle: "Word to PDF",
    toolWordPdfDesc: "Convert DOCX to PDF",
    toolMergeTitle: "Merge PDF",
    toolMergeDesc: "Combine multiple PDFs into one",
    toolSplitTitle: "Split PDF",
    toolSplitDesc: "Extract pages or separate",
    toolCompressTitle: "Compress PDF",
    toolCompressDesc: "Reduce file size cleanly",
    toolPdfExcelTitle: "PDF to Excel",
    toolPdfExcelDesc: "Extract tables to XLSX",
    toolExcelPdfTitle: "Excel to PDF",
    toolExcelPdfDesc: "Convert XLSX to PDF",
    toolPptPdfTitle: "PowerPoint to PDF",
    toolPptPdfDesc: "Convert PPTX slides to PDF",
    toolPdfImgTitle: "PDF to JPG/PNG",
    toolPdfImgDesc: "Export pages as images",
    toolImgPdfTitle: "JPG/PNG to PDF",
    toolImgPdfDesc: "Create PDF from images",
    toolRotateTitle: "Rotate PDF",
    toolRotateDesc: "Rotate 90°, 180°, 270°",
    toolWatermarkTitle: "Watermark",
    toolWatermarkDesc: "Stamp custom text watermark",
    toolPageNumTitle: "Page Numbers",
    toolPageNumDesc: "Add page numbers to PDF",
    toolProtectTitle: "Protect PDF",
    toolProtectDesc: "Encrypt PDF with password",
    toolUnlockTitle: "Unlock PDF",
    toolUnlockDesc: "Remove password protection",
    labelSplitMode: "Split Mode:",
    splitAllPages: "📦 Split all pages into individual PDFs in ZIP",
    splitCustomPages: "✂️ Selected pages (by range)",
    themeDark: "🌙 Dark",
    themeLight: "☀️ Light",
    tabAlifbo: "🔤 Alphabet Converter",
    tabAlifboDesc: "Cyrillic, Latin, New Latin",
    tabTranslate: "🌐 AI Translator",
    tabTranslateDesc: "Russian, Uzbek, English",
    tabAbout: "ℹ️ About the App",
    tabAboutDesc: "Author & Donate (Card, QR)",

    pdfHeaderTitle: "📑 Convert PDF Documents to Editable Word (.docx)",
    pdfHeaderDesc: "All tables, headings, font styles and images are preserved 100%.",
    pdfModeDirect: "Convert to Word (.docx) Only",
    pdfModeDirectSub: "Create an editable Word file without changing language/alphabet",
    pdfModeNewLat: "Convert to Word + New Latin",
    pdfModeNewLatSub: "Converts PDF to Word and switches to Ö, Ğ, Ş, Ç",
    pdfModeRuUz: "Convert to Word + Translate to Uzbek",
    pdfModeRuUzSub: "Converts Russian PDF to Word and translates into Uzbek",
    pdfDropTitle: "Drop your PDF file here",
    pdfDropSub: "or click the button below to browse",
    btnSelectPdf: "📂 Choose PDF File",
    pdfNote: "🔒 Large multi-page PDF documents are converted in just a few seconds.",
    btnConvertPdf: "Convert to Word (.docx)",
    btnDownloadDocx: "Download Word Document (.docx)",

    alifboHeaderTitle: "🔤 Uzbek Alphabet Converter (Word, Excel & Text)",
    alifboHeaderDesc: "Convert between Cyrillic, Latin, and New Latin (Ö, Ğ, Ş, Ç) with intact styles.",
    dirCyrToNew: "Cyrillic ➔ New Latin",
    dirOldToNew: "Old Latin ➔ New Latin",
    dirCyrToOld: "Cyrillic ➔ Official Latin",
    dirLatToCyr: "Latin ➔ Cyrillic",
    fileDropTitle: "Drop your Word (.docx) or Excel (.xlsx) file here",
    fileDropSub: "or click the button below to browse",
    btnSelectDoc: "📂 Choose Word / Excel File",
    formatNote: "🔒 Fonts, colors, tables and Excel formulas are preserved 100%!",
    btnConvertAlifbo: "Convert Alphabet",
    alifboSuccessTitle: "Document successfully converted to the new alphabet!",
    btnDownloadResult: "Download Converted File",

    liveEditorTitle: "✍️ Live Text Editor (Instant Conversion)",
    inputOriginalText: "Original Text",
    outputConvertedText: "Converted Text",
    btnSample: "💡 Sample",
    btnClear: "🗑 Clear",
    btnCopy: "📋 Copy",
    btnRunConvert: "⚡ Convert",

    transHeaderTitle: "🌐 AI Document & Text Translator (RU / UZ / EN)",
    transHeaderDesc: "High-accuracy fluent translation for Word, Excel, PDF, and text.",
    transRuUzDesc: "Translate documents from Russian to Uzbek",
    transUzRuDesc: "Translate documents from Uzbek to Russian",
    transEnUzDesc: "Translate documents from English to Uzbek",
    transUzEnDesc: "Translate documents from Uzbek to English",
    transDropTitle: "Drop the file to translate here",
    transDropSub: "or click the button below to browse",
    btnSelectTrans: "📂 Choose Document",
    transNote: "🔒 Preserves document tables, alignments, and text formatting.",
    btnRunTranslateDoc: "Translate Document",
    transSuccessTitle: "Document successfully translated!",
    transSuccessDesc: "You can download the translated file now",
    btnDownloadTrans: "Download Translated Document",
    transLiveTitle: "✍️ Live Text Translator",
    transInputLabel: "Original Text",
    transOutputLabel: "Translated Result",
    btnRunTranslate: "⚡ Translate",

    aboutTitle: "ℹ️ About the App & Project Support",
    aboutSub: "Program creator information and optional donation for future development.",
    cardCreatorLabel: "Program Creator",
    btnCopyCard: "Copy Card Number (5614 6819 0834 3415)",
    donateHint: "You can support the development of the project through any mobile banking app (Click, Payme, Zoomrad, Anorbank, Uzum, etc.).",
    cardRawText: "Card number:",
    missionTitle: "🎯 Purpose & Mission",
    missionDesc: "This software suite was created by Ismoilov Nodir to streamline workflow, enable lossless PDF-to-Word conversion, ease transition to the new Uzbek Latin alphabet, and provide accurate translations between Russian, Uzbek, and English.",
    footerCreator: "Program creator:",
    btnCancel: "✖ Cancel",
    resSuccessTitle: "Word document prepared successfully!",
    resSuccessDesc: "All tables and text blocks preserved in editable Word format.",

    loadingTitle: "Processing Document...",
    loadingSub: "AI is formatting text, fonts and tables accurately",
    loadingPdfTitle: "Converting PDF to Word...",
    loadingPdfSub: "All tables, texts and images are preserved 100%",
    loadingTransTitle: "AI is Translating Document...",
    loadingTransSub: "Artificial intelligence is translating the document accurately",
    loadingAlifboTitle: "Converting to New Alphabet...",
    loadingAlifboSub: "Fonts and tables are being updated to the new alphabet",
    loadingTimerPrefix: "In progress: "
  }
};

let currentLang = 'ru';

document.addEventListener('DOMContentLoaded', () => {
  // ------------------------------------------------------------------------
  // 1. Language Switcher (Default Russian)
  // ------------------------------------------------------------------------
  const savedLang = localStorage.getItem('alifba_lang') || 'ru';
  currentLang = savedLang;

  const langBtns = document.querySelectorAll('.lang-btn');
  langBtns.forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-lang') === currentLang);
    btn.addEventListener('click', () => {
      langBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentLang = btn.getAttribute('data-lang') || 'ru';
      localStorage.setItem('alifba_lang', currentLang);
      applyLanguage(currentLang);
    });
  });

  function applyLanguage(lang) {
    const dict = I18N[lang] || I18N.ru;
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });
    if (themeBtnLabel) {
      themeBtnLabel.textContent = (currentTheme === 'dark') ? (dict.themeDark || "Тёмная") : (dict.themeLight || "Светлая");
    }
    if (window.updatePdfStudioLang) {
      window.updatePdfStudioLang();
    }
  }

  // ------------------------------------------------------------------------
  // 1.1 Theme Switcher (Sky Light & Orange by default)
  // ------------------------------------------------------------------------
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const themeBtnIcon = themeToggleBtn ? themeToggleBtn.querySelector('.theme-btn-icon') : null;
  const themeBtnLabel = themeToggleBtn ? themeToggleBtn.querySelector('.theme-btn-label') : null;

  let currentTheme = localStorage.getItem('alifba_theme_v2') || 'light';

  function applyTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('alifba_theme_v2', theme);

    const dict = I18N[currentLang] || I18N.ru;
    if (theme === 'dark') {
      if (themeBtnIcon) themeBtnIcon.textContent = '🌙';
      if (themeBtnLabel) themeBtnLabel.textContent = dict.themeDark || "Тёмная";
    } else {
      if (themeBtnIcon) themeBtnIcon.textContent = '☀️';
      if (themeBtnLabel) themeBtnLabel.textContent = dict.themeLight || "Светлая";
    }
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
      const isDark = newTheme === 'dark';
      const toastMsg = currentLang === 'uz' 
        ? (isDark ? "🌙 Tungi mavzu yoqildi" : "☀️ Kunduzgi mavzu yoqildi")
        : (currentLang === 'en' 
            ? (isDark ? "🌙 Dark theme activated" : "☀️ Light theme activated")
            : (isDark ? "🌙 Тёмная тема активирована" : "☀️ Светлая тема активирована"));
      showToast(toastMsg);
    });
  }

  // Initial theme application
  applyTheme(currentTheme);

  // Initial language application (Russian by default)
  applyLanguage(currentLang);

  // ------------------------------------------------------------------------
  // Global Animated Central Loading Overlay Controller (with Live % & Status)
  // ------------------------------------------------------------------------
  const loadingOverlay = document.getElementById('loading-overlay');
  const loadingPercent = document.getElementById('loading-percent');
  const loadingProgressFill = document.getElementById('loading-progress-fill');
  const loadingStatusText = document.getElementById('loading-status-text');
  const loadingTitle = document.getElementById('loading-title');
  const loadingSubtitle = document.getElementById('loading-subtitle');
  const loadingTimerText = document.getElementById('loading-timer-text');
  let loadingInterval = null;
  let progressPollingInterval = null;
  let loadingSeconds = 0;

  function setProgressUI(percent, statusMsg = null) {
    const p = Math.min(100, Math.max(0, Math.round(percent)));
    if (loadingPercent) loadingPercent.textContent = `${p}%`;
    if (loadingProgressFill) loadingProgressFill.style.width = `${p}%`;
    if (statusMsg && loadingStatusText) {
      loadingStatusText.textContent = statusMsg;
    }
  }

  function showLoader(mode = 'auto', taskId = null) {
    if (!loadingOverlay) return;
    loadingSeconds = 0;
    setProgressUI(3, "Boshlanmoqda (3%)...");

    const dict = I18N[currentLang] || I18N.uz;

    if (mode === 'pdf_to_word' || mode === 'pdf_direct') {
      if (loadingTitle) loadingTitle.textContent = dict.loadingPdfTitle || "PDF Wordga O‘tkazilmoqda...";
      if (loadingSubtitle) loadingSubtitle.textContent = dict.loadingPdfSub || "Barcha jadvallar, matnlar va rasmlar xatosiz tartiblanmoqda";
    } else if (mode.includes('ru_to_uz') || mode.includes('uz_to_ru') || mode.includes('en_to_uz') || mode.includes('uz_to_en')) {
      if (loadingTitle) loadingTitle.textContent = dict.loadingTransTitle || "AI Hujjatni Tarjima Qilmoqda...";
      if (loadingSubtitle) loadingSubtitle.textContent = dict.loadingTransSub || "Sun'iy intellekt matn mazmunini ravon va xatosiz tarjima qilmoqda";
    } else {
      if (loadingTitle) loadingTitle.textContent = dict.loadingAlifboTitle || "Hujjat Yangi Alifboga O‘girilmoqda...";
      if (loadingSubtitle) loadingSubtitle.textContent = dict.loadingAlifboSub || "Harflar, jadvallar va shriftlar Yangi Lotin formatiga o‘tkazilmoqda";
    }

    const timerPrefix = dict.loadingTimerPrefix || "Jarayon davom etmoqda: ";
    if (loadingTimerText) loadingTimerText.textContent = `${timerPrefix} 0s`;

    clearInterval(loadingInterval);
    loadingInterval = setInterval(() => {
      loadingSeconds++;
      if (loadingTimerText) loadingTimerText.textContent = `${timerPrefix} ${loadingSeconds}s`;
    }, 1000);

    // Real vaqtda serverdagi /api/task-progress/<taskId> dan foizni so'rab turish
    clearInterval(progressPollingInterval);
    if (taskId) {
      progressPollingInterval = setInterval(async () => {
        try {
          const resp = await fetch(`/api/task-progress/${taskId}`);
          if (resp.ok) {
            const data = await resp.json();
            if (data.success && typeof data.percent === 'number') {
              setProgressUI(data.percent, data.status);
            }
          }
        } catch (e) {
          // background polling safe
        }
      }, 250);
    }

    loadingOverlay.classList.add('active');
  }

  function hideLoader() {
    if (!loadingOverlay) return;
    clearInterval(loadingInterval);
    clearInterval(progressPollingInterval);
    setProgressUI(100, "Tayyor! Muvaffaqiyatli yakunlandi (100%)");
    setTimeout(() => {
      loadingOverlay.classList.remove('active');
    }, 450);
  }

  // ------------------------------------------------------------------------
  // 2. Tab Navigation (4 Distinct Modules)
  // ------------------------------------------------------------------------
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add('active');
      }
    });
  });

  // ------------------------------------------------------------------------
  // 3. Module Mode Selectors (Radio Cards)
  // ------------------------------------------------------------------------
  document.querySelectorAll('.mode-selector-grid').forEach(grid => {
    const cards = grid.querySelectorAll('.mode-radio-card');
    cards.forEach(card => {
      card.addEventListener('click', () => {
        cards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
      });
    });
  });

  // ------------------------------------------------------------------------
  // 4. File Upload Handler for Alifbo and Translate modules
  // ------------------------------------------------------------------------
  document.querySelectorAll('.tab-content:not(#module-pdf) .file-drop-area').forEach(dropZone => {
    const section = dropZone.closest('.tab-content');
    const fileInput = dropZone.querySelector('.file-input-el');
    const selectedPanel = section.querySelector('.selected-file-panel');
    const fileNameEl = section.querySelector('.target-file-name');
    const fileSizeEl = section.querySelector('.target-file-size');
    const btnCancel = section.querySelector('.btn-cancel-action');
    const btnProcess = section.querySelector('.btn-process-action');
    const resultPanel = section.querySelector('.result-panel');
    const downloadBtn = section.querySelector('.download-btn-target');

    let stagedFile = null;

    dropZone.addEventListener('click', (e) => {
      if (e.target !== fileInput) {
        fileInput.value = '';
        fileInput.click();
      }
    });

    ['dragenter', 'dragover'].forEach(evt => {
      dropZone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(evt => {
      dropZone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
      });
    });

    dropZone.addEventListener('drop', (e) => {
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        setFile(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener('change', () => {
      if (fileInput.files && fileInput.files.length > 0) {
        setFile(fileInput.files[0]);
      }
    });

    function setFile(file) {
      stagedFile = file;
      fileNameEl.textContent = file.name;
      fileSizeEl.textContent = formatBytes(file.size);
      selectedPanel.style.display = 'flex';
      if (resultPanel) resultPanel.style.display = 'none';
    }

    if (btnCancel) {
      btnCancel.addEventListener('click', () => {
        stagedFile = null;
        fileInput.value = '';
        selectedPanel.style.display = 'none';
        if (resultPanel) resultPanel.style.display = 'none';
      });
    }

    if (btnProcess) {
      btnProcess.addEventListener('click', async () => {
        if (!stagedFile) return;

        // Determine active mode from the radio cards in this section
        const activeRadio = section.querySelector('.mode-radio-card.active');
        const mode = activeRadio ? activeRadio.getAttribute('data-mode') : 'auto';

        const taskId = 'task_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);

        const formData = new FormData();
        formData.append('file', stagedFile);
        formData.append('mode', mode);
        formData.append('task_id', taskId);

        btnProcess.disabled = true;
        btnProcess.classList.add('loading');
        showLoader(mode, taskId);

        try {
          const resp = await fetch('/api/convert-file', {
            method: 'POST',
            body: formData
          });
          const res = await resp.json();

          if (res.success) {
            if (resultPanel && downloadBtn) {
              resultPanel.style.display = 'block';
              downloadBtn.href = res.download_url;
              downloadBtn.setAttribute('download', res.filename);
            }
            showToast(currentLang === 'ru' ? "Файл успешно обработан!" : (currentLang === 'en' ? "File prepared successfully!" : "Fayl muvaffaqiyatli tayyorlandi!"));
            if (typeof refreshCurrentUser === 'function') refreshCurrentUser();
          } else {
            if (res.limit_reached && typeof openVipModal === 'function') {
              openVipModal();
            } else if (res.need_auth && typeof openAuthModal === 'function') {
              openAuthModal('login');
            }
            showToast(res.error || "Xatolik yuz berdi!", true);
          }
        } catch (err) {
          showToast("Xatolik: " + err.message, true);
        } finally {
          btnProcess.disabled = false;
          btnProcess.classList.remove('loading');
          hideLoader();
        }
      });
    }
  });

  // ------------------------------------------------------------------------
  // 4b. PDF Studio Interactive Controller (15-in-1 Suite)
  // ------------------------------------------------------------------------
  const PDF_TOOLS_CONFIG = {
    pdf_to_word: {
      title: { uz: "PDF ➔ Word Konverteri", ru: "Конвертер PDF в Word", en: "PDF to Word Converter" },
      desc: { uz: "PDF faylni barcha jadvallar bilan Word (.docx) formatiga xatosiz o‘tkazing.", ru: "Конвертируйте PDF в редактируемый Word (.docx) со всеми таблицами.", en: "Convert PDF to editable Word (.docx) preserving all tables." },
      badgeClass: "badge-blue",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "PDF faylingizni bu yerga tashlang", ru: "Перетащите PDF файл сюда", en: "Drop your PDF file here" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Word (.docx) ga O‘tkazish", ru: "Конвертировать в Word", en: "Convert to Word" },
      optPanelId: "opt-panel-pdf_to_word"
    },
    word_to_pdf: {
      title: { uz: "Word ➔ PDF Konverteri", ru: "Конвертер Word в PDF", en: "Word to PDF Converter" },
      desc: { uz: "Word (.docx, .doc) hujjatini sifatli va o‘zgarmas PDF ga aylantiring.", ru: "Преобразуйте Word (.docx, .doc) в качественный PDF документ.", en: "Convert Word (.docx, .doc) documents into high-quality PDF." },
      badgeClass: "badge-blue-dark",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M12 18v-6"/><path d="m9 15 3 3 3-3"/></svg>',
      accept: ".docx,.doc",
      multiple: false,
      formatPill: "📄 Word (.docx, .doc)",
      dropTitle: { uz: "Word (.docx, .doc) faylni tashlang", ru: "Перетащите Word файл сюда", en: "Drop Word (.docx, .doc) file here" },
      btnSelect: { uz: "📂 Word Faylni Tanlash", ru: "📂 Выбрать Word файл", en: "📂 Select Word File" },
      btnAction: { uz: "PDF ga Aylantirish", ru: "Преобразовать в PDF", en: "Convert to PDF" },
      optPanelId: null
    },
    merge: {
      title: { uz: "PDF larni Birlashtirish (Merge PDF)", ru: "Объединение PDF файлов", en: "Merge PDF Files" },
      desc: { uz: "Bir nechta PDF fayllarni tanlang va ularni bitta yaxlit hujjatga birlashtiring.", ru: "Выберите несколько PDF файлов и соедините их в один общий документ.", en: "Combine multiple PDF documents into a single unified file." },
      badgeClass: "badge-red",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>',
      accept: ".pdf",
      multiple: true,
      formatPill: "📑 2 yoki undan ortiq .PDF",
      dropTitle: { uz: "Bir nechta PDF fayllarni bu yerga tashlang", ru: "Перетащите несколько PDF файлов сюда", en: "Drop multiple PDF files here" },
      btnSelect: { uz: "📂 PDF Fayllarni Tanlash (Bir nechta)", ru: "📂 Выбрать PDF файлы (несколько)", en: "📂 Select Multiple PDFs" },
      btnAction: { uz: "Birlashtirish (Merge)", ru: "Объединить PDF", en: "Merge PDFs" },
      optPanelId: null
    },
    split: {
      title: { uz: "PDF ni Ajratish va Kesish (Split PDF)", ru: "Разделение PDF файлов", en: "Split PDF Pages" },
      desc: { uz: "PDF sahifalarini ajratib, har bir sahifani alohida PDF qilib bitta qulay ZIP arxivda yuklab oling.", ru: "Разделите страницы PDF и скачайте каждую отдельным PDF в едином ZIP архиве.", en: "Split PDF pages into separate documents and download as a single ZIP archive." },
      badgeClass: "badge-orange",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "Ajratiladigan PDF faylni tashlang", ru: "Перетащите PDF файл для разделения", en: "Drop PDF file to split" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Sahifalarni Ajratish (ZIP)", ru: "Разделить в ZIP архив", en: "Split to ZIP Archive" },
      optPanelId: "opt-panel-split"
    },
    compress: {
      title: { uz: "PDF Hajmini Siqish (Compress PDF)", ru: "Сжатие PDF файлов", en: "Compress PDF" },
      desc: { uz: "Sifatni saqlagan holda PDF hajmini (MB) sezilarli darajada kamaytiring.", ru: "Уменьшите размер PDF документа при сохранении высокого качества.", en: "Reduce PDF file size without noticeable loss of quality." },
      badgeClass: "badge-green",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 14 10 14 10 20"/><polyline points="20 10 14 10 14 4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "Siqiladigan PDF faylni tashlang", ru: "Перетащите PDF файл для сжатия", en: "Drop PDF file to compress" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Hajmni Siqish", ru: "Сжать PDF", en: "Compress PDF" },
      optPanelId: "opt-panel-compress"
    },
    pdf_to_excel: {
      title: { uz: "PDF ➔ Excel Jadvallar", ru: "Конвертер PDF в Excel", en: "PDF to Excel Converter" },
      desc: { uz: "PDF dagi barcha jadvallarni avtomatik aniqlab Excel (.xlsx) ga ko‘chiring.", ru: "Извлеките все таблицы из PDF файла в формат Excel (.xlsx).", en: "Extract all tables from PDF into editable Excel (.xlsx) sheets." },
      badgeClass: "badge-emerald",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/><path d="M9 3v18"/><path d="M15 3v18"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "Jadvalli PDF faylni tashlang", ru: "Перетащите PDF файл с таблицами", en: "Drop PDF file with tables" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Excel (.xlsx) ga O‘tkazish", ru: "Экспортировать в Excel", en: "Convert to Excel" },
      optPanelId: null
    },
    excel_to_pdf: {
      title: { uz: "Excel ➔ PDF Konverteri", ru: "Конвертер Excel в PDF", en: "Excel to PDF Converter" },
      desc: { uz: "Excel (.xlsx, .xls) jadvallarini toza va sifatli PDF ga aylantiring.", ru: "Преобразуйте таблицы Excel в идеальный PDF документ.", en: "Convert Excel (.xlsx, .xls) spreadsheets to clean PDF." },
      badgeClass: "badge-teal",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><rect x="8" y="12" width="8" height="6"/></svg>',
      accept: ".xlsx,.xls",
      multiple: false,
      formatPill: "📊 Excel (.xlsx, .xls)",
      dropTitle: { uz: "Excel faylingizni bu yerga tashlang", ru: "Перетащите Excel файл сюда", en: "Drop your Excel file here" },
      btnSelect: { uz: "📂 Excel Faylni Tanlash", ru: "📂 Выбрать Excel файл", en: "📂 Select Excel File" },
      btnAction: { uz: "PDF ga Aylantirish", ru: "Преобразовать в PDF", en: "Convert to PDF" },
      optPanelId: null
    },
    ppt_to_pdf: {
      title: { uz: "PowerPoint ➔ PDF Konverteri", ru: "Конвертер PowerPoint в PDF", en: "PowerPoint to PDF Converter" },
      desc: { uz: "Taqdimot (.pptx, .ppt) slaydlarini yuqori sifatli PDF ga aylantiring.", ru: "Преобразуйте презентации PowerPoint в качественный PDF формат.", en: "Convert PowerPoint (.pptx, .ppt) slides to PDF." },
      badgeClass: "badge-amber",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
      accept: ".pptx,.ppt",
      multiple: false,
      formatPill: "📽️ PPTX (.pptx, .ppt)",
      dropTitle: { uz: "PowerPoint faylni bu yerga tashlang", ru: "Перетащите PowerPoint файл сюда", en: "Drop PowerPoint file here" },
      btnSelect: { uz: "📂 Taqdimotni Tanlash", ru: "📂 Выбрать презентацию", en: "📂 Select Presentation" },
      btnAction: { uz: "PDF ga Aylantirish", ru: "Преобразовать в PDF", en: "Convert to PDF" },
      optPanelId: null
    },
    pdf_to_images: {
      title: { uz: "PDF ➔ Rasmlar (JPG/PNG)", ru: "Конвертер PDF в Картинки", en: "PDF to Images (JPG/PNG)" },
      desc: { uz: "PDF ning har bir sahifasini alohida sifatli rasm qilib ZIP arxivda oling.", ru: "Преобразуйте каждую страницу PDF в качественное изображение в ZIP.", en: "Export all PDF pages as separate images in a ZIP archive." },
      badgeClass: "badge-yellow",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "PDF faylingizni bu yerga tashlang", ru: "Перетащите PDF файл сюда", en: "Drop your PDF file here" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Rasmlarga O‘tkazish (ZIP)", ru: "Экспортировать в картинки", en: "Export to Images" },
      optPanelId: "opt-panel-pdf_to_images"
    },
    images_to_pdf: {
      title: { uz: "Rasmlar ➔ PDF (JPG to PDF)", ru: "Конвертер картинок в PDF", en: "Images to PDF (JPG to PDF)" },
      desc: { uz: "Bir yoki bir nechta JPG/PNG rasmlarni bitta PDF kitobga aylantiring.", ru: "Объедините несколько картинок JPG/PNG в один PDF документ.", en: "Combine one or more JPG/PNG images into a single PDF document." },
      badgeClass: "badge-violet",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><circle cx="10" cy="13" r="2"/><path d="m20 17-2.5-2.5a2 2 0 0 0-2.8 0L8 21"/></svg>',
      accept: ".jpg,.jpeg,.png,.webp,.bmp",
      multiple: true,
      formatPill: "🖼️ Rasmlar (.jpg, .png...)",
      dropTitle: { uz: "Bir yoki bir nechta rasmlarni tashlang", ru: "Перетащите одну или несколько картинок сюда", en: "Drop one or multiple images here" },
      btnSelect: { uz: "📂 Rasmlarni Tanlash", ru: "📂 Выбрать картинки", en: "📂 Select Images" },
      btnAction: { uz: "PDF Hujjat Yaratish", ru: "Создать PDF документ", en: "Create PDF Document" },
      optPanelId: null
    },
    rotate: {
      title: { uz: "PDF ni Burish (Rotate PDF)", ru: "Поворот страниц PDF", en: "Rotate PDF Pages" },
      desc: { uz: "Noto‘g‘ri yoki teskari turgan sahifalarni 90°, 180° yoki 270° ga burib to‘g‘rilang.", ru: "Поверните нужные или все страницы документа на 90°, 180° или 270°.", en: "Rotate specific or all pages by 90°, 180°, or 270°." },
      badgeClass: "badge-cyan",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><polyline points="21 3 21 8 16 8"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "Buriladigan PDF faylni tashlang", ru: "Перетащите PDF файл для поворота", en: "Drop PDF file to rotate" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Sahifalarni Burish", ru: "Повернуть страницы", en: "Rotate Pages" },
      optPanelId: "opt-panel-rotate"
    },
    watermark: {
      title: { uz: "Suv Belgisi Qo‘yish (Watermark)", ru: "Водяной знак на PDF", en: "Watermark PDF" },
      desc: { uz: "PDF sahifalariga maxfiy matn, tashkilot nomi yoki mualliflik belgisini tushiring.", ru: "Добавьте водяной знак с вашим текстом по диагонали каждой страницы.", en: "Stamp a custom text watermark diagonally across each page." },
      badgeClass: "badge-pink",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "Suv belgisi qo‘yiladigan PDF ni tashlang", ru: "Перетащите PDF для добавления знака", en: "Drop PDF to watermark" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Suv Belgisini Qo‘yish", ru: "Добавить водяной знак", en: "Add Watermark" },
      optPanelId: "opt-panel-watermark"
    },
    page_numbers: {
      title: { uz: "Sahifa Raqamlari (Page Numbers)", ru: "Нумерация страниц PDF", en: "Add Page Numbers" },
      desc: { uz: "Barcha sahifalarga tartib bilan sahifa raqamlarini avtomatik qo‘yib chiqing.", ru: "Автоматически добавьте красивые номера на все страницы документа.", en: "Add page numbers automatically to all pages of your PDF." },
      badgeClass: "badge-purple",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M8 7h6"/><path d="M8 11h8"/><path d="M8 15h4"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "Raqamlanadigan PDF faylni tashlang", ru: "Перетащите PDF для нумерации", en: "Drop PDF to number" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Sahifalarni Raqamlash", ru: "Добавить номера", en: "Add Numbers" },
      optPanelId: "opt-panel-page_numbers"
    },
    protect: {
      title: { uz: "PDF ga Parol Qo‘yish (Protect PDF)", ru: "Защита PDF паролем", en: "Protect PDF with Password" },
      desc: { uz: "Hujjatni ochish uchun maxfiy parol o‘rnating va AES-256 bilan shifrlang.", ru: "Установите надежный пароль и зашифруйте PDF алгоритмом AES-256.", en: "Secure your document with password encryption (AES-256)." },
      badgeClass: "badge-slate",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "Himoyalanadigan PDF faylni tashlang", ru: "Перетащите PDF для защиты", en: "Drop PDF to protect" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Parol bilan Himoyalash", ru: "Защитить паролем", en: "Protect with Password" },
      optPanelId: "opt-panel-protect"
    },
    unlock: {
      title: { uz: "Parolni Olib Tashlash (Unlock PDF)", ru: "Снять защиту с PDF", en: "Unlock Protected PDF" },
      desc: { uz: "Parolli PDF faylning parolini olib tashlab, erkin foydalaniladigan qiling.", ru: "Удалите пароль с защищенного PDF документа для свободного доступа.", en: "Remove password protection from your encrypted PDF." },
      badgeClass: "badge-indigo",
      iconSvg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>',
      accept: ".pdf",
      multiple: false,
      formatPill: "📑 .PDF",
      dropTitle: { uz: "Parolli PDF faylingizni bu yerga tashlang", ru: "Перетащите защищенный PDF сюда", en: "Drop protected PDF here" },
      btnSelect: { uz: "📂 PDF Faylni Tanlash", ru: "📂 Выбрать PDF файл", en: "📂 Select PDF File" },
      btnAction: { uz: "Parolni Olib Tashlash", ru: "Снять защиту", en: "Unlock PDF" },
      optPanelId: "opt-panel-unlock"
    }
  };

  function initPdfStudio() {
    const pdfSection = document.getElementById('module-pdf');
    if (!pdfSection) return;

    let activeTool = 'pdf_to_word';
    let stagedPdfFiles = [];

    const toolCards = pdfSection.querySelectorAll('.pdf-tool-card');
    const wsTitle = document.getElementById('pdf-workspace-title');
    const wsDesc = document.getElementById('pdf-workspace-desc');
    const wsIcon = document.getElementById('pdf-workspace-icon');
    const wsPill = document.getElementById('pdf-workspace-pill');
    const optPanels = pdfSection.querySelectorAll('.tool-opt-panel');

    const dropZone = document.getElementById('pdf-tool-drop-zone');
    const fileInput = document.getElementById('pdf-tool-file-input');
    const dropTitle = document.getElementById('pdf-drop-title');
    const btnSelectText = document.getElementById('pdf-btn-select-text');
    const formatPills = document.getElementById('pdf-tool-format-pills');

    const selectedBox = document.getElementById('pdf-tool-selected-box');
    const fileNameEl = document.getElementById('pdf-tool-file-name');
    const fileSizeEl = document.getElementById('pdf-tool-file-size');
    const multiListEl = document.getElementById('pdf-tool-multi-list');
    const btnCancel = document.getElementById('pdf-tool-btn-cancel');
    const btnProcess = document.getElementById('pdf-tool-btn-process');
    const btnProcessText = document.getElementById('pdf-tool-btn-process-text');

    const resultBox = document.getElementById('pdf-tool-result-box');
    const resultTitle = document.getElementById('pdf-tool-result-title');
    const downloadBtn = document.getElementById('pdf-tool-download-btn');
    const downloadBtnText = document.getElementById('pdf-tool-download-btn-text');

    // Radios inside options
    pdfSection.querySelectorAll('.opt-radios').forEach(group => {
      const btns = group.querySelectorAll('.opt-radio-btn');
      btns.forEach(b => {
        b.addEventListener('click', () => {
          btns.forEach(x => x.classList.remove('active'));
          b.classList.add('active');
          if (group.id === 'split-mode-radios') {
            const isCustom = b.getAttribute('data-val') === 'custom';
            const wrap = document.getElementById('split-custom-input-wrap');
            if (wrap) wrap.style.display = isCustom ? 'block' : 'none';
          }
        });
      });
    });

    // Tool Card switching
    toolCards.forEach(card => {
      card.addEventListener('click', () => {
        toolCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        activeTool = card.getAttribute('data-tool') || 'pdf_to_word';
        applyToolConfig(activeTool);
      });
    });

    function applyToolConfig(toolKey) {
      const cfg = PDF_TOOLS_CONFIG[toolKey] || PDF_TOOLS_CONFIG.pdf_to_word;
      const lang = currentLang || 'ru';

      if (wsTitle) wsTitle.textContent = (cfg.title && cfg.title[lang]) || (cfg.title && cfg.title.ru) || cfg.title.uz;
      if (wsDesc) wsDesc.textContent = (cfg.desc && cfg.desc[lang]) || (cfg.desc && cfg.desc.ru) || cfg.desc.uz;
      if (wsPill) wsPill.textContent = cfg.formatPill || '.PDF';

      if (wsIcon) {
        wsIcon.className = 'tool-badge-icon workspace-current-icon ' + cfg.badgeClass;
        wsIcon.innerHTML = cfg.iconSvg;
      }

      // Hide all option panels, show relevant
      optPanels.forEach(p => p.style.display = 'none');
      if (cfg.optPanelId) {
        const targetPanel = document.getElementById(cfg.optPanelId);
        if (targetPanel) targetPanel.style.display = 'block';
      }

      // Update drop zone
      if (dropZone) dropZone.setAttribute('data-accept', cfg.accept);
      if (fileInput) {
        fileInput.accept = cfg.accept;
        fileInput.multiple = cfg.multiple;
        fileInput.value = '';
      }

      if (dropTitle) dropTitle.textContent = (cfg.dropTitle && cfg.dropTitle[lang]) || (cfg.dropTitle && cfg.dropTitle.ru) || cfg.dropTitle.uz;
      if (btnSelectText) btnSelectText.textContent = (cfg.btnSelect && cfg.btnSelect[lang]) || (cfg.btnSelect && cfg.btnSelect.ru) || cfg.btnSelect.uz;
      if (formatPills) formatPills.innerHTML = `<span class="pill pill-pdf">${cfg.formatPill}</span>`;
      if (btnProcessText) btnProcessText.textContent = (cfg.btnAction && cfg.btnAction[lang]) || (cfg.btnAction && cfg.btnAction.ru) || cfg.btnAction.uz;

      // Clear staged files
      stagedPdfFiles = [];
      if (selectedBox) selectedBox.style.display = 'none';
      if (resultBox) resultBox.style.display = 'none';
      if (multiListEl) {
        multiListEl.innerHTML = '';
        multiListEl.style.display = 'none';
      }
    }

    window.updatePdfStudioLang = () => {
      applyToolConfig(activeTool);
    };

    // Drop zone interactions
    if (dropZone && fileInput) {
      dropZone.addEventListener('click', (e) => {
        if (e.target !== fileInput) {
          fileInput.value = '';
          fileInput.click();
        }
      });

      ['dragenter', 'dragover'].forEach(evt => {
        dropZone.addEventListener(evt, (e) => {
          e.preventDefault();
          dropZone.classList.add('dragover');
        });
      });

      ['dragleave', 'drop'].forEach(evt => {
        dropZone.addEventListener(evt, (e) => {
          e.preventDefault();
          dropZone.classList.remove('dragover');
        });
      });

      dropZone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          setPdfFiles(Array.from(e.dataTransfer.files));
        }
      });

      fileInput.addEventListener('change', () => {
        if (fileInput.files && fileInput.files.length > 0) {
          setPdfFiles(Array.from(fileInput.files));
        }
      });
    }

    function setPdfFiles(filesList) {
      const cfg = PDF_TOOLS_CONFIG[activeTool] || PDF_TOOLS_CONFIG.pdf_to_word;
      if (!cfg.multiple) {
        stagedPdfFiles = [filesList[0]];
      } else {
        stagedPdfFiles = filesList;
      }

      if (stagedPdfFiles.length === 1) {
        const file = stagedPdfFiles[0];
        if (fileNameEl) fileNameEl.textContent = file.name;
        if (fileSizeEl) fileSizeEl.textContent = formatBytes(file.size);
        if (multiListEl) multiListEl.style.display = 'none';
      } else {
        const totalSize = stagedPdfFiles.reduce((acc, f) => acc + f.size, 0);
        if (fileNameEl) fileNameEl.textContent = `${stagedPdfFiles.length} ta fayl tanlandi`;
        if (fileSizeEl) fileSizeEl.textContent = `Umumiy hajm: ${formatBytes(totalSize)}`;
        if (multiListEl) {
          multiListEl.innerHTML = stagedPdfFiles.map((f, i) => `
            <div class="file-chip">
              <span class="file-chip-num">#${i + 1}</span>
              <span class="file-chip-name">${f.name}</span>
              <span class="file-chip-size">(${formatBytes(f.size)})</span>
            </div>
          `).join('');
          multiListEl.style.display = 'flex';
        }
      }

      if (selectedBox) selectedBox.style.display = 'flex';
      if (resultBox) resultBox.style.display = 'none';
    }

    if (btnCancel) {
      btnCancel.addEventListener('click', () => {
        stagedPdfFiles = [];
        if (fileInput) fileInput.value = '';
        if (selectedBox) selectedBox.style.display = 'none';
        if (resultBox) resultBox.style.display = 'none';
        if (multiListEl) {
          multiListEl.innerHTML = '';
          multiListEl.style.display = 'none';
        }
      });
    }

    if (btnProcess) {
      btnProcess.addEventListener('click', async () => {
        if (!stagedPdfFiles || stagedPdfFiles.length === 0) {
          showToast("Iltimos, avval fayl tanlang!", true);
          return;
        }

        const cfg = PDF_TOOLS_CONFIG[activeTool] || PDF_TOOLS_CONFIG.pdf_to_word;
        const taskId = 'task_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);

        const formData = new FormData();
        formData.append('tool', activeTool);
        formData.append('task_id', taskId);

        if (cfg.multiple) {
          stagedPdfFiles.forEach(f => formData.append('files', f));
        } else {
          formData.append('file', stagedPdfFiles[0]);
        }

        // Tool-specific options
        if (activeTool === 'pdf_to_word') {
          const activeRadio = pdfSection.querySelector('#opt-panel-pdf_to_word .mode-radio-card.active');
          formData.append('pdf_mode', activeRadio ? activeRadio.getAttribute('data-mode') : 'pdf_to_word');
        } else if (activeTool === 'split') {
          const splitModeOpt = document.querySelector('#split-mode-radios .opt-radio-btn.active');
          const modeVal = splitModeOpt ? splitModeOpt.getAttribute('data-val') : 'har_biri';
          if (modeVal === 'custom') {
            const rangeVal = document.getElementById('split-page-range')?.value.trim();
            formData.append('page_range', rangeVal || 'har_biri');
          } else {
            formData.append('page_range', 'har_biri');
          }
        } else if (activeTool === 'compress') {
          const activeOpt = document.querySelector('#compress-level-radios .opt-radio-btn.active');
          formData.append('quality', activeOpt ? activeOpt.getAttribute('data-val') : 'medium');
        } else if (activeTool === 'rotate') {
          const activeOpt = document.querySelector('#rotate-angle-radios .opt-radio-btn.active');
          formData.append('angle', activeOpt ? activeOpt.getAttribute('data-val') : '90');
        } else if (activeTool === 'watermark') {
          const wmText = document.getElementById('watermark-text-input')?.value || 'KONFIDENSIAL';
          const wmSize = document.getElementById('watermark-size-input')?.value || '38';
          formData.append('text', wmText);
          formData.append('fontsize', wmSize);
        } else if (activeTool === 'page_numbers') {
          const activeOpt = document.querySelector('#page-number-pos-radios .opt-radio-btn.active');
          formData.append('position', activeOpt ? activeOpt.getAttribute('data-val') : 'bottom-right');
        } else if (activeTool === 'protect') {
          const pw = document.getElementById('protect-password-input')?.value;
          if (!pw) {
            showToast("Iltimos, parol kiriting!", true);
            return;
          }
          formData.append('password', pw);
        } else if (activeTool === 'unlock') {
          const pw = document.getElementById('unlock-password-input')?.value || '';
          formData.append('password', pw);
        } else if (activeTool === 'pdf_to_images') {
          const fmtOpt = document.querySelector('#pdf-img-format-radios .opt-radio-btn.active');
          const dpiOpt = document.querySelector('#pdf-img-dpi-radios .opt-radio-btn.active');
          formData.append('format', fmtOpt ? fmtOpt.getAttribute('data-val') : 'png');
          formData.append('dpi', dpiOpt ? dpiOpt.getAttribute('data-val') : '150');
        }

        btnProcess.disabled = true;
        btnProcess.classList.add('loading');
        showLoader(activeTool, taskId);

        try {
          const resp = await fetch('/api/pdf-tool', {
            method: 'POST',
            body: formData
          });
          const res = await resp.json();

          if (res.success) {
            if (resultBox && downloadBtn) {
              resultBox.style.display = 'block';
              downloadBtn.href = res.download_url;
              downloadBtn.setAttribute('download', res.filename);
              if (resultTitle) resultTitle.textContent = res.message || "Amal muvaffaqiyatli bajarildi!";
              if (downloadBtnText) downloadBtnText.textContent = res.filename;
            }
            showToast(currentLang === 'ru' ? "Успешно выполнено!" : (currentLang === 'en' ? "Successfully completed!" : "Amal muvaffaqiyatli bajarildi!"));
            if (typeof refreshCurrentUser === 'function') refreshCurrentUser();
          } else {
            if (res.limit_reached && typeof openVipModal === 'function') {
              openVipModal();
            } else if (res.need_auth && typeof openAuthModal === 'function') {
              openAuthModal('login');
            }
            showToast(res.error || "Xatolik yuz berdi!", true);
          }
        } catch (err) {
          showToast("Xatolik: " + err.message, true);
        } finally {
          btnProcess.disabled = false;
          btnProcess.classList.remove('loading');
          hideLoader();
        }
      });
    }

    // Expose update for language changes
    window.updatePdfStudioLang = function() {
      applyToolConfig(activeTool);
    };

    // Initialize default tool
    applyToolConfig('pdf_to_word');
  }

  initPdfStudio();

  // ------------------------------------------------------------------------
  // 5. Alifbo Live Text Converter
  // ------------------------------------------------------------------------
  const alifboInput = document.querySelector('.alifbo-input');
  const alifboOutput = document.querySelector('.alifbo-output');
  const btnRunAlifbo = document.querySelector('.btn-run-alifbo-text');
  const btnSampleAlifbo = document.querySelector('.btn-sample-alifbo');
  const btnClearAlifbo = document.querySelector('.btn-clear-alifbo');
  const btnCopyAlifbo = document.querySelector('.btn-copy-alifbo');
  const alifboInCount = document.querySelector('.alifbo-in-counter');
  const alifboOutCount = document.querySelector('.alifbo-out-counter');
  const alifboSpeed = document.querySelector('.alifbo-speed');

  if (alifboInput && alifboOutput) {
    let alifboDebounce = null;
    alifboInput.addEventListener('input', () => {
      updateAlifboCounters();
      clearTimeout(alifboDebounce);
      alifboDebounce = setTimeout(doAlifboTextConversion, 400);
    });

    if (btnRunAlifbo) btnRunAlifbo.addEventListener('click', doAlifboTextConversion);
    if (btnClearAlifbo) {
      btnClearAlifbo.addEventListener('click', () => {
        alifboInput.value = '';
        alifboOutput.value = '';
        updateAlifboCounters();
      });
    }
    if (btnSampleAlifbo) {
      btnSampleAlifbo.addEventListener('click', () => {
        alifboInput.value = `Ўзбекистон Республикаси Президентининг Фармони.
O'zbekiston xalqi qadimiy boy madaniyatga ega bo'lib, uning tili davlat timsolidir.
Шаҳар ва қишлоқларда янги мактабlar, шифохоналар ва саноат корхоналари қурилмоқда. G'alaba bizniki!`;
        updateAlifboCounters();
        doAlifboTextConversion();
      });
    }
    if (btnCopyAlifbo) {
      btnCopyAlifbo.addEventListener('click', () => {
        copyToClipboard(alifboOutput.value);
      });
    }
  }

  async function doAlifboTextConversion() {
    const text = alifboInput.value.trim();
    if (!text) {
      alifboOutput.value = '';
      updateAlifboCounters();
      return;
    }
    const activeRadio = document.querySelector('#module-alifbo .mode-radio-card.active');
    const mode = activeRadio ? activeRadio.getAttribute('data-mode') : 'cyr_to_new_lat';

    try {
      const resp = await fetch('/api/convert-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, mode, o_variant: 'ö', apostrophe: 'ʼ' })
      });
      const res = await resp.json();
      if (res.success) {
        alifboOutput.value = res.converted_text;
        if (alifboSpeed) alifboSpeed.textContent = (res.stats.duration_ms || 0) + ' ms';
        updateAlifboCounters();
      } else if (res.limit_reached && typeof openVipModal === 'function') {
        openVipModal();
        showToast(res.error || "Kunlik limitga yetdingiz! VIP obuna oling.", true);
      }
    } catch (e) {
      console.error(e);
    }
  }

  function updateAlifboCounters() {
    if (!alifboInput || !alifboOutput) return;
    const inV = alifboInput.value;
    const inW = inV.trim() ? inV.trim().split(/\s+/).length : 0;
    if (alifboInCount) alifboInCount.textContent = `${inW} so‘z | ${inV.length} belgi`;

    const outV = alifboOutput.value;
    const outW = outV.trim() ? outV.trim().split(/\s+/).length : 0;
    if (alifboOutCount) alifboOutCount.textContent = `${outW} so‘z | ${outV.length} belgi`;
  }

  // ------------------------------------------------------------------------
  // 6. Translation Live Text Converter
  // ------------------------------------------------------------------------
  const transInput = document.querySelector('.trans-input');
  const transOutput = document.querySelector('.trans-output');
  const btnRunTrans = document.querySelector('.btn-run-trans-text');
  const btnSampleTrans = document.querySelector('.btn-sample-trans');
  const btnClearTrans = document.querySelector('.btn-clear-trans');
  const btnCopyTrans = document.querySelector('.btn-copy-trans');
  const transInCount = document.querySelector('.trans-in-counter');
  const transOutCount = document.querySelector('.trans-out-counter');
  const transSpeed = document.querySelector('.trans-speed');

  if (transInput && transOutput) {
    let transDebounce = null;
    transInput.addEventListener('input', () => {
      updateTransCounters();
      clearTimeout(transDebounce);
      transDebounce = setTimeout(doTransTextConversion, 500);
    });

    if (btnRunTrans) btnRunTrans.addEventListener('click', doTransTextConversion);
    if (btnClearTrans) {
      btnClearTrans.addEventListener('click', () => {
        transInput.value = '';
        transOutput.value = '';
        updateTransCounters();
      });
    }
    if (btnSampleTrans) {
      btnSampleTrans.addEventListener('click', () => {
        const activeRadio = document.querySelector('#module-translate .mode-radio-card.active');
        const mode = activeRadio ? activeRadio.getAttribute('data-mode') : 'ru_to_uz';
        if (mode === 'en_to_uz') {
          transInput.value = "Hello! Welcome to our system. This document contains essential guidelines for digital transformation.";
        } else if (mode === 'uz_to_en') {
          transInput.value = "Assalomu alaykum! Bizning tizimimizga xush kelibsiz. Ushbu hujjat raqamli texnologiyalar haqida maʼlumot beradi.";
        } else if (mode === 'uz_to_ru') {
          transInput.value = "Assalomu alaykum! Hurmatli hamkasblar, kelgusi yig‘ilish kun tartibi bilan tanishib chiqing.";
        } else {
          transInput.value = "Здравствуйте! Уважаемые коллеги, ознакомьтесь с повесткой дня предстоящего заседания.";
        }
        updateTransCounters();
        doTransTextConversion();
      });
    }
    if (btnCopyTrans) {
      btnCopyTrans.addEventListener('click', () => {
        copyToClipboard(transOutput.value);
      });
    }
  }

  async function doTransTextConversion() {
    const text = transInput.value.trim();
    if (!text) {
      transOutput.value = '';
      updateTransCounters();
      return;
    }
    const activeRadio = document.querySelector('#module-translate .mode-radio-card.active');
    const mode = activeRadio ? activeRadio.getAttribute('data-mode') : 'ru_to_uz';

    try {
      const resp = await fetch('/api/convert-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, mode })
      });
      const res = await resp.json();
      if (res.success) {
        transOutput.value = res.converted_text;
        if (transSpeed) transSpeed.textContent = (res.stats.duration_ms || 0) + ' ms';
        updateTransCounters();
      } else if (res.limit_reached && typeof openVipModal === 'function') {
        openVipModal();
        showToast(res.error || "Kunlik limitga yetdingiz! VIP obuna oling.", true);
      }
    } catch (e) {
      console.error(e);
    }
  }

  function updateTransCounters() {
    if (!transInput || !transOutput) return;
    const inV = transInput.value;
    const inW = inV.trim() ? inV.trim().split(/\s+/).length : 0;
    if (transInCount) transInCount.textContent = `${inW} words | ${inV.length} chars`;

    const outV = transOutput.value;
    const outW = outV.trim() ? outV.trim().split(/\s+/).length : 0;
    if (transOutCount) transOutCount.textContent = `${outW} words | ${outV.length} chars`;
  }

  // ------------------------------------------------------------------------
  // 7. Copy Card Number (Ismoilov Nodir)
  // ------------------------------------------------------------------------
  const btnCopyCard = document.getElementById('btn-copy-card');
  if (btnCopyCard) {
    btnCopyCard.addEventListener('click', () => {
      copyToClipboard(CARD_NUMBER);
      showToast(currentLang === 'ru' ? "Номер карты скопирован: 5614 6819 0834 3415" : (currentLang === 'en' ? "Card number copied: 5614 6819 0834 3415" : "Karta raqami nusxalandi: 5614 6819 0834 3415"));
    });
  }

  // ------------------------------------------------------------------------
  // Helper Functions
  // ------------------------------------------------------------------------
  async function copyToClipboard(text) {
    if (!text) return;
    try {
      await navigator.clipboard.writeText(text);
      showToast(currentLang === 'ru' ? "Скопировано в буфер обмена! 📋" : (currentLang === 'en' ? "Copied to clipboard! 📋" : "Nusxalandi! 📋"));
    } catch (e) {
      const el = document.createElement('textarea');
      el.value = text;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      showToast("Nusxalandi! 📋");
    }
  }

  function formatBytes(bytes, decimals = 1) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  let toastTimeout = null;
  const toast = document.getElementById('toast');
  function showToast(message, isError = false) {
    if (!toast) return;
    clearTimeout(toastTimeout);
    toast.textContent = message;
    toast.style.borderLeftColor = isError ? '#dc2626' : '#10b981';
    toast.classList.add('show');
    toastTimeout = setTimeout(() => {
      toast.classList.remove('show');
    }, 3500);
  }

  // ------------------------------------------------------------------------
  // 8. Foydalanuvchi Tizimi (Auth) va VIP Obuna Boshqaruvi
  // ------------------------------------------------------------------------
  let currentAuthUser = null;
  let currentSystemConfig = {
    card_number: '5614 6819 0834 3415',
    admin_telegram: 'alifbauz',
    vip_price: '25000'
  };

  const authModal = document.getElementById('auth-modal');
  const btnCloseAuthModal = document.getElementById('btn-close-auth-modal');
  const tabBtnLogin = document.getElementById('tab-btn-login');
  const tabBtnRegister = document.getElementById('tab-btn-register');
  const formUserLogin = document.getElementById('form-user-login');
  const formUserRegister = document.getElementById('form-user-register');
  const loginErrorBox = document.getElementById('login-error-box');
  const registerErrorBox = document.getElementById('register-error-box');
  const linkSwitchToRegister = document.getElementById('link-switch-to-register');
  const linkSwitchToLogin = document.getElementById('link-switch-to-login');

  const vipModal = document.getElementById('vip-payment-modal');
  const btnCloseVipPayModal = document.getElementById('btn-close-vip-pay-modal');
  const btnOpenVipModal = document.getElementById('btn-open-vip-modal');
  const btnCopyVipCard = document.getElementById('btn-copy-vip-card');
  const btnSendTgReceipt = document.getElementById('btn-send-tg-receipt');
  const vipPriceVal = document.getElementById('vip-price-val');
  const vipCardNumText = document.getElementById('vip-card-num-text');
  const vipTgUsername = document.getElementById('vip-tg-username');
  const vipUserLoginHint = document.getElementById('vip-user-login-hint');

  const authHeaderContainer = document.getElementById('auth-header-container');
  const announcementBanner = document.getElementById('announcement-banner');
  const announcementText = document.getElementById('announcement-text');

  function openAuthModal(tab = 'login') {
    if (!authModal) return;
    if (loginErrorBox) { loginErrorBox.style.display = 'none'; loginErrorBox.textContent = ''; }
    if (registerErrorBox) { registerErrorBox.style.display = 'none'; registerErrorBox.textContent = ''; }
    switchAuthTab(tab);
    authModal.classList.add('active');
  }

  function closeAuthModal() {
    if (authModal) authModal.classList.remove('active');
  }

  function switchAuthTab(tab) {
    if (tab === 'login') {
      if (tabBtnLogin) tabBtnLogin.classList.add('active');
      if (tabBtnRegister) tabBtnRegister.classList.remove('active');
      if (formUserLogin) formUserLogin.style.display = 'block';
      if (formUserRegister) formUserRegister.style.display = 'none';
    } else {
      if (tabBtnRegister) tabBtnRegister.classList.add('active');
      if (tabBtnLogin) tabBtnLogin.classList.remove('active');
      if (formUserRegister) formUserRegister.style.display = 'block';
      if (formUserLogin) formUserLogin.style.display = 'none';
    }
  }

  function openVipModal() {
    if (!vipModal) return;
    if (currentAuthUser && vipUserLoginHint) {
      vipUserLoginHint.textContent = currentAuthUser.username;
    } else if (vipUserLoginHint) {
      vipUserLoginHint.textContent = "loginingiz";
    }
    vipModal.classList.add('active');
  }

  function closeVipModal() {
    if (vipModal) vipModal.classList.remove('active');
  }

  async function refreshCurrentUser() {
    try {
      const resp = await fetch('/api/auth/me');
      const data = await resp.json();
      currentAuthUser = data.user || null;
      const sys = data.settings || data.system || {};
      const cardNum = sys.card_number || "5614 6819 0834 3415";
      const tgUser = sys.telegram_admin || sys.admin_telegram || "alifbauz";
      const vipPrice = (sys.vip_monthly_price || sys.vip_price || "25 000") + "";
      const dLimit = data.daily_limit || 5;

      currentSystemConfig = {
        card_number: cardNum,
        card_holder: sys.card_holder || "ISMOILOV NODIR",
        admin_telegram: tgUser,
        vip_price: vipPrice
      };

      if (vipPriceVal) vipPriceVal.textContent = vipPrice.replace(/\s*so'?m.*/i, '');
      if (vipCardNumText) vipCardNumText.textContent = cardNum;
      if (vipTgUsername) vipTgUsername.textContent = tgUser;
      if (btnSendTgReceipt) {
        btnSendTgReceipt.href = `https://t.me/${tgUser.replace('@', '')}`;
      }

      if (announcementBanner && announcementText) {
        if (sys.announcement_active && sys.announcement_text) {
          announcementText.textContent = sys.announcement_text;
          announcementBanner.style.display = 'block';
        } else {
          announcementBanner.style.display = 'none';
        }
      }

      if (authHeaderContainer) {
        if (data.logged_in && data.user) {
          const u = data.user;
          const used = u.used_today !== undefined ? u.used_today : 0;
          const limitBadge = u.is_vip
            ? `<span class="user-limit-pill vip" title="VIP Obuna faol">👑 VIP</span>`
            : `<span class="user-limit-pill free" title="Kunlik foydalanish: ${used}/${dLimit}">Bugun: ${used}/${dLimit} ta</span>`;

          authHeaderContainer.innerHTML = `
            <div class="user-badge-header">
              <span class="user-badge-avatar">👤</span>
              <span class="user-badge-name" title="${escapeHtml(u.name)} (${escapeHtml(u.username)})">${escapeHtml(u.name)}</span>
              ${limitBadge}
              <button id="btn-user-logout" class="btn btn-secondary btn-sm" title="Hisobdan chiqish" style="padding: 4px 8px; font-size: 0.8rem; margin-left: 2px;">
                🚪
              </button>
            </div>
          `;
          const btnLogout = document.getElementById('btn-user-logout');
          if (btnLogout) {
            btnLogout.addEventListener('click', handleUserLogout);
          }
        } else {
          const guestUsed = data.guest_used_today || 0;
          authHeaderContainer.innerHTML = `
            <span class="user-limit-pill free" title="Mehmon sifatida bugungi limit" style="margin-right: 6px;">Bugun: ${guestUsed}/${dLimit} ta</span>
            <button id="btn-open-auth-modal" class="btn btn-secondary btn-sm" type="button">
              <span>👤</span> <span>Kirish</span>
            </button>
          `;
        }
      }
    } catch (e) {
      console.warn('Auth status check error:', e);
    }
  }

  async function handleUserLogout() {
    try {
      const resp = await fetch('/api/auth/logout', { method: 'POST' });
      const res = await resp.json();
      if (res.success) {
        showToast("Hisobingizdan muvaffaqiyatli chiqildi!");
        refreshCurrentUser();
      }
    } catch (e) {
      console.error(e);
    }
  }

  function escapeHtml(text) {
    if (!text) return '';
    return String(text).replace(/[&<>"']/g, function(m) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m];
    });
  }

  // Event Listeners for Auth & VIP
  document.addEventListener('click', (e) => {
    if (e.target.closest('#btn-open-auth-modal')) {
      openAuthModal('login');
    }
  });

  if (btnCloseAuthModal) btnCloseAuthModal.addEventListener('click', closeAuthModal);
  if (tabBtnLogin) tabBtnLogin.addEventListener('click', () => switchAuthTab('login'));
  if (tabBtnRegister) tabBtnRegister.addEventListener('click', () => switchAuthTab('register'));
  if (linkSwitchToRegister) {
    linkSwitchToRegister.addEventListener('click', (e) => {
      e.preventDefault();
      switchAuthTab('register');
    });
  }
  if (linkSwitchToLogin) {
    linkSwitchToLogin.addEventListener('click', (e) => {
      e.preventDefault();
      switchAuthTab('login');
    });
  }

  if (btnOpenVipModal) btnOpenVipModal.addEventListener('click', openVipModal);
  if (btnCloseVipPayModal) btnCloseVipPayModal.addEventListener('click', closeVipModal);

  if (btnCopyVipCard) {
    btnCopyVipCard.addEventListener('click', () => {
      const cardNum = currentSystemConfig.card_number || "5614 6819 0834 3415";
      copyToClipboard(cardNum.replace(/\s+/g, ''));
      showToast("Karta raqami nusxalandi: " + cardNum);
    });
  }

  if (authModal) {
    authModal.addEventListener('click', (e) => {
      if (e.target === authModal) closeAuthModal();
    });
  }
  if (vipModal) {
    vipModal.addEventListener('click', (e) => {
      if (e.target === vipModal) closeVipModal();
    });
  }

  // Form Submissions
  if (formUserLogin) {
    formUserLogin.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (loginErrorBox) loginErrorBox.style.display = 'none';
      const username = (document.getElementById('login-username-input') || {}).value?.trim();
      const password = (document.getElementById('login-password-input') || {}).value;

      if (!username || !password) return;

      try {
        const resp = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });
        const res = await resp.json();
        if (res.success) {
          closeAuthModal();
          showToast(`Xush kelibsiz, ${res.user.name}! 👋`);
          formUserLogin.reset();
          refreshCurrentUser();
        } else {
          if (loginErrorBox) {
            loginErrorBox.textContent = res.error || "Login yoki parol noto‘g‘ri!";
            loginErrorBox.style.display = 'block';
          }
        }
      } catch (err) {
        if (loginErrorBox) {
          loginErrorBox.textContent = "Server bilan aloqa uzildi!";
          loginErrorBox.style.display = 'block';
        }
      }
    });
  }

  if (formUserRegister) {
    formUserRegister.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (registerErrorBox) registerErrorBox.style.display = 'none';
      const name = (document.getElementById('reg-name-input') || {}).value?.trim();
      const username = (document.getElementById('reg-username-input') || {}).value?.trim();
      const password = (document.getElementById('reg-password-input') || {}).value;

      if (!name || !username || !password) return;

      try {
        const resp = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, username, password })
        });
        const res = await resp.json();
        if (res.success) {
          closeAuthModal();
          showToast(`Tabriklaymiz, ${res.user.name}! Ro‘yxatdan muvaffaqiyatli o‘tdingiz! 🎉`);
          formUserRegister.reset();
          refreshCurrentUser();
        } else {
          if (registerErrorBox) {
            registerErrorBox.textContent = res.error || "Ro‘yxatdan o‘tishda xatolik yuz berdi!";
            registerErrorBox.style.display = 'block';
          }
        }
      } catch (err) {
        if (registerErrorBox) {
          registerErrorBox.textContent = "Server bilan aloqa uzildi!";
          registerErrorBox.style.display = 'block';
        }
      }
    });
  }

  // Initial load
  refreshCurrentUser();
});
