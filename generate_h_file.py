import pandas as pd
import re
import os
import ast


### PARAMETERS
parameters_excel_file = 'parameters_xls_3_bottom_plate_boven.xlsx'     # Replace with your Excel file path
template_file = 'template_xls_3_bottom_plate_boven.H'  # Replace with your template file path


### NO TOUCHY TOUCHY !
def main():
    selections_folder = 'selections'            # Folder containing selections files
    output_folder = 'generated_h_files'

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read Excel file into a DataFrame with all data as strings
    try:
        df = pd.read_excel(parameters_excel_file, header=None, dtype=str)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Extract parameter names from the first column
    parameter_names = df.iloc[:, 0].astype(str).str.strip()
    num_columns = df.shape[1]

    # Check if there are multiple parameter sets
    if num_columns < 2:
        print("Error: The Excel file must contain at least two columns (parameters and one set of values).")
        return

    # Iterate over each parameter set (column)
    for col_index in range(1, num_columns):
        print(f"\nProcessing parameter set from column {col_index}")

        # Build param_dict for the current parameter set
        param_dict = {}
        for k, v in zip(parameter_names, df.iloc[:, col_index]):
            # Strip whitespace and convert parameter names to strings
            k = str(k).strip()
            v_str = str(v).strip()

            # Debugging: Print raw value
            print(f"Processing parameter '{k}': raw value '{v_str}' (repr: {repr(v_str)})")

            # Handle 'nan' or empty values
            if v_str.lower() == 'nan' or v_str == '':
                print(f"Parameter '{k}' has empty or NaN value.")
                param_dict[k] = None
                continue

            # Replace Unicode minus sign with ASCII hyphen-minus
            v_str = v_str.replace('−', '-')

            # Check if the value is a list
            if v_str.startswith('[') and v_str.endswith(']'):
                # Attempt to parse as list
                try:
                    v_list = ast.literal_eval(v_str)
                    if isinstance(v_list, list):
                        param_dict[k] = v_list
                        print(f"Parameter '{k}' parsed as list: {v_list}")
                        continue  # Move to next parameter
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing list for parameter '{k}': {e}")
                    param_dict[k] = v_str  # Store as string if parsing fails
                    continue  # Move to next parameter

            # Replace comma with dot for decimal separator, if necessary (but not in list strings)
            if not (k.startswith('FOR_') and v_str.startswith('[') and v_str.endswith(']')):
                v_str = v_str.replace(',', '.')

            # Strip quotes if present
            v_str = v_str.strip('"').strip("'")

            # Attempt to convert numeric values
            try:
                v_num = float(v_str)
                param_dict[k] = v_num
                print(f"Parameter '{k}' parsed as float: {v_num}")
            except ValueError:
                # Keep as string
                v_upper = v_str.upper()
                if v_upper in ['YES', 'NO']:
                    param_dict[k] = v_upper
                else:
                    param_dict[k] = v_str  # Preserve original casing
                print(f"Parameter '{k}' kept as string: {param_dict[k]}")

        # Debug: Print the parameter dictionary
        print("Parameter Dictionary:")
        for key, value in param_dict.items():
            print(f"'{key}': {value} (type: {type(value).__name__})")

        # Get PartNumber for output filename
        part_number = param_dict.get('PartNumber')
        if not part_number:
            print("Error: 'PartNumber' parameter not found in the current parameter set.")
            continue  # Skip this parameter set
        output_filename = os.path.join(output_folder, f"{str(part_number)}.H")  # Save to generated_h_files/

        # Read the template file
        try:
            with open(template_file, 'r') as file:
                template_content = file.read()
        except Exception as e:
            print(f"Error reading template file: {e}")
            continue  # Skip this parameter set

        content = template_content  # Start with the template content

        # Process USES_ blocks first
        content = process_uses_blocks(content, param_dict)

        # Process FOR_ blocks
        content = process_for_blocks(content, param_dict)

        # Evaluate expressions and replace placeholders outside FOR_ blocks
        content = evaluate_expressions_in_content(content, param_dict)

        # Now, process SELECT_ placeholders
        content = process_select_placeholders(content, param_dict, selections_folder)

        # Write the output file
        try:
            with open(output_filename, 'w') as file:
                file.write(content)
            print(f"Generated file: {output_filename}")
        except Exception as e:
            print(f"Error writing output file: {e}")

