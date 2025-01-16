import os
import argparse

def combine_files_in_directory(directory_path):
    """Combines two test files in each subdirectory into a single output file."""
    for subdir, _, files in os.walk(directory_path):
        test_files = [f for f in files if f.startswith("test_") and f.endswith(".py")]
        if len(test_files) == 2:
            file_paths = [os.path.join(subdir, f) for f in test_files]
            output_file = os.path.join(subdir, "combined_tests.py")
            combine_files(file_paths, output_file)
            print(f"Combined files in {subdir} into {output_file}.")

def combine_files(file_paths, output_path):
    """Combines the contents of multiple Python files into one, ensuring no duplicate imports or test case conflicts."""
    import_lines = set()
    test_cases = []
    test_case_counter = 0

    for file_path in file_paths:
        with open(file_path, "r") as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith("import") or line.startswith("from"):
                    import_lines.add(line.strip())
                elif line.startswith("def test_case_"):
                    test_case_counter += 1
                    new_test_case_name = f"def test_case_{test_case_counter}():\n"
                    test_cases.append(new_test_case_name)
                elif test_cases:
                    test_cases[-1] += line  # Append the rest of the test case content

    # Write the combined content to the output file
    with open(output_path, "w") as output:
        # Write unique imports
        for import_line in sorted(import_lines):
            output.write(f"{import_line}\n")
        output.write("\n")

        # Write all test cases
        for test_case in test_cases:
            output.write(f"{test_case}\n")

def main():
    parser = argparse.ArgumentParser(description="Combine test files in subdirectories.")
    parser.add_argument("--directory", type=str, required=True, help="The root directory containing subdirectories with test files.")
    args = parser.parse_args()

    combine_files_in_directory(args.directory)

if __name__ == "__main__":
    main()
