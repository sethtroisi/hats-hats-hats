'''
Copyright 2023 Seth Troisi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import json
import re
import os

JSON_OUTPUT = "HatsV1.json"
HATS_DIR = "static/HatsV1"

IGNORE_TAGS = [
    re.compile("^[\s&-]*$"),
    re.compile("hat", re.I),
    re.compile("front", re.I),
    re.compile("back", re.I),
]

def ignore_tag(tag):
    if not tag:
        return True
    return any(pattern.match(tag) for pattern in IGNORE_TAGS)

def fn_to_tags(fn):
    tags = os.path.splitext(fn)[0].split()
    tags = [tag for tag in tags if not ignore_tag(tag)]
    return tags

def main():
    # Quick and Dirty v0

    collection = {}


    for fn in os.listdir(HATS_DIR):
        path = os.path.join(HATS_DIR, fn)
        element = {
            "name": fn,
            "thumbnails": [path],
            "tags": fn_to_tags(fn),
        }
        collection[fn] = element

    print("Saving data on", len(collection), "hats")

    with open(JSON_OUTPUT, "w") as f:
        json.dump(collection, f)

if __name__ == "__main__":
    main()
