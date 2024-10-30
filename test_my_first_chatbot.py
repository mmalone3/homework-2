import unittest
from unittest.mock import patch, MagicMock
from openai import AsyncOpenAI

class TestCustomChatGPT(unittest.TestCase):

    def setUp(self):
        # Reset the messages list before each test
        global messages
        messages = []

    @patch('openai.ChatCompletion.create')
    async def test_custom_chatgpt_success(self, mock_create):
        mock_response = MagicMock()
        mock_response.choices = [{'message': {'content': 'Test response'}}]
        mock_create.return_value = mock_response

        client = AsyncOpenAI(api_key='your_api_key_here')
        
        result = await client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': 'Test input'}],
            max_tokens=500
        )

        self.assertEqual(result.choices[0].message.content, 'Test response')
        mock_create.assert_called_once_with(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': 'Test input'}],
            max_tokens=500
        )

    @patch('openai.ChatCompletion.create')
    async def test_custom_chatgpt_exception(self, mock_create):
        mock_create.side_effect = Exception('API Error')

        client = AsyncOpenAI(api_key='your_api_key_here')
        
        result = await client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': 'Test input'}],
            max_tokens=500
        )

        self.assertEqual(result.choices[0].message.content, 'An error occurred: API Error')
        mock_create.assert_called_once_with(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': 'Test input'}],
            max_tokens=500
        )

    async def test_custom_chatgpt_empty_input(self):
        client = AsyncOpenAI(api_key='your_api_key_here')
        
        result = await client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': ''}],
            max_tokens=500
        )
        
        # Actual content depends on GPT's response
        self.assertIsNotNone(result.choices[0].message.content)

    @patch('openai.ChatCompletion.create')
    async def test_custom_chatgpt_multiple_calls(self, mock_create):
        mock_response_1 = MagicMock()
        mock_response_1.choices = [{'message': {'content': 'First response'}}]
        mock_response_2 = MagicMock()
        mock_response_2.choices = [{'message': {'content': 'Second response'}}]
        mock_create.side_effect = [mock_response_1, mock_response_2]

        client = AsyncOpenAI(api_key='your_api_key_here')
        
        result_1 = await client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': 'First input'}],
            max_tokens=500
        )
        result_2 = await client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': 'Second input'}],
            max_tokens=500
        )

        self.assertEqual(result_1.choices[0].message.content, 'First response')
        self.assertEqual(result_2.choices[0].message.content, 'Second response')
        self.assertEqual(len(messages), 4)  # Two user messages and two assistant messages

if __name__ == '__main__':
    unittest.main()