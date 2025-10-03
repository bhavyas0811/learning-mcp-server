# AI Agent with Multi-Server MCP Automation System

This project demonstrates a sophisticated **AI Agent** that uses an **LLM (Gemini 2.0 Flash)** to autonomously orchestrate **TWO MCP servers** simultaneously. The LLM calls MCP tools to perform complete end-to-end automation: **Math Calculations → Paint Visualization → File Saving → Email with Attachments**.

## 🎯 Complete Agentic Workflow

```
User Input → AI Agent → LLM (Gemini) → MCP Tool Calls → Multi-Server Results
    ↓           ↓           ↓              ↓                   ↓
 15, 8, +,  AI Agent   Gemini 2.0      Paint + Gmail        Email with
"Result:"  Triggers   Flash LLM       MCP Servers          Attachment
            LLM       Tool Selection   Execute Functions     Delivered
```

## 🧠 AI Agent Architecture

The **AI Agent** orchestrates the workflow by:
- **Triggering** the LLM (Gemini 2.0 Flash) with workflow instructions
- **LLM** autonomously decides which MCP tools to call and when
- **Routes** LLM-generated function calls to appropriate MCP servers
- **Manages** real-time results and adapts workflow as needed
- **Completes** the entire 6-step workflow through LLM-driven automation

## 📁 Files

### Core Components
- **`client.py`** - AI Agent that calls Gemini 2.0 Flash LLM to orchestrate MCP servers
- **`paint_mcp_server.py`** - Paint automation MCP server (25 tools) with save functionality  
- **`gmail_mcp_server.py`** - Gmail communication MCP server (7 tools) with attachment support
- **`.env`** - Environment variables (Google API key for Gemini LLM)

### Key Features
- **🤖 AI Agent → LLM → MCP**: Clear separation of Agent, LLM, and MCP tool execution
- **🧠 LLM Decision Making**: Gemini 2.0 Flash autonomously selects and calls MCP tools
- **🔄 Iterative LLM Calls**: Max 15 LLM iterations with adaptive MCP tool selection
- **🎯 Goal-Oriented LLM**: LLM completes full workflow through strategic MCP calls
- **📁 Directory Control**: MCP tools save files to specific `D:\TSAI\assignment-4\mcp` directory
- **🔧 Real-time LLM Adaptation**: LLM handles MCP tool errors and adjusts strategy

### Required Setup Files (You Need to Provide)
- **`credentials.json`** - Gmail OAuth 2.0 credentials
- **`token.json`** - Will be created after first Gmail authentication

## 🚀 Features

### Enhanced User Input
- **Two Numbers**: Any integers for calculation
- **Math Operation**: Choose from 6 operations (add, subtract, multiply, divide, power, remainder)
- **Message Prefix**: Custom text prefix for the result
- **Email Address**: Recipient for the final notification

### Paint Server Tools (25 tools)
- **Math Functions**: `add`, `subtract`, `multiply`, `divide`, `power`, `remainder`, `sqrt`, `cbrt`, `factorial`, `log`, `sin`, `cos`, `tan`
- **String Utils**: `strings_to_chars_to_int`, `fibonacci_numbers`, `int_list_to_exponential_sum`
- **Paint Automation**:
  - `open_paint()` - Opens Paint with multi-method foreground handling
  - `draw_rectangle_with_pencil()` - Draws 400x200px rectangle using pencil tool
  - `add_text_to_rectangle(text)` - Adds calculated result text inside rectangle
  - `save_paint_file(filename, file_path)` - **Enhanced: Saves to specified directory with timestamp**

### Gmail Server Tools (7 tools)
- **Email Functions**:
  - `send-email(recipient, subject, message)` - Basic email sending
  - `send-email-with-attachment(recipient, subject, message, attachment_path)` - **Enhanced: MIME multipart with file attachment**
  - `get-unread-emails()`, `read-email()`, `trash-email()`, `mark-email-as-read()`, `open-email()`

### AI Agent → LLM → MCP Multi-Server Architecture
- **AI Agent Orchestration**: Agent triggers LLM with workflow goals and tool descriptions
- **LLM Tool Selection**: Gemini 2.0 Flash autonomously decides which MCP tools to call
- **Concurrent MCP Connections**: Both MCP servers connected and managed simultaneously  
- **Intelligent MCP Routing**: System routes LLM-selected tools across 32 functions in 2 MCP servers
- **LLM Error Handling**: LLM analyzes MCP tool failures and selects retry strategies
- **Stateful LLM Context**: LLM maintains calculation results and file paths across iterations
- **Dynamic LLM Planning**: LLM adapts MCP tool calls based on real-time results

