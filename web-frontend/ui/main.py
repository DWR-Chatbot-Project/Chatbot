import datetime
import os

import openai
import requests
import uvicorn
from dotenv import load_dotenv
# from flask import Flask, redirect, render_template, request, session, url_for
from fastapi import (Cookie, Depends, FastAPI, Form, HTTPException, Request,
                     Response)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import bloom, langOpen

load_dotenv()
app = FastAPI()
app.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')
# openai.api_key = os.environ.get("OPENAI_API_KEY")
openai_api_key_header = APIKeyHeader(name="token")

bloomLlama = None
langChainAI = None
# index = initialize_index("index.json")
OPENAI_API_KEY = ""

# mounts the static folder that contains the css file
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# locates the template files that will be modified at run time
# with the dialog form the user and bot
templates = Jinja2Templates(directory="templates")

# user data
user = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})

def validate(token: str):
    api_endpoint = "https://api.openai.com/v1/chat/completions"
    api_key = token

    headers = {
        "Content-Type" : "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "user", "content": "Say this is a test!"}
    ]

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }

    response = requests.post(api_endpoint, json=data, headers=headers)
    return response

# Beware that most browsers cache GET requests 
# (i.e., saved in browser's history), thus making 
# them less secure compared to POST, as the data 
# sent are part of the URL and visible to anyone 
# who has access to the device. Thus, GET method 
# should not be used when sending passwords or 
# other sensitive information.
# @app.post("/login", response_class=HTMLResponse)
# async def login(token: str, request: Request):
#     # form = await request.form()
#     # print("login form data:", form.values())
#     # api_key = form.get("access_token")
#     print("apikey from login main.py: ", token)
#     try:
#         response = validate(token)
#         print("login response: ", response.json())
#         if ("error" in response.json()):
#             error = response.json()["error"]
#             raise HTTPException(status_code=400, detail=error["message"])
#     except Exception as e:
#         context = {"request": request, "error_message": str(e)}
#         print("login error: ", context)
#         return templates.TemplateResponse('login.html', context=context)
    
#     return templates.TemplateResponse("chatbot.html", {"request": request})

# @app.post("/login")
# async def login(token: str, response: Response):
#     print("apikey from login main.py: ", token)
    
#     response = validate(token)
#     print("login response: ", response.json())
#     if ("error" in response.json()):
#         error = response.json()["error"]
#          # Redirect back to the login page with an error message
#         response.set_cookie(key="message", value=error.message)
#         return RedirectResponse(url="/login")
    
#     # Store the session token or other identifying information in a cookie
    
#     # response.set_cookie(key="username", value=username)
#     # Redirect to the chatbot page upon successful login
#     return RedirectResponse(url="/chatbot")
    
@app.post("/login")
async def login(token: str, response: Response):
    result = validate(token)
    print("login response: ", result.json())
    if ("error" in result.json()):
        error = result.json()["error"]
        response.set_cookie(key="message", value=error["message"])
        return {"error": error["message"]}
    else:
        return {"redirect": "/chatbot"}

@app.post("/initLlamaIndex")
async def initLlamaIndex(token: str):
    openai.api_key = token
    global bloomLlama
    bloomLlama = bloom.initialize_index("bloomLlama.json")
    return {"success": True}

@app.post("/initLangOpen")
async def initLangOpen(token: str):
    openai.api_key = token
    global langChainAI
    langChainAI = langOpen.initialize_index("langOpen")
    return {"success": True}

# Chatbot endpoint
@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot(request: Request):
    startTime = ""
    context = {"request": request, "startTime": startTime}
    return templates.TemplateResponse("chatbot.html", context=context)

@app.get("/reply")
def reply(input: str, modelName: str):
    if (modelName == "bloom"):
        bot_reply = bloomLlama.query(input)
        return {"bot_reply": bot_reply}
    else:
        bot_reply = langOpen.answer_question(langChainAI, input)
        print("bot reply: ", bot_reply)
        return {"bot_reply": bot_reply}
    
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
