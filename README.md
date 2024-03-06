# auto_followup: Simple Radiology Report Processor

## Description
This Python script processes radiology reports to determine the need for a follow-up exam. It reads a given input CSV file containing radiology reports, runs each report through a Large Language Model (LLM) to summarize the findings, and outputs the results to a new CSV file. This process includes assessing whether a follow-up exam is recommended based on the summarized findings.

## Installation
To run this script, you need Python installed on your machine along with several dependencies. The script has been tested on Python 3.8+.

First, ensure you have Python installed. Then, install the required packages using pip:

```bash
pip install pandas argparse subprocess tempfile os csv
```

## Usage
To use this script, you need to provide an input CSV file and specify an output file for the results. The input CSV file should have at least two columns: ACC_NUM and TEXT, where ACC_NUM is a unique identifier for each report, and TEXT contains the radiology report text lines.

Example
If your input file is named radiology_reports.csv and you want to output the results to processed_reports.csv, run the following command:
```bash
python radiology_report_processor.py --input_csv path/to/your/input.csv --output_csv path/to/your/output.csv
```

After running the script, processed_reports.csv will contain the ACC_NUM, the original TEXT, and the LLM_Output indicating the summary of the findings and whether a follow-up exam is recommended.
