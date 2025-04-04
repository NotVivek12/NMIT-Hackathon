# OmniBot API Backend

Backend API for OmniBot - The AI Swiss Army Knife, a versatile chatbot that integrates multiple APIs to handle diverse user requests.

## Features

- **YouTube Summary API**: Fetch and summarize YouTube video transcripts
- **Weather API**: Get current weather information for any location
- **EV Charging Stations API**: Find nearby EV charging stations
- **Image Generation API**: Generate images from text prompts using DALL-E
- **Cryptocurrency API**: Get real-time cryptocurrency prices and data
- **Frontend Integration**: Serves the frontend web app and handles API requests

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Groq API**: AI model for text processing and summarization
- **YouTube Transcript API**: For fetching video transcripts
- **OpenWeatherMap API**: For weather data
- **OpenCage API**: For geocoding
- **Open Charge Map API**: For EV charging stations
- **OpenAI API**: For image generation with DALL-E
- **Alpaca/CoinGecko API**: For cryptocurrency data

## Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the `backend` directory with your API keys (see `.env.example` for required keys).

### Running the Application

1. Start the API server:
   ```bash
   python run.py
   ```

2. The API will be available at `http://localhost:8000`
3. API documentation will be available at `http://localhost:8000/docs`

## API Endpoints

### YouTube API

- `POST /api/youtube/summarize`: Summarize a YouTube video by URL

### Weather API

- `POST /api/weather/current`: Get current weather for a location

### EV Stations API

- `POST /api/ev-stations/nearby`: Find nearby EV charging stations

### Image Generation API

- `POST /api/images/generate`: Generate an image based on a text prompt

### Cryptocurrency API

- `POST /api/crypto/price`: Get current price and data for a cryptocurrency

## Development

### Project Structure

```
backend/
├── app/
│   ├── models/         # Pydantic models for request/response
│   ├── routers/        # API route handlers
│   ├── services/       # Business logic and external API integration
│   └── main.py         # FastAPI application initialization
├── .env                # Environment variables (not in version control)
├── .env.example        # Example environment variables
├── requirements.txt    # Project dependencies
├── setup.py            # Package setup
└── run.py              # Script to run the application
```

### Adding a New Service

1. Create a new service class in `app/services/`
2. Create models in `app/models/schemas.py`
3. Create a router in `app/routers/`
4. Register the router in `app/main.py`

## License

This project is licensed under the MIT License. 