INPUT
-----
{
  "messages": ["what is my name?"]
}

        │
        ▼

CHATBOT NODE
------------
LLM invoked

        │
        ▼

RESPONSE GENERATED
------------------
"I don't know your name yet."

        │
        ▼

NEW STATE
---------
{
 "messages": [
   "what is my name?",
   "I don't know your name yet."
 ]
}

        │
        ▼

LOOP RECEIVES chunk
-------------------

chunk = {
 "messages": [
   HumanMessage(...),
   AIMessage(...)
 ]
}

        │
        ▼

chunk["messages"][-1]
---------------------

AIMessage("I don't know your name yet.")

        │
        ▼

pretty_print()

OUTPUT
------

AI: I don't know your name yet.