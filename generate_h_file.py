import pandas as pd
import re
import os

def main():
    # Specify your Excel file and template file here
    excel_file = 'parameters.xlsx'     # Replace with your Excel file path
    template_file = 'template.H'       # Replace with your template file path
    labels_folder = 'labels'           # Folder containing label files
    output_folder = 'generated_h_files'

    # Read Excel file into a DataFrame
    try:
        df = pd.read_excel(excel_file, header=None)
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

            # Replace comma with dot for decimal separator, if necessary
            v_str = v_str.replace(',', '.')

            # Strip quotes if present
            v_str = v_str.strip('"').strip("'")

            # Attempt to convert numeric values
            try:
                v_num = float(v_str)
                param_dict[k] = v_num
            except ValueError:
                # Keep as string
                v_upper = v_str.upper()
                if v_upper in ['YES', 'NO']:
                    param_dict[k] = v_upper
                else:
                    param_dict[k] = v_str  # Preserve original casing

        # Debug: Print the parameter dictionary
        print("Parameter Dictionary:")
        for key, value in param_dict.items():
            print(f"'{key}': '{value}' (type: {type(value).__name__})")

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

        # Process USES conditional blocks
        def process_uses_blocks(content):
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

        # Process USES blocks first
        content = process_uses_blocks(template_content)

        # Replace placeholders with evaluated expressions
        def evaluate_expression(match):
            expr = match.group(1)
            original_expr = expr  # Keep for error messages

            # Skip SELECT_ placeholders for now
            if expr.startswith('SELECT_'):
                return match.group(0)

            try:
                # Safely evaluate the expression
                # Only allow the parameters in param_dict as variables
                local_dict = {}
                for key, value in param_dict.items():
                    if isinstance(value, (int, float)):
                        local_dict[key] = value
                result = eval(expr, {"__builtins__": None}, local_dict)
                # Format the result with sign, preserving decimals
                sign = '+' if result >= 0 else '-'
                return f"{sign}{abs(result):g}"
            except Exception as e:
                print(f"Error evaluating expression '{original_expr}': {e}")
                return match.group(0)  # Return original placeholder on error

        # Replace all placeholders in the content (except SELECT_)
        content = re.sub(r'\{([^\{\}]+)\}', evaluate_expression, content)

        # Replace any remaining placeholders with their string values (except SELECT_)
        def replace_remaining_placeholders(match):
            placeholder = match.group(1)
            # Skip SELECT_ placeholders for now
            if placeholder.startswith('SELECT_'):
                return match.group(0)
            value = param_dict.get(placeholder, match.group(0))
            return str(value)

        content = re.sub(r'\{([^\{\}]+)\}', replace_remaining_placeholders, content)

        # Now, process SELECT_ placeholders
        def process_select_placeholders(content):
            pattern = r'\{(SELECT_[^\{\}]+)\}'
            def replace_select(match):
                select_param = match.group(1)
                filename = param_dict.get(select_param)
                if not filename:
                    print(f"Warning: No value found for parameter '{select_param}'.")
                    return match.group(0)  # Keep the placeholder unchanged
                filepath = os.path.join(labels_folder, filename)
                try:
                    with open(filepath, 'r') as f:
                        file_content = f.read()
                    return file_content
                except Exception as e:
                    print(f"Error reading file '{filepath}': {e}")
                    return match.group(0)  # Keep the placeholder unchanged
            content = re.sub(pattern, replace_select, content)
            return content

        # Finally, process SELECT_ placeholders
        content = process_select_placeholders(content)

        # Write the output file
        try:
            with open(output_filename, 'w') as file:
                file.write(content)
            print(f"Generated file: {output_filename}")
        except Exception as e:
            print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()
