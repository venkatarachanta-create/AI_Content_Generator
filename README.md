# 📄 4: AI Content Generator

## 🎯 Problem Statement

Creating long-form content — blog posts, articles, explainers — is time-consuming. A writer typically starts with an outline, expands each section into full prose, and then condenses it into a summary. That's exactly how a well-designed AI pipeline should work too.

**Your task:** Complete the Content Generator pipeline in this repository. The scaffolding is already in place — your job is to **replace all three placeholder implementations** with real LLM-powered logic using `PromptTemplate` and LangChain.

The finished tool should:
- **Generate a structured outline** from any topic using an LLM
- **Expand that outline** into a full, readable piece of content — section by section
- **Summarize the content** into a concise paragraph that captures the key points

---

## 📁 Repository Structure

```
Option4_Content_Generator/
│
├── main.py                   # CLI entry point — run your generator here
├── Content_Generator.ipynb   # Guided notebook — start here if you're new
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### What each file does

| File | Purpose |
|---|---|
| `main.py` | Parses the `--topic` CLI argument, calls all three pipeline functions in sequence, and prints the output |
| `Content_Generator.ipynb` | Step-by-step guided notebook with hints for building and testing each function |
| `requirements.txt` | Lists `openai`, `langchain` — install before starting |

---

## 🛠️ Setup

### 1. Clone the repository and navigate to this folder

```bash
git clone <repo-url>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

Create a `.env` file in this folder:

```
OPENAI_API_KEY=your_key_here
```

Then load it at the top of your script:

```python
from dotenv import load_dotenv
load_dotenv()
```

