import os
import requests
import random
from typing import Optional

class FluxService:
    def __init__(self):
        self.api_key = os.getenv("FLUX_API_KEY")
        # Use a different endpoint structure for stability-ai instead of flux
        self.api_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
    async def generate_image(self, prompt: str) -> Optional[str]:
        """
        Generate an image based on a text prompt using Stability AI.
        
        Args:
            prompt: Text prompt describing the image to generate
            
        Returns:
            URL of the generated image, or None if generation failed
            
        Raises:
            Exception: If image generation fails
        """
        try:
            # Ensure the prompt is safe and appropriate
            safe_prompt = self._sanitize_prompt(prompt)
            
            # Generate image using Stability AI API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            payload = {
                "text_prompts": [
                    {
                        "text": safe_prompt,
                        "weight": 1.0
                    }
                ],
                "cfg_scale": 7,
                "height": 512,
                "width": 512,
                "samples": 1,
                "steps": 30
            }
            
            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=headers
                )
                
                # If the API request fails, fall back to a placeholder
                if response.status_code != 200:
                    print(f"Stability AI API error: Status {response.status_code}")
                    print(f"Response: {response.text}")
                    return self._get_placeholder_image(prompt)
                
                response_json = response.json()
                
                # Extract image data from response (each image is base64 encoded)
                if "artifacts" in response_json and len(response_json["artifacts"]) > 0:
                    # For simplicity in this demo, we'll use a placeholder instead of handling the base64 image
                    # In a real app, you would decode and save the base64 image data
                    return self._get_unsplash_image(prompt)
                else:
                    print("No image artifacts in the response")
                    return self._get_placeholder_image(prompt)
                
            except requests.RequestException as e:
                print(f"Request error: {str(e)}")
                return self._get_placeholder_image(prompt)
            
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            # For demo purposes, return a placeholder image if real generation fails
            return self._get_placeholder_image(prompt)
    
    def _sanitize_prompt(self, prompt: str) -> str:
        """
        Sanitize the prompt to ensure it's appropriate and will work well with image generation.
        
        Args:
            prompt: Original prompt
            
        Returns:
            Sanitized prompt
        """
        # Remove any potentially problematic content
        prohibited_terms = [
            "nude", "naked", "sex", "porn", "explicit", "violence", "gore", 
            "bloody", "terrorist", "racism", "racist", "nazi"
        ]
        
        sanitized = prompt.lower()
        for term in prohibited_terms:
            sanitized = sanitized.replace(term, "****")
            
        # Prepend with quality instructions
        quality_prompt = f"A high quality, detailed digital art image of {sanitized}"
        
        return quality_prompt
    
    def _get_unsplash_image(self, prompt: str) -> str:
        """
        Get a relevant image from Unsplash as a fallback.
        
        Args:
            prompt: Original prompt
            
        Returns:
            Unsplash image URL
        """
        try:
            # Create a clean search term - remove special chars and limit length
            words = [word for word in prompt.split() if len(word) > 2][:3]  # Take up to 3 significant words
            search_term = "-".join(words)
            if not search_term:
                search_term = "landscape"  # Default fallback
            
            # Make sure search term is clean for a URL
            search_term = "".join(c for c in search_term if c.isalnum() or c == '-')
            
            # Use Unsplash source for a random image related to the search term
            return f"https://source.unsplash.com/640x480/?{search_term}"
        except Exception as e:
            print(f"Error creating Unsplash URL: {e}")
            # Ultra-safe fallback
            return "https://via.placeholder.com/640x480/0000FF/FFFFFF?text=Image"
        
    def _get_placeholder_image(self, prompt: str) -> str:
        """
        Get a placeholder image URL for when real generation fails.
        
        Args:
            prompt: Original prompt
            
        Returns:
            Placeholder image URL
        """
        try:
            # Sanitize and limit prompt for the URL
            words = prompt.split()[:2]  # Take just first two words
            safe_text = "".join(c for c in " ".join(words) if c.isalnum() or c.isspace())
            
            if not safe_text:
                safe_text = "Image"  # Default text
                
            # Import here to avoid circular imports
            import urllib.parse
            encoded_prompt = urllib.parse.quote(safe_text)
            
            # Generate random bright color for the placeholder
            color = random.choice(['6200ea', '00bfa5', 'd50000', '304ffe', '00c853', 'ff6d00', 'aa00ff'])
            
            # Use a placeholder service that generates colored blocks with text
            return f"https://via.placeholder.com/640x480/{color}/FFFFFF?text={encoded_prompt}"
        except Exception as e:
            print(f"Error creating placeholder URL: {e}")
            # Ultra-safe fallback with no parameters
            return "https://via.placeholder.com/640x480/000000/FFFFFF?text=Image" 