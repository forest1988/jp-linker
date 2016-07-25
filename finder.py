import os
import re
import codecs
import json
import pickle
import argparse

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

def find_all_keywords(data, matcher_keyword):
    for match in matcher_keyword.finditer(data):
        yield match.group("keyword"), match.group(0)

def read_file(file, encoding=None):
    fp = None
    try:
        fp = codecs.open(file, 'r', encoding)
        return fp.read()
    finally:
        if fp is not None:
            fp.close()

def find_fileEntries(directory, pattern_file, pattern_keyword, encoding):
    matcher_file = re.compile(pattern_file, re.IGNORECASE)
    matcher_keyword = re.compile(pattern_keyword, re.IGNORECASE)
    fileEntries = []
    for file in find_all_files(directory, matcher_file):
        data = read_file(file, encoding)
        fileEntry = FileEntry(file)
        for keyword, target in find_all_keywords(data, matcher_keyword):
            keywordEntry = KeywordEntry(keyword, target)
            fileEntry.keywordEntries.append(keywordEntry)
        yield fileEntry

def find_fileEntries_as_json(directory, pattern_file, pattern_keyword, encoding=None):
    return [fileEntry.encodeAsJson() for fileEntry in find_fileEntries(directory, pattern_file, pattern_keyword, encoding)]

def find_fileEntries_as_csv(directory, pattern_file, pattern_keyword, encoding=None):
    return "".join([fileEntry.encodeAsCsv() for fileEntry in find_fileEntries(directory, pattern_file, pattern_keyword, encoding)])


# print(find_fileEntries_as_json("sample", ".*\.html", "<a (.*?)href=(.*?)>(?P<keyword>.*?)</a>", 'utf-8'))
# print(find_fileEntries_as_csv("sample", ".*\.html", "<a (.*?)href=(.*?)>(?P<keyword>.*?)</a>", 'utf-8'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-j", "--json", action="store_true")
    group.add_argument("-c", "--csv", action="store_true")
    parser.add_argument("-d", "--dir", default=".")
    parser.add_argument("-f", "--file", default=".*\.html")
    parser.add_argument("-k", "--keyword", default="<a (.*?)href=(.*?)>(?P<keyword>.*?)</a>")
    parser.add_argument("-e", "--encoding", default="utf-8")
    args = parser.parse_args()
    if args.json:
        print(find_fileEntries_as_json(args.dir, args.file, args.keyword, args.encoding))
    elif args.csv:
        print(find_fileEntries_as_csv(args.dir, args.file, args.keyword, args.encoding))
    else:
        parser.print_help()
    print(args)