<h1>Building a Cooking Expert AI Agent with Phidata and Django Rest Framework (DRF)</h1>

Updated blog link: https://dev.to/shemanto_sharkar/building-a-cooking-expert-ai-agent-with-phidata-and-django-rest-framework-drf-3nch

![Screen-Recording](https://github.com/user-attachments/assets/ebcddd15-1e24-4848-86ea-5808c3606f68)


Artificial Intelligence (AI) is reshaping industries, and the concept of AI agents is leading this transformation. Imagine a world where billions of AI agents assist us in every field of work – from healthcare and education to cooking and transportation. Even Mark Zuckerberg has spoken about the rise of AI agents and their potential to revolutionize how we interact with technology. In this blog, I’ll walk you through the process of building a custom AI agent api using **Phidata** and **Django Rest Framework (DRF)**. This agent will act as a **cooking and food expert**, answering your culinary questions and providing helpful tips and recipes.

---

## **What is an AI Agent?**

Imagine you have a virtual assistant in your kitchen named ChefBot. You can ask ChefBot, "How do I bake a chocolate cake?" or "What can I cook with chicken and spinach?" ChefBot understands your questions, uses its knowledge of recipes, and provides accurate and helpful answers. That’s what an **AI agent** does.

An **AI agent** is a software entity that performs tasks intelligently by interacting with users, tools, and other systems. Unlike an AI model, which is just a mathematical function trained on data, an **agent** is a complete system that leverages one or more models to achieve specific objectives. It combines the following components:

- **AI Model**: The underlying machine learning model, such as GPT or Groq, that generates intelligent responses.
- **Tools**: Plugins or functionalities the agent can use, such as web search or APIs.
- **Knowledge Base**: A storage system for the agent’s memory or external knowledge.
- **Storage**: A backend system, like a database, for session management or historical data.

In this project, we’ll use **Phidata** to build an AI agent specialized in food and cooking. Our agent will provide recipes, cooking tips, and answer food-related queries.

---

## **What Makes Phidata Special?**

Phidata simplifies the creation of AI agents by providing:

1. **Model Integration**:
   - Easily integrate pre-trained models like OpenAI GPT or Groq.
   - Customize model behavior using descriptions and instructions.

2. **Tools**:
   - **What are tools?** Tools extend the agent’s abilities by connecting it to external functionalities. For example:
     - A **web search tool** can help the agent look up recipes or cooking methods online if its internal knowledge is insufficient.
     - A **unit conversion tool** could allow the agent to convert between cups and grams seamlessly.
   - **Analogy**: Think of tools as specialized gadgets your ChefBot uses to enhance its cooking knowledge, like a spice rack or a cookbook.

3. **Knowledge Base**:
   - **What is a knowledge base?** It is where the agent stores and retrieves information. For example:
     - A vector database like **PgVector** can store recipes and their ingredients in a way that the agent can search and retrieve related information efficiently.
     - Semantic search in the knowledge base enables the agent to answer "What desserts can I make with chocolate?" by looking up stored recipes.
   - **Analogy**: Imagine ChefBot has a personal diary of recipes and tips it can flip through to answer your questions.

4. **Storage**:
   - **What is storage?** This refers to databases used for session management or storing interaction history. For example:
     - A **Postgres database** can store past interactions, so the agent remembers what you asked last time.
     - This is useful for continuity in conversations or analyzing frequently asked questions.
   - **Analogy**: ChefBot keeps a logbook of all your past recipe requests to serve you better in the future.

By combining these features, Phidata allows developers to build comprehensive, intelligent agents tailored to specific needs.

---

## **Project Overview**

We’ll build a **Cooking Expert AI Agent** that:
1. Accepts cooking-related instructions from the user via a REST API.
2. Processes the instruction using a pre-trained AI model (e.g., Groq).
3. Returns the agent’s intelligent response with helpful food-related information.

### **Technologies Used**
- **Django**: Web framework for building the API.
- **Django REST Framework (DRF)**: For creating and managing API endpoints.
- **Phidata**: To define and interact with the AI agent.


---

## **Step-by-Step Guide**
### **0. create python environment**
Open your terminal or command prompt.

Create the environment,I am using conda package manager:
```bash
conda create -n myenv python=3.12 -y
```
activate the environment
```bash
conda activate myenv```

### **1. Setting Up the Project**
Install the required dependencies:
```bash
pip install django djangorestframework phidata python-dotenv groq
```

Start by creating a new Django project and app:
```bash
django-admin startproject my_project .
django-admin startapp api
```



Add `rest_framework` and `api` to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'api',
]
```

---

### **2. Defining the AI Agent**
Create a folder named `agents/` to store the agent logic. In `agents/agent.py`, define your custom agent:

```python
from phi.agent import Agent
from phi.model.groq import Groq

from dotenv import load_dotenv
load_dotenv()

chef_agent = Agent(
    model=Groq(id='llama-3.3-70b-versatile'),
    tools=[],
    show_tool_calls=True,
    description="You are a recipe expart. You will be given a recipe and you have to answer the questions related to it.",
    instructions=[""],
)

def process_instruction(instruction: str) -> str:
    response = chef_agent.run(instruction, stream=False)
    return response.content
```

---

### **3. Creating the API**

#### **Serializers**
In `api/serializers.py`, define the input and output serializers:

```python
from rest_framework import serializers

class InstructionSerializer(serializers.Serializer):
    instruction = serializers.CharField(max_length=500)

class ResponseSerializer(serializers.Serializer):
    response = serializers.CharField(max_length=10000)  
```

#### **Views**
In `api/views.py`, implement the API view:

```python
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from agents.agent import process_instruction

class AgentView(APIView):
    def post(self, request):
        serializer = instruction_serializer(data=request.data)
        # input validation
        if serializer.is_valid():
            instruction = serializer.validated_data['instruction']
            
            #process the instruction using agent
            try:
                agent_response = process_instruction(instruction)
                
            except Exception as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            #return the response
            response = {"response" : agent_response}
            response_data = response_serializer(data=response)
            if response_data.is_valid():
                return Response(response_data.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### **Routing**
In `api/urls.py`, define the endpoint:

```python
from django.urls import path
from .views import AgentView

urlpatterns = [
    path('agent/', AgentView.as_view(), name='agent-api'),
]
```

Include this in the main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),
]
```

---

### **4. Running the Project**
Run the Django development server:
```bash
python manage.py runserver
```

Send a POST request to `http://127.0.0.1:8000/api/agent/` with a JSON body:
```json
{
    "instruction": "How do I bake a chocolate cake?"
}
```

The response will be:
```json
{
    "response": "Baking a chocolate cake requires the following steps: ..."
}
```

---

### **5. Key Learnings**

- **Phidata**: Simplifies AI integration with pre-built tools and models.
- **Django REST Framework**: Provides a robust and scalable way to create APIs.
- **Dotenv**: Keeps sensitive configurations secure and manageable.

---

### **Next Steps**

- Add tools to your agent for more functionality (e.g., web search, database queries).
- Deploy your application using ASGI servers like Uvicorn or Daphne for better scalability.
- Extend the agent to include memory or knowledge base integration.

Building an AI agent with Phidata and Django REST Framework unlocks a wide range of possibilities for creating intelligent web applications. Let your imagination run wild and start building AI-powered tools today!

---

Do you have questions or ideas for improvement? Feel free to share your thoughts in the comments!

