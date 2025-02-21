from flask import Flask, request, jsonify
from flask_cors import CORS
import ast

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

def safe_eval(expression, variables):
    """Safely evaluate arithmetic expressions without using eval."""
    try:
        tree = ast.parse(expression, mode='eval')
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Name, ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod)):
                raise ValueError("Unsupported operation")
        return eval(expression, {"__builtins__": {}}, variables)
    except Exception as e:
        return f"Error: {str(e)}"

def run_mandy_code(code):
    """Simple Mandy interpreter for executing basic commands and arithmetic operations."""
    lines = code.split('\n')
    output = []
    variables = {}
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("!!"):  # Ignore empty lines and comments
            continue
        
        parts = line.split()
        if not parts:
            continue
        
        cmd = parts[0].lower()
        
        try:
            if cmd == "write":  # Print output
                expression = ' '.join(parts[1:])
                result = safe_eval(expression, variables)
                output.append(str(result))
            elif cmd == "take":  # Variable declaration
                if len(parts) >= 4 and parts[2] == "=":
                    var_name = parts[1]
                    var_value = ' '.join(parts[3:])
                    variables[var_name] = safe_eval(var_value, variables)
            elif cmd in variables:  # Handling stored variables
                output.append(str(variables[cmd]))
            else:
                output.append(f"Error: Unknown command '{cmd}'")
        except Exception as e:
            output.append(f"Error: {str(e)}")
    
    return '\n'.join(output)

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    code = data.get("code", "")
    output = run_mandy_code(code)
    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
