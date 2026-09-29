🤖 AI Room Recommendation System

An AI-powered backend system that provides intelligent room recommendations using semantic search and vector embeddings. The system retrieves relevant rooms based on user queries and enhances results using LLM-based responses.

🚀 Features
🧠 Semantic search using vector embeddings (pgvector)
⚡ FastAPI backend for scalable APIs
🤖 LLM-based contextual recommendations
📊 Cosine similarity search for accurate retrieval
🧩 Modular backend architecture (controllers, services, repositories)
📦 Structured API responses and error handling

🏗️ Architecture
The system works in the following flow:

Data Processing
- Room details are converted into embeddings using an LLM

Storage
- Embeddings are stored in PostgreSQL using pgvector

Query Handling
- User query is converted into embedding
- Similarity search retrieves top matching rooms

Response Generation
- LLM generates context-aware recommendations

🛠️ Tech Stack
Backend: FastAPI  
Database: PostgreSQL (pgvector)  
AI/ML: AWS Bedrock (Embeddings + LLM)  
ORM: SQLAlchemy  

📦 Project Setup

1. Clone the repository
git clone https://github.com/aakashkarunanithi/room-recommendation-system
cd room-recommendation-system

2. Install dependencies
pip install -r requirements.txt

3. Setup environment variables

Create a .env file:

DATABASE_URL=
AWS_ACCESS_KEY=
AWS_SECRET_KEY=

4. Run the application
uvicorn main:app --reload

📂 Project Structure

src/
 ├── config/        # Application configuration and environment settings
 ├── constants/     # Static values and constant definitions
 ├── controllers/   # API controllers (request/response handling)
 ├── database/      # Database connection and session management
 ├── dtos/          # Data Transfer Objects for structured API responses
 ├── errors/        # Custom exceptions and error handling logic
 ├── migrations/    # Database migration scripts
 ├── models/        # Database models and schemas
 ├── repositories/  # Data access layer (DB operations)
 ├── routers/       # API route definitions
 ├── services/      # Business logic layer
 ├── utilities/     # Helper functions and reusable utilities
 └── app.py         # Application entry point

🔐 Security
- Environment variables are stored securely in .env
- Sensitive data is excluded using .gitignore
