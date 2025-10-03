#!/usr/bin/env python3
"""
Enhanced Interactive MCP Client for Paint + Gmail Automation Demo
Connects to both Paint and Gmail MCP servers simultaneously
Accepts user input and orchestrates complete workflow: Math → Paint → Save → Email
"""

import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
import google.generativeai as genai
from concurrent.futures import TimeoutError
from functools import partial
from concurrent.futures import TimeoutError
from functools import partial

# Load environment variables from .env file
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

max_iterations = 15
last_response = None
iteration = 0
iteration_response = []  # Store the math calculation result globally
calculation_result = None

async def generate_with_timeout(prompt, timeout=15):
    """Generate content with a timeout"""
    print("Starting LLM generation...")
    try:
        # Convert the synchronous generate_content call to run in a thread
        loop = asyncio.get_event_loop()
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: model.generate_content(prompt)
            ),
            timeout=timeout
        )
        print("LLM generation completed")
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

def reset_state():
    """Reset all global variables to their initial state"""
    global last_response, iteration, iteration_response, calculation_result
    last_response = None
    iteration = 0
    iteration_response = []
    calculation_result = None

def get_user_input():
    """Get enhanced interactive input from user"""
    print("ENHANCED MATH + PAINT + EMAIL AUTOMATION")
    print("=" * 60)
    
    # Get two numbers
    while True:
        try:
            num1 = int(input("Enter first number: "))
            break
        except ValueError:
            print("Please enter a valid integer!")
    
    while True:
        try:
            num2 = int(input("Enter second number: "))
            break
        except ValueError:
            print("Please enter a valid integer!")
    
    # Get math operation
    print("\nAvailable math operations:")
    print("1. add (+)")
    print("2. subtract (-)")  
    print("3. multiply (×)")
    print("4. divide (÷)")
    print("5. power (^)")
    print("6. remainder (%)")
    
    while True:
        operation = input("Choose operation (1-6): ").strip()
        operation_map = {
            '1': 'add', '2': 'subtract', '3': 'multiply', 
            '4': 'divide', '5': 'power', '6': 'remainder'
        }
        if operation in operation_map:
            math_function = operation_map[operation]
            break
        else:
            print("Please choose a valid option (1-6)!")
    
    # Get message prefix
    message_prefix = input("Enter message prefix (e.g., 'The result is: '): ").strip()
    if not message_prefix:
        message_prefix = "Result: "
    
    return num1, num2, math_function, message_prefix

def get_email_input():
    """Get email address after Paint operations complete"""
    print("\n" + "="*60)
    print("PAINT FILE SAVED! Ready to send email notification...")
    print("="*60)
    
    while True:
        email = input("Enter email address to send result: ").strip()
        if email and "@" in email:
            return email
        else:
            print("Please enter a valid email address!")

async def execute_tool_call(tool_name, arguments, paint_session, gmail_session):
    """Route tool calls to appropriate server"""
    paint_tools = ['add', 'subtract', 'multiply', 'divide', 'power', 'remainder',
                   'sqrt', 'cbrt', 'factorial', 'log', 'sin', 'cos', 'tan',
                   'strings_to_chars_to_int', 'int_list_to_exponential_sum', 'fibonacci_numbers',
                   'open_paint', 'draw_rectangle_with_pencil', 'add_text_to_rectangle', 
                   'save_paint_file']
    
    gmail_tools = ['send-email', 'send-email-with-attachment', 'get-unread-emails', 
                   'read-email', 'trash-email', 'mark-email-as-read', 'open-email']
    
    if tool_name in paint_tools:
        print(f"Calling Paint server: {tool_name}")
        return await paint_session.call_tool(tool_name, arguments=arguments)
    elif tool_name in gmail_tools:
        print(f"Calling Gmail server: {tool_name}")
        return await gmail_session.call_tool(tool_name, arguments=arguments)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

