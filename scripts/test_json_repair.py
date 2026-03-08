import json

def repair_json(text):
    """
    Attempts to repair a truncated JSON string by adding missing closing braces/brackets.
    """
    text = text.strip()
    stack = []
    in_string = False
    escape = False
    
    for i, char in enumerate(text):
        if char == '"' and not escape:
            in_string = not in_string
        if in_string:
            if char == '\\':
                escape = not escape
            else:
                escape = False
            continue
        
        if char == '{':
            stack.append('}')
        elif char == '[':
            stack.append(']')
        elif char in ('}', ']') and stack:
            if stack[-1] == char:
                stack.pop()
    
    # Close any remaining open constructs
    return text + "".join(reversed(stack))

def test_repair():
    test_cases = [
        ('{"a": 1, "b": [1, 2', '{"a": 1, "b": [1, 2]}'),
        ('{"summary": {"name": "test", "rows": 10', '{"summary": {"name": "test", "rows": 10}}'),
        ('[{"id": 1}, {"id": 2', '[{"id": 1}, {"id": 2}]'),
        ('{"text": "val with } brace"', '{"text": "val with } brace"}'),
        ('{"nested": {"list": [1, 2', '{"nested": {"list": [1, 2]}}'),
    ]
    
    for input_str, expected in test_cases:
        repaired = repair_json(input_str)
        print(f"Input:    {input_str}")
        print(f"Repaired: {repaired}")
        try:
            json.loads(repaired)
            print("Status:   SUCCESS (Valid JSON)")
        except json.JSONDecodeError as e:
            print(f"Status:   FAILED ({e})")
        print("-" * 20)

if __name__ == "__main__":
    test_repair()
