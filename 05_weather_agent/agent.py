from dotenv import load_dotenv
import os
import requests
from openai import OpenAI
import json

load_dotenv();


# this was one of the tool used to get the weather of the city and this tool is going to be used by the agent whenever required and the agent can call this tool by following the rules mentioned in the system prompt
def get_weather(city:str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('OPEN_WEATHER_API')}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city.lower()} is {response.text}"
    
    return f"Some thing went wrong"

available_tools = {
    "get_weather":get_weather
}



client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


SYSTEM_PROMPT = '''
     you are expert ai assisatant in resolving using queires using chain of thought you work on START , PLAN and OUTPUT steps .
     
     you need to plan what need to be done , the plan can be multiple steps once you think enough plan has been done finally you can give an output
     
     for every tool call wait for the observe step which is the output from the called tool.
     
     Rules : 
        -Strictly follow given json output format
        -only run once step at a time 
        -the sequence of steps is start (where user gives an input) , PLAN(That can be multiple times) and finally OUTPUT(which is going to be dispayed to the user)
        -you can also call the tool  if required from the list of available tools
    
    Output JSON format:
    {"step":"START" | "PLAN" | "OUTPUT" | "TOOL" , "content":"string","tool":"string", "input":"string"}
    
    Available Tools :
    1. get_weather(city:str) : this tool gives the current weather of the city in string format
    
    Example:- 
    1.
    
    START: Hey , can you solve 2 + 3 * 5 / 10;
    PLAN:{"step":"PLAN" , "content":"seems line user intrested in maths problem"}
    PLAN:{"step":"PLAN" , "content":"Looking at the problem the problem can solved by using the algebra"}
    PLAN:{"step":"PLAN" , "content":"yes the bodmas is the correct thing to be done here"}
    PLAN:{"step":"PLAN" , "content":"first we must multiply 3 * 5 which is 15"}
    PLAN:{"step":"PLAN" , "content":"now the new equztion is 2 + 15 / 10"}
    PLAN:{"step":"PLAN" , "content":"now we must perform divide 15 / 10 = 1.5"}
    PLAN:{"step":"PLAN" , "content":"now the new equztion is 2 + 1.5"}
    PLAN:{"step":"PLAN" , "content":"now we must perform addition 2 +1.5"}
    PLAN:{"step":"PLAN" , "content":"now finally perform the add 2 + 1.5 = 3.5 "}
    PLAN:{"step":"PLAN" , "content":"Great , we have solved and finaly got the answer with 3.5 as ans "}
    PLAN:{"step":"OUTPUT" , "content":"3.5"}
    
    2.
    
    START: Hey , what is the current weather in delhi?
    PLAN:{"step":"PLAN" , "content":"seems like user is intrested in knowing the current weather of delhi"};
    PLAN:{"step":"PLAN" , "content":"lets see if we have a tool to get the weather information"};
    PLAN:{"step":"PLAN" , "content":"great we have a tool called get_weather(city:str) that can give us the current weather of the city in string format"};
    PLAN:{"step":"PLAN" , "content":"i need to call the tool get_weather(city:str) with the city name as delhi"};
    PLAN:{"step":"TOOL" , "tool":"get_weather", "input":"delhi"}
    PLAN:{"step":"OBSERVER" , "content":"The weather in delhi is sunny with temperature 25°C"}
    PLAN:{"step":"PLAN" , "content":"Great , i have got the weather information of delhi now i can give the final output to the user"};
    PLAN:{"step":"OUTPUT" , "content":"The current weather in delhi is sunny with temperature 25°C"}
    
    
'''

# steps to automate this process

# 1. base condition :- when the step is OUTPUT then break and stop the    api calls

# 2. take query from the user and then process 

# 3. continue the thinking process up to the step:OUTPUT


print("\n\n\n")


message_history = [
     {'role':"system","content":SYSTEM_PROMPT},
]
while True:
    user_query = input(f"👉 Enter Your Query Here : ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        reponse = client.chat.completions.create(
            model="gemini-2.5-flash",
            response_format={
                "type":"json_object"
            },  
            messages = message_history
        )
        raw_result = (reponse.choices[0].message.content)
        message_history.append({"role":"assistant","content":raw_result})
        # we have to continuesly append the message for the continues chain of thought process and also for the tool calls and its response 
        parsed_result = json.loads(raw_result)
        
        if parsed_result.get("step") == "START":
            print("🔥",parsed_result.get("content"))
            continue
        
        if parsed_result.get("step") == "PLAN":
            print("🧠",parsed_result.get("content"))
            continue
        
        if parsed_result.get("step") == "TOOL":
            tool_to_be_called = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            print("� Calling tool:", tool_to_be_called, "with input:", tool_input)
            tool_response = available_tools[tool_to_be_called](tool_input)
            message_history.append({"role":"developer" , "content" : json.dumps({"tool":tool_to_be_called , "input":tool_input,"output":tool_response})})
            continue;
            
            
        if parsed_result.get("step") == "OUTPUT":
            print("📤",parsed_result.get("content"))
            break;
    
    
print("\n\n\n")

    
# reponse = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     response_format={
#         "type":"json_object"
#     },
#     messages=[
#         {'role':"system","content":SYSTEM_PROMPT},
#         {'role':"user","content":"Hey, write a code to add n numbers in java script "},
#         # manually keep adding the message to the history
#         {"role":"assistant","content":json.dumps(
#             {"step":"START", "content":"The user wants a JavaScript function to add 'n' numbers."}
#         )},
#         {"role":"assistant","content":json.dumps(
#             {"step": "PLAN", "content": "The user wants to add 'n' numbers using JavaScript. This implies a function that can accept a variable number of arguments and sum them up."}
#         )},
#         {"role":"assistant","content":json.dumps(
#             {"step": "PLAN", "content": "I will define a JavaScript function called 'addNumbers'. This function should be able to accept any number of arguments."}
#         )},
#         {"role":"assistant","content":json.dumps(
#             {"step": "PLAN", "content": "Inside the function, I will initialize a variable, say `total`, to 0."}
#         )},
#         {"role":"assistant","content":json.dumps(
#             {"step": "PLAN", "content": "I will then iterate over all the arguments passed to the function, adding each argument's value to the `total`."}
#         )},
#         {"role":"assistant","content":json.dumps(
#             {"step": "PLAN", "content": "I will use the rest parameter syntax (`...numbers`) to collect all arguments into an array within the function."}
#         )},
#         {"role":"assistant","content":json.dumps(
#             {"step": "PLAN", "content": "The implementation will involve a loop (like `forEach` or `reduce`) to go through the array of numbers and accumulate their sum."}
#         )},
#         {"role":"assistant","content":json.dumps(
#            {"step": "PLAN", "content": "Finally, I will return the `total`."}
#         )},
#         {"role":"assistant","content":json.dumps(
#            {"step": "OUTPUT", "content": "```javascript\nfunction addNumbers(...numbers) {\n  let total = 0;\n  for (const num of numbers) {\n    total += num;\n  }\n  return total;\n}\n\n// Example usage:\nconsole.log(addNumbers(1, 2, 3));         // Output: 6\nconsole.log(addNumbers(10, 20, 30, 40));  // Output: 100\nconsole.log(addNumbers(5));               // Output: 5\nconsole.log(addNumbers());                // Output: 0\nconsole.log(addNumbers(1.5, 2.5, 3));     // Output: 7\n```"}
#         )},
        
#     ]
# )

# print(reponse.choices[0].message.content)