import re


class MarkdownString(str):
    def __new__(cls, content):
        # Ensure the instance is created as a string
        return super().__new__(cls, content)

    def __init__(self, content):
        self.content = content

    def to_ansi(self):
        ansi_content = self.content

        # Convert markdown bold (**text** or __text__) to ANSI bold (\033[1mtext\033[0m)
        ansi_content = re.sub(r'\*\*(.*?)\*\*|__(.*?)__', r'\033[1m\1\2\033[0m', ansi_content)

        # Convert markdown italic (*text* or _text_) to ANSI italic (\033[3mtext\033[0m)
        ansi_content = re.sub(r'\*(.*?)\*|_(.*?)_', r'\033[3m\1\2\033[0m', ansi_content)

        # Convert markdown code (`text`) to ANSI reverse video (\033[7mtext\033[0m)
        ansi_content = re.sub(r'`(.*?)`', r'\033[7m\1\033[0m', ansi_content)

        # Add more markdown to ANSI conversions as needed

        return ansi_content

    def __str__(self):
        return self.to_ansi()


# Example usage
md_string = MarkdownString("This is **bold**, this is *italic*, and this is `code`.")
print(md_string)
