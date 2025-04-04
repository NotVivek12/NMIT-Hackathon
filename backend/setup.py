from setuptools import setup, find_packages

setup(
    name="omnibot-api",
    version="1.0.0",
    packages=find_packages(),
    description="Backend API for OmniBot - The AI Swiss Army Knife",
    author="NMIT Hackathon Team",
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "pydantic>=2.0.2",
        "python-dotenv>=1.0.0",
        "httpx>=0.24.1",
        "python-multipart>=0.0.6",
        "requests>=2.31.0",
        "jinja2>=3.1.2",
        "youtube-transcript-api>=0.6.1",
        "openai>=0.27.8",
        "groq>=0.3.0",
        "serper-dev>=0.1.4",
        "opencage>=2.3.0",
        "beautifulsoup4>=4.12.2",
        "alpaca-trade-api>=3.0.0",
    ],
) 