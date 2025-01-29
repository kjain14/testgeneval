import json
import argparse

def extract_passing_instances(input_json_path, output_txt_path):
    # Open and read the JSON file
    with open(input_json_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Collect instance IDs where tests_passed is True
    passing_instances = [
        instance_id
        for instance_id, instance_data in data.items()
        if instance_data["full"]["tests_passed"][0]
    ]
    
    # Write the passing IDs to the output text file
    with open(output_txt_path, 'w') as output_file:
        for instance_id in passing_instances:
            output_file.write(instance_id + '\n')

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract IDs where full tests pass.")
    parser.add_argument('--input_json', required=True, help="Path to the input JSON file.")
    parser.add_argument('--output_txt', required=True, help="Path to the output TXT file.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the extraction function
    extract_passing_instances(args.input_json, args.output_txt)

if __name__ == "__main__":
    main()
