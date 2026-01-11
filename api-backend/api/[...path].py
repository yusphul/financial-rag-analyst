# api-backend/api/[...path].py
from api.index import app  # FastAPI app

# Vercel will route /api/* to this catch-all file,
# and FastAPI will handle paths like /health, /chat, etc.