from agents import State, router_agent, info_collection_agent, simplifier_agent
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Initialize the StateGraph
graph = StateGraph(State)

graph.add_node("classifier", router_agent)
graph.add_node("info_collector", info_collection_agent)
graph.add_node("simplifier", simplifier_agent)

graph.add_edge(START, "classifier")
graph.add_edge("classifier", "info_collector")
graph.add_edge("info_collector", "simplifier")
graph.add_edge("simplifier", END)

app = graph.compile()

# Run the application
if __name__ == "__main__":
    while True:
        user_input = input("\nSmart Explainer Ready! Ask me anything (or type 'quit' to exit): ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break

        inputs = {
            "user_input": user_input,
            "messages": []  
        }
        print("\nThinking...\n" + "-"*50)
        for step in app.stream(inputs, stream_mode="values"):
            if "final_answer" in step:
                print("\nFinal Answer:\n")
                print(step["final_answer"])
        print("-"*50)