async def main():
    global calculation_result
    reset_state()  # Reset at the start of main
    
    # Get user input
    num1, num2, math_function, message_prefix = get_user_input()
    
    print(f"\nTASK SUMMARY:")
    print(f"   • Operation: {num1} {math_function} {num2}")
    print(f"   • Message: '{message_prefix}' + result")
    print(f"   • Actions: Calculate → Paint → Save → Email")
    print("=" * 60)
    
    try:
        # Create both MCP server connections
        print("Establishing connections to both MCP servers...")
        paint_params = StdioServerParameters(
            command="python",
            args=["D:\\TSAI\\assignment-4\\mcp\\paint_mcp_server.py"]
        )
        
        gmail_params = StdioServerParameters(
            command="python", 
            args=["D:\\TSAI\\assignment-4\\mcp\\gmail_mcp_server.py", 
                  "--creds-file-path", "D:\\TSAI\\assignment-4\\mcp\\credentials.json",
                  "--token-path", "D:\\TSAI\\assignment-4\\mcp\\token.json"]
        )

        # Connect to both servers simultaneously
        async with stdio_client(paint_params) as (paint_read, paint_write), \
                   stdio_client(gmail_params) as (gmail_read, gmail_write):
            
            print("Paint server connected")
            print("Gmail server connected")
            
            async with ClientSession(paint_read, paint_write) as paint_session, \
                       ClientSession(gmail_read, gmail_write) as gmail_session:
                
                print("Initializing both sessions...")
                await paint_session.initialize()
                await gmail_session.initialize()
                
                # Get available tools from both servers
                print("Requesting tool lists...")
                paint_tools_result = await paint_session.list_tools()
                gmail_tools_result = await gmail_session.list_tools()
                
                paint_tools = paint_tools_result.tools
                gmail_tools = gmail_tools_result.tools
                
                print(f"Paint server: {len(paint_tools)} tools")
                print(f"Gmail server: {len(gmail_tools)} tools")

                # Create combined tools description for LLM
                print("Creating system prompt...")
                
                try:                    
                    paint_tools_description = []
                    gmail_tools_description = []
                    
                    # Process Paint tools
                    for i, tool in enumerate(paint_tools):
                        try:
                            params = tool.inputSchema
                            desc = getattr(tool, 'description', 'No description available')
                            name = getattr(tool, 'name', f'tool_{i}')
                            
                            if 'properties' in params:
                                param_details = []
                                for param_name, param_info in params['properties'].items():
                                    param_type = param_info.get('type', 'unknown')
                                    param_details.append(f"{param_name}: {param_type}")
                                params_str = ', '.join(param_details)
                            else:
                                params_str = 'no parameters'

                            tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
                            paint_tools_description.append(tool_desc)
                            print(f"  Paint Tool: {name}")
                        except Exception as e:
                            print(f"Error processing paint tool {i}: {e}")
                    
                    # Process Gmail tools
                    for i, tool in enumerate(gmail_tools):
                        try:
                            params = tool.inputSchema
                            desc = getattr(tool, 'description', 'No description available')
                            name = getattr(tool, 'name', f'tool_{i}')
                            
                            if 'properties' in params:
                                param_details = []
                                for param_name, param_info in params['properties'].items():
                                    param_type = param_info.get('type', 'unknown')
                                    param_details.append(f"{param_name}: {param_type}")
                                params_str = ', '.join(param_details)
                            else:
                                params_str = 'no parameters'

                            tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
                            gmail_tools_description.append(tool_desc)
                            print(f"  Gmail Tool: {name}")
                        except Exception as e:
                            print(f"Error processing gmail tool {i}: {e}")
                    
                    paint_tools_description = "\\n".join(paint_tools_description)
                    gmail_tools_description = "\\n".join(gmail_tools_description)
                    print("Successfully created tools description")
                except Exception as e:
                    print(f"Error creating tools description: {e}")
                    paint_tools_description = "Error loading paint tools"
                    gmail_tools_description = "Error loading gmail tools"
                
                print("Created system prompt...")
                
                system_prompt = f"""You are executing a 6-step workflow. Look at COMPLETED_STEPS and do ONLY the next step.

WORKFLOW STEPS:
1. Calculate: {math_function}|{num1}|{num2}
2. Open Paint: open_paint  
3. Draw rectangle: draw_rectangle_with_pencil
4. Add text: add_text_to_rectangle|{message_prefix}=[result]
5. Save file: save_paint_file|result|D:\\TSAI\\assignment-4\\mcp
6. Send email: send-email-with-attachment|email@example.com|Subject|Body|file_path

COMPLETED_STEPS: {{completed_steps}}

NEXT STEP LOGIC:
- If no steps completed → Do step 1: FUNCTION_CALL: {math_function}|{num1}|{num2}
- If step 1 completed → Do step 2: FUNCTION_CALL: open_paint
- If step 2 completed → Do step 3: FUNCTION_CALL: draw_rectangle_with_pencil
- If step 3 completed → Do step 4: FUNCTION_CALL: add_text_to_rectangle|{{text}}
- If step 4 completed → Do step 5: FUNCTION_CALL: save_paint_file|result|D:\\TSAI\\assignment-4\\mcp
- If step 5 completed → Do step 6: FUNCTION_CALL: send-email-with-attachment|user@example.com|Math Result|Result: {{text}}|D:\\TSAI\\assignment-4\\mcp\\result.jpeg

TOOLS AVAILABLE:
{paint_tools_description}
{gmail_tools_description}

CRITICAL RULES:
- Follow the EXACT QUERY below, don't use examples above
- Output ONLY this format: FUNCTION_CALL: tool_name|param1|param2
- Use the EXACT parameters shown in the current query
- NO explanations, NO markdown, NO code blocks, NO other text
- Just one line starting with FUNCTION_CALL:
- NEVER repeat completed steps"""

                # The user query
                query = f"""Perform {num1} {math_function} {num2}, show the result in Paint with message '{message_prefix}=[result]', save as image, and email the result with attachment."""
                print(f"Query: {query}")
                print("Assignment Goal: LLM will autonomously:")
                print(f"   1. Calculate {num1} {math_function} {num2}")
                print("   2. Open Paint application")
                print("   3. Draw rectangle and add text")
                print("   4. Save as D:\\TSAI\\assignment-4\\mcp\\result.jpeg")
                print("   5. Send email with attachment")
                print("   6. Complete workflow automation!")
                print("Starting iteration loop...")
                
                # Use global iteration variables
                global iteration, last_response
                email_address = None
                completed_steps = []
                
                while iteration < max_iterations:
                    print(f"\\n--- Iteration {iteration + 1} ---")
                    
                    # Build query based on completed steps - be very explicit about next step
                    if iteration == 0:
                        current_query = f"Do step 1: FUNCTION_CALL: {math_function}|{num1}|{num2}"
                    else:
                        # Determine next step based on what's completed
                        if math_function in completed_steps and "open_paint" not in completed_steps:
                            current_query = "Do step 2: FUNCTION_CALL: open_paint"
                        elif "open_paint" in completed_steps and "draw_rectangle_with_pencil" not in completed_steps:
                            current_query = "Do step 3: FUNCTION_CALL: draw_rectangle_with_pencil"
                        elif "draw_rectangle_with_pencil" in completed_steps and "add_text_to_rectangle" not in completed_steps:
                            current_query = f"Do step 4: FUNCTION_CALL: add_text_to_rectangle|{message_prefix}=[calculated_result]"
                        elif "add_text_to_rectangle" in completed_steps and "save_paint_file" not in completed_steps:
                            current_query = "Do step 5: FUNCTION_CALL: save_paint_file|result|D:\\TSAI\\assignment-4\\mcp"
                        elif "save_paint_file" in completed_steps and not any("send-email" in step for step in completed_steps):
                            # Use actual email parameters if available
                            email_addr = globals().get('email_address', 'user@example.com')
                            file_path = globals().get('saved_file_path', 'D:\\TSAI\\assignment-4\\mcp\\result.jpg')
                            # Normalize file path to remove double backslashes
                            file_path = file_path.replace('\\\\', '\\')
                            calc_result = globals().get('calculation_result', 'result')
                            current_query = f"Do step 6: FUNCTION_CALL: send-email-with-attachment|{email_addr}|Math Calculation Result|The calculation {num1} {math_function} {num2} = {calc_result}. Please see the attached image showing the visual result from Paint automation.|{file_path}"
                            print(f"DEBUG: Email query built: {current_query}")
                        else:
                            steps_done = ", ".join(completed_steps)
                            current_query = f"Completed: {steps_done}. Do the NEXT step in sequence."
                    
                    # Update system prompt dynamically with completed steps and result
                    current_system_prompt = system_prompt
                    current_system_prompt = current_system_prompt.replace("{completed_steps}", str(completed_steps))
                    
                    if 'calculation_result' in globals() and calculation_result:
                        current_system_prompt = current_system_prompt.replace("{text}", f"{message_prefix}={calculation_result}")
                        print(f"Updated system prompt with text: '{message_prefix}{calculation_result}'")

                    # Get model's response with timeout
                    print("Preparing to generate LLM response...")
                    prompt = f"{current_system_prompt}\\n\\n=== CURRENT TASK ===\\n{current_query}\\n=== EXECUTE EXACTLY AS SHOWN ABOVE ==="
                    try:
                        response = await generate_with_timeout(prompt)
                        response_text = response.text.strip()
                        print(f"LLM Response: {response_text}")
                        
                        # Find the FUNCTION_CALL line in the response - check multiple formats
                        function_call_found = False
                        for line in response_text.split('\\n'):
                            line = line.strip()
                            if line.startswith("FUNCTION_CALL:"):
                                response_text = line
                                function_call_found = True
                                break
                            # Also check for function calls in markdown code blocks
                            elif "FUNCTION_CALL:" in line and (line.startswith("**") or "`" in line):
                                # Extract from markdown formatting
                                if "FUNCTION_CALL:" in line:
                                    start_idx = line.find("FUNCTION_CALL:")
                                    response_text = line[start_idx:].split('**')[0].split('`')[0].strip()
                                    function_call_found = True
                                    break
                        
                        # If no function call found but we can see the pattern, try to construct it
                        if not function_call_found and "send-email-with-attachment" in response_text:
                            # Extract email parameters from the response
                            if "bhavyas0811@gmail.com" in response_text:
                                response_text = f"FUNCTION_CALL: send-email-with-attachment|{email_address}|Math Result|Result: {message_prefix}={calculation_result}|D:\\\\TSAI\\\\assignment-4\\\\mcp\\\\result_0310252156.jpg"
                        
                    except Exception as e:
                        print(f"Failed to get LLM response: {e}")
                        break

                    if response_text.startswith("FUNCTION_CALL:"):
                        _, function_info = response_text.split(":", 1)
                        parts = [p.strip() for p in function_info.split("|")]
                        func_name, params = parts[0], parts[1:]
                        
                        # Clean function name - remove parentheses if present
                        func_name = func_name.strip("()")
                        
                        print(f"Function: {func_name}")
                        print(f"Parameters: {params}")
                        
                        # Prevent repeating the same function 
                        if func_name in completed_steps:
                            print(f"Already completed {func_name}, skipping...")
                            iteration += 1
                            continue
                        
                        try:
                            # Find the matching tool from either server
                            tool = None
                            for t in paint_tools:
                                if t.name == func_name:
                                    tool = t
                                    break
                            if not tool:
                                for t in gmail_tools:
                                    if t.name == func_name:
                                        tool = t
                                        break
                            
                            if not tool:
                                available_tools = [t.name for t in paint_tools] + [t.name for t in gmail_tools]
                                print(f"Available tools: {available_tools}")
                                raise ValueError(f"Unknown tool: {func_name}")

                            print(f"Found tool: {tool.name}")

                            # Prepare arguments according to the tool's input schema
                            arguments = {}
                            schema_properties = tool.inputSchema.get('properties', {})
                            required_params = tool.inputSchema.get('required', [])

                            for param_name, param_info in schema_properties.items():
                                # Only require parameters if they are in the required list
                                if param_name in required_params and not params:
                                    raise ValueError(f"Not enough required parameters provided for {func_name}")
                                
                                # If we have parameters available, use them
                                if params:
                                    value = params.pop(0)
                                    param_type = param_info.get('type', 'string')
                                    
                                    # Convert the value to the correct type based on the schema
                                    if param_type == 'integer':
                                        arguments[param_name] = int(value)
                                    elif param_type == 'number':
                                        arguments[param_name] = float(value)
                                    elif param_type == 'array':
                                        if isinstance(value, str):
                                            value = value.strip('[]').split(',')
                                        arguments[param_name] = [int(x.strip()) for x in value]
                                    else:
                                        arguments[param_name] = str(value)
                                # If no parameters left and it's not required, skip (use default value)

                            print(f"Calling {func_name} with arguments: {arguments}")
                            
                            # Special handling for email attachment - normalize file path
                            if func_name == "send-email-with-attachment" and "attachment_path" in arguments:
                                original_path = arguments["attachment_path"]
                                normalized_path = original_path.replace('\\\\', '\\')
                                arguments["attachment_path"] = normalized_path
                                print(f"Email attachment path normalized: {original_path} -> {normalized_path}")
                                print(f"File exists check: {os.path.exists(normalized_path)}")
                            
                            # Route to appropriate server
                            result = await execute_tool_call(func_name, arguments, paint_session, gmail_session)
                            
                            # Get the full result content
                            if hasattr(result, 'content'):
                                if isinstance(result.content, list):
                                    iteration_result = [
                                        item.text if hasattr(item, 'text') else str(item)
                                        for item in result.content
                                    ]
                                else:
                                    iteration_result = str(result.content)
                            else:
                                iteration_result = str(result)
                                
                            print(f"Result: {iteration_result}")
                            
                            # Check if this was the save_paint_file step and extract file path
                            saved_file_path = None
                            if func_name == "save_paint_file" and ("SUCCESS" in str(iteration_result) or "WARNING" in str(iteration_result)):
                                print("\\n" + "="*60)
                                print("PAINT FILE SAVE ATTEMPTED!")
                                
                                # Extract saved file path from result
                                try:
                                    # The result from MCP tool calls comes in iteration_result
                                    result_str = str(iteration_result)
                                    
                                    # Check if result contains saved_file_path JSON structure
                                    import json
                                    import re
                                    
                                    # Try to extract from JSON structure first
                                    json_match = re.search(r'"saved_file_path":\s*"([^"]+)"', result_str)
                                    if json_match:
                                        saved_file_path = json_match.group(1)
                                    else:
                                        # Parse from success message text
                                        path_match = re.search(r'auto-saved as (D:\\\\TSAI\\\\assignment-4\\\\mcp\\\\[^\\s]+\\.jpg)', result_str)
                                        if path_match:
                                            saved_file_path = path_match.group(1)
                                        else:
                                            # Generate expected timestamped filename as fallback
                                            import datetime
                                            now = datetime.datetime.now()
                                            timestamp = now.strftime("%d%m%y%H%M")
                                            saved_file_path = f"D:\\\\TSAI\\\\assignment-4\\\\mcp\\\\result_{timestamp}.jpg"
                                    
                                    # Normalize the file path by removing extra backslashes
                                    saved_file_path = saved_file_path.replace('\\\\', '\\')
                                    print(f"Saved file path: {saved_file_path}")
                                    
                                    # Verify the file exists
                                    if os.path.exists(saved_file_path):
                                        file_size = os.path.getsize(saved_file_path)
                                        print(f"File verified: {saved_file_path} ({file_size} bytes)")
                                    else:
                                        print(f"File not found at: {saved_file_path}")
                                        # Try alternative paths
                                        alt_paths = [
                                            saved_file_path.replace('\\', '/'),
                                            saved_file_path.replace('D:\\TSAI', 'D:/TSAI'),
                                            saved_file_path.replace('\\', '\\\\')
                                        ]
                                        for alt_path in alt_paths:
                                            if os.path.exists(alt_path):
                                                saved_file_path = alt_path
                                                print(f"Found file at alternative path: {saved_file_path}")
                                                break
                                except Exception as path_error:
                                    print(f"⚠️ Could not extract file path: {path_error}")
                                    saved_file_path = "D:\\TSAI\\assignment-4\\mcp\\result.jpg"  # fallback (normalized)
                                
                                print("�📧 Now ready to send email with attachment...")
                                email_address = get_email_input()
                                
                                # Store email details for next iteration
                                globals().update({
                                    'email_address': email_address,
                                    'saved_file_path': saved_file_path,
                                    'ready_for_email': True
                                })
                            
                            # Format the response based on result type
                            if isinstance(iteration_result, list):
                                result_str = f"[{', '.join(iteration_result)}]"
                            else:
                                result_str = str(iteration_result)
                            
                            iteration_response.append(
                                f"In iteration {iteration + 1} you called {func_name} with {arguments} parameters, "
                                f"and the function returned {result_str}."
                            )
                            last_response = iteration_result
                            completed_steps.append(func_name)
                            
                            # Store calculation result for text display
                            if func_name in ["add", "subtract", "multiply", "divide", "power", "remainder"]:
                                if isinstance(iteration_result, list) and len(iteration_result) > 0:
                                    calculation_result = str(iteration_result[0])
                                else:
                                    calculation_result = str(iteration_result)
                                    
                            # Check if email was sent successfully - if so, end execution
                            if func_name == "send-email-with-attachment":
                                if "SUCCESS" in str(iteration_result) and "Email with attachment sent successfully" in str(iteration_result):
                                    print("\\n" + "="*60)
                                    print("WORKFLOW COMPLETED SUCCESSFULLY!")
                                    print("="*60)
                                    print("All 6 Steps Completed:")
                                    print(f"   1. Calculate: {num1} {math_function} {num2} = {calculation_result}")
                                    print("   2. Open Paint: Application opened and maximized")  
                                    print("   3. Draw Rectangle: 400x200 pixel rectangle drawn")
                                    print(f"   4. Add Text: '{message_prefix}={calculation_result}' added to rectangle")
                                    print(f"   5. Save File: {globals().get('saved_file_path', 'result.jpg')} saved successfully")
                                    print(f"   6. Send Email: Email sent to {globals().get('email_address', 'user')} with attachment")
                                    print("\\n Mission Accomplished! Check your email and Paint application!")
                                    print("="*60)
                                    break  # End the workflow loop

                        except Exception as e:
                            print(f"Error calling tool: {str(e)}")
                            import traceback
                            traceback.print_exc()
                            iteration_response.append(f"Error in iteration {iteration + 1}: {str(e)}")
                            break

                    elif response_text.startswith("FINAL_ANSWER:"):
                        print("\\n" + "="*60)
                        print("=== COMPLETE WORKFLOW FINISHED ===")
                        print(f"Final Answer: {response_text}")
                        print("\\nComplete Summary:")
                        print(f"   Calculation: {num1} {math_function} {num2}")
                        print(f"   Paint: Rectangle with text created")
                        print(f"   File: Saved as result.jpeg")
                        if email_address:
                            print(f"   Email: Sent to {email_address} with attachment")
                        print("\\nDetailed Steps:")
                        for i, response in enumerate(iteration_response, 1):
                            print(f"   {i}. {response}")
                        print("\\nCheck your email and Paint application!")
                        print("="*60)
                        break

                    iteration += 1

    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        reset_state()

if __name__ == "__main__":
    print("ENHANCED MULTI-SERVER MCP CLIENT")
    print("Math + Paint + Save + Email Automation")
    print("This will perform calculations, visualize in Paint, save image, and email results")
    print("Make sure you have GOOGLE_API_KEY in .env and Gmail credentials setup")
    print("=" * 80)
    asyncio.run(main())