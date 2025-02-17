import openai
import os
from typing import Dict, List
import json

class PaperReviewer:
    def __init__(self):
        # Initialize OpenAI client
        self.api_key = os.getenv('SAMBANOVA_API_KEY')
        print(self.api_key)
        if not self.api_key:
            raise ValueError("Please set OPENAI_API_KEY environment variable")
        
        self.client = openai.OpenAI(api_key=self.api_key, base_url="https://api.sambanova.ai/v1")
        
        # Define the system prompt for paper review
        self.system_prompt = """
        You are an expert academic paper reviewer. Your task is to:
        1. Analyze the paper's content critically
        2. Identify strengths and weaknesses
        3. Provide constructive feedback
        4. Check for clarity and coherence
        5. Evaluate methodology and results
        Please be thorough but constructive in your feedback.
        """

    def review_paper(self, paper_text: str) -> Dict:
        """
        Review the given paper text using OpenAI's API.
        
        Args:
            paper_text (str): The text content of the paper to review
            
        Returns:
            Dict: Review results containing feedback and suggestions
        """
        try:
            response = self.client.chat.completions.create(
                model="Meta-Llama-3.1-405B-Instruct",  # You can adjust the model as needed
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Please review this academic paper: \n\n{paper_text}"}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return {
                "review": response.choices[0].message.content,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_specific_feedback(self, paper_text: str, aspect: str) -> Dict:
        """
        Get feedback on a specific aspect of the paper.
        
        Args:
            paper_text (str): The text content of the paper
            aspect (str): Specific aspect to review (e.g., 'methodology', 'writing', 'structure')
            
        Returns:
            Dict: Specific feedback on the requested aspect
        """
        try:
            prompt = f"Please review specifically the {aspect} of this paper: \n\n{paper_text}"
            
            response = self.client.chat.completions.create(
                model="Meta-Llama-3.1-405B-Instruct",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return {
                "feedback": response.choices[0].message.content,
                "aspect": aspect,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

# Example usage
if __name__ == "__main__":
    reviewer = PaperReviewer()
    
    # Example paper text (you would replace this with actual paper content)
    sample_paper = """
    Hello world
    """
    
    # Get general review
    review_result = reviewer.review_paper(sample_paper)
    print("General Review:", json.dumps(review_result, indent=2))
    
    # Get specific feedback on methodology
    methodology_feedback = reviewer.get_specific_feedback(sample_paper, "methodology")
    print("Methodology Feedback:", json.dumps(methodology_feedback, indent=2)) 