## 🛠️ Setup Instructions

### 1. Environment Setup
```bash
# Install required packages (already in pyproject.toml)
pip install mcp fastmcp google-generativeai pywinauto pywin32 python-dotenv google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Required Configuration Files

You need to create/populate these **3 essential files** before running:

#### 📄 `.env` File (Google Gemini API Key)
Create `.env` file in the `mcp` folder with your Google AI Studio API key:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

**To get your Google Gemini API Key:**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" → "Create API Key"
4. Copy the generated key and paste it in `.env` file

#### 📄 `credentials.json` (Gmail OAuth Credentials)
Create Gmail API credentials for email functionality:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. **Enable Gmail API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"
4. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop application"
   - Name it (e.g., "MCP Gmail Client")
   - Download the JSON file
5. **Save as `credentials.json`** in the `mcp` folder

**Required Gmail Scopes**: `https://www.googleapis.com/auth/gmail.modify`

#### 📄 `token.json` (Auto-Generated)
This file will be **automatically created** during first run:
- When you first run the system, it will open a browser
- Sign in with your Google account
- Grant permissions to access Gmail
- `token.json` will be saved automatically
- Subsequent runs will use this token (no browser needed)

## 🎮 How to Run

### Prerequisites Check
Before running, ensure you have all required files:

- [ ] **`.env`** - Google Gemini API key (create this file)
- [ ] **`credentials.json`** - Gmail OAuth credentials (download from Google Cloud Console)
- [ ] **`token.json`** - Will be auto-generated on first run
- [ ] **Paint application** - Available on Windows
- [ ] **Internet connection** - For Gemini LLM and Gmail API

### Running the System
```bash
cd D:\TSAI\assignment-4\mcp
python client.py
```

**First Run Setup:**
1. System will open browser for Gmail authentication
2. Sign in and grant permissions
3. `token.json` will be created automatically
4. System will start the AI Agent workflow

### Example Session
```
🚀 ENHANCED MULTI-SERVER MCP CLIENT
📊 Math + 🎨 Paint + 💾 Save + 📧 Email Automation

ENHANCED MATH + PAINT + EMAIL AUTOMATION
============================================================
Enter first number: 25
Enter second number: 8
Available math operations:
1. add (+)
2. subtract (-)
3. multiply (×)
4. divide (÷)
5. power (^)
6. remainder (%)
Choose operation (1-6): 1
Enter message prefix (e.g., 'The result is: '): The sum is: 

🎯 TASK SUMMARY:
   • Operation: 25 add 8
   • Message: 'The sum is: ' + result
   • Actions: Calculate → Paint → Save → Email
============================================================
```

## 📊 Complete Automation Flow

### Phase 1: Dual Server Connection
```
🔌 Establishing connections to both MCP servers...
🎨 Paint server connected
📧 Gmail server connected
🔧 Initializing both sessions...
📋 Requesting tool lists...
🎨 Paint server: 25 tools
📧 Gmail server: 7 tools
```

### Phase 2: Calculation & Visualization
```
🔄 --- Iteration 1 ---
🧠 LLM Response: FUNCTION_CALL: add|25|8
🎨 Calling Paint server: add
📋 Result: 33

🔄 --- Iteration 2 ---
🧠 LLM Response: FUNCTION_CALL: open_paint
🎨 Paint opens and comes to foreground

🔄 --- Iteration 3 ---
🧠 LLM Response: FUNCTION_CALL: draw_rectangle_with_pencil
🎨 Rectangle drawn with pencil tool

🔄 --- Iteration 4 ---
🧠 LLM Response: FUNCTION_CALL: add_text_to_rectangle|The sum is: 33
🎨 Text added to rectangle center
```

### Phase 3: File Save & Email Preparation
```
🔄 --- Iteration 5 ---
🧠 LLM Response: FUNCTION_CALL: save_paint_file|D:\TSAI\assignment-4\demo2\result.jpeg
🎨 Paint file saved successfully

============================================================
🎨 PAINT FILE SAVED SUCCESSFULLY!
📧 Now ready to send email with attachment...
============================================================
Enter email address to send result: user@example.com
```