def process_uses_blocks(content, param_dict):
    pattern = r'\{(USES_[^\}]+)\}(.*?)\{\1\}'
    def replace_uses(match):
        uses_param = match.group(1)
        block_content = match.group(2)
        uses_value = param_dict.get(uses_param, 'NO')
        if isinstance(uses_value, str):
            uses_value = uses_value.upper()
        if uses_value == 'YES':
            return block_content
        else:
            return ''
    while re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, replace_uses, content, flags=re.DOTALL)
    return content

def process_for_blocks(content, param_dict):
    pattern = r'\{(FOR_[^\}]+)\}(.*?)\{\1\}'
    def replace_for(match):
        for_param = match.group(1)  # The parameter name with FOR_
        block_content = match.group(2)  # The content inside the FOR_ block
        vector = param_dict.get(for_param)
        print(f"Processing FOR_ block for parameter '{for_param}': vector = {vector}")
        if isinstance(vector, list):
            result = ""
            param_name = for_param.replace('FOR_', '', 1)
            for value in vector:
                # For each value, process the block content separately
                temp_content = block_content
                # Create a local copy of param_dict with the current value
                local_param_dict = param_dict.copy()
                local_param_dict[param_name] = value
                # Process expressions and placeholders within the block
                temp_content_evaluated = evaluate_expressions_in_content(temp_content, local_param_dict)
                result += temp_content_evaluated + '\n'
            return result
        else:
            print(f"Warning: FOR_ parameter '{for_param}' is missing or not a list.")
            return ''  # Remove the block if the vector is missing or invalid
    while re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, replace_for, content, flags=re.DOTALL)
    return content

def evaluate_expressions_in_content(content, local_param_dict):
    # First, evaluate expressions
    content = re.sub(r'\{([^\{\}]+)\}', lambda match: evaluate_expression(match, local_param_dict), content)
    # Then, replace remaining placeholders
    content = re.sub(r'\{([^\{\}]+)\}', lambda match: replace_remaining_placeholders(match, local_param_dict), content)
    return content

def evaluate_expression(match, local_param_dict):
    expr = match.group(1)
    original_expr = expr  # Keep for error messages

    # Skip SELECT_ placeholders for now
    if expr.startswith('SELECT_'):
        return match.group(0)

    try:
        # Safely evaluate the expression
        # Only allow the parameters in local_param_dict as variables
        local_dict = {}
        for key, value in local_param_dict.items():
            if isinstance(value, (int, float)):
                local_dict[key] = value
        result = eval(expr, {"__builtins__": None}, local_dict)
        # Format the result with sign, preserving decimals
        sign = '+' if result >= 0 else '-'
        return f"{sign}{abs(result):g}"
    except Exception as e:
        print(f"Error evaluating expression '{original_expr}': {e}")
        return match.group(0)  # Return original placeholder on error

def replace_remaining_placeholders(match, local_param_dict):
    placeholder = match.group(1)
    # Skip SELECT_ placeholders
    if placeholder.startswith('SELECT_'):
        return match.group(0)
    value = local_param_dict.get(placeholder, match.group(0))
    return str(value)

def process_select_placeholders(content, param_dict, selections_folder):
    pattern = r'\{(SELECT_[^\{\}]+)\}'
    def replace_select(match):
        select_param = match.group(1)
        filename = param_dict.get(select_param)
        if not filename:
            print(f"Warning: No value found for parameter '{select_param}'.")
            return match.group(0)  # Keep the placeholder unchanged
        filepath = os.path.join(selections_folder, filename)
        try:
            with open(filepath, 'r') as f:
                file_content = f.read()
            return file_content
        except Exception as e:
            print(f"Error reading file '{filepath}': {e}")
            return match.group(0)  # Keep the placeholder unchanged
    return re.sub(pattern, replace_select, content)

if __name__ == "__main__":
    main()
