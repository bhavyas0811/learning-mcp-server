# Enhanced Paint Automation MCP Server with Save Function
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import math
import sys
import os
from pywinauto.application import Application
import win32gui
import win32con
import win32api
import pyautogui
import keyboard
import time

# instantiate MCP server
mcp = FastMCP("PaintAutomationServer")

# Global application handle for Paint
paint_app = None

# MATH TOOLS
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"CALLED: add({a}, {b})")
    result = int(a + b)
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print(f"CALLED: subtract({a}, {b})")
    result = int(a - b)
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print(f"CALLED: multiply({a}, {b})")
    result = int(a * b)
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print(f"CALLED: divide({a}, {b})")
    result = float(a / b)
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print(f"CALLED: power({a}, {b})")
    result = int(a ** b)
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def remainder(a: int, b: int) -> int:
    """Remainder of two numbers division"""
    print(f"CALLED: remainder({a}, {b})")
    result = int(a % b)
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print(f"CALLED: sqrt({a})")
    result = float(a ** 0.5)
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print(f"CALLED: cbrt({a})")
    result = float(a ** (1/3))
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def factorial(a: int) -> int:
    """Factorial of a number"""
    print(f"CALLED: factorial({a})")
    result = int(math.factorial(a))
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def log(a: int) -> float:
    """Natural logarithm of a number"""
    print(f"CALLED: log({a})")
    result = float(math.log(a))
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def sin(a: int) -> float:
    """Sine of a number"""
    print(f"CALLED: sin({a})")
    result = float(math.sin(a))
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def cos(a: int) -> float:
    """Cosine of a number"""
    print(f"CALLED: cos({a})")
    result = float(math.cos(a))
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def tan(a: int) -> float:
    """Tangent of a number"""
    print(f"CALLED: tan({a})")
    result = float(math.tan(a))
    print(f"RESULT: {result}")
    return result

# STRING UTILITY TOOLS
@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print(f"CALLED: strings_to_chars_to_int('{string}')")
    result = [int(ord(char)) for char in string]
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print(f"CALLED: int_list_to_exponential_sum({int_list})")
    result = sum(math.exp(i) for i in int_list)
    print(f"RESULT: {result}")
    return result

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

