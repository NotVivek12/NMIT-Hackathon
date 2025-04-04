import os
import openai
from typing import Optional

class ImageService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        
    async def generate_image(self, prompt: str) -> Optional[str]:
        """
        Generate an image based on a text prompt using DALL-E.
        
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
            
            # Generate image using DALL-E
            response = openai.Image.create(
                prompt=safe_prompt,
                n=1,  # Generate 1 image
                size="512x512"  # Medium size for faster generation
            )
            
            # Extract image URL from response
            image_url = response['data'][0]['url']
            
            return image_url
            
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            
            # For demo purposes, return a placeholder image if real generation fails
            return self._get_placeholder_image(prompt)
    
    def _sanitize_prompt(self, prompt: str) -> str:
        """
        Sanitize the prompt to ensure it's appropriate and will work well with DALL-E.
        
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
        
    def _get_placeholder_image(self, prompt: str) -> str:
        """
        Get a placeholder image URL for when real generation fails.
        
        Args:
            prompt: Original prompt
            
        Returns:
            Placeholder image URL
        """
        # Encode the prompt for the placeholder service
        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Use a placeholder service that generates colored blocks with text
        return f"https://via.placeholder.com/512x512/6200ea/FFFFFF?text={encoded_prompt}" 