import re
import json
import re

class Ronj2Json:
    def __init__(self, file_path):
        self.file_path = file_path
        self.markdown_text = ''
        self.result = []

    def read_markdown_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.markdown_text = f.read()

    def parse_markdown(self):
        pattern = re.compile(r'(\d+)\s名前：(.+?)\s\d{4}/\d{2}/\d{2}\(\w+\)\s\d{2}:\d{2}:\d{2}\.\d{2}\sID:\w+\n\*\*(.*?)\*\*(?:\n|$)', re.MULTILINE | re.DOTALL)
        matches = pattern.findall(self.markdown_text)

        for match in matches:
            item = {
                'number': match[0],
                'name': match[1],
                'message': match[2].strip()
            }
            self.result.append(item)

    def display_result(self):
        for item in self.result:
            print(f"{item['number']} 名前：{item['name']}")
            print(f"メッセージ：{item['message']}\n")

    def process_markdown(self):
        self.read_markdown_file()
        self.parse_markdown()
        self.display_result()
# # 使用例
# file_path = 'path/to/your/markdown/file.md'
# processor = Ronj2Json(file_path)
# processor.process_markdown()