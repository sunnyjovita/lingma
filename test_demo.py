import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
from io import StringIO

# Add the directory containing demo.py to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demo


class TestDemo(unittest.TestCase):

    @patch('demo.OpenAI')
    @patch('builtins.input', side_effect=['Hello', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_quit_command(self, mock_stdout, mock_input, mock_openai):
        """Test that the program exits correctly when user enters 'quit'"""
        
        # Mock the OpenAI client and its response
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        
        # Mock the chat completion response
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [MagicMock()]
        mock_chunk1.choices[0].delta.content = "Hi there!"
        mock_chunk1.choices[0].delta.reasoning_content = None
        
        mock_completion = MagicMock()
        mock_completion.__iter__.return_value = [mock_chunk1]
        mock_client_instance.chat.completions.create.return_value = mock_completion
        
        # Run the main function
        demo.main()
        
        # Check that the welcome message was printed
        output = mock_stdout.getvalue()
        self.assertIn("Welcome to the AI Chat Client!", output)
        self.assertIn("Type 'quit' or press Ctrl+C to exit.", output)
        
        # Check that the goodbye message was printed
        self.assertIn("Goodbye!", output)
        
        # Check that the OpenAI client was initialized with correct parameters
        mock_openai.assert_called_once()
        
        # Check that the chat completion was called
        mock_client_instance.chat.completions.create.assert_called_once()

    @patch('demo.OpenAI')
    @patch('builtins.input', side_effect=['Hello', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_exit_command(self, mock_stdout, mock_input, mock_openai):
        """Test that the program exits correctly when user enters 'exit'"""
        
        # Mock the OpenAI client and its response
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        
        # Mock the chat completion response
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [MagicMock()]
        mock_chunk1.choices[0].delta.content = "Hi there!"
        mock_chunk1.choices[0].delta.reasoning_content = None
        
        mock_completion = MagicMock()
        mock_completion.__iter__.return_value = [mock_chunk1]
        mock_client_instance.chat.completions.create.return_value = mock_completion
        
        # Run the main function
        demo.main()
        
        # Check that the goodbye message was printed
        output = mock_stdout.getvalue()
        self.assertIn("Goodbye!", output)

    @patch('demo.OpenAI')
    @patch('builtins.input', side_effect=['Hello', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_q_command(self, mock_stdout, mock_input, mock_openai):
        """Test that the program exits correctly when user enters 'q'"""
        
        # Mock the OpenAI client and its response
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        
        # Mock the chat completion response
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [MagicMock()]
        mock_chunk1.choices[0].delta.content = "Hi there!"
        mock_chunk1.choices[0].delta.reasoning_content = None
        
        mock_completion = MagicMock()
        mock_completion.__iter__.return_value = [mock_chunk1]
        mock_client_instance.chat.completions.create.return_value = mock_completion
        
        # Run the main function
        demo.main()
        
        # Check that the goodbye message was printed
        output = mock_stdout.getvalue()
        self.assertIn("Goodbye!", output)

    @patch('demo.OpenAI')
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_keyboard_interrupt(self, mock_stdout, mock_input, mock_openai):
        """Test that the program exits correctly on keyboard interrupt"""
        
        # Run the main function
        demo.main()
        
        # Check that the goodbye message was printed
        output = mock_stdout.getvalue()
        self.assertIn("Goodbye!", output)

    @patch('demo.OpenAI')
    @patch('builtins.input', side_effect=['Hello', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_conversation_flow(self, mock_stdout, mock_input, mock_openai):
        """Test the conversation flow and message handling"""
        
        # Mock the OpenAI client and its response
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        
        # Mock the chat completion response with multiple chunks
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [MagicMock()]
        mock_chunk1.choices[0].delta.content = "Hello! How can I help you today?"
        mock_chunk1.choices[0].delta.reasoning_content = None
        mock_chunk1.usage = None

        mock_completion = MagicMock()
        mock_completion.__iter__.return_value = [mock_chunk1]
        mock_client_instance.chat.completions.create.return_value = mock_completion
        
        # Run the main function
        demo.main()
        
        # Check that conversation round header was printed
        output = mock_stdout.getvalue()
        self.assertIn("Conversation Round 1", output)
        self.assertIn("Complete Response", output)
        
        # Check that the API was called with correct messages
        call_args = mock_client_instance.chat.completions.create.call_args
        messages = call_args[1]['messages']
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['role'], 'user')
        self.assertEqual(messages[0]['content'], 'Hello')

    @patch('demo.OpenAI')
    @patch('builtins.input', side_effect=['Hello', 'Another message', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_multiple_conversations(self, mock_stdout, mock_input, mock_openai):
        """Test multiple conversation rounds"""
        
        # Mock the OpenAI client and its responses
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        
        # Mock the chat completion responses
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [MagicMock()]
        mock_chunk1.choices[0].delta.content = "Hello response"
        mock_chunk1.choices[0].delta.reasoning_content = None
        
        mock_chunk2 = MagicMock()
        mock_chunk2.choices = [MagicMock()]
        mock_chunk2.choices[0].delta.content = "Another response"
        mock_chunk2.choices[0].delta.reasoning_content = None

        mock_completion = MagicMock()
        mock_completion.__iter__.return_value = [mock_chunk1]
        mock_completion2 = MagicMock()
        mock_completion2.__iter__.return_value = [mock_chunk2]
        
        # Make it return different responses for each call
        mock_client_instance.chat.completions.create.side_effect = [mock_completion, mock_completion2]
        
        # Run the main function
        demo.main()
        
        # Check that both conversation rounds happened
        output = mock_stdout.getvalue()
        self.assertIn("Conversation Round 1", output)
        self.assertIn("Conversation Round 2", output)

    @patch('demo.OpenAI')
    @patch('builtins.input', side_effect=['Hello', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_api_error_handling(self, mock_stdout, mock_input, mock_openai):
        """Test that API errors are handled gracefully"""
        
        # Mock the OpenAI client to raise an exception
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        mock_client_instance.chat.completions.create.side_effect = Exception("API Error")
        
        # Run the main function
        demo.main()
        
        # Check that the error message was printed
        output = mock_stdout.getvalue()
        self.assertIn("Error calling API: API Error", output)
        self.assertIn("Goodbye!", output)

    @patch('demo.OpenAI')
    @patch('builtins.input', side_effect=['Hello', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_reasoning_content_display(self, mock_stdout, mock_input, mock_openai):
        """Test that reasoning content is displayed correctly when present"""
        
        # Mock the OpenAI client and its response with reasoning content
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance
        
        # Mock the chat completion response with reasoning content
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [MagicMock()]
        mock_chunk1.choices[0].delta.content = None
        mock_chunk1.choices[0].delta.reasoning_content = "Let me think about this..."
        
        mock_chunk2 = MagicMock()
        mock_chunk2.choices = [MagicMock()]
        mock_chunk2.choices[0].delta.content = "This is my response"
        mock_chunk2.choices[0].delta.reasoning_content = None

        mock_completion = MagicMock()
        mock_completion.__iter__.return_value = [mock_chunk1, mock_chunk2]
        mock_client_instance.chat.completions.create.return_value = mock_completion
        
        # Run the main function
        demo.main()
        
        # Check that both thinking process and response were printed
        output = mock_stdout.getvalue()
        self.assertIn("Thinking Process", output)
        self.assertIn("Let me think about this...", output)
        self.assertIn("Complete Response", output)
        self.assertIn("This is my response", output)


if __name__ == '__main__':
    unittest.main()