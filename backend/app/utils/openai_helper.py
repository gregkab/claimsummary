import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from ..exceptions import AIServiceError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openai_helper")

class BaseAgent:
    """Base class for AI agents with common OpenAI functionality."""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=api_key)
    
    def _call_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        model: str = "gpt-4",
        response_format: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Make an API call to OpenAI.
        
        Args:
            system_prompt: The system message defining the AI's role
            user_prompt: The user's message/query
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens in response
            model: The OpenAI model to use
            response_format: Optional format specification for response
        
        Returns:
            The AI's response text
        """
        try:
            # Log the prompt
            logger.info(f"OpenAI Prompt: {user_prompt}")
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Set up call parameters
            params = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            
            if max_tokens:
                params["max_tokens"] = max_tokens
                
            if response_format:
                params["response_format"] = response_format
            
            # Make the API call
            response = self.client.chat.completions.create(**params)
            
            # Log the response
            result = response.choices[0].message.content
            logger.info(f"OpenAI Response: {result}")
            
            return result
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise AIServiceError(f"OpenAI API error: {str(e)}")

class ClaimsAnalysisAgent(BaseAgent):
    """Agent specialized for analyzing claims emails and extracting action items."""
    
    SYSTEM_PROMPT = "You are a helpful assistant that analyzes emails to extract action items."
    
    def extract_action_items(self, email_content: str, claim_id: int) -> Dict:
        """
        Uses OpenAI to extract action items from an email.
        
        Args:
            email_content: The cleaned email content
            claim_id: The ID of the claim this email is associated with
            
        Returns:
            A dictionary containing summary and list of action items
        """
        try:
            prompt = f"""
            You are a claims assistant AI. Analyze the following email thread and:
            1. Provide a 3-sentence plain-language summary of the conversation.
            2. Extract all action items with clear descriptions, assignees (if mentioned), and deadlines or due dates.

            Email Thread:
            {email_content}
            
            Return your response as a JSON object with the following structure:
            {{
              "summary": "...",
              "action_items": [
                {{
                  "description": "...",
                  "assignee": "...",  // leave empty if not specified
                  "due_date": "YYYY-MM-DD",  // leave empty if not specified
                  "confidence": 0.95  // your confidence level in identifying this action item (0-1)
                }}
              ]
            }}
            """
            
            # Set up JSON response format
            response_format = {"type": "json_object"}
            
            # Get AI response
            result_text = self._call_openai(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.3,
                model="gpt-4",
                response_format=response_format
            )
            
            # Parse the response content as JSON
            result = json.loads(result_text)
            
            # Add claim_id to each action item
            for item in result.get("action_items", []):
                item["claim_id"] = claim_id
                
                # Convert due_date string to datetime if present
                if item.get("due_date"):
                    try:
                        item["due_date"] = datetime.strptime(item["due_date"], "%Y-%m-%d")
                    except ValueError:
                        item["due_date"] = None
            
            return result
            
        except AIServiceError as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            # Return fallback response
            return {
                "summary": f"Error processing email content: {str(e)}",
                "action_items": []
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "summary": f"Unexpected error processing email: {str(e)}",
                "action_items": []
            }

# Create an instance for easy import
claims_agent = ClaimsAnalysisAgent()