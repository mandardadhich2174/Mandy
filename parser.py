# -*- coding: utf-8 -*-
import re

def execute_mandy(code):
    variables = {}
    lines = code.strip().split("\n")  # Split input into lines

    for line in lines:
        line = line.strip()

        # ✅ Skip empty lines
        if line == "":
            continue
        
        # ✅ Ignore comments
        if line.startswith("!!"):
            continue

        # ✅ Case-insensitive commands
        words = line.split(" ", 1)  
        command = words[0].lower()

        # ✅ Handle variable assignment (Take a = "text" or Take a = 10)
        if command == "take" and len(words) > 1:
            match = re.match(r'(\w+) = (.+)', words[1])
            if match:
                var_name, value = match.groups()
                
                # Handle strings with proper quotes
                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    variables[var_name] = value[1:-1]  # Remove quotes
                elif value.isdigit():
                    variables[var_name] = int(value)  # Convert to number
                else:
                    print(f"SyntaxError: Invalid assignment '{line}'")
            continue

        # ✅ Handle Write (printing)
        if command == "write" and len(words) > 1:
            content = words[1].strip()

            # ✅ Check if it's a properly quoted string
            if (content.startswith('"') and content.endswith('"')) or (content.startswith("'") and content.endswith("'")):
                print(content[1:-1])  # Remove quotes and print
            
            # ✅ Check if it's a variable
            elif content in variables:
                print(variables[content])

            # ❌ Error: Unsupported operation
            else:
                print(f"Error: Unsupported operation '{line}'")
            continue

        # ❌ If no match, print an error
        print(f"SyntaxError: Invalid syntax '{line}'")


# ✅ Test Cases
mandy_code = """
Write "hello"
Write 'world'
Write "a"
Take msg = "Mandy Language"
Write msg
"""

execute_mandy(mandy_code)
