import os
import argparse
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# ── Initialise LLM ────────────────────────────────────────────────────────────
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY is missing. Add it to your .env file or environment."
    )

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)


# ── Stage 1: Generate Outline ─────────────────────────────────────────────────
def generate_outline(topic: str) -> list:
    """
    Generates a structured blog post outline for the given topic.

    Args:
        topic (str): The subject of the blog post.

    Returns:
        list: A list of section heading strings.
    """
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="""
You are an expert blog outline writer.

Create a structured outline for a blog post about:
{topic}

Instructions:
1. Return exactly 5 numbered section headings.
2. Put each heading on a separate line.
3. Make the headings relevant to the topic.
4. Arrange them in a logical sequence.
5. Do not include explanations or introductory text.
6. Return only the numbered list.
"""
    )

    formatted = prompt.format(topic=topic)
    response = llm.invoke(formatted)

    # Split the response into lines and remove blank lines
    outline = [
        line.strip()
        for line in response.content.splitlines()
        if line.strip()
    ]

    return outline


# ── Stage 2: Generate Full Content ────────────────────────────────────────────
def generate_content(outline: list) -> str:
    """
    Expands an outline into a full markdown-formatted blog post.

    Args:
        outline (list): Section headings from generate_outline().

    Returns:
        str: A complete blog post in Markdown format.
    """
    outline_str = "\n".join(outline)

    prompt = PromptTemplate(
        input_variables=["outline"],
        template="""
You are an expert technical blog writer.

Write a complete, informative blog post based on this outline:

{outline}

Instructions:
1. Start with an appropriate blog title.
2. Follow the outline sections in the order provided.
3. Use Markdown headings (##) for each main section.
4. Write 2-3 informative paragraphs per section.
5. Explain technical concepts clearly and accurately.
6. Include practical examples where appropriate.
7. Use smooth transitions between sections.
8. Finish with a useful conclusion.
9. Do not repeat the numbered outline as the entire article.
10. Return only the completed Markdown blog post.
"""
    )

    formatted = prompt.format(outline=outline_str)
    response = llm.invoke(formatted)

    return response.content


# ── Stage 3: Summarize ────────────────────────────────────────────────────────
def summarize(content: str) -> str:
    """
    Produces a concise 3-5 sentence summary of the full blog post.

    Args:
        content (str): The full blog post text.

    Returns:
        str: A short summary paragraph.
    """
    # Truncate content to limit prompt size
    content_trimmed = content[:3000]

    prompt = PromptTemplate(
        input_variables=["content"],
        template="""
You are an expert summarization assistant.

Summarize the following blog post:

{content}

Instructions:
1. Summarize the main topic and key takeaways.
2. Preserve the most important information.
3. Use clear, concise language.
4. Do not introduce facts absent from the original content.
5. Write exactly 3-5 sentences.
6. Return only the summary paragraph.
"""
    )

    formatted = prompt.format(content=content_trimmed)
    response = llm.invoke(formatted)

    return response.content


# ── Main (CLI entry point) ────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=(
            "AI Content Generator — generates a blog outline, "
            "content, and summary."
        )
    )

    parser.add_argument(
        "--topic",
        required=True,
        help='Topic for the blog post. Example: "Getting started with LangChain"'
    )

    args = parser.parse_args()

    print("\n🔄 Running Content Generator Pipeline")
    print(f"   Topic: {args.topic}")
    print("=" * 60)

    try:
        # Step 1: Generate outline
        print("\n📝 STEP 1 — Generating Outline...")
        outline = generate_outline(args.topic)

        if not outline:
            raise RuntimeError("The LLM did not generate an outline.")

        print("OUTLINE:")
        for i, point in enumerate(outline, 1):
            print(f"  {i}. {point}")

        # Step 2: Generate content
        print("\n📄 STEP 2 — Generating Full Content...")
        content = generate_content(outline)

        if not content.strip():
            raise RuntimeError("The LLM did not generate blog content.")

        print("\nCONTENT (first 500 characters):")
        print(content[:500], "...")

        # Step 3: Generate summary
        print("\n🔍 STEP 3 — Summarizing...")
        summary = summarize(content)

        if not summary.strip():
            raise RuntimeError("The LLM did not generate a summary.")

        print("\nSUMMARY:")
        print(summary)

        print("\n" + "=" * 60)
        print("✅ Content generation pipeline completed successfully!")

    except Exception as exc:
        print(f"\n❌ Pipeline failed: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()