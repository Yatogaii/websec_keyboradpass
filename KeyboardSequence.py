import csv

import json

def transform_characters(s):
    transform_dict = {
        '!': '1',
        '@': '2',
        '#': '3',
        '$': '4',
        '%': '5',
        '^': '6',
        '&': '7',
        '*': '8',
        '(': '9',
        ')': '0',
        '{': '[',
        '}': ']',
        '|': '\\',
        ':': ';',
        '"': "'",
        '<': ',',
        '>': '.',
        '?': '/',
        '+': '=',
        '_': '-',
        'Q': 'q',
        'W': 'w',
        'E': 'e',
        'R': 'r',
        'T': 't',
        'Y': 'y',
        'U': 'u',
        'I': 'i',
        'O': 'o',
        'P': 'p',
        'A': 'a',
        'S': 's',
        'D': 'd',
        'F': 'f',
        'G': 'g',
        'H': 'h',
        'J': 'j',
        'K': 'k',
        'L': 'l',
        'Z': 'z',
        'X': 'x',
        'C': 'c',
        'V': 'v',
        'B': 'b',
        'N': 'n',
        'M': 'm'
    }

    return ''.join(transform_dict.get(char, char) for char in s)


class KeyboardGraph:
    layout = []
    def __init__(self, layout):
        self.graph = self.build_graph(layout)

    DIRECTIONS = {
        (-1, 0): 'W',  # Up
        (1, 0): 'X',  # Down
        (0, -1): 'A',  # Left
        (0, 1): 'D',  # Right
        (-1, -1): 'Q',  # Left up
        (-1, 1): 'E',  # Right up
        (1, -1): 'Z',  # Left down
        (1, 1): 'C'   # Right down
    }

    def build_graph(self, layout):
        graph = {}
        rows = len(layout)
        self.layout = layout

        for r in range(rows):
            cols = len(layout[r])
            for c in range(cols):
                key = layout[r][c]
                adjacent_keys = []

                for (i, j), dir_symbol in self.DIRECTIONS.items():
                    new_r, new_c = r + i, c + j
                    if 0 <= new_r < rows and 0 <= new_c < len(layout[new_r]):
                        adjacent_keys.append(layout[new_r][new_c])
                graph[key] = adjacent_keys
        return graph

    def convert_to_pattern(self, s):
        prev_char = s[0]
        pattern = ""

        for curr_char in s[1:]:
            direction_found = False

            # 查找prev_char与curr_char之间的方向
            for (i, j), dir_symbol in self.DIRECTIONS.items():
                if curr_char in self.graph[prev_char]:
                    # 使用layout获取它们的位置
                    prev_r, prev_c = self.get_position(prev_char, self.layout)
                    new_r, new_c = prev_r + i, prev_c + j
                    if 0 <= new_r < len(self.layout) and 0 <= new_c < len(self.layout[new_r]) and self.layout[new_r][new_c] == curr_char:
                        pattern += dir_symbol
                        direction_found = True
                        break

            # 如果没有找到方向（例如，两个字符不相邻），添加一个占位符
            if not direction_found:
                pattern += '?'

            prev_char = curr_char

        return pattern

    def get_position(self, char, layout):
        for r in range(len(layout)):
            for c in range(len(layout[r])):
                if layout[r][c] == char:
                    return r, c
        return -1, -1  # 未找到字符

    def is_keyboard_sequence(self, s, min_length=2):
        s=  s.encode("ascii", errors="ignore").decode("ascii")
        n = len(s)
        for i in range(n):
            sequence_length = 1
            while i + sequence_length < n and s[i + sequence_length -1] in self.graph.keys() \
            and s[i + sequence_length] in self.graph[s[i + sequence_length - 1]]:
                sequence_length += 1

            if sequence_length >= min_length:
                return True, s[i:i+sequence_length]

        return False, ""

def extract_second_column(file_path):
    results = []
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 1:
                # 去除双引号并添加到结果列表
                results.append(row[1].strip('\''))

    return results

if __name__ == '__main__':
    layout = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'"],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']]

    keyboard = KeyboardGraph(layout)

    def process_file(filepath):
        map_patterns = {}
        csv_data = extract_second_column(filepath)

        for each in csv_data:
            res, sequence = keyboard.is_keyboard_sequence(transform_characters(each), 3)
            if res:
                pattern = keyboard.convert_to_pattern(sequence)
                if pattern not in map_patterns:
                    map_patterns[pattern] = {"count": 0, "string": {}}

                map_patterns[pattern]["count"] += 1
                map_patterns[pattern]["string"][sequence] = map_patterns[pattern]["string"].get(sequence, 0) + 1

        # Sort by count
        sorted_patterns = dict(sorted(map_patterns.items(), key=lambda item: item[1]['count'], reverse=True))
        return sorted_patterns

    yahoo_data = process_file(r'datas/yahoo.csv')
    with open(r'datas/yahoo.json', 'w', encoding='utf-8') as f:
        json.dump(yahoo_data, f, ensure_ascii=False, indent=4)

    csdn_data = process_file(r'datas/csdn.csv')
    with open(r'datas/csdn.json', 'w', encoding='utf-8') as f:
        json.dump(csdn_data, f, ensure_ascii=False, indent=4)
