import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import spacy
import re
from typing import Dict, List, Tuple

# Load environment variables
load_dotenv()

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

# Get API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables. Please set OPENAI_API_KEY in your .env file.")

# Set up OpenAI client
client = OpenAI(api_key=api_key)

class RestaurantAssistant:
    def __init__(self):
        self.context = {
            "chat_history": [],
            "collected_info": {},
            "required_info": {
                'location': [],
                'cuisine_type': [],
                'diet_restrictions': [],
                'budget': [],
                'mood': []
            }
        }

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract restaurant-related entities using spaCy and custom patterns"""
        doc = nlp(text)
        entities = {
            'location': [],
            'cuisine_type': [],
            'diet_restrictions': [],
            'budget': [],
            'mood': []
        }

        # Extract location entities
        for ent in doc.ents:
            if ent.label_ in ['GPE', 'LOC']:
                entities['location'].append(ent.text)

        # Extract budget patterns like "$20" or "under 50"
        budget_pattern = r'\$?\d+(?:,\d{3})*(?:\.\d{2})?|\bunder\s+\$?\d+'
        budget_matches = re.finditer(budget_pattern, text.lower())
        for match in budget_matches:
            entities['budget'].append(match.group())

        # Extract cuisine types
        cuisine_types = ['italian', 'chinese', 'mexican', 'japanese', 'thai', 'indian', 
                        'mediterranean', 'french', 'korean', 'vietnamese', 'greek', 'american']
        entities['cuisine_type'] = [c for c in cuisine_types if c in text.lower()]

        # Extract dietary restrictions
        diet_terms = ['vegetarian', 'vegan', 'gluten-free', 'halal', 'kosher', 'pescatarian']
        entities['diet_restrictions'] = [d for d in diet_terms if d in text.lower()]

        # Extract mood terms (e.g., vibe, occasion)
        mood_terms = ['romantic', 'casual', 'fancy', 'family', 'date', 'party', 'quiet', 'trendy', 'cozy']
        entities['mood'] = [m for m in mood_terms if m in text.lower()]

        return entities

    def update_context(self, entities: Dict):
        """Update context with extracted restaurant information"""
        info = self.context['required_info']

        if entities['location'] and not info['location']:
            info['location'] = entities['location'][0]

        if entities['cuisine_type'] and not info['cuisine_type']:
            info['cuisine_type'] = entities['cuisine_type'][0]

        if entities['diet_restrictions']:
            info['diet_restrictions'].extend([d for d in entities['diet_restrictions'] if d not in info['diet_restrictions']])

        if entities['budget'] and not info['budget']:
            info['budget'] = entities['budget'][0]

        if entities['mood']:
            info['mood'].extend([m for m in entities['mood'] if m not in info['mood']])

    def generate_system_prompt(self) -> str:
        collected = self.context['required_info']
        missing = {k: v for k, v in collected.items() if not v}
        #has_interests = len(collected['interests']) > 0
        
        prompt = """You are an assistant helping suggest restaurants/eateries. Be conversational and natural, but ensure you gather
        all necessary information. Current status:
        
        Information collected: {collected_info}
        Missing information: {missing_info}
        
        Guidelines:
        1. Acknowledge any new information provided
        2. Ask for missing information naturally within the conversation
        3. Generate restaurant suggestions only when you have most of the essential information
        4. Be sure to ask questions one at a time so as to not overwhelm the user
        5. Keep the conversation engaging and natural while gathering information
        
        Your response should feel like a natural conversation while gently guiding the user to provide missing information.
        When providing the final plan, format it clearly with restaurant name, details, address, and cost."""

        return prompt.format(
            collected_info=json.dumps(collected),
            missing_info=json.dumps(missing)
        )

    def process_query(self, message: str, chat_history) -> tuple:
        try:
            if chat_history is None:
                chat_history = []

            # Extract and update information
            entities = self.extract_entities(message)
            self.update_context(entities)
            
            # Generate dynamic system prompt
            system_prompt = self.generate_system_prompt()

            # Get conversation history
            conversation_history = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add chat history
            for msg, response in chat_history:
                conversation_history.extend([
                    {"role": "user", "content": msg},
                    {"role": "assistant", "content": response}
                ])
            
            # Add current message
            conversation_history.append({"role": "user", "content": message})

            # Get response from GPT-4
            response = client.chat.completions.create(
                model="gpt-4",
                messages=conversation_history,
                temperature=0.7,
                max_tokens=1000
            )

            assistant_response = response.choices[0].message.content.strip()
            chat_history.append((message, assistant_response))
            return "", chat_history

        except Exception as e:
            print(f"Error processing query: {e}")
            return "", chat_history + [(message, f"I apologize, but I encountered an error: {str(e)}")]

def create_interface():
    assistant = RestaurantAssistant()
    
    with gr.Blocks(theme=gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="amber",
        font=gr.themes.GoogleFont("Raleway")),
        css="""#chat-container {
            background: #fafafa;
            border-radius: 12px;
            padding: 1.5em;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 1em;
        }

        .chatbox-modern {
            background-color: #fff;
            border-radius: 8px;
            border: 1px solid #eee;
        }

        .tips-box {
            background: #fdf6f0;
            padding: 1em;
            border-radius: 10px;
            border-left: 4px solid #f39c12;
            color: #333 !important;
            background-color: #fc8c03;
        }"""
    ) as interface:

        gr.Markdown(
            """
            <div style="text-align: center; padding: 1em;">
                <h1 style="font-size: 2.5em; margin-bottom: 0.2em;">🍴 Food Scout</h1>
                <h3 style="font-weight: 400; color: #666;">Smart, personalized restaurant ideas—right when you need them.</h3>
            </div>
            """,
            elem_classes="text-center"
        )

        with gr.Group(elem_classes="chat-section", elem_id="chat-container"):
            chatbot = gr.Chatbot(
                label=None,
                height=480,
                show_label=False,
                container=True,
                elem_classes="chatbox-modern"
            )

        with gr.Row(equal_height=True):
            msg = gr.Textbox(
                placeholder="Try something like: 'Find vegan brunch in Austin'...",
                show_label=False,
                lines=1,
                scale=8
            )
            submit = gr.Button("🍽️ Ask", variant="primary", scale=2)

        with gr.Row():
            clear = gr.Button("🧹 Clear Chat", variant="secondary", scale=1)
            example_questions = gr.Button("💡 Show Examples", variant="secondary", scale=1)

        gr.Markdown("---")

        with gr.Group():
            gr.Markdown("""
            ### ✨ Tips for Better Suggestions
            - Specify **your location** (e.g., New York, downtown, near campus)
            - Mention a **cuisine** (like Thai, Korean BBQ, Italian)
            - Add **diet preferences**: vegetarian, halal, gluten-free, etc.
            - Include a **budget** if you want: “under $20” or “fancy”
            - Mention your **vibe**: cozy, romantic, casual, trendy
            """, elem_classes="tips-box")

        def clear_history():
            assistant.context = {
                "chat_history": [],
                "collected_info": {},
                "required_info": {
                    "location": None,
                    "cuisine_type": None,
                    "diet_restrictions": None,
                    "budget": None,
                    "mood": None
                }
            }
            return None
            
        msg.submit(assistant.process_query, [msg, chatbot], [msg, chatbot])
        submit.click(assistant.process_query, [msg, chatbot], [msg, chatbot])
        clear.click(clear_history, None, chatbot)
        example_questions.click(lambda: "Best eateries in New York City", None, msg)

        return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_name="127.0.0.1", server_port=7860)