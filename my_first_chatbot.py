import asyncio
from openai import AsyncOpenAI
import gradio

async def custom_chatgpt(user_input):
    messages = [{"role": "user", "content": user_input}]
    
    
    # Read the API key from a file
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()
    
    client = AsyncOpenAI(api_key=api_key)
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )
    
    chatgpt_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": chatgpt_response})
    
    return chatgpt_response

bot_title = input("Enter the title of the bot: ")
bot_type = input("Enter the type of the bot: ")

demo = gradio.Interface(
    fn=custom_chatgpt,
    inputs=gradio.Textbox(lines=2, label="Input Text"),
    outputs="text",
    title=f"{bot_title} ({bot_type})",
    description="My First Chatbot - Chat with an AI-powered bot"
)

if __name__ == "__main__":
    demo.launch()
