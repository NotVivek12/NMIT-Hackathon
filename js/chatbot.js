// Chatbot functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatbotMessages = document.getElementById('chatbot-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-btn');
    
    // API base URL - change this to the actual backend URL when deployed
    const API_BASE_URL = '/api';  // Will be served by FastAPI at the same origin
    
    // Add event listeners for chatbot
    if (sendButton && userInput) {
        // Send message on button click
        sendButton.addEventListener('click', () => {
            sendMessage();
        });

        // Send message on Enter key
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Function to add a message to the chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message');
        
        if (isUser) {
            messageDiv.classList.add('user');
        } else {
            messageDiv.classList.add('bot');
        }

        const avatar = document.createElement('div');
        avatar.classList.add('chat-avatar');
        
        const icon = document.createElement('i');
        icon.classList.add('fas');
        icon.classList.add(isUser ? 'fa-user' : 'fa-robot');
        
        avatar.appendChild(icon);
        
        const bubble = document.createElement('div');
        bubble.classList.add('chat-bubble');
        
        if (typeof message === 'string') {
            const p = document.createElement('p');
            p.textContent = message;
            bubble.appendChild(p);
        } else {
            // Complex message with multiple parts
            if (message.response) {
                const p = document.createElement('p');
                p.textContent = message.response;
                bubble.appendChild(p);
            }
            
            if (message.details) {
                const ul = document.createElement('ul');
                message.details.forEach(detail => {
                    const li = document.createElement('li');
                    li.textContent = detail;
                    ul.appendChild(li);
                });
                bubble.appendChild(ul);
            }
            
            if (message.image) {
                const img = document.createElement('img');
                img.src = message.image;
                img.alt = "Generated image";
                bubble.appendChild(img);
            }
            
            if (message.map) {
                const p = document.createElement('p');
                const a = document.createElement('a');
                a.href = message.map;
                a.target = "_blank";
                a.textContent = "View on map";
                p.appendChild(a);
                bubble.appendChild(p);
            }
            
            if (message.suggestions) {
                const p = document.createElement('p');
                p.textContent = "You can try:";
                bubble.appendChild(p);
                
                const ul = document.createElement('ul');
                message.suggestions.forEach(suggestion => {
                    const li = document.createElement('li');
                    li.textContent = suggestion;
                    ul.appendChild(li);
                });
                bubble.appendChild(ul);
            }
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        
        chatbotMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of the chat
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Function to show loading indicator
    function showLoading() {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', 'bot');
        messageDiv.id = 'loading-message';
        
        const avatar = document.createElement('div');
        avatar.classList.add('chat-avatar');
        
        const icon = document.createElement('i');
        icon.classList.add('fas', 'fa-robot');
        
        avatar.appendChild(icon);
        
        const bubble = document.createElement('div');
        bubble.classList.add('chat-bubble');
        
        const loadingIndicator = document.createElement('div');
        loadingIndicator.classList.add('loading-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('loading-dot');
            loadingIndicator.appendChild(dot);
        }
        
        bubble.appendChild(loadingIndicator);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        
        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Function to remove the loading indicator
    function removeLoading() {
        const loadingMessage = document.getElementById('loading-message');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }

    // Function to detect intent from user input
    function detectIntent(input) {
        input = input.toLowerCase();
        
        if (input.includes('youtube') || input.includes('summarize') || input.includes('video')) {
            return 'youtube';
        } else if (input.includes('weather') || input.includes('forecast')) {
            return 'weather';
        } else if (input.includes('ev') || input.includes('charging') || input.includes('station')) {
            return 'ev';
        } else if (input.includes('draw') || input.includes('generate') || input.includes('image') || input.includes('picture')) {
            return 'image';
        } else if (input.includes('bitcoin') || input.includes('price') || input.includes('crypto') || input.includes('eth')) {
            return 'crypto';
        } else {
            return 'unknown';
        }
    }

    // Function to extract parameters from user input
    function extractParams(input, intent) {
        switch (intent) {
            case 'youtube':
                // Extract YouTube URL
                const urlRegex = /(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)[a-zA-Z0-9_-]+)/i;
                const match = input.match(urlRegex);
                return match ? { url: match[0] } : null;
                
            case 'weather':
                // Extract location
                const weatherLocation = input.replace(/weather|forecast|temperature|in/gi, '').trim();
                if (weatherLocation) {
                    return { location: weatherLocation };
                }
                return null;
                
            case 'ev':
                // Extract location for EV stations
                const evLocation = input.replace(/ev|charging|station|near|find|stations/gi, '').trim();
                if (evLocation) {
                    return { location: evLocation };
                }
                return null;
                
            case 'image':
                // Extract prompt for image generation
                const prompt = input.replace(/draw|generate|image|picture|of|a/gi, '').trim();
                if (prompt) {
                    return { prompt };
                }
                return null;
                
            case 'crypto':
                // Extract cryptocurrency symbol
                let symbol = 'BTC'; // Default
                if (input.includes('ethereum') || input.includes('eth')) {
                    symbol = 'ETH';
                } else if (input.includes('solana') || input.includes('sol')) {
                    symbol = 'SOL';
                } else if (input.includes('doge') || input.includes('dogecoin')) {
                    symbol = 'DOGE';
                }
                return { symbol };
                
            default:
                return null;
        }
    }

    // Function to call API based on intent
    async function callAPI(intent, params) {
        try {
            let endpoint = '';
            let requestBody = {};
            
            switch (intent) {
                case 'youtube':
                    endpoint = `${API_BASE_URL}/youtube/summarize`;
                    requestBody = { url: params.url };
                    break;
                    
                case 'weather':
                    endpoint = `${API_BASE_URL}/weather/current`;
                    requestBody = { location: params.location };
                    break;
                    
                case 'ev':
                    endpoint = `${API_BASE_URL}/ev/nearby`;
                    requestBody = { location: params.location };
                    break;
                    
                case 'image':
                    endpoint = `${API_BASE_URL}/image/generate`;
                    requestBody = { prompt: params.prompt };
                    break;
                    
                case 'crypto':
                    endpoint = `${API_BASE_URL}/crypto/price`;
                    requestBody = { symbol: params.symbol };
                    break;
                    
                default:
                    throw new Error('Unknown intent');
            }
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
            
        } catch (error) {
            console.error('API call error:', error);
            return null;
        }
    }

    // Function to format API response for display
    function formatResponse(intent, apiResponse) {
        if (!apiResponse) {
            return {
                response: "I'm having trouble with that request right now. Please try again later.",
                details: ["There was an error processing your request."]
            };
        }
        
        switch (intent) {
            case 'youtube':
                return {
                    response: `Here's a summary of "${apiResponse.title}":`,
                    details: apiResponse.summary
                };
                
            case 'weather':
                return {
                    response: `Current weather in ${apiResponse.weather.location}:`,
                    details: [
                        `Temperature: ${apiResponse.weather.temperature}°C (${apiResponse.weather.temperature_fahrenheit.toFixed(1)}°F)`,
                        `Conditions: ${apiResponse.weather.conditions}`,
                        `Humidity: ${apiResponse.weather.humidity}%`,
                        `Wind Speed: ${apiResponse.weather.wind_speed} km/h`
                    ]
                };
                
            case 'ev':
                const stationDetails = apiResponse.stations.map(station => 
                    `🔌 ${station.name} - ${station.available}/${station.total} available`
                );
                return {
                    response: `I found these EV charging stations near ${apiResponse.location}:`,
                    details: stationDetails,
                    map: apiResponse.map_url
                };
                
            case 'image':
                return {
                    response: `I've created an image based on: "${apiResponse.prompt}"`,
                    image: apiResponse.image_url
                };
                
            case 'crypto':
                return {
                    response: `Current ${apiResponse.name} (${apiResponse.symbol}) price:`,
                    details: [
                        `${apiResponse.symbol}/USD: $${apiResponse.crypto.price.toLocaleString()} (${apiResponse.crypto.change_24h > 0 ? '+' : ''}${apiResponse.crypto.change_24h.toFixed(2)}% in last 24h)`,
                        `Market Cap: $${(apiResponse.crypto.market_cap / 1_000_000_000).toFixed(1)} Billion`,
                        `24h Volume: $${(apiResponse.crypto.volume_24h / 1_000_000_000).toFixed(1)} Billion`
                    ]
                };
                
            default:
                return {
                    response: "I'm not sure how to help with that yet. Here are some things you can try:",
                    suggestions: [
                        "Summarize this YouTube video: https://youtube.com/watch?v=dQw4w9WgXcQ",
                        "What's the weather in Tokyo?",
                        "Find EV charging stations near Central Park",
                        "Draw a cat playing piano",
                        "What's the price of Bitcoin?"
                    ]
                };
        }
    }

    // Function to handle API errors with fallback responses
    function getFallbackResponse(intent) {
        // Simulate responses for demonstration when API is unavailable
        const fallbacks = {
            youtube: {
                response: "Here's a summary of that YouTube video:",
                details: [
                    "The video discusses climate change impacts on global ecosystems.",
                    "Key points include rising sea levels affecting coastal communities.",
                    "It presents solutions like renewable energy and policy changes."
                ]
            },
            weather: {
                response: "Here's the current weather in Tokyo:",
                details: [
                    "Temperature: 22°C (72°F)",
                    "Conditions: Partly Cloudy",
                    "Humidity: 65%",
                    "Wind: 8 km/h"
                ]
            },
            ev: {
                response: "I found these EV charging stations near Central Park:",
                details: [
                    "🔌 Central Park North - 110th St (2 available)",
                    "🔌 Columbus Circle Parking (4 available)",
                    "🔌 Museum of Natural History Garage (1 available)"
                ],
                map: "https://www.google.com/maps/search/ev+charging+stations/@40.7831,-73.9712,14z/"
            },
            image: {
                response: "I've created an image of a cat playing piano:",
                image: "https://via.placeholder.com/400x300/6200ea/FFFFFF?text=Cat+Playing+Piano"
            },
            crypto: {
                response: "Current Bitcoin price:",
                details: [
                    "BTC/USD: $51,432.78 (+2.3% in last 24h)",
                    "Market Cap: $986.7 Billion",
                    "24h Volume: $32.4 Billion"
                ]
            },
            default: {
                response: "I'm not sure how to help with that yet. Here are some things you can try:",
                suggestions: [
                    "Summarize this YouTube video: https://youtube.com/watch?v=dQw4w9WgXcQ",
                    "What's the weather in Tokyo?",
                    "Find EV charging stations near Central Park",
                    "Draw a cat playing piano",
                    "What's the price of Bitcoin?"
                ]
            }
        };
        
        return fallbacks[intent] || fallbacks.default;
    }

    // Function to send message
    async function sendMessage() {
        const message = userInput.value.trim();
        
        if (message) {
            // Add user message to chat
            addMessage(message, true);
            userInput.value = '';
            
            // Show loading indicator
            showLoading();
            
            // Detect intent from message
            const intent = detectIntent(message);
            
            // Extract parameters based on intent
            const params = extractParams(message, intent);
            
            try {
                // Only call API if we have the necessary parameters
                let response;
                
                if (params) {
                    // Call the appropriate API
                    const apiResponse = await callAPI(intent, params);
                    
                    // Format the response for display
                    response = formatResponse(intent, apiResponse);
                } else {
                    // No parameters, use default response
                    response = getFallbackResponse('default');
                }
                
                // Remove loading indicator
                removeLoading();
                
                // Add bot response to chat
                addMessage(response);
                
            } catch (error) {
                console.error('Error processing message:', error);
                
                // Remove loading indicator
                removeLoading();
                
                // Use fallback response
                const fallback = getFallbackResponse(intent);
                addMessage(fallback);
            }
        }
    }
}); 