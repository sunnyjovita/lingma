import os
import sys
from openai import OpenAI


def main():
    # Initialize the OpenAI client
    client = OpenAI(
        # If you use a model in the China (Beijing) region, you must use an API key from the China (Beijing) region. You can obtain the API key from: https://bailian.console.alibabacloud.com/?tab=model#/api-key
        # If you have not configured the environment variable, replace the value with your Model Studio API key: api_key="sk-xxx"
        api_key=os.getenv("OPENAI_API_KEY", "sk-88f0ac7465964de58fe487e66d24ea05"),
        # If you use a model in the China (Beijing) region, you must replace the URL with: https://dashscope.aliyuncs.com/compatible-mode/v1
        base_url=os.getenv("OPENAI_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
    )
    
    messages = []
    conversation_idx = 1
    
    print("Welcome to the AI Chat Client!")
    print("Type 'quit' or press Ctrl+C to exit.\n")
    
    while True:
        try:
            # Get user input
            user_input = input("Enter your message (or 'quit' to exit): ")
            
            # Check if user wants to quit
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        
        # Add user message to conversation history
        user_msg = {"role": "user", "content": user_input}
        messages.append(user_msg)
        
        # Print conversation header
        print("="*20 + f"Conversation Round {conversation_idx}" + "="*20)
        conversation_idx += 1
        
        # Initialize variables for this response
        reasoning_content = ""  # Define the complete thinking process
        answer_content = ""     # Define the complete response
        is_answering = False   # Determine whether the thinking process is finished and the response has started
        
        try:
            # Create a chat completion request
            completion = client.chat.completions.create(
                # You can replace this with other deep thinking models as needed.
                model=os.getenv("OPENAI_MODEL", "qwen-plus"),
                messages=messages,
                # The enable_thinking parameter enables the thinking process. This parameter is invalid for the qwen3-30b-a3b-thinking-2507, qwen3-235b-a22b-thinking-2507, and QwQ models.
                extra_body={"enable_thinking": False},
                stream=True,
                # stream_options={
                #     "include_usage": True
                # }
            )
        except Exception as e:
            print(f"Error calling API: {e}")
            continue
        
        # Process streaming response
        for chunk in completion:
            # If chunk.choices is empty, print the usage.
            if not chunk.choices:
                print("\nUsage:")
                print(chunk.usage)
            else:
                delta = chunk.choices[0].delta
                # Print the thinking process
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                    if not is_answering:
                        print("=" * 20 + "Thinking Process" + "=" * 20)
                    print(delta.reasoning_content, end='', flush=True)
                    reasoning_content += delta.reasoning_content
                else:
                    # Start responding
                    if delta.content and not is_answering:
                        print("\n" + "=" * 20 + "Complete Response" + "=" * 20 + "\n")
                        is_answering = True
                    # Print the response process
                    if delta.content:
                        print(delta.content, end='', flush=True)
                        answer_content += delta.content
        
        # Add the content of the model's response to the context.
        messages.append({"role": "assistant", "content": answer_content})
        print("\n")


if __name__ == "__main__":
    main()