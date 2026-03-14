import re
import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from textblob import TextBlob
import tkinter as tk
from tkinter import scrolledtext
import pyttsx3


# =============================
# TEXT-TO-SPEECH (ботът говори)
# =============================
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("voice", engine.getProperty("voices")[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()


# =============================
#  AI MODEL (Smart v7.0)
# =============================
training_sentences = [
    "ти си тъп", "мразя те", "идиот си", "ти си глупак", "ненормален си",
    "здравей", "как си", "благодаря ти", "добър ден", "приятно ми е",
    "какво правиш", "радвам се", "добре съм", "тъжно ми е", "яд ме е"
]

training_labels = [
    "toxic", "toxic", "toxic", "toxic", "toxic",
    "neutral", "neutral", "neutral", "neutral", "neutral",
    "neutral", "positive", "positive", "negative", "negative"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(training_sentences)
model = LogisticRegression().fit(X, training_labels)


# =============================
# 20+ INTENTS
# =============================
INTENTS = {
    "greeting": ["здравей", "привет", "здрасти", "хей", "hello", "hi"],

    "how_are_you": ["как си", "как сте", "как върви"],
    "thanks": ["благодаря", "мерси"],
    "bye": ["чао", "довиждане", "лека", "бай"],
    "who_are_you": ["кой си", "какво си", "как се казваш"],
    "help": ["help", "помощ", "какво можеш"],

    # настроение
    "happy": ["радвам", "щастлив", "яко ми е", "супер съм"],
    "sad": ["тъжно", "депрес", "плача"],
    "angry": ["яд ме", "мразя", "бесен"],
    "tired": ["уморен", "спи ми се", "изморен", "натоварен"],
    "bored": ["скучно", "умирам от скука"],

    # разговор
    "day": ["как върви денят", "как ти мина денят", "какво правиш"],
    "night": ["лека нощ", "добър вечер"],
    "weather": ["времето", "топло ли е", "студено ли е"],

    # социални
    "compliment": ["харесвам те", "готин си", "сладък си", "красив"],
    "insult_light": ["гадно", "тъп ли си", "гаден"],

    # работа/учене
    "school": ["училище", "уни", "лекции", "учене"],
    "work": ["работа", "job", "проект", "task"],

    # интереси
    "hobby": ["хоби", "какво обичаш", "интереси"],
}


# =============================
# ОТГОВОРИ (много варианти)
# =============================
INTENT_RESPONSES = {

    "greeting": [
        "Здравей! 😊",
        "Хей! Радвам се да те видя! 😄",
        "Привет! Как върви денят?",
        "Здравей! Как си днес?"
    ],

    "how_are_you": [
        "Супер съм! А ти как си? 😊",
        "Много добре! Благодаря! ❤️",
        "Добре съм! Как е при теб?",
        "Чудесно настроение имам! Ти?"
    ],

    "thanks": [
        "Моля ти се! ❤️",
        "Винаги насреща!",
        "Супер, радвам се! 😊",
        "С удоволствие!"
    ],

    "bye": [
        "До скоро! 👋",
        "Чао, пази се!",
        "Лека вечер! 🌙",
        "Хубав ден ти желая! 😊"
    ],

    "who_are_you": [
        "Аз съм интелигентен агент 🤖.",
        "Един приятел, с който можеш да си говориш 😊",
        "Малък AI, но голямо сърце ❤️",
        "Бот с мисия да помага!"
    ],

    "help": [
        "Мога да говоря, да слушам и да разпознавам емоции 🤖",
        "Мога да отговарям на въпроси и да водя разговор!",
        "Говори ми и ще ти отговоря 😊"
    ],

    "happy": [
        "Супер! Радвам се много! 😄",
        "Чудесно настроение имаш! ✨",
        "Страхотно! ❤️"
    ],

    "sad": [
        "Съжалявам… 😔 Тук съм, ако искаш да поговорим.",
        "Хей… всичко ще се оправи ❤️",
        "Понякога е тежко, но ти си силен човек."
    ],

    "angry": [
        "Разбирам… Нека опитаме да говорим спокойно ❤️",
        "Хей, спокойно… всичко е наред.",
        "Кажи ми какво те ядоса?"
    ],

    "tired": [
        "Изглежда си натоварен… почини си ❤️",
        "Хей, заслужаваш малка пауза 😴",
        "Много работа? Разбирам те напълно…"
    ],

    "bored": [
        "Хайде да си поговорим! 😊",
        "Искаш ли да ти разкажа нещо?",
        "Скуката е знак, че търсиш нещо ново ✨"
    ],

    "day": [
        "Моят ден беше супер! А твоят? 😊",
        "Какво прави денят ти хубав?",
        "Как минава всичко при теб?"
    ],

    "night": [
        "Спокойна нощ! 🌙",
        "Приятна вечер! ✨",
        "Надявам се да си отпочинеш! 😴"
    ],

    "weather": [
        "Хаха, бот съм — за мен винаги е 22°C 😄",
        "А при теб как е времето?",
        "Слънчево настроение имам! ☀️"
    ],

    "compliment": [
        "Ооо, много мило 😳❤️",
        "Благодаря ти! Това значи много! ☺️",
        "Много си сладък/сладка! 💗"
    ],

    "insult_light": [
        "Хей… спокойно 😅",
        "Еее, не бъди такъв/такава 😂",
        "Хах, знам че не го мислиш така 😉"
    ],

    "school": [
        "Лекции, а? Тежко понякога 😅",
        "Какъв предмет имаш?",
        "Кой курс си?"
    ],

    "work": [
        "Работата понякога изцежда… 😅",
        "Как върви проектът?",
        "Какво работиш в момента?"
    ],

    "hobby": [
        "Хмм, интересно! А ти какво обичаш?",
        "Моето хоби е да говоря с теб 🤖❤️",
        "Какво ти е най-любимо да правиш?"
    ],

    "default": [
        "Разкажи ми още 😊",
        "Интересно 🤔 продължи!",
        "Искам да чуя повече! ❤️",
        "Хмм… любопитно 😄"
    ]
}


# =============================
# TOXICITY, EMOTION, INTENT
# =============================
BAD_WORDS = ["тъп", "глупак", "идиот", "малоумен", "ненормален"]

context = {"offense_count": 0}


def detect_emotion(text):
    if "питах" in text.lower():
        return "neutral"
    p = TextBlob(text).sentiment.polarity
    if p > 0.2: return "positive"
    if p < -0.2: return "negative"
    return "neutral"


def detect_toxicity(text):
    if any(s in text.lower() for s in ["кой си", "какво си"]):
        return "neutral"
    X_test = vectorizer.transform([text])
    return model.predict(X_test)[0]


def rule_based_offense(text):
    t = text.lower()
    if t.startswith(("ама", "но", "обаче")):
        return False
    return any(w in t for w in BAD_WORDS)


def detect_intent(text):
    t = text.lower()
    for intent, words in INTENTS.items():
        for w in words:
            if w in t:
                return intent
    return "default"


def respond(text):
    t = text.lower()

    # извинение = reset
    if detect_intent(t) == "apology":
        context["offense_count"] = 0
        return "Всичко е наред ❤️"

    # безопасни
    if t in ["кой си", "какво си"]:
        return random.choice(INTENT_RESPONSES["who_are_you"])

    # токсичност
    if detect_toxicity(text) == "toxic" or rule_based_offense(text):
        context["offense_count"] += 1
        if context["offense_count"] == 1:
            return "Моля те, нека не се обиждаме 🙂"
        if context["offense_count"] == 2:
            return "Това не е приятен тон…"
        return "Това беше грубо. Спирам разговора."

    # емоция
    emotion = detect_emotion(text)
    if emotion == "positive":
        return "Много се радвам да го чуя! 🌟"
    if emotion == "negative":
        return "Разбирам… звучи тежко 😔"

    # intent
    intent = detect_intent(text)
    return random.choice(INTENT_RESPONSES.get(intent, INTENT_RESPONSES["default"]))



# =============================
# GUI INTERFACE
# =============================
root = tk.Tk()
root.title("Smart Chat Agent v7.0 – Premium GUI")
root.geometry("650x750")
root.configure(bg="#1e1e1e")  # dark


# DARK / LIGHT THEMES
def set_dark_theme():
    root.configure(bg="#1e1e1e")
    chat_window.configure(bg="#252526", fg="#dcdcdc")
    entry.configure(bg="#333333", fg="white")
    send_button.configure(bg="#0078d4")
    quick_frame.configure(bg="#1e1e1e")


def set_light_theme():
    root.configure(bg="white")
    chat_window.configure(bg="#f5f5f5", fg="black")
    entry.configure(bg="white", fg="black")
    send_button.configure(bg="#0078d4")
    quick_frame.configure(bg="white")


# CHAT WINDOW
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Segoe UI", 12))
chat_window.tag_config("user", foreground="#68a0f8")
chat_window.tag_config("bot", foreground="#98f57a")
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Segoe UI", 14))
entry.pack(padx=10, pady=5, fill=tk.X)


# QUICK REPLY BUTTONS
quick_frame = tk.Frame(root, bg="#1e1e1e")
quick_frame.pack(padx=10, pady=5, fill=tk.X)

quick_msgs = ["Здравей", "Как си?", "Помощ", "Какво правиш?", "Кой си?", "Чао"]

def quick_send(msg):
    entry.insert(0, msg)
    send_message()

for q in quick_msgs:
    tk.Button(quick_frame, text=q,
              command=lambda m=q: quick_send(m),
              bg="#3a3a3a", fg="white",
              relief=tk.FLAT, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)


# SEND MESSAGE LOGIC
def send_message():
    user_text = entry.get()
    if not user_text.strip():
        return

    chat_window.insert(tk.END, f"Ти: {user_text}\n", "user")
    entry.delete(0, tk.END)

    bot_response = respond(user_text)
    chat_window.insert(tk.END, f"Бот: {bot_response}\n\n", "bot")
    chat_window.see(tk.END)

    speak(bot_response)


# BUTTONS
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(padx=10, pady=10, fill=tk.X)

send_button = tk.Button(button_frame, text="Send", command=send_message,
                        bg="#0078d4", fg="white", font=("Segoe UI", 14))
send_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

theme_button = tk.Button(button_frame, text="🌙/☀",
                         command=lambda: toggle_theme(),
                         bg="#3a3a3a", fg="white", font=("Segoe UI", 14))
theme_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)


# THEME TOGGLE
current_theme = "dark"
def toggle_theme():
    global current_theme
    if current_theme == "dark":
        set_light_theme()
        current_theme = "light"
    else:
        set_dark_theme()
        current_theme = "dark"


set_dark_theme()
root.mainloop()
