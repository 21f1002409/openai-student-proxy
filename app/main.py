from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, api_keys, openai_proxy

app = FastAPI(
    title="Student OpenAI API Proxy",
    description="A serverless API that provides temporary access to OpenAI API for students",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(api_keys.router)
app.include_router(openai_proxy.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Student OpenAI API Proxy",
        "docs": "/docs",
        "version": "1.0.0"
    }
