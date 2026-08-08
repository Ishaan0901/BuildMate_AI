import os 
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
load_dotenv()


#   Initializig the LLM:
llm=ChatGroq(
    model='llama-3.3-70b-versatile'
)


#                                                           Setting up the state:
#   1. Reducer function:
def reducer(existing_dict:dict,new_dict:dict)->dict:
    if existing_dict==None:
        return new_dict
    return {**existing_dict,**new_dict}

#   2. State dictionary:
class suggesting_state(TypedDict):
    query: str
    info: Annotated[dict[str,str],reducer]



#                                                           Creating the nodes:
#   1. Project advisor:
def advice_agent(state:suggesting_state)->dict:

    prompt = (f'''
    You are a practical Project Idea Advisor for developers and AI/ML learners.
    Analyze the user's learning experience and project description. Identify the main concepts they 
    learned and suggest 3 NEW project ideas that help them apply or extend those concepts.
    For each idea, provide:
    * Project name
    * Short description
    * Key features
    * How the learned concept is used
    * Difficulty level

    Requirements:
    * Make all 3 projects meaningfully different from each other.
    * Progress from beginner-friendly to more challenging.
    * Prefer realistic projects that a student can actually build.
    * Avoid repeating the project already mentioned.
    * Avoid generic or overly ambitious ideas.
    * Do not introduce technologies that are unrelated to the user's topic.
    * Focus on practical use cases rather than simply demonstrating the same concept again.

    Return only the project ideas. Do not add an introduction or conclusion.
    User input:
    {state['query']}
    ''')

    advice=llm.invoke(prompt).content
    return {'info':{'advice':advice}}


#   2. Github Agent:
def github_agent(state:suggesting_state)->dict:

    prompt = f'''
        You are a professional GitHub README writer.
        Create a clean, professional, copy-paste-ready README.md for the project described in the user's input.
        Use Markdown formatting and include these sections when enough information is available:
        # Project Title
        ## Overview
        ## Features
        ## Technologies Used
        ## How It Works
        ## Installation
        ## Usage
        ## Future Improvements

        Requirements:
        * Use only information supported by the user's input.
        * Never invent technologies, features, commands, file names, APIs, or implementation details.
        * If information is missing, omit that section instead of writing "not provided".
        * Keep the explanation concise and technically accurate.
        * Make the README suitable for a student GitHub project.
        * Do not add unnecessary badges, emojis, or promotional language.
        * Do not mention that you are an AI.
        * Return ONLY the final README content.

        User input:
        {state['query']}
        '''

    repo=llm.invoke(prompt).content
    return {'info':{'repo':repo}}


#   3. Linkedin Agent:
def linkedin_agent(state:suggesting_state)->dict:

    prompt = f'''
        You are a LinkedIn content writer helping a developer share their genuine learning journey.
        Read the user's input and write a concise, engaging LinkedIn post about what they learned and what they built.

        The post should:
        * Start with a strong but natural hook.
        * Clearly explain what was learned.
        * Briefly describe what was built.
        * Mention the important technical concepts involved.
        * Include one genuine learning or takeaway.
        * End with a natural closing.
        * Include 4-6 relevant hashtags.

        Writing style:
        * Sound like a real student/developer sharing their progress.
        * Keep the language simple and natural.
        * Be confident but not exaggerated.
        * Avoid corporate or motivational clichés.
        * Avoid phrases like "the possibilities are endless", "game-changing", "unlock the full potential", etc.
        * Do not claim expertise or mastery.
        * Do not invent achievements, results, or technologies.
        * Keep it concise enough for LinkedIn.

        Return ONLY the final LinkedIn post. Do not add explanations or labels such as "Here is your post".

        User input:
        {state['query']}
        '''

    linkedin_post=llm.invoke(prompt).content
    return {'info':{'linkedin_post':linkedin_post}}



#                                                           Creating the Graph:
builder=StateGraph(suggesting_state)

#   Adding Nodes:
builder.add_node('advice_node',advice_agent)
builder.add_node('github_node',github_agent)
builder.add_node('linkedin_node',linkedin_agent)

#   Connecting Nodes:
#   1.Fan-Out
builder.add_edge(START,'advice_node')
builder.add_edge(START,'github_node')
builder.add_edge(START,'linkedin_node')

#   2.Fan-In
builder.add_edge('advice_node',END)
builder.add_edge('github_node',END)
builder.add_edge('linkedin_node',END)

#   compiling the graph:
app=builder.compile()



#                                                           Getting the output from GRAPH....

#   This block only runs when project.py is executed directly (e.g. `python project.py`).
#   Importing this module (e.g. `from project import app`) will NOT trigger it.

if __name__ == "__main__":

    sample_query='''
                    Today I started my LangGraph journey. 
                    I learned about sequential workflows and how states, nodes, and edges work together to build an AI workflow. 
                    To practice this concept, I built a small project where multiple steps execute sequentially 
                    to process a user's input and generate a final response. This project helped me understand 
                    how LangGraph manages state and controls the flow of information between different nodes.
                    '''

    initial_state = {
        "query": sample_query,
        "info": {} 
    }

    print("i got your query ..... let me process it \n")
    result=app.invoke(initial_state)

    #       printing the advice:

    print('='*50,'\n')
    print("\tHere's my advice for you:\n")
    print('='*50,'\n')
    print(result['info']['advice'],'\n\n')

    #       printing the repo:

    print('='*50,'\n')
    print("\tHere is a github repo for you:\n")
    print('='*50,'\n')
    print(result['info']['repo'],'\n\n')

    #       printing the post:

    print('='*50,'\n')
    print("\tHere is a linkedin post for you:\n")
    print('='*50,'\n')
    print(result['info']['linkedin_post'],'\n\n')