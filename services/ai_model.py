import google.generativeai as genai

class AIModel:
    def __init__(self, api_key):
        # Configure the model using the API key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    def generate_content(self, prompt):
        try:
            # Call the model to generate content based on the prompt
            response = self.model.generate_content(prompt)
            # Return the generated text if available
            return response.parts[0].text if response.parts else ''
        except Exception as e:
            print(f"Error during content generation: {e}")
            return ''  # Return empty string in case of error
