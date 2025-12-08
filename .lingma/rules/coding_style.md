---
trigger: always_on
---

# Sunny’s Universal Coding Style Rules (for LLMs)

> When generating or translating code in **any programming language**, strictly follow these rules—even if they contradict the language’s common conventions.

---

## 1. Top-of-File Header

Always begin the script with a **brief, clear comment** (1–3 lines) explaining:
- What the script does  
- Who wrote it (optional)  
- Its purpose  

**Example (Python):**
```python
# Hello! This is Sunny's streaming AI chat client.
# It connects to a compatible OpenAI API endpoint and supports
# environment-based configuration and clear response formatting.

## 2. Explain Every Logical Block
Place a short, plain-English comment immediately before each non-trivial code block
(e.g., setup, input loop, API call, response handling).

## 3. Use Descriptive snake_case Identifiers
Use snake_case for variables, functions, and flags in all languages
(e.g., conversation_idx, is_answering, api_client).
Only use language-mandated syntax where required
(e.g., Java class names must be PascalCase).

## 4. Robust Error Handling
Wrap API calls, user input, and network I/O in try/catch (or equivalent) blocks that print friendly, non-technical error messages, such as:
"Error calling API: {e}"

## 5. Never Skip Comments
Always comment, even if the code seems “obvious”
Prioritize readability for newcomers over brevity or cleverness