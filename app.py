from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. Define a tool (e.g., a simple calculator)
def calculate(expression: str) -> str:
    try:
        return str(eval(expression)) # Be cautious with eval in production!
    except Exception as e:
        return f"Error: {e}"

tools = [
    Tool(
        name="calculator",
        func=calculate,
        description="Useful for performing calculations. Input should be a mathematical expression.",
    )
]

# 2. Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0) # Replace with your preferred LLM

# 3. Define the prompt for the agent
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant. Use the calculator tool when needed."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# 4. Create the agent
agent = create_react_agent(llm, tools, prompt)

# 5. Create the agent executor (the runtime for the agent)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 6. Run the agent
response = agent_executor.invoke({"input": "What is 123 * 456?"})
print(response["output"])