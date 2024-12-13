from datasets import Dataset, DatasetDict
from inference.configs.config_utils import get_first_method_partial_python
import re

class CATLMPrompt:
    def __init__(self):
        self.PROMPT_FULL = """{code_src}
<|codetestpair|>
{imports}
"""

        self.PROMPT_FULL_NO_IMPORT = """{code_src}
<|codetestpair|>
"""

        self.PROMPT_COMPLETION = """{code_src}
<|codetestpair|>
{test_src}
"""
    def postprocess_output(self, text, is_full):
        if not is_full:
            return text

        # Match all function definitions in the text
        function_definitions = list(re.finditer(r"def\s+\w+\s*\(.*?\):", text))

        # If there is at least one function definition, remove the last one
        if function_definitions:
            last_function_start = function_definitions[-1].start()
            text = text[:last_function_start].rstrip()

        return text


    def add_prompts_to_dataset(self, dataset, no_import=False, tokenizer=None):
        assert tokenizer != None
        test_data = dataset["test"]

        new_arr = []
        for new_data in test_data.select(range(1)):
            code_src = new_data["code_src"]
            full_context = self.PROMPT_FULL.format(
                code_src=code_src,
                imports="\n".join(new_data["local_imports"]),
            )
            full_context_no_import = self.PROMPT_FULL_NO_IMPORT.format(
                code_src=code_src
            )
            first_context = self.PROMPT_COMPLETION.format(
                code_src=code_src, test_src=new_data["preds_context"]["preamble"]
            )
            last_context = self.PROMPT_COMPLETION.format(
                code_src=code_src, test_src=new_data["preds_context"]["last_minus_one"]
            )
            extra_context = self.PROMPT_COMPLETION.format(
                code_src=code_src, test_src=new_data["preds_context"]["last"]
            )

            new_data["preds_prompts"] = {
                "full": full_context_no_import if no_import else full_context,
                "first": first_context,
                "last": last_context,
                "extra": extra_context,
            }
            new_arr.append(new_data)

        final_dataset = DatasetDict({"test": Dataset.from_list(new_arr)})

        return final_dataset
