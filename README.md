# OmniBot - Multi-Service Chatbot

OmniBot is a versatile chatbot that integrates multiple services to provide users with various functionalities through a single interface. The project was developed as part of the NMIT Hackathon.

## Features

- **YouTube Summarization**: Get concise summaries of YouTube videos by providing the URL
- **Weather Information**: Check weather conditions for any location
- **EV Charging Station Finder**: Locate nearby EV charging stations
- **Image Generation**: Generate images from text descriptions
- **Cryptocurrency Pricing**: Get real-time cryptocurrency price information

## Tech Stack

### Backend
- FastAPI (Python)
- Various API integrations (YouTube Transcript, OpenWeatherMap, Open Charge Map, DALL-E, CoinGecko)
- JWT Authentication
- Groq/Gemini AI for content processing

### Frontend
- HTML, CSS, JavaScript
- Interactive chat interface

## Setup and Installation

1. Clone the repository:
```
git clone https://github.com/NotVivek12/NMIT-Hackathon.git
```

2. Navigate to the project directory:
```
cd NMIT-Hackathon
```

3. Install backend requirements:
```
cd backend
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
WEATHER_API_KEY=your_openweathermap_api_key
```

5. Run the application:
```
python run.py
```

6. Access the application at `http://localhost:8001` or the login page at `http://localhost:8001/login`

## Authentication

- Login with demo credentials:
  - Email: demo@example.com
  - Password: password123
- Or register a new account

## Usage Examples

- "Summarize this YouTube video: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
- "What's the weather like in London?"
- "Find EV charging stations near Barcelona"
- "Generate an image of a cat playing piano"
- "Show me the price of Bitcoin"

## Contributors

- Team NMIT Hackathon