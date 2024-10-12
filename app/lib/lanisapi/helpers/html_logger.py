import os
from time import time

class HTMLLogger:
    """Provide various logging functions to send HTML code for bug reports."""
    
    html_log_path = os.path.join(os.path.dirname(__file__), 'log/html_logs.txt')

    @classmethod
    def init(cls) -> None:
        """Create an initial html_logs.txt file and checks if saving is allowed."""
        # Ensure the log directory exists
        os.makedirs(os.path.dirname(cls.html_log_path), exist_ok=True)

        if not os.path.exists(cls.html_log_path):
            with open(cls.html_log_path, "w", encoding="utf-8") as file:
                file.writelines(
                    [
                        "## Info ################################################################################################\n",
                        "# This file has various HTML data WHICH MAY CONTAIN SENSITIVE DATA but it's very useful for debugging! #\n",
                        "# This file will be uploaded by you to the GitHub errors page if any warning or error occurred!         #\n"
                        "########################################################################################################\n",
                        "\n",
                        "## Format ############################################################################################\n"
                        "# timestamp-library function name-(if multiple data) id of HTML element-name of wanted data: Message #\n"
                        "######################################################################################################\n",
                    ]
                )

    @classmethod
    def log_missing_element(
        cls,
        html: str,
        function_name: str,
        element_index: str,
        attribute_name: str,
    ) -> None:
        """Log a missing HTML element.

        Parameters
        ----------
        html : str
            The pure HTML of the element
        function_name : str
            The name of the causative function.
        element_index : str
            The index of an element if the function tries to get a set of data.
        attribute_name : str
            The name of the wanted data.
        """
        log = f"""
#--Start------------------------#
{int(time())}-{function_name}-{element_index}-{attribute_name}: Missing element!

*~~Element-HTML~~~~~~~~~~~~*

{html}
#--End--------------------------#

"""

        with open(cls.html_log_path, "a", encoding="utf-8") as file:
            file.write(log)