> **No OpenAI key?** You can use [Groq](https://console.groq.com) (free tier) or [Google Gemini](https://aistudio.google.com) instead. Just swap the LLM in your LangChain setup.

---

## 🧱 What You Need to Implement

Open `main.py`. You'll find **three functions** with `# TODO` comments. Each one is a stage in the content generation pipeline — implement them in order.

---

### Function 1: `generate_outline(topic: str) → list`

**What it should do:** Take a topic string and return a Python list of section headings that form a logical outline for a blog post or article on that topic.

**Current placeholder:**
```python
def generate_outline(topic: str) -> list:
    # TODO: use PromptTemplate + LLM to create an outline
    return [f"Introduction to {topic}", "Key Concepts", "Conclusion"]
```

**Your implementation must:**
- Use a `PromptTemplate` with a `{topic}` placeholder and a clear instruction like *"Generate a structured outline with 4–6 section headings for a blog post about {topic}. Return only the headings as a numbered list."*
- Parse the LLM's response into a clean Python list (split by newline and strip numbering)

**Tips:**
- Use a low `temperature` (e.g., `0.3`) here — you want a structured, consistent outline, not a creative one
- Ask the LLM to return *only* the headings with no extra commentary, to make parsing easier

---

### Function 2: `generate_content(outline: list) → str`

**What it should do:** Take the outline list and return a full piece of content — one paragraph or more per section heading.

**Current placeholder:**
```python
def generate_content(outline: list) -> str:
    # TODO: expand outline into full content using LLM
    return "\n\n".join([f"## {h}\nContent for {h}." for h in outline])
```

**Your implementation must:**
- Loop through each heading in the outline and call the LLM to generate content for that section
- Format the output with Markdown headings (`## Heading`) followed by the generated paragraph(s)
- Return the full content as a single string

**Challenge (Optional):** Instead of making one LLM call per heading, pass the entire outline to the LLM in a single call and ask it to write all sections at once. Compare the two approaches — which gives better output?

**Tips:**
- Use `temperature=0.7` for more natural, expressive prose
- Keep each section prompt focused: *"Write 2–3 paragraphs for a blog section titled '{heading}'. The blog is about {topic}."*

---

### Function 3: `summarize(content: str) → str`

**What it should do:** Take the full generated content and return a concise 3–5 sentence summary that captures the key points.

**Current placeholder:**
```python
def summarize(content: str) -> str:
    # TODO: produce a short summary using LLM
    return content[:200] + "..."
```

**Your implementation must:**
- Use a `PromptTemplate` with a `{content}` placeholder and an instruction like *"Summarize the following article in 3–5 sentences, capturing the key points clearly."*
- Pass the full generated content as input and return the LLM's summary as a string

**Tips:**
- Use a low `temperature` (e.g., `0.3`) for a clean, factual summary
- If the content is very long, consider passing only the first 2000 characters to stay within token limits

---

## ▶️ How to Run

```bash
python main.py --topic "Getting started with LangChain"
python main.py --topic "How transformer models work"
python main.py --topic "Best practices for prompt engineering"
```

### Expected output format

```
OUTLINE:
 1. Introduction to LangChain
 2. Core Components: Chains, Prompts, and Models
 3. Setting Up Your First LangChain App
 4. Real-World Use Cases
 5. Common Pitfalls and How to Avoid Them
 6. Conclusion

CONTENT:
 ## Introduction to LangChain
 LangChain is an open-source framework designed to simplify building
 applications powered by large language models...

 ## Core Components: Chains, Prompts, and Models
 At the heart of LangChain are three building blocks...

 ...

SUMMARY:
 LangChain is a powerful framework for building LLM-powered applications.
 It provides modular components like chains, prompt templates, and model
 integrations that can be combined to create complex pipelines...
```

---

## 📓 Using the Notebook

If you prefer to build and test iteratively, start with `Content_Generator.ipynb`. It walks you through each function one cell at a time with hints.

**Recommended workflow:**
1. Implement and test `generate_outline()` in the notebook first — verify the output is a clean list
2. Feed that outline into `generate_content()` and check each section reads naturally
3. Pass the full content into `summarize()` and verify the summary is accurate and concise
4. Once all three work, copy the implementations into `main.py`
5. Run `main.py` end-to-end to verify the full pipeline works together

---

## ✅ Evaluation Criteria

| Criteria | Weightage |
|---|---|
| `generate_outline()` uses PromptTemplate + LLM and returns a proper Python list (not hardcoded) | 25% |
| `generate_content()` expands the outline into readable, coherent content per section | 30% |
| `summarize()` produces a concise, accurate summary using an LLM (not a string slice) | 20% |
| Code is clean, readable, and well-commented | 15% |
| Successfully runs end-to-end via `main.py` with the full pipeline | 10% |

---


## ❓ FAQ

**Q: Can I use a different LLM — Gemini, Groq, Mistral?**
Yes. Just replace `ChatOpenAI` with the appropriate LangChain wrapper. The `PromptTemplate` and LCEL structure stays the same.

**Q: My outline comes back as a paragraph instead of a list. How do I fix it?**
Be more explicit in your prompt — instruct the LLM to return *only* a numbered list with one heading per line and no extra text. Then split the response by `\n` and strip the numbering.

**Q: `generate_content()` is making too many API calls and is slow. What can I do?**
Try the single-call approach (Stretch Goal) — pass the entire outline in one prompt and ask the LLM to write all sections. It's faster and often produces more cohesive content.

**Q: Can I change the output format printed by `main.py`?**
The three sections (`OUTLINE`, `CONTENT`, `SUMMARY`) should be preserved. You may enhance the formatting or add separators.

---

## 💬 Need Help?

- Post questions in the cohort Discord/WhatsApp group under `#assignment-1-help` as instructed.
- Check the notebook hints before asking — most common issues are covered there.

> 🧠 **Pro Tip:** This assignment has three LLM calls in sequence — each one depends on the output of the last. That's a real-world AI pipeline. The biggest skill here isn't just making each call work; it's making the *handoff* between steps clean. Spend time on how you parse `generate_outline()`'s output and feed it into `generate_content()` — that's where most bugs hide.

---

*Happy building! The scaffolding is ready — your job is to bring it to life.* 🚀
