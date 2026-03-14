# Smart Chat Agent

An intelligent chatbot developed as a course project for **Artificial Intelligence Fundamentals**.

The chatbot can detect toxic language, analyze the emotional tone of messages, recognize user intent, and respond appropriately during a conversation.

---

#  Project Goal

The goal of this project is to develop a chatbot that can:

- detect **toxic or offensive language**
- perform **sentiment analysis**
- recognize **user intent**
- respond in a **natural conversational way**
- demonstrate core concepts from **Artificial Intelligence and NLP**

---

## 1. Machine Learning – Toxicity Detection

The system uses a **Logistic Regression** classifier.

Input text is converted into numerical features using:

```
Bag-of-Words → CountVectorizer
```

The model classifies text into the following categories:

- toxic
- neutral
- positive
- negative

Example:

```
"You are stupid" → toxic
"Hello" → neutral
"Thank you" → positive
```

---

## 2. Rule-Based Safety Layer

In addition to the machine learning model, a **rule-based fallback mechanism** is implemented.

This component checks messages against a predefined list of offensive words.

Purpose:

- increase reliability
- prevent missed toxic messages
- improve system robustness

---

## 3. Sentiment Analysis

Sentiment analysis is implemented using the **TextBlob** library.

```
TextBlob(text).sentiment.polarity
```

Polarity values:

| Value | Meaning |
|------|------|
> 0.2 | Positive sentiment |
< -0.2 | Negative sentiment |
Between | Neutral sentiment |

This allows the chatbot to react emotionally rather than returning static responses.

---

## 4. Intent Recognition

The chatbot detects **user intentions** using keyword matching.

Example intents:

| Intent | Example |
|------|------|
greeting | hello, hi |
thanks | thank you |
bye | goodbye |
school | lecture, university |
work | project, job |

This enables the chatbot to hold basic conversations.

---

#  Toxic Language Escalation

The chatbot tracks repeated offenses using:

```
context["offense_count"]
```

Escalation logic:

| Offense Count | Response |
|------|------|
1 | Friendly warning |
2 | Stronger warning |
3 | Conversation terminated |

This simulates basic **dialogue management** rather than simple conditional logic.

---

# 🖥 Graphical User Interface

The project includes a GUI built with **Tkinter**.

Interface features:

- chat window with scroll
- text input field
- send button
- quick message buttons
- dark / light theme toggle
- text-to-speech responses

---

# Technologies Used

| Technology | Purpose |
|------|------|
Python | Main programming language |
scikit-learn | Machine learning |
CountVectorizer | Text vectorization |
LogisticRegression | Text classification |
TextBlob | Sentiment analysis |
Tkinter | GUI interface |
pyttsx3 | Text-to-speech |



# ▶ Run the Application

```bash
python chatbot_gui_v7.py
```


#  Author

Victoria Kostadinova  
Artificial Intelligence Student  
Technical University of Varna