### Phase 4: Email with Attachment
```
🔄 --- Iteration 6 ---
🧠 LLM Response: FUNCTION_CALL: send-email-with-attachment|user@example.com|Math Calculation Result|The calculation 25 add 8 = 33. Please see the attached image.|D:\TSAI\assignment-4\demo2\result.jpeg
📧 Calling Gmail server: send-email-with-attachment
📧 Email with attachment sent successfully

🎉 === COMPLETE WORKFLOW FINISHED ===
```

## 📋 Expected Outputs

### 1. Console Logs
- Detailed step-by-step execution logs
- Server connection status
- Tool call routing information
- Success/error messages for each operation

### 2. Paint Application
- Opens automatically and stays in foreground
- Rectangle drawn with pencil tool
- Text displayed: "The sum is: 33" (example)
- File saved as `result.jpeg`

### 3. Saved File
- **Location**: `D:\TSAI\assignment-4\demo2\result.jpeg`
- **Content**: Screenshot of Paint canvas with rectangle and text
- **Format**: JPEG image file

### 4. Email Sent
- **Recipient**: User-provided email address
- **Subject**: "Math Calculation Result"
- **Body**: "The calculation 25 add 8 = 33. Please see the attached image."
- **Attachment**: `result.jpeg` file

## 🏗️ Architecture

### AI Agent → LLM → MCP Architecture
```
                    AI Agent (client.py)
                         |
                   Gemini 2.0 Flash LLM
                         |
                    +----|----+
                    |         |
            Paint MCP Server   Gmail MCP Server
                |              |
         [25 Math & Paint]  [7 Email Tools]
         [Tools & Save]    [Attachment Support]
```

### LLM → MCP Tool Routing Logic
```python
# AI Agent provides tool descriptions to LLM
paint_tools = ['add', 'multiply', 'open_paint', 'save_paint_file', ...]
gmail_tools = ['send-email', 'send-email-with-attachment', ...]

# LLM decides which tool to call, AI Agent routes to MCP server
if llm_selected_tool in paint_tools:
    result = await paint_session.call_tool(llm_selected_tool, llm_arguments)
elif llm_selected_tool in gmail_tools:
    result = await gmail_session.call_tool(llm_selected_tool, llm_arguments)
```

### LLM-Driven Workflow State Management
- **LLM Iteration Tracking**: LLM maintains context across MCP tool calls
- **AI Agent State**: Tracks completed MCP operations and results between LLM calls
- **Email Input Pause**: AI Agent pauses LLM workflow for user email input
- **MCP Result Verification**: LLM analyzes MCP tool results before next step
- **LLM Error Recovery**: LLM decides recovery strategy when MCP tools fail

## 🎯 Key Enhancements

### vs Original Demo
- ✅ **Dual Server Architecture**: Paint + Gmail simultaneously
- ✅ **File Save Capability**: Paint canvas → JPEG file
- ✅ **Email Attachments**: Send images via email
- ✅ **Enhanced Math Options**: 6 different operations
- ✅ **Interactive Email Input**: User provides recipient
- ✅ **Complete Workflow**: End-to-end automation
- ✅ **Better Error Handling**: Multi-server error management
- ✅ **State Persistence**: Workflow continues across servers

### Technical Improvements
- **Concurrent Server Connections**: Both servers active simultaneously
- **Tool Auto-Routing**: Intelligent function call distribution
- **Enhanced Paint Save**: Robust file saving with verification
- **Gmail Attachment Support**: Full MIME multipart email handling
- **Workflow Interruption**: Seamless user input integration
- **Comprehensive Logging**: Detailed operation tracking

## ⚠️ Setup Requirements Summary

**You must create these files before running:**

### 🔑 Required Files:
1. **`.env`** - Google Gemini API key from [AI Studio](https://aistudio.google.com/)
2. **`credentials.json`** - Gmail OAuth credentials from [Google Cloud Console](https://console.cloud.google.com/)
3. **`token.json`** - Auto-generated on first run (browser authentication)

### 📝 Quick Setup Checklist:
- [ ] Create `.env` with `GOOGLE_API_KEY=your_key_here`
- [ ] Download `credentials.json` from Google Cloud Console
- [ ] Enable Gmail API in Google Cloud Console
- [ ] Run `python client.py` for first-time authentication
- [ ] Grant Gmail permissions in browser popup
- [ ] System ready for AI Agent automation!

**After setup, the AI Agent will autonomously orchestrate the entire workflow using LLM-driven MCP tool calls!**

This enhanced demo demonstrates a complete business workflow: **User Input → Calculation → Visualization → Documentation → Communication** - all automated through intelligent LLM orchestration of multiple specialized MCP servers.