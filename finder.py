import os
import re
import codecs
import json
import pickle
import argparse

default_file_pattern = ".*\.html"
default_keyword_pattern = "<a (.*?)href=[\"'](?P<target>.*?)[\"'](.*)>(?P<keyword>.*?)</a>"
default_encoding = "utf-8"
escape_strings = {
                  ".":"\\.",
                  "^":"\\^",
                  "$":"\\$",
                  "*":"\\*",
                  "+":"\\+",
                  "?":"\\?",
                  "{":"\\{",
                  "}":"\\}",
                  "[":"\\[",
                  "]":"\\]",
                  "\\":"\\\\",
                  "|":"\\|",
                  "(":"\\(",
                  ")":"\\)"
}

class FileEntry:
    def __init__(self):
        self.file = ""
        self.keywordEntries = []

    def __init__(self, file):
        self.file = file
        self.keywordEntries = []

    def encodeAsJson(self):
        return {'file':self.file, 'keywordEntries':[keywordEntry.encodeAsJson() for keywordEntry in self.keywordEntries]}

    def encodeAsCsv(self):
        result = []
        for keywordEntry in self.keywordEntries:
            result.append(",".join([self.file, keywordEntry.keyword, keywordEntry.target]))
        return "\n".join(result)

class KeywordEntry:
    def __init__(self):
        self.keyword = ""
        self.target = ""

    def __init__(self, keyword, target):
        self.keyword = keyword
        self.target = target

    def encodeAsJson(self):
        return {'keyword':self.keyword, 'target':self.target}
    
    def encodeAsCsv(self):
        return ",".join([self.keyword, self.target])

class FileEntryJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (FileEntry, KeywordEntry)):
            return obj.encodeAsJson()
        return json.JSONEncoder.default(self, obj)

def find_all_files(directory, matcher_file=None):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if matcher_file is None or matcher_file.match(file):
                path = os.path.join(root, file)
                if os.path.isfile(path):
                    yield os.path.join(root, file)

def escape_special_characters(str):
    for key, value in escape_strings.items():
        str = str.replace(key, value)
    return str

def find_all_keywords(data, matcher_keyword, escape):
    for match in matcher_keyword.finditer(data):
        keyword = match.group("keyword")
        if escape:
            keyword = escape_special_characters(keyword)
        yield keyword, match.group("target")

def read_file(file, encoding=None):
    fp = None
    try:
        fp = codecs.open(file, 'r', encoding)
        return fp.read()
    finally:
        if fp is not None:
            fp.close()

def find_fileEntries(directory, pattern_file, pattern_keyword, encoding, escape):
    matcher_file = re.compile(pattern_file, re.IGNORECASE)
    matcher_keyword = re.compile(pattern_keyword, re.IGNORECASE)
    fileEntries = []
    for file in find_all_files(directory, matcher_file):
        data = read_file(file, encoding)
        fileEntry = FileEntry(file)
        for keyword, target in find_all_keywords(data, matcher_keyword, escape):
            keywordEntry = KeywordEntry(keyword, target)
            fileEntry.keywordEntries.append(keywordEntry)
        yield fileEntry

def find_fileEntries_as_json(directory, pattern_file, pattern_keyword, encoding=None, escape=False):
    return [fileEntry.encodeAsJson() for fileEntry in find_fileEntries(directory, pattern_file, pattern_keyword, encoding, escape)]

def find_fileEntries_as_csv(directory, pattern_file, pattern_keyword, encoding=None, escape=False):
    return "".join([fileEntry.encodeAsCsv() for fileEntry in find_fileEntries(directory, pattern_file, pattern_keyword, encoding, escape)])

def find_fileEntries_as_file_csv(directory, pattern_file, pattern_keyword, encoding=None, escape=False):
    fileSet = set()
    for fileEntry in find_fileEntries(directory, pattern_file, pattern_keyword, encoding, escape):
        fileSet.add(fileEntry.file)
    result = []
    for file in fileSet:
        result.append(",".join([file, "1"]))
    return "\n".join(result)

def find_fileEntries_as_keyword_csv(directory, pattern_file, pattern_keyword, encoding=None, escape=False):
    keywords = {}
    for fileEntry in find_fileEntries(directory, pattern_file, pattern_keyword, encoding, escape):
        for keywordEntry in fileEntry.keywordEntries:
            keywords[keywordEntry.keyword] = keywordEntry.target
    result = []
    for keyword, target in keywords.items():
        result.append(",".join([keyword, target, "1"]))
    return "\n".join(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-j", "--json", action="store_true", help="output as json")
    group.add_argument("-c", "--csv", action="store_true", help="output as csv")
    group.add_argument("-cf", "--file_csv", action="store_true", help="output as file csv")
    group.add_argument("-ck", "--keyword_csv", action="store_true", help="output as keyword csv")
    parser.add_argument("-d", "--dir", default=".", help="dir to find recursively")
    parser.add_argument("-f", "--file", default=default_file_pattern, help="file pattern (default: '" + default_file_pattern + "')")
    parser.add_argument("-k", "--keyword", default=default_keyword_pattern, help="keyword pattern, 'keyword' and 'target' group names must be specified (default: '" + default_keyword_pattern + "')")
    parser.add_argument("-e", "--encoding", default=default_encoding, help="encoding for reading files (default: '" + default_encoding + "')")
    parser.add_argument("-s", "--escape", action="store_true", help="escape regex special characters")
    args = parser.parse_args()
    if args.json:
        print(find_fileEntries_as_json(args.dir, args.file, args.keyword, args.encoding, args.escape))
    elif args.csv:
        print(find_fileEntries_as_csv(args.dir, args.file, args.keyword, args.encoding, args.escape))
    elif args.file_csv:
        print(find_fileEntries_as_file_csv(args.dir, args.file, args.keyword, args.encoding, args.escape))
    elif args.keyword_csv:
        print(find_fileEntries_as_keyword_csv(args.dir, args.file, args.keyword, args.encoding, args.escape))
    else:
        parser.print_help()
