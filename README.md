
# 🧠 Blog Generation Pipeline using Google ADK & Gemini

This project demonstrates how to build a multi-agent workflow using Google’s Agent Development Kit (ADK) and Gemini models to automate the creation of high-quality blog posts — from outlining to writing and final editing.

---

## 🚀 Overview

The system uses a SequentialAgent workflow where each agent handles a distinct stage of content creation:

1. **OutlineAgent** — Generates a detailed blog outline (headline, intro, sections, and conclusion).  
2. **WriterAgent** — Expands the outline into a full 200–300 word blog post.  
3. **EditorAgent** — Polishes the blog for grammar, clarity, and flow.  

You can easily extend this pipeline by adding new agents (e.g., a ResearchAgent or SEOAgent) to perform additional tasks.

---

## 🧩 Architecture

| Agent | Model | Purpose | Output Key |
|--------|--------|----------|-------------|
| **OutlineAgent** | Gemini-2.5-flash-lite | Create a structured blog outline | blog_outline |
| **WriterAgent** | Gemini-2.5-flash-lite | Write a full blog draft from the outline | blog_draft |
| **EditorAgent** | Gemini-2.5-flash-lite | Edit and refine the draft for clarity and quality | final_blog |
| **BlogPipeline (Root)** | SequentialAgent | Executes the agents in sequence | — |

All agents use a retry configuration for robustness against transient API errors (e.g., 429, 500, 503, 504).

---

## ⚙️ Setup & Usage

### 1. Install dependencies
Make sure you have the Google ADK and genai packages installed:

`pip install google-adk google-genai`

### 2. Authenticate with Google
Ensure your environment is authenticated for Gemini API access:

`gcloud auth application-default login`

### 3. Run the pipeline

```python
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=root_agent)
result = runner.run("The rise of ethical AI in business")

print(result.output["final_blog"])
````

---

## 🔁 Retry Configuration

To make the pipeline resilient, each Gemini model is initialized with a HttpRetryOptions object:

```python
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)
```

---

## 🧠 Extending the Pipeline

You can easily integrate other agents such as:

* ResearchAgent — Uses google_search to gather information.
* SummarizerAgent — Produces concise summaries.
* SEOAgent — Optimizes content for search engines.

Example:

```python
root_agent = SequentialAgent(
    name="EnhancedBlogPipeline",
    sub_agents=[research_agent, summarizer_agent, outline_agent, writer_agent, editor_agent],
)
```

---

## 💡 Example Output

**Prompt:**
“The future of AI in healthcare”

**Generated Blog (excerpt):**
AI is revolutionizing healthcare by enhancing diagnostics, reducing costs, and improving patient outcomes. From predictive analytics to robotic surgeries, the integration of artificial intelligence is redefining how doctors and patients interact...

---

## 🧰 Technologies Used

* Google ADK
* Gemini Models
* Python 3.10+

---

## 📄 License

This project is licensed under the Apache 2.0 License — feel free to use and modify.

---

## 🧾 Credits

Created using Google ADK, Gemini 2.5 Flash Lite, and InMemoryRunner to demonstrate a modular, LLM-driven blog generation pipeline.

```

