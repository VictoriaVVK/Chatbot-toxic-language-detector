import re
import sys
import unicodedata
from datetime import datetime

# ----------------------------
# Конфигурация
# ----------------------------
LEXICON = {
    # Примерни НЕ-крайни/НЕ-слур думи за демонстрация (замени/допълни от файл при нужда):
    # В реалния проект използвай отделен файл с одобрен списък от преподавателя.
    "low":    ["глупав", "глупак", "неучтив", "невъзпитан"],
    "medium": ["идиот", "тъпак", "простак"],
    "high":   ["малоумен", "ненормален"]  # умишлено оставени като корени за да хванем варианти
}

LEET_MAP = str.maketrans({
    "0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t",
    "@": "a", "$": "s", "!": "i", "€": "e"
})

MASK_CHAR = "•"

RESPONSES = {
    "low":    "Нека опитаме по-приятелски тон 🙂",
    "medium": "Нека запазим уважението. Перефразирай, моля.",
    "high":   "Открит е оскърбителен израз. Моля, въздържай се."
}

# ----------------------------
# Нормализация и помощни
# ----------------------------
def normalize(text: str) -> str:
    # NFKC: унифицира варианти, translit на leet, понижение на регистъра, премахва control chars
    t = text.translate(LEET_MAP).lower()
    t = unicodedata.normalize("NFKC", t)
    return t

def build_patterns(words):
    # Правим regex, който хваща отделна дума, удължения и междинни разделители ( ., _ - )
    # Пр.: "и.д.!и0т", "идиоооот", "и*д*и*о*т"
    pats = []
    for w in words:
        # заменяме всяка буква с клас, позволяващ не-буквени разделители и повторения
        chars = [re.escape(ch) + r"(?:[\W_]*" + re.escape(ch) + r")*" for ch in w]
        fuzzy = r"\b" + "".join(chars) + r"\b"
        pats.append(re.compile(fuzzy, flags=re.IGNORECASE | re.UNICODE))
    return pats

PATTERNS = {
    level: build_patterns(LEXICON[level]) for level in LEXICON
}

def mask_match(text, match):
    s, e = match.span()
    return text[:s] + MASK_CHAR * (e - s) + text[e:]

def scan_text(raw_text: str):
    """Връща (level_found or None, masked_text, [списък на съвпадения])"""
    text = raw_text
    norm = normalize(raw_text)
    hits = []
    level_found = None

    # приоритизираме high > medium > low
    for level in ("high", "medium", "low"):
        for rgx in PATTERNS[level]:
            for m in rgx.finditer(norm):
                hits.append((level, m))
                level_found = level if level_found is None else level_found
    # Маскиране (по оригиналния текст с приблизителни позиции)
    # За простота маскираме по думите в нормализирания текст чрез повторно търсене в оригинала
    if hits:
        # сортираме по начало, за да маскираме отзад напред и да не местим индекси
        spans = []
        for level, m in hits:
            # груба ре-локализация: търсим „ядрото“ (премахнати небуквени) в оригинала
            core = re.sub(r"[\W_]+", "", m.group(0))
            m2 = re.search(re.escape(core), re.sub(r"[\W_]+", "", raw_text), flags=re.IGNORECASE)
            # ако не намерим, ползваме директно позициите от нормализирания (може да не съвпаднат 1:1)
            if not m2:
                continue
            # Намираме видимата последователност в raw_text с „разредени“ символи
            # За безопасност – просто заменяме всички видими букви от core в raw_text еднократно
            # (работи прилично за демо без да чупим индекси)
        masked = raw_text
        # най-просто: замаскирай всички буквенo-съвпадащи поднизове от лексикона
        for level in ("high", "medium", "low"):
            for w in LEXICON[level]:
                # позволи случайни разделители между буквите
                letters = list(w)
                fuzz = r"".join([re.escape(ch) + r"[\W_]*" for ch in letters])
                pattern_visible = re.compile(fuzz, flags=re.IGNORECASE | re.UNICODE)
                masked = pattern_visible.sub(lambda m: MASK_CHAR * len(m.group(0)), masked)
        return level_found, masked, [h[0] for h in hits]
    return None, raw_text, []

# ----------------------------
# Основен чат цикъл
# ----------------------------
def main():
    print("AI Chatbot (Offense Detector) — BG/EN")
    print("Напиши съобщение. Команди: /add <дума>, /stats, /quit")
    temp_added = []
    total_hits = 0

    while True:
        try:
            msg = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not msg:
            continue
        if msg.lower() in ("/quit", "/exit"):
            print("До скоро!")
            break

        if msg.startswith("/add "):
            word = msg[5:].strip().lower()
            if not word:
                print("Използвай: /add <дума>")
                continue
            LEXICON["low"].append(word)
            PATTERNS["low"] = build_patterns(LEXICON["low"])
            temp_added.append(word)
            print(f"Добавих „{word}“ към временния лексикон (ниво: low).")
            continue

        if msg == "/stats":
            print(f"Засичания в сесията: {total_hits}. Временни думи: {', '.join(temp_added) if temp_added else 'няма'}")
            continue

        level, masked, hits = scan_text(msg)
        if level:
            total_hits += len(hits)
            print(masked)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Detected: {level.upper()} — {RESPONSES[level]}")
        else:
            # нормален отговор (placeholder диалог)
            print("Разбирам. Благодаря за коректния тон! Как мога да помогна?")

if __name__ == "__main__":
    main()
