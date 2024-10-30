import asyncio
from openai import AsyncOpenAI
import gradio

async def custom_chatgpt(user_input):
    messages = [{"role": "user", "content": user_input}]
    
    client = AsyncOpenAI(api_key="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")
    
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