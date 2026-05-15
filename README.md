
## 📁 Repository Overview

### 1. 🌙 DIU Sleep Health Dashboard (`app.py`)

A comprehensive machine learning and research dashboard designed to analyze and predict sleep disorders among university students. It combines classical predictive modeling with LLM-generated research insights.

* **Key Features:**
* **ML Diagnostic Pipeline:** Uses a `MultiOutputClassifier` wrapped around a `RandomForestClassifier` to evaluate multiple risk clusters simultaneously (Insomnia, Sleep Deprivation, Sleep Apnea, Circadian Rhythm issues, and Stress/Anxiety).
* **Path-Solving System:** Automatically searches across expected directory trees to reliably locate the Excel dataset.
* **Theme-Aware Styling:** Custom CSS configurations injected to override default Streamlit metric wrappers for polished data visibility.
* **Research Insights:** Leverages LangChain and `ChatMistralAI` (`mistral-small-2603`) to compile clinical lifestyle interventions based on the target student's specific risk profile.


* **How to Run:**
```bash
streamlit run app.py

```



### 2. 🎭 Persona Chatbot (`chat.py`)

An interactive LLM playground demonstrating dynamic system prompt mutations and advanced conversation session-state handling.

* **Key Features:**
* **Real-time Personality Morphing:** Features a sidebar toggle allowing immediate swapping between unique behavioral personas (Angry 😡, Funny 😂, Sad 😔).
* **Dynamic Prompt Engineering:** Automatically alters the active index of the LangChain message history object (`SystemMessage`) to manipulate the model's emotional vector without breaking chat continuity.
* **State Control:** Hard reset functions to flush message memory objects and clean cache instances via explicit execution reruns.


* **How to Run:**

```bash
    streamlit run chat.py
    ```

### 3. 💖 Puja AI: Companion Chatbot (`chatbot.py`)
A specialized conversational interface tailored for human-centric sentiment emulation, focusing on empathetic responses and persistent context preservation.

*   **Key Features:**
    *   **Deep Persona Anchoring:** Leverages a dense initial system prompt guiding the agent to hold a caring, highly supportive avatar identity permanently.
    *   **Custom Interface Styling:** Employs personalized UI avatar configurations (`avatar="💖"`) native to Streamlit chat components to decouple the agent visually from standard stock assistant graphics.
    *   **Persistent Context Stream:** Maintained history arrays feeding directly to `mistral-small-latest` for zero-friction dialogue tracking.
*   **How to Run:**
    ```bash
    streamlit run chatbot.py
    ```

---

## 🛠️ Unified Core Tech Stack
*   **Frontend Ecosystem:** Streamlit 
*   **LLM Orchestration:** LangChain Core (`SystemMessage`, `HumanMessage`, `AIMessage`), LangChain MistralAI (`ChatMistralAI`)
*   **Machine Learning Suite:** Scikit-learn (`RandomForestClassifier`, `MultiOutputClassifier`, `LabelEncoder`)
*   **Data Processing:** Pandas, Openpyxl (Excel parsing engine)
*   **Environment Logic:** Python-dotenv

---

## 🔧 Installation & Environment Setup

1. **Clone the Repository:**
   
```bash
   git clone https://github.com/tirtha4542/ChatBot.git
   cd ChatBot

```

2. **Establish Environment Configurations:**
Create a `.env` file in the root directory to store your service credentials securely:

```env
   MISTRAL_API_KEY=your_secret_mistral_api_key_here

```

3. **Install Core Requirements:**
Ensure you have your environment variables set up, then install the underlying packages:

```bash
   pip install streamlit pandas openpyxl scikit-learn langchain-core langchain-mistralai python-dotenv

```

---

## 🚀 Execution Strategy

Since every Python file operates as an **entirely isolated utility or application**, navigate to the root directory and choose the specific environment pipeline you wish to spin up:

```bash
# To run the Sleep Analysis Research Tool:
streamlit run app.py

# To run the Dynamic Persona Testing Box:
streamlit run chat.py

# To run the Puja Companion Interface:
streamlit run chatbot.py

```

```

```
