from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

# # Research Agent: Its job is to use the google_search tool and present findings.
# research_agent = Agent(
#     name="ResearchAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     instruction="""You are a specialized research agent. Your only job is to use the
#     google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
#     tools=[google_search],
#     output_key="research_findings",  # The result of this agent will be stored in the session state with this key.
# )

# print("✅ research_agent created.")

# # Summarizer Agent: Its job is to summarize the text it receives.
# summarizer_agent = Agent(
#     name="SummarizerAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     # The instruction is modified to request a bulleted list for a clear output format.
#     instruction="""Read the provided research findings: {research_findings}
# Create a concise summary as a bulleted list with 3-5 key points.""",
#     output_key="final_summary",
# )

# print("✅ summarizer_agent created.")

# # Root Coordinator: Orchestrates the workflow by calling the sub-agents as tools.
# root_agent = Agent(
#     name="ResearchCoordinator",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     # This instruction tells the root agent HOW to use its tools (which are the other agents).
#     instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
# 1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
# 2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
# 3. Finally, present the final summary clearly to the user as your response.""",
#     # We wrap the sub-agents in `AgentTool` to make them callable tools for the root agent.
#     tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
# )

# print("✅ root_agent created.")

# runner = InMemoryRunner(agent=root_agent)

# Outline Agent: Creates the initial blog post outline.
outline_agent = Agent(
    name="OutlineAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""Create a blog outline for the given topic with:
    1. A catchy headline
    2. An introduction hook
    3. 3-5 main sections with 2-3 bullet points for each
    4. A concluding thought""",
    output_key="blog_outline",  # The result of this agent will be stored in the session state with this key.
)

print("✅ outline_agent created.")

# Writer Agent: Writes the full blog post based on the outline from the previous agent.
writer_agent = Agent(
    name="WriterAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    # The `{blog_outline}` placeholder automatically injects the state value from the previous agent's output.
    instruction="""Following this outline strictly: {blog_outline}
    Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
    output_key="blog_draft",  # The result of this agent will be stored with this key.
)

print("✅ writer_agent created.")

editor_agent = Agent(
    name="EditorAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    # This agent receives the `{blog_draft}` from the writer agent's output.
    instruction="""Edit this draft: {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhancing overall clarity.""",
    output_key="final_blog",  # This is the final output of the entire pipeline.
)

print("✅ editor_agent created.")

root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)

print("✅ Sequential Agent created.")

runner = InMemoryRunner(agent=root_agent)
