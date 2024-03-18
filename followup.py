
import pandas as pd
import argparse
import subprocess
import tempfile
import os
import csv

def run_llm(report_text):
    # Create a temporary file to hold the report text
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(report_text)
        tmp_path = tmp.name

    # Define the LLM command and the prompt
    command = "ollama run mistral"
    prompt1 = "You are answering a boolean question. The question will either be true/yes/affirmative, or false/no/negative. IMPORTANT: If yes or true or affirmative, return '1'. If no or false or negative, return '0'."
    prompt2 = "Does this report mention a follow-up exam?"
    full_command = f"{command} '{prompt1}' $(cat '{tmp_path}') '{prompt2}'"

    try:
        result_process = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = result_process.stdout.strip()  # Strip to remove leading/trailing whitespace

        print("LLM Output:", result)  # Print the LLM output for debugging/verification

        if result_process.returncode != 0:
            print(f"Error running LLM: {result_process.stderr}")
            result = 'Error encountered during processing'  # Provide a default error message
    except subprocess.CalledProcessError as e:
        print(f"Error running LLM: {e}")
        result = 'Error encountered during processing'  # Provide a default error message

    # Delete the temporary file
    os.unlink(tmp_path)

    return result  # Return the direct output from the LLM

# Set up the argument parser
parser = argparse.ArgumentParser(description='Process radiology reports to determine the need for a follow-up exam.')
parser.add_argument('--input_csv', type=str, required=True, help='Input CSV file path')
parser.add_argument('--output_csv', type=str, required=True, help='Output CSV file path')

# Parse the command-line arguments
args = parser.parse_args()

# Read the CSV file
df = pd.read_csv(args.input_csv)

# Group by ACC_NUM and concatenate the text
grouped_reports = df.groupby('ACC_NUM')['TEXT'].apply(' '.join).reset_index()

# Run each report through the LLM
grouped_reports['LLM_Output'] = grouped_reports['TEXT'].apply(run_llm)

# Write the results to the new CSV file, including all reports with their ACC_NUM and LLM_Output
grouped_reports.to_csv(args.output_csv, index=False, quoting=csv.QUOTE_ALL)

print(f"Processed reports are saved to {args.output_csv}")

