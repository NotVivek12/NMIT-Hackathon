import os
import groq
from typing import List, Dict, Any

class GroqService:
    def __init__(self):
        self.client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-70b-8192"  # Using Llama 3 70B model for best quality

    async def summarize_text(self, text: str, max_points: int = 3) -> List[str]:
        """
        Summarize text into key points using Groq's LLM.
        
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text into key points. You respond in JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            # Extract the summary points from the response
            summary_text = response.choices[0].message.content.strip()
            
            # Handle the response - could be JSON or plain text
            if summary_text.startswith("[") and summary_text.endswith("]"):
                import json
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
            print(f"Error in Groq summarization: {str(e)}")
            return [f"Failed to generate summary: {str(e)}"]

    async def process_search_results(self, query: str, search_results: List[Dict[str, Any]]) -> List[str]:
        """
        Process search results using Groq's LLM to extract key information.
        
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides concise information based on search results. You respond in JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            # Extract the information points from the response
            result_text = response.choices[0].message.content.strip()
            
            # Handle the response - could be JSON or plain text
            if result_text.startswith("[") and result_text.endswith("]"):
                import json
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
            print(f"Error in Groq search processing: {str(e)}")
            return [f"Failed to process search results: {str(e)}"] 