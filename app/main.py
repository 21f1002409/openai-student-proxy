
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, api_keys, llm_proxy

app = FastAPI(
    title="Student LLM API Proxy",
    description="A serverless API that provides temporary access to multiple LLM providers for students",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(api_keys.router)
app.include_router(llm_proxy.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Student LLM API Proxy",
        "docs": "/docs",
        "version": "1.0.0"
    }
