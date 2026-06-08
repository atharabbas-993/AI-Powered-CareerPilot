# 🤖 CareerPilot AI — Pakistan AI Career Roadmap Bot

<div align="center">

![CareerPilot AI Banner](https://img.shields.io/badge/CareerPilot-AI%20Career%20Roadmap-blue?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![LLaMA](https://img.shields.io/badge/LLaMA_3.1-Groq-green?style=for-the-badge)

**An AI-powered career counselor for Pakistani students who want to enter the Artificial Intelligence field.**

[🚀 Live Demo](https://huggingface.co/spaces/AtharAbbas993/CareerPilot-AI) · [📧 Contact](https://github.com/AtharAbbas993)

</div>

---

## 📌 About The Project

**CareerPilot AI** is a personalized AI career roadmap bot built specifically for Pakistani students. It guides students through 8 different AI domains and generates a complete, personalized career roadmap based on their education, skills, and goals.


---

## ✨ Features

- 🎯 **8 AI Career Domains** — ML, DL, Computer Vision, NLP, MLOps, Data Science, GenAI, AI Research
- 🗺️ **Personalized Roadmap** — Custom career plan based on student profile
- 🏢 **Pakistani Job Market** — Real companies hiring in Pakistan
- 🆓 **Free Resources Only** — No paid courses recommended
- 💬 **Follow-up Chat** — Ask questions about your roadmap
- ⬇️ **Downloadable Roadmap** — Save your plan as a text file
- 🔒 **Secure & Safe** — Prompt injection defense built in
- 🌙 **Dark Blue/Red UI** — Beautiful animated interface

---

## 🧠 Prompt Engineering Techniques Used

| Technique | Purpose |
|---|---|
| Role Prompting | Ustad Tariq — Expert Pakistani Career Counselor |
| Chain of Thought | Step by step career analysis |
| ReAct Prompting | Thought → Action → Observation flow |
| Self Consistency | Asks LLM 3 times for reliable answers |
| Negative Prompting | Strict rules on what bot should never do |
| Output Format Control | Clean structured roadmap output |
| Prompt Templates | Reusable career prompt structure |
| Prompt Chaining | Multi-step pipeline for roadmap generation |
| Prompt Injection Defense | Security layers for safe usage |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10 | Core language |
| Streamlit | Web UI framework |
| Groq API | Free LLM API |
| LLaMA 3.1 | Language model |
| Docker | Containerization |
| HuggingFace Spaces | Deployment platform |
| Git & GitHub | Version control |

---

## 🤖 AI Domains Covered

```
1. 🧠 Machine Learning Engineer
2. ⚡ Deep Learning Engineer
3. 👁️ Computer Vision Engineer
4. 💬 NLP Engineer
5. ⚙️ MLOps Engineer
6. 📊 Data Scientist
7. ✨ Generative AI Engineer
8. 🔬 AI Research Engineer
```

---

## 🚀 How It Works

```
Step 1 → Student selects AI domain
         ↓
Step 2 → Student fills profile form
         (education, skills, experience)
         ↓
Step 3 → AI generates personalized roadmap
         (Self Consistency — 3 passes)
         ↓
Step 4 → Student gets complete career plan
         + can ask follow-up questions
         + can download roadmap
```

---

## 📁 Project Structure

```
pakistan-ai-career-bot/
│
├── app.py              → Main Streamlit application
├── prompts.py          → System prompts & templates
├── domains.py          → 8 AI domains data
├── requirements.txt    → Python dependencies
├── Dockerfile          → Docker configuration
├── .dockerignore       → Docker ignore rules
├── .gitignore          → Git ignore rules
└── README.md           → Project documentation
```

---

## ⚙️ Run Locally

### Prerequisites
- Python 3.10+
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### Steps

```bash
# Clone the repository
git clone https://github.com/AtharAbbas993/pakistan-ai-career-bot.git

# Navigate to project
cd pakistan-ai-career-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your API key
echo GROQ_API_KEY=your_api_key_here > .env

# Run the app
streamlit run app.py
```

Open 👉 `http://localhost:8501`

---

## 🐳 Run with Docker

```bash
# Build Docker image
docker build -t careerpilot-ai .

# Run container
docker run -p 7860:7860 -e GROQ_API_KEY=your_api_key_here careerpilot-ai
```

Open 👉 `http://localhost:7860`

---

## 🌐 Deployment

Deployed on **HuggingFace Spaces** using Docker.

👉 **Live App:** [https://huggingface.co/spaces/AtharAbbas993/CareerPilot-AI](https://huggingface.co/spaces/AtharAbbas993/CareerPilot-AI)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open an issue for bugs
- Suggest new AI domains
- Improve the UI
- Add more Pakistani companies

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Athar Abbas**
- GitHub: [@AtharAbbas993](https://github.com/AtharAbbas993)
- HuggingFace: [@AtharAbbas993](https://huggingface.co/AtharAbbas993)

---

<div align="center">

Built with ❤️ for Pakistani AI Students

⭐ Star this repo if you found it helpful!

</div>
