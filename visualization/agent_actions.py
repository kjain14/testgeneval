import argparse
import collections
import json
import os

import matplotlib.pyplot as plt


def count_commands(root_dir):
    """
    Parses JSON files in the given directory and counts occurrences of commands.
    
    :param root_dir: Root directory containing subdirectories with JSON files.
    :return: Dictionary with command counts.
    """
    command_counts = collections.Counter()

    for subdir in sorted(os.listdir(root_dir)):
        subdir_path = os.path.join(root_dir, subdir)
        if os.path.isdir(subdir_path):  # Check if it's a directory
            for file in sorted(os.listdir(subdir_path)):
                if file.endswith('.json'):
                    file_path = os.path.join(subdir_path, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)  # Load JSON data
                            tool_calls = data.get('response', {}).get('choices', [{}])[0].get('message', {}).get('tool_calls', [])
                            
                            last_tool_call = tool_calls[-1] if tool_calls else {}
                            try:
                                tool_call_dict = eval(last_tool_call.get('function', {}).get('arguments', '{}'))
                                if tool_call_dict and isinstance(tool_call_dict, dict):
                                    command = tool_call_dict.get('command')
                                    if command:
                                        if "coverage" in command:
                                            command = "coverage"
                                        elif "find" in command or 'ls' in command :
                                            command = "find"
                                        elif 'C-c' in command or 'pip' in command or len(command) > 20:
                                            command = "execute"
                                        command_counts[command] += 1
                            except Exception:
                                continue
                    except Exception:
                        continue

    return command_counts

def plot_command_frequencies(command_counts):
    """
    Generates an improved single-column bar plot for command frequency using seaborn.

    :param command_counts: Dictionary containing command frequencies.
    """
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1.5)  

    # Prepare data
    command_counts_new = {
        'View': command_counts['view'], 
        'Write': command_counts['create'], 
        'Edit': command_counts['str_replace'] + command_counts['insert'] + command_counts['undo_edit'], 
        'Navigate': command_counts['find'], 
        'Tests': command_counts['coverage'], 
        'Bash': command_counts['execute']
    }
    
    # Convert to DataFrame for easier plotting with seaborn
    df = pd.DataFrame({
        'Command Type': list(command_counts_new.keys()),
        'Frequency': list(command_counts_new.values())
    })
    
    # Sort by frequency in descending order (highest values first)
    df = df.sort_values('Frequency', ascending=False)
    print("Sorted data:")
    print(df)  # Print the sorted data to verify
    
    # Create figure - narrower for single column
    plt.figure(figsize=(7, 6))
    
    # Create plot
    ax = sns.barplot(
        x='Frequency', 
        y='Command Type', 
        data=df,
        color='#87CEFA',
        orient='h'  # Horizontal bars work better for single column
    )
    
    # Add values to the end of bars
    for i, v in enumerate(df['Frequency']):
        ax.text(v + 0.5, i, str(v), va='center')
    
    plt.savefig('command_frequencies.png', bbox_inches='tight')
    plt.savefig('command_frequencies.eps', bbox_inches='tight')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze command frequency in JSON files.")
    parser.add_argument('--root_dir', type=str, required=True, help="Root directory containing subdirectories with JSON files.")
    args = parser.parse_args()

    command_counts = count_commands(args.root_dir)
    plot_command_frequencies(command_counts)
