import os
import json
import google.generativeai as genai
from typing import List, Dict, Any

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        # Use gemini-1.0-pro which is available for free
        self.model = genai.GenerativeModel('gemini-1.0-pro')

    async def summarize_text(self, text: str, max_points: int = 3) -> List[str]:
        """
        Summarize text into key points using Google's Gemini Pro model.
        
        Args:
            text: The text to summarize
            max_points: Maximum number of key points to return
            
        Returns:
            List of summary points
        """
        prompt = f"""
        Please summarize the following text into {max_points} key points. Format your response
        as a JSON array of strings, with each string being a key point from the text.
        
        Text to summarize:
        {text}
        
        Response (JSON array only):
        """
        
        try:
            # Ensure text is not too long for the model
            if len(text) > 25000:  # Gemini 1.0 models have lower context limits than 1.5
                text = text[:25000] + "..."
                prompt = f"""
                Please summarize the following text into {max_points} key points. Format your response
                as a JSON array of strings, with each string being a key point from the text.
                
                Text to summarize (truncated due to length):
                {text}
                
                Response (JSON array only):
                """
            
            response = self.model.generate_content(prompt)
            
            # Extract the summary points from the response
            summary_text = response.text.strip()
            
            # Handle the response - could be JSON or plain text
            if summary_text.startswith("[") and summary_text.endswith("]"):
                try:
                    summary_points = json.loads(summary_text)
                    return summary_points
                except json.JSONDecodeError:
                    # Fall back to text processing if JSON parsing fails
                    pass
            
            # Process as plain text if JSON parsing failed
            lines = summary_text.split("\n")
            summary_points = [line.strip().lstrip("•-*").strip() for line in lines if line.strip()]
            
            return summary_points[:max_points]
            
        except Exception as e:
            print(f"Error in Gemini summarization: {str(e)}")
            # Return a fallback response
            return ["Unable to summarize the video. Please try a different video or try again later."]

    async def process_search_results(self, query: str, search_results: List[Dict[str, Any]]) -> List[str]:
        """
        Process search results using Gemini to extract key information.
        
        Args:
            query: The user's original query
            search_results: List of search result dictionaries
            
        Returns:
            List of processed information points
        """
        # Format the search results
        formatted_results = "\n\n".join([
            f"Title: {result.get('title', 'No title')}\n"
            f"Snippet: {result.get('snippet', 'No snippet')}"
            for result in search_results[:5]  # Limit to top 5 results
        ])
        
        prompt = f"""
        Based on the following search results for the query "{query}", provide a concise answer with 
        key information points. Format your response as a JSON array of strings.
        
        Search results:
        {formatted_results}
        
        Response (JSON array only):
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract the information points from the response
            result_text = response.text.strip()
            
            # Handle the response - could be JSON or plain text
            if result_text.startswith("[") and result_text.endswith("]"):
                try:
                    info_points = json.loads(result_text)
                    return info_points
                except json.JSONDecodeError:
                    # Fall back to text processing if JSON parsing fails
                    pass
            
            # Process as plain text if JSON parsing failed
            lines = result_text.split("\n")
            info_points = [line.strip().lstrip("•-*").strip() for line in lines if line.strip()]
            
            return info_points
            
        except Exception as e:
            print(f"Error in Gemini search processing: {str(e)}")
            return ["Unable to process the search results. Please try a different query or try again later."] 