# 🍴 Food Scout - AI Restaurant Recommendations

| ![Overview](https://github.com/DoubleStyx/CS-6320.002-Project/blob/main/images/graph.png?raw=true) | [![🎥 Watch the Demo](https://img.youtube.com/vi/X3G--T7PZB4/0.jpg)](https://www.youtube.com/watch?v=X3G--T7PZB4) |
|:---------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------:|
| Overview                                                                                           | 🎥 Demo                                                                                                       |

**Food Scout** is a next-generation conversational assistant designed to enhance how users explore local dining options. Harnessing the power of advanced Natural Language Processing (NLP) and the conversational capabilities of GPT-4, this tool delivers intelligent, context-aware restaurant recommendations tailored to individual preferences.

---

## 🎯 What Does Food Scout Do?

Food Scout acts as your personal restaurant guide, engaging users in natural conversation to understand dining needs—whether it's finding sushi on a budget or locating a romantic dinner spot in a new city. It combines structured NLP insights with dynamic dialogue to recommend the perfect place to eat.

---

## 🧠 Key Features

- **Conversational Guidance**  
  Natural, back-and-forth interactions help users narrow down options based on location, cuisine, price range, and more.

- **Entity Recognition with NLP**  
  Utilizes spaCy and custom regex patterns to identify key details from user input such as food type, geographic location, and budget.

- **AI-Powered Chat with GPT-4**  
  GPT-4 provides fluid, contextually relevant responses to ensure users feel understood and engaged.

- **Smart Context Handling**  
  Maintains memory of the conversation to ask relevant follow-up questions and refine recommendations on the fly.

---

## 🧩 System Components

| Layer          | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| **Frontend**   | Built using **Gradio**, offering a simple and interactive chat experience.  |
| **NLP Engine** | Powered by **spaCy** and **regex**, it extracts structured data from input. |
| **AI Core**    | Uses **OpenAI GPT-4** for dynamic language generation and decision logic.    |
| **Context Tracker** | Manages session state and conversation flow to stay on topic.         |

---

## ⚙️ Technology Stack

- **Language**: Python  
- **Interface**: Gradio  
- **Language Model**: GPT-4 by OpenAI  
- **NLP Toolkit**: spaCy  
- **Pattern Matching**: Regular Expressions

---

## 🚀 Purpose

Food Scout was developed to bridge the gap between traditional search tools and human-like travel and dining guidance. It’s more than a chatbot—it's a smart assistant that adapts to your tastes, making food discovery smoother and more intuitive than ever before.


### Instructions to Setup and Run the Project
1. **Clone the repository**:
   ```
   git clone https://github.com/DoubleStyx/CS-6320.002-Project
   
## Setup Virtual Environment
```
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate for Windows
```

## Install Requirements
```
pip install -r requirements.txt
```
## Environment Variables
Create a .env file in the root directory with the following keys:
```
OPENAI_API_KEY=your_openai_api_key
```
## Run the Application
```
python app.py
```
Access the Interface
Open the local URL in your browser to interact with the assistant.


### Team Members and Contributions
- **Kyle Poulson**: UI/UX Development - Gradio interface, conversation flow testing, designing user-friendly input prompts.


>>>>>>> 0a8b1f4a27cc81f189330c2f8882461fcde98831