# PAINT AUTOMATION TOOLS
@mcp.tool()
async def open_paint() -> dict:
    """Open Microsoft Paint and maximize it, bringing it to foreground"""
    global paint_app
    try:
        print("OPENING PAINT...")
        
        # Start Paint application
        paint_app = Application().start('mspaint.exe')
        print("Paint process started")
        
        # Wait for Paint to fully load
        time.sleep(3.0)
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        print(f"Paint window found: {paint_window.window_text()}")
        
        # Maximize the window
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        print("Paint window maximized")
        
        # Wait for maximize to complete
        time.sleep(1.0)
        
        # Bring Paint to foreground with multiple methods for reliability
        print("Bringing Paint to foreground...")
        
        # Method 1: Standard set_focus
        paint_window.set_focus()
        
        # Method 2: Force foreground window
        win32gui.SetForegroundWindow(paint_window.handle)
        
        # Method 3: Restore and show window on top
        win32gui.ShowWindow(paint_window.handle, win32con.SW_RESTORE)
        win32gui.ShowWindow(paint_window.handle, win32con.SW_SHOW)
        win32gui.BringWindowToTop(paint_window.handle)
        
        # Method 4: Set window to topmost temporarily, then remove topmost
        win32gui.SetWindowPos(paint_window.handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        time.sleep(0.5)
        win32gui.SetWindowPos(paint_window.handle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, 
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        
        # Final maximize to ensure it's properly displayed
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        
        # Additional focus and activation
        win32gui.SetActiveWindow(paint_window.handle)
        time.sleep(0.5)
        
        print("Paint should now be in foreground and visible")
        
        # Get final window size
        final_rect = paint_window.rectangle()
        print(f"Final Paint window: {final_rect.width()}x{final_rect.height()}")
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"SUCCESS: Paint opened, maximized, and brought to foreground. Window size: {final_rect.width()}x{final_rect.height()} at position ({final_rect.left},{final_rect.top})"
                )
            ]
        }
    except Exception as e:
        print(f"Error opening Paint: {e}")
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"ERROR opening Paint: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def draw_rectangle_with_pencil() -> dict:
    """Draw a rectangle using the pencil tool"""
    global paint_app
    try:
        if not paint_app:
            return {"content": [TextContent(type="text", text="ERROR: Paint not open. Call open_paint first.")]}
        
        print("DRAWING RECTANGLE WITH PENCIL...")
        
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint stays in foreground
        print("Ensuring Paint is in foreground for drawing...")
        paint_window.set_focus()
        win32gui.SetForegroundWindow(paint_window.handle)
        win32gui.BringWindowToTop(paint_window.handle)
        time.sleep(0.5)
        
        from pywinauto import mouse, keyboard
        
        # Close any dialogs
        keyboard.send_keys('{ESC}')
        time.sleep(0.2)
        
        # Get window dimensions
        window_rect = paint_window.rectangle()
        
        # Calculate safe canvas area
        safe_canvas_left = window_rect.left + 300
        safe_canvas_top = window_rect.top + 300
        safe_canvas_right = window_rect.right - 300
        safe_canvas_bottom = window_rect.bottom - 200
        
        # Calculate center
        canvas_center_x = (safe_canvas_left + safe_canvas_right) // 2
        canvas_center_y = (safe_canvas_top + safe_canvas_bottom) // 2
        
        # Select pencil tool
        keyboard.send_keys('%h')  # Alt+H for Home tab
        time.sleep(0.3)
        keyboard.send_keys('p')   # P for Pencil tool
        time.sleep(0.3)
        print("Pencil tool selected")
        
        # Define rectangle coordinates
        rect_width = 400
        rect_height = 200
        rect_left = canvas_center_x - (rect_width // 2)
        rect_top = canvas_center_y - (rect_height // 2)
        rect_right = rect_left + rect_width
        rect_bottom = rect_top + rect_height
        
        print(f"Drawing rectangle: ({rect_left},{rect_top}) to ({rect_right},{rect_bottom})")
        
        # Draw rectangle outline with pencil
        # TOP LINE
        mouse.press(coords=(rect_left, rect_top))
        for x in range(rect_left, rect_right + 1, 10):
            mouse.move(coords=(x, rect_top))
            time.sleep(0.001)
        mouse.release(coords=(rect_right, rect_top))
        time.sleep(0.2)
        
        # RIGHT LINE
        mouse.press(coords=(rect_right, rect_top))
        for y in range(rect_top, rect_bottom + 1, 10):
            mouse.move(coords=(rect_right, y))
            time.sleep(0.001)
        mouse.release(coords=(rect_right, rect_bottom))
        time.sleep(0.2)
        
        # BOTTOM LINE
        mouse.press(coords=(rect_right, rect_bottom))
        for x in range(rect_right, rect_left - 1, -10):
            mouse.move(coords=(x, rect_bottom))
            time.sleep(0.001)
        mouse.release(coords=(rect_left, rect_bottom))
        time.sleep(0.2)
        
        # LEFT LINE
        mouse.press(coords=(rect_left, rect_bottom))
        for y in range(rect_bottom, rect_top - 1, -10):
            mouse.move(coords=(rect_left, y))
            time.sleep(0.001)
        mouse.release(coords=(rect_left, rect_top))
        
        print("Rectangle drawn with pencil tool")
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"SUCCESS: Rectangle drawn with pencil tool. Size: {rect_width}x{rect_height} pixels at coordinates ({rect_left},{rect_top}) to ({rect_right},{rect_bottom})"
                )
            ]
        }
        
    except Exception as e:
        print(f"Error drawing rectangle: {e}")
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"ERROR drawing rectangle with pencil: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def add_text_to_rectangle(text: str) -> dict:
    """Add text inside the rectangle that was just drawn"""
    global paint_app
    try:
        if not paint_app:
            return {"content": [TextContent(type="text", text="ERROR: Paint not open. Call open_paint first.")]}
        
        print(f"ADDING TEXT: '{text}'")
        
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint stays in foreground for text input
        print("Ensuring Paint is in foreground for text input...")
        paint_window.set_focus()
        win32gui.SetForegroundWindow(paint_window.handle)
        win32gui.BringWindowToTop(paint_window.handle)
        time.sleep(1.0)
        
        from pywinauto import mouse, keyboard
        
        # Select text tool
        keyboard.send_keys('%h')  # Alt+H for Home tab
        time.sleep(1.0)
        keyboard.send_keys('t')   # T for Text tool
        time.sleep(1.5)
        print("Text tool selected")
        
        # Calculate text position (center of rectangle from previous function)
        window_rect = paint_window.rectangle()
        safe_canvas_left = window_rect.left + 300
        safe_canvas_top = window_rect.top + 300
        safe_canvas_right = window_rect.right - 300
        safe_canvas_bottom = window_rect.bottom - 200
        
        canvas_center_x = (safe_canvas_left + safe_canvas_right) // 2
        canvas_center_y = (safe_canvas_top + safe_canvas_bottom) // 2
        
        # Text position (center of rectangle)
        text_center_x = canvas_center_x - 50
        text_center_y = canvas_center_y - 10
        
        print(f"Text position: ({text_center_x}, {text_center_y})")
        
        # Click in center of rectangle
        mouse.click(coords=(text_center_x, text_center_y))
        time.sleep(1.5)
        
        # Set center alignment
        keyboard.send_keys('^e')  # Ctrl+E for center alignment
        time.sleep(0.5)
        
        # Type the text
        keyboard.send_keys(text)
        time.sleep(1.0)
        print(f"Text typed: '{text}'")

        # Increase Font Size
        keyboard.send_keys('^a')  # Ctrl+A to select all text
        for _ in range(3):  # Increase size 3 times (e.g., from 11 to 18 or 24)
            keyboard.send_keys('^+{>}') # Ctrl+Shift+>
            time.sleep(0.1)
        
        # Click elsewhere to finish
        mouse.click(coords=(text_center_x + 150, text_center_y + 100))
        time.sleep(0.5)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"SUCCESS: Text '{text}' added to rectangle center at coordinates ({text_center_x}, {text_center_y})"
                )
            ]
        }
        
    except Exception as e:
        print(f"Error adding text: {e}")
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"ERROR adding text: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def save_paint_file(filename: str = "result", file_path: str = None) -> dict:
    """Automatically save the current Paint file as JPEG with timestamped filename
    
    Args:
        filename: Base filename for the saved file (without extension)
                 If a full path is provided, it will extract just the filename part
    """
    global paint_app
    try:
        if not paint_app:
            return {"content": [TextContent(type="text", text="ERROR: Paint not open. Call open_paint first.")]}
        
        # Handle filename parameter (can be just filename or full path)
        import datetime
        import os
        
        # If filename contains a full path, extract just the filename part
        if "\\" in filename or "/" in filename:
            filename = os.path.splitext(os.path.basename(filename))[0]
        
        # Generate timestamp in ddmmyyhhmm format
        now = datetime.datetime.now()
        timestamp = now.strftime("%d%m%y%H%M")
        
        # Use file_path if provided, otherwise default to assignment directory
        save_directory = file_path if file_path else "D:\\TSAI\\assignment-4\\mcp"
        actual_file_path = f"{save_directory}\\{filename}_{timestamp}.jpg"
        
        print(f"AUTO-SAVING PAINT FILE: {actual_file_path}")
        print(f"Target directory: {save_directory}")
        
        paint_window = paint_app.window(class_name='MSPaintApp')
        paint_window.set_focus()
        # Make sure Paint is focused
        win32gui.SetForegroundWindow(paint_window.handle)
        time.sleep(1.0)
        
        # Open save dialog using keyboard (simplified approach like simple_paint_test.py)
        print(f"Saving as: {filename}_{timestamp}.jpg")
        print("Opening Save dialog with Ctrl+S...")
        keyboard.send('ctrl+s')
        time.sleep(5.0)  # Wait for dialog to fully open
        
        print("Typing filename with extension in quotes...")
        # First type the filename in the filename field
        keyboard.send('ctrl+a')  # Select all in filename field
        time.sleep(0.5)
        keyboard.send('delete')  # Delete
        time.sleep(0.5)
        
        # Type filename with quotes and .jpg extension (this automatically sets file type)
        quoted_filename = f'"{filename}_{timestamp}.jpg"'
        print(f"Typing quoted filename: {quoted_filename}")
        keyboard.write(quoted_filename, delay=0.1)
        time.sleep(2.0)
        
        # Navigate to the specified directory by typing the full path AFTER filename is entered
        print(f"Now navigating to directory: {save_directory}")
        keyboard.send('ctrl+l')  # Focus on address bar in save dialog
        time.sleep(1.0)
        keyboard.write(save_directory, delay=0.1)  # Type the directory path
        time.sleep(1.0)
        keyboard.send('enter')  # Navigate to directory
        time.sleep(2.0)  # Wait for directory navigation to complete
        
        print("Pressing Enter to save...")
        keyboard.send('enter')  # Confirm filename field
        keyboard.send('enter')  # Save
        time.sleep(3.0)
        
        # Handle possible overwrite dialog (simplified)
        print("Handling possible overwrite dialog...")
        keyboard.send('enter')  # In case there's an overwrite dialog
        time.sleep(2.0)
        
        # Check if file was saved (prioritize the intended directory first)
        possible_paths = [
            f"{save_directory}\\{filename}_{timestamp}.jpg",
            f"{save_directory}\\{filename}_{timestamp}.jpeg",
            f"D:\\TSAI\\assignment-4\\mcp\\{filename}_{timestamp}.jpg",
            f"D:\\TSAI\\assignment-4\\mcp\\{filename}_{timestamp}.jpeg",
            f"C:\\Users\\{os.getenv('USERNAME')}\\Documents\\{filename}_{timestamp}.jpg",
            f"C:\\Users\\{os.getenv('USERNAME')}\\Pictures\\{filename}_{timestamp}.jpg"
        ]
        
        saved_file = None
        for path in possible_paths:
            if os.path.exists(path):
                file_size = os.path.getsize(path)
                print(f"File found: {path} (size: {file_size} bytes)")
                saved_file = path
                actual_file_path = path  # Update the actual path
                break
        
        if not saved_file:
            print("No file found. Checking current directory...")
            # List all files in current directory that match our pattern
            import glob
            pattern = f"*{timestamp}*"
            matches = glob.glob(pattern)
            if matches:
                print(f"Found files: {matches}")
                # Use the first match as the saved file
                saved_file = matches[0]
                actual_file_path = os.path.abspath(saved_file)
            else:
                print("No matching files found")
        
        # Verify file was saved and return path info
        if os.path.exists(actual_file_path):
            file_size = os.path.getsize(actual_file_path)
            return {
                "content": [TextContent(
                    type="text", 
                    text=f"SUCCESS: Paint file auto-saved as {actual_file_path} (size: {file_size} bytes). File ready for email attachment."
                )],
                "saved_file_path": actual_file_path,  # Return path for email attachment
                "file_size": file_size
            }
        else:
            # Create fallback filename if save dialog failed
            return {
                "content": [TextContent(
                    type="text", 
                    text=f"WARNING: Automated save may have failed. Expected file: {actual_file_path}. Please check Paint window and save manually if needed."
                )],
                "saved_file_path": actual_file_path,  # Still return expected path
                "file_size": 0
            }
            
    except Exception as e:
        print(f"Error auto-saving Paint file: {e}")
        return {
            "content": [TextContent(
                type="text", 
                text=f"ERROR saving Paint file: {str(e)}"
            )]
        }

if __name__ == "__main__":
    print("STARTING ENHANCED PAINT AUTOMATION MCP SERVER")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution