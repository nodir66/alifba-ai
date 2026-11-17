# -*- coding: utf-8 -*-
"""
Yangi O'zbek Alifbosi va Tarjima Dvigateli (Advanced Converter Engine)
Quyidagi barcha yo'nalishlarni to'liq qo'llab-quvvatlaydi:
1. Кирилл -> Yangi Lotin (Ö, Ğ, Ş, Ç)
2. Eski Lotin -> Yangi Lotin (Ö, Ğ, Ş, Ç)
3. Кирилл -> Amaldagi/Eski Lotin (Oʻ, Gʻ, Sh, Ch)
4. Lotin -> Кирилл (Ў, Ғ, Ш, Ч, Ю, Я, Ё, Е, Э)
5. Aralash -> Yangi Lotin
6. Rus tili -> O'zbek tili (AI Tarjima)
7. O'zbek tili -> Rus tili (AI Tarjima)
"""

import re
import time
import unicodedata
from translator_engine import translate_text

# Lug'at - Kirilldan Lotinga maxsus so'zlar
SMART_WORDS_CYR = {
    "цирк": "sirk", "циркнинг": "sirkning", "циркка": "sirkka", "циркда": "sirkda",
    "цемент": "sement", "цементнинг": "sementning", "цементlash": "sementlash",
    "центнер": "sentner", "центнердан": "sentnerdan",
    "цех": "sex", "цехи": "sexi", "цехлар": "sexlar", "цехда": "sexda",
    "циркуль": "sirkul", "цилиндр": "silindr",
    "концерт": "konsert", "концертлар": "konsertlar", "концерти": "konserti",
    "процент": "protsent", "процентлар": "protsentlar", "проценти": "protsenti",
    
    "акция": "aksiya", "акциядор": "aksiyador", "акциядорлик": "aksiyadorlik", "акциялар": "aksiyalar", "акцияси": "aksiyasi",
    "лекция": "leksiya", "лекциялар": "leksiyalar", "лекцияси": "leksiyasi",
    "секция": "seksiya", "секциялар": "seksiyalar", "секцияси": "seksiyasi",
    "функция": "funksiya", "функциялар": "funksiyalar", "функцияси": "funksiyasi",
    "инфекция": "infeksiya", "инфекциялар": "infeksiyalar", "инфекцияси": "infeksiyasi",
    "коллекция": "kolleksiya", "коллекциялар": "kolleksiyalar",
    "фракция": "fraksiya", "фракциялар": "fraksiyalar",
    "инъекция": "inyeksiya", "реакция": "reaksiya", "реакциялар": "reaksiyalar",
    "дирекция": "direksiya", "инспекция": "inspeksiya",
    "революция": "revolyutsiya", "эволюция": "evolyutsiya",
    "конституция": "konstitutsiya", "конституцияси": "konstitutsiyasi", "конституциявий": "konstitutsiyaviy",
    "провокация": "provokatsiya", "эвакуация": "evakuatsiya", "корпорация": "korporatsiya",
    "нация": "natsiya", "рация": "ratsiya", "доцент": "dotsent", "офицер": "ofitser",
    
    "январь": "yanvar", "февраль": "fevral", "апрель": "aprel",
    "июнь": "iyun", "июль": "iyul", "сентябрь": "sentabr",
    "октябрь": "oktabr", "ноябрь": "noyabr", "декабрь": "dekabr",
    
    "лагерь": "lager", "рубль": "rubl", "роль": "rol", "роли": "roli",
    "пароль": "parol", "пароли": "paroli", "пароллар": "parollar",
    "контроль": "kontrol", "модель": "model", "модели": "modeli",
    "фестиваль": "festival", "альбом": "albom",
    "автомобиль": "avtomobil", "автомобиллар": "avtomobillar",
    "медаль": "medal", "педаль": "pedal", "деталь": "detal",
    "асфальт": "asfalt", "культура": "kultura", "фильм": "film",
    "мультфильм": "multfilm", "пальто": "palto", "бульвар": "bulvar",
    "спектакль": "spektakl", "ансамбль": "ansambl", "батальон": "batalyon",
    "почтальон": "poçtalyon", "павильон": "pavilyon", "бульон": "bulyon",
    "объект": "obyekt", "субъект": "subyekt", "объектив": "obyektiv", "субъектив": "subyektiv"
}

# Himoyalangan havolalar, elektron pochtalar, yo'llar
PROTECTED_PATTERN = re.compile(
    r'(https?://[^\s<>"\']+|www\.[^\s<>"\']+|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+|[A-Za-z]:\\[^\s<>"\']+)'
)

CYR_VOWELS = set("аеёиоуэюяўАЕЁИОУЭЮЯЎaeiouöõAEIOUÖÕ")
APOSTROPHE_CHARS_REGEX = r"['`’‘ʻ´\"»«£^~]"


class UzbekTransliterator:
    def __init__(self, o_variant='ö', apostrophe_style='ʼ'):
        self.set_settings(o_variant, apostrophe_style)

    def set_settings(self, o_variant='ö', apostrophe_style='ʼ'):
        self.o_variant = 'õ' if o_variant in ['õ', 'tilde'] else 'ö'
        if self.o_variant == 'õ':
            self.O_CHAR = 'Õ'
            self.o_char = 'õ'
        else:
            self.O_CHAR = 'Ö'
            self.o_char = 'ö'

        self.G_CHAR = 'Ğ'
        self.g_char = 'ğ'
        self.SH_CHAR = 'Ş'
        self.sh_char = 'ş'
        self.CH_CHAR = 'Ç'
        self.ch_char = 'ç'
        self.APOSTROPHE = apostrophe_style

    def detect_script(self, text):
        if not text:
            return 'empty'
        cyr_count = len(re.findall(r'[\u0400-\u04FF]', text))
        old_lat_matches = len(re.findall(r"[oOgG]['`’‘ʻ´\"]|[sScC][hH]", text))
        lat_count = len(re.findall(r'[a-zA-Z]', text))

        if cyr_count > 0 and old_lat_matches > 0:
            return 'mixed'
        elif cyr_count > 0 and cyr_count >= lat_count * 0.3:
            return 'cyr'
        elif old_lat_matches > 0 or lat_count > 0:
            return 'old_lat'
        return 'auto'

    def _match_case(self, original_word, converted_word):
        if original_word.isupper() and len(original_word) > 1:
            return converted_word.upper()
        if original_word.istitle():
            return converted_word.capitalize()
        return converted_word

    # ------------------------------------------------------------------------
    # 1. Eski Lotin -> Yangi Lotin (Ö, Ğ, Ş, Ç)
    # ------------------------------------------------------------------------
    def convert_old_latin_to_new(self, text, stats=None):
        if not text:
            return text

        tokens = []
        last_end = 0
        for m in PROTECTED_PATTERN.finditer(text):
            start, end = m.span()
            if start > last_end:
                tokens.append((text[last_end:start], False))
            tokens.append((text[start:end], True))
            last_end = end
        if last_end < len(text):
            tokens.append((text[last_end:], False))

        res_parts = []
        for part, is_protected in tokens:
            if is_protected:
                res_parts.append(part)
                continue

            t = part
            if stats is not None:
                stats['o_count'] += len(re.findall(r'[oO]' + APOSTROPHE_CHARS_REGEX, t))
                stats['g_count'] += len(re.findall(r'[gG]' + APOSTROPHE_CHARS_REGEX, t))
                stats['sh_count'] += len(re.findall(r'[sS][hH]', t))
                stats['ch_count'] += len(re.findall(r'[cC][hH]', t))

            # O' -> Ö
            t = re.sub(r'O' + APOSTROPHE_CHARS_REGEX, self.O_CHAR, t)
            t = re.sub(r'o' + APOSTROPHE_CHARS_REGEX, self.o_char, t)

            # G' -> Ğ
            t = re.sub(r'G' + APOSTROPHE_CHARS_REGEX, self.G_CHAR, t)
            t = re.sub(r'g' + APOSTROPHE_CHARS_REGEX, self.g_char, t)

            # SH va CH
            t = re.sub(r'SH(?=[A-ZÖĞŞÇ])', self.SH_CHAR, t)
            t = re.sub(r'CH(?=[A-ZÖĞŞÇ])', self.CH_CHAR, t)
            t = re.sub(r'Sh', self.SH_CHAR, t)
            t = re.sub(r'SH', self.SH_CHAR, t)
            t = re.sub(r'sh', self.sh_char, t)
            t = re.sub(r'Ch', self.CH_CHAR, t)
            t = re.sub(r'CH', self.CH_CHAR, t)
            t = re.sub(r'ch', self.ch_char, t)

            # Tutuq belgisi
            alph = r'a-zA-Z' + self.O_CHAR + self.o_char + self.G_CHAR + self.g_char + self.SH_CHAR + self.sh_char + self.CH_CHAR + self.ch_char
            t = re.sub(r'(?<=[' + alph + r'])' + APOSTROPHE_CHARS_REGEX + r'(?=[' + alph + r'])', self.APOSTROPHE, t)

            res_parts.append(t)

        return "".join(res_parts)

    # ------------------------------------------------------------------------
    # 2. Кирилл -> Yangi Lotin (Ö, Ğ, Ş, Ç)
    # ------------------------------------------------------------------------
    def convert_cyrillic_to_new(self, text, stats=None):
        return self._convert_cyrillic_general(text, target_type='new', stats=stats)

    # ------------------------------------------------------------------------
    # 3. Кирилл -> Amaldagi/Eski Lotin (1995: Oʻ, Gʻ, Sh, Ch)
    # ------------------------------------------------------------------------
    def convert_cyrillic_to_old(self, text, stats=None):
        return self._convert_cyrillic_general(text, target_type='old', stats=stats)

    def _convert_cyrillic_general(self, text, target_type='new', stats=None):
        if not text:
            return text

        tokens = []
        last_end = 0
        for m in PROTECTED_PATTERN.finditer(text):
            start, end = m.span()
            if start > last_end:
                tokens.append((text[last_end:start], False))
            tokens.append((text[start:end], True))
            last_end = end
        if last_end < len(text):
            tokens.append((text[last_end:], False))

        res_parts = []
        word_token_pattern = re.compile(r'([а-яА-ЯёЁўЎғҒқҚҳҲъЪьЬ]+)')

        for part, is_protected in tokens:
            if is_protected:
                res_parts.append(part)
                continue

            sub_parts = []
            last_w_end = 0
            for wm in word_token_pattern.finditer(part):
                w_start, w_end = wm.span()
                if w_start > last_w_end:
                    sub_parts.append(part[last_w_end:w_start])
                w = wm.group(1)
                sub_parts.append(self._convert_cyrillic_word_typed(w, target_type=target_type, stats=stats))
                last_w_end = w_end
            if last_w_end < len(part):
                sub_parts.append(part[last_w_end:])

            res_parts.append("".join(sub_parts))

        return "".join(res_parts)

    def _convert_cyrillic_word_typed(self, word, target_type='new', stats=None):
        if not word:
            return word

        lower_word = word.lower()

        # Lug'at tekshiruvi
        if lower_word in SMART_WORDS_CYR:
            cand = SMART_WORDS_CYR[lower_word]
            if target_type == 'old':
                cand = cand.replace('ö', "oʻ").replace('Ö', "Oʻ")
                cand = cand.replace('ğ', "gʻ").replace('Ğ', "Gʻ")
                cand = cand.replace('ş', "sh").replace('Ş', "Sh")
                cand = cand.replace('ç', "ch").replace('Ç', "Ch")
            else:
                if self.o_char != 'ö':
                    cand = cand.replace('ö', self.o_char).replace('Ö', self.O_CHAR)
            return self._match_case(word, cand)

        for base, repl in SMART_WORDS_CYR.items():
            if lower_word.startswith(base) and len(lower_word) > len(base):
                suffix = lower_word[len(base):]
                suffix_conv = self._convert_cyrillic_phonetic_typed(suffix, target_type=target_type, prev_char=base[-1], stats=stats)
                cand = repl + suffix_conv
                if target_type == 'old':
                    cand = cand.replace('ö', "oʻ").replace('Ö', "Oʻ")
                    cand = cand.replace('ğ', "gʻ").replace('Ğ', "Gʻ")
                    cand = cand.replace('ş', "sh").replace('Ş', "Sh")
                    cand = cand.replace('ç', "ch").replace('Ç', "Ch")
                else:
                    if self.o_char != 'ö':
                        cand = cand.replace('ö', self.o_char).replace('Ö', self.O_CHAR)
                return self._match_case(word, cand)

        return self._convert_cyrillic_phonetic_typed(word, target_type=target_type, stats=stats)

    def _convert_cyrillic_phonetic_typed(self, text, target_type='new', prev_char=None, stats=None):
        chars = list(text)
        n = len(chars)
        out = []

        is_new = (target_type == 'new')
        o_rep_l = self.o_char if is_new else "oʻ"
        o_rep_u = self.O_CHAR if is_new else "Oʻ"
        g_rep_l = self.g_char if is_new else "gʻ"
        g_rep_u = self.G_CHAR if is_new else "Gʻ"
        sh_rep_l = self.sh_char if is_new else "sh"
        sh_rep_u = self.SH_CHAR if is_new else "Sh"
        ch_rep_l = self.ch_char if is_new else "ch"
        ch_rep_u = self.CH_CHAR if is_new else "Ch"

        for i in range(n):
            ch = chars[i]
            prev_ch = chars[i - 1] if i > 0 else prev_char
            next_ch = chars[i + 1] if i + 1 < n else None
            is_next_upper = next_ch.isupper() if next_ch and next_ch.isalpha() else False

            # E / e
            if ch == 'е':
                if prev_ch is None or prev_ch in ' \t\n\r"\'`([{<-—–' or prev_ch in CYR_VOWELS or prev_ch in 'ъЪьЬ':
                    out.append('ye')
                    if stats: stats['ye_count'] += 1
                else:
                    out.append('e')
            elif ch == 'Е':
                is_ye = (prev_ch is None or prev_ch in ' \t\n\r"\'`([{<-—–' or prev_ch in CYR_VOWELS or prev_ch in 'ъЪьЬ')
                if is_ye:
                    out.append('YE' if is_next_upper else 'Ye')
                    if stats: stats['ye_count'] += 1
                else:
                    out.append('E')

            # Ё / ё
            elif ch == 'ё': out.append('yo')
            elif ch == 'Ё': out.append('YO' if is_next_upper else 'Yo')

            # Ю / ю
            elif ch == 'ю': out.append('yu')
            elif ch == 'Ю': out.append('YU' if is_next_upper else 'Yu')

            # Я / я
            elif ch == 'я': out.append('ya')
            elif ch == 'Я': out.append('YA' if is_next_upper else 'Ya')

            # Ц / ц
            elif ch == 'ц':
                if prev_ch is None or not prev_ch.isalpha() or prev_ch in 'кК':
                    out.append('s')
                else:
                    out.append('ts')
                if stats: stats['ts_count'] += 1
            elif ch == 'Ц':
                if prev_ch is None or not prev_ch.isalpha() or prev_ch in 'кК':
                    out.append('S')
                else:
                    out.append('TS' if is_next_upper else 'Ts')
                if stats: stats['ts_count'] += 1

            # Ў / ў
            elif ch == 'ў':
                out.append(o_rep_l)
                if stats: stats['o_count'] += 1
            elif ch == 'Ў':
                out.append(o_rep_u if (not is_next_upper or is_new) else "Oʻ")
                if stats: stats['o_count'] += 1

            # Ғ / ғ
            elif ch == 'ғ':
                out.append(g_rep_l)
                if stats: stats['g_count'] += 1
            elif ch == 'Ғ':
                out.append(g_rep_u if (not is_next_upper or is_new) else "Gʻ")
                if stats: stats['g_count'] += 1

            # Ш / ш
            elif ch == 'ш':
                out.append(sh_rep_l)
                if stats: stats['sh_count'] += 1
            elif ch == 'Ш':
                out.append(sh_rep_u if (not is_next_upper or is_new) else "SH")
                if stats: stats['sh_count'] += 1

            # Ч / ч
            elif ch == 'ч':
                out.append(ch_rep_l)
                if stats: stats['ch_count'] += 1
            elif ch == 'Ч':
                out.append(ch_rep_u if (not is_next_upper or is_new) else "CH")
                if stats: stats['ch_count'] += 1

            # Щ / щ
            elif ch == 'щ':
                out.append(sh_rep_l)
                if stats: stats['sh_count'] += 1
            elif ch == 'Щ':
                out.append(sh_rep_u if (not is_next_upper or is_new) else "SH")
                if stats: stats['sh_count'] += 1

            # Ъ / ъ (Tutuq belgisi)
            elif ch in 'ъЪ':
                out.append(self.APOSTROPHE)
                if stats: stats['tutuq_count'] += 1

            # Ь / ь
            elif ch in 'ьЬ':
                if next_ch and next_ch.lower() in 'еёюя':
                    out.append('y')
                else:
                    pass

            # Standart harflar
            elif ch == 'а': out.append('a')
            elif ch == 'А': out.append('A')
            elif ch == 'б': out.append('b')
            elif ch == 'Б': out.append('B')
            elif ch == 'в': out.append('v')
            elif ch == 'В': out.append('V')
            elif ch == 'г': out.append('g')
            elif ch == 'Г': out.append('G')
            elif ch == 'д': out.append('d')
            elif ch == 'Д': out.append('D')
            elif ch == 'ж': out.append('j')
            elif ch == 'Ж': out.append('J')
            elif ch == 'з': out.append('z')
            elif ch == 'З': out.append('Z')
            elif ch == 'и': out.append('i')
            elif ch == 'И': out.append('I')
            elif ch == 'й': out.append('y')
            elif ch == 'Й': out.append('Y')
            elif ch == 'к': out.append('k')
            elif ch == 'К': out.append('K')
            elif ch == 'л': out.append('l')
            elif ch == 'Л': out.append('L')
            elif ch == 'м': out.append('m')
            elif ch == 'М': out.append('M')
            elif ch == 'н': out.append('n')
            elif ch == 'Н': out.append('N')
            elif ch == 'о': out.append('o')
            elif ch == 'О': out.append('O')
            elif ch == 'п': out.append('p')
            elif ch == 'П': out.append('P')
            elif ch == 'р': out.append('r')
            elif ch == 'Р': out.append('R')
            elif ch == 'с': out.append('s')
            elif ch == 'С': out.append('S')
            elif ch == 'т': out.append('t')
            elif ch == 'Т': out.append('T')
            elif ch == 'у': out.append('u')
            elif ch == 'У': out.append('U')
            elif ch == 'ф': out.append('f')
            elif ch == 'Ф': out.append('F')
            elif ch == 'х': out.append('x')
            elif ch == 'Х': out.append('X')
            elif ch == 'ҳ': out.append('h')
            elif ch == 'Ҳ': out.append('H')
            elif ch == 'қ': out.append('q')
            elif ch == 'Қ': out.append('Q')
            elif ch == 'э': out.append('e')
            elif ch == 'Э': out.append('E')
            else:
                out.append(ch)

        return "".join(out)

    # ------------------------------------------------------------------------
    # 4. Lotin (eski yoki yangi) -> Кирилл
    # ------------------------------------------------------------------------
    def convert_latin_to_cyrillic(self, text, stats=None):
        if not text:
            return text

        tokens = []
        last_end = 0
        for m in PROTECTED_PATTERN.finditer(text):
            start, end = m.span()
            if start > last_end:
                tokens.append((text[last_end:start], False))
            tokens.append((text[start:end], True))
            last_end = end
        if last_end < len(text):
            tokens.append((text[last_end:], False))

        res_parts = []
        for part, is_protected in tokens:
            if is_protected:
                res_parts.append(part)
                continue

            t = part

            # O' va G'
            t = re.sub(r'O' + APOSTROPHE_CHARS_REGEX, 'Ў', t)
            t = re.sub(r'o' + APOSTROPHE_CHARS_REGEX, 'ў', t)
            t = re.sub(r'G' + APOSTROPHE_CHARS_REGEX, 'Ғ', t)
            t = re.sub(r'g' + APOSTROPHE_CHARS_REGEX, 'ғ', t)

            # Yangi alifbo belgilari
            t = t.replace('Ö', 'Ў').replace('ö', 'ў')
            t = t.replace('Õ', 'Ў').replace('õ', 'ў')
            t = t.replace('Ğ', 'Ғ').replace('ğ', 'ғ')
            t = t.replace('Ş', 'Ш').replace('ş', 'ш')
            t = t.replace('Ç', 'Ч').replace('ç', 'ч')

            # Birikmalar
            compounds = [
                ('SH', 'Ш'), ('Sh', 'Ш'), ('sh', 'ш'),
                ('CH', 'Ч'), ('Ch', 'Ч'), ('ch', 'ч'),
                ('YO', 'Ё'), ('Yo', 'Ё'), ('yo', 'ё'),
                ('YU', 'Ю'), ('Yu', 'Ю'), ('yu', 'ю'),
                ('YA', 'Я'), ('Ya', 'Я'), ('ya', 'я'),
                ('YE', 'Е'), ('Ye', 'Е'), ('ye', 'е'),
                ('TS', 'Ц'), ('Ts', 'Ц'), ('ts', 'ц'),
            ]
            for lat, cyr in compounds:
                t = t.replace(lat, cyr)

            # So'z boshidagi E -> Э
            t = re.sub(r'(^|[\s\b.,!?;:\-–—\(\)\[\]"\'`])E', r'\1Э', t)
            t = re.sub(r'(^|[\s\b.,!?;:\-–—\(\)\[\]"\'`])e', r'\1э', t)

            singles = {
                'a': 'а', 'A': 'А', 'b': 'б', 'B': 'Б', 'd': 'д', 'D': 'Д',
                'e': 'е', 'E': 'Е', 'f': 'ф', 'F': 'Ф', 'g': 'г', 'G': 'Г',
                'h': 'ҳ', 'H': 'Ҳ', 'i': 'и', 'I': 'И', 'j': 'ж', 'J': 'Ж',
                'k': 'к', 'K': 'К', 'l': 'л', 'L': 'Л', 'm': 'м', 'M': 'М',
                'n': 'н', 'N': 'Н', 'o': 'о', 'O': 'О', 'p': 'п', 'P': 'П',
                'q': 'қ', 'Q': 'Қ', 'r': 'р', 'R': 'Р', 's': 'с', 'S': 'С',
                't': 'т', 'T': 'Т', 'u': 'у', 'U': 'У', 'v': 'в', 'V': 'В',
                'x': 'х', 'X': 'Х', 'y': 'й', 'Y': 'Й', 'z': 'з', 'Z': 'З'
            }
            chars = []
            for c in t:
                chars.append(singles.get(c, c))
            t = "".join(chars)

            # Harflar orasidagi yoki so'ngidagi apostrof -> ъ
            t = re.sub(r'(?<=[а-яА-ЯёЁўЎғҒқҚҳҲ])' + APOSTROPHE_CHARS_REGEX, 'ъ', t)

            res_parts.append(t)

        return "".join(res_parts)

    def convert_mixed(self, text, stats=None):
        step1 = self.convert_cyrillic_to_new(text, stats=stats)
        step2 = self.convert_old_latin_to_new(step1, stats=stats)
        return step2

    # ------------------------------------------------------------------------
    # Asosiy convert metodi (Barcha yo'nalishlar uchun)
    # ------------------------------------------------------------------------
    def convert(self, text, mode='auto', return_stats=False):
        start_time = time.perf_counter()
        stats = {
            'word_count': len(text.split()) if text else 0,
            'char_count': len(text) if text else 0,
            'mode_used': mode,
            'sh_count': 0,
            'ch_count': 0,
            'o_count': 0,
            'g_count': 0,
            'ye_count': 0,
            'ts_count': 0,
            'tutuq_count': 0,
            'duration_ms': 0.0
        }

        if not text or not isinstance(text, str):
            return (text, stats) if return_stats else text

        # Yo'nalishga qarab chaqirish
        if mode == 'ru_to_uz':
            result = translate_text(text, src='ru', dest='uz')
        elif mode == 'uz_to_ru':
            result = translate_text(text, src='uz', dest='ru')
        elif mode == 'en_to_uz':
            result = translate_text(text, src='en', dest='uz')
        elif mode == 'uz_to_en':
            result = translate_text(text, src='uz', dest='en')
        elif mode == 'cyr_to_old_lat':
            result = self.convert_cyrillic_to_old(text, stats=stats)
        elif mode == 'lat_to_cyr':
            result = self.convert_latin_to_cyrillic(text, stats=stats)
        elif mode in ['old_lat_to_new_lat', 'cyr_to_new_lat', 'mixed_to_new_lat', 'auto']:
            # Yangi Lotinga o'girishda matn Kirill yoki Eski Lotin bo'lishidan qat'i nazar to'liq o'giriladi
            result = self.convert_mixed(text, stats=stats)
        else:
            result = self.convert_mixed(text, stats=stats)

        elapsed = (time.perf_counter() - start_time) * 1000.0
        stats['duration_ms'] = round(elapsed, 2)

        if return_stats:
            return result, stats
        return result
