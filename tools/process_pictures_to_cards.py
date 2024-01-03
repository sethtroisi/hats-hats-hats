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
import os
import re

import get_image_size

JSON_OUTPUT = "HatsV1.json"
HATS_DIR = "static/HatsV1"

IGNORE_WORDS = [re.compile(word, re.I) for word in (
    "hat", "front", "back", "and", "a", "an", "to"
)]
IGNORE_TAGS = [
    re.compile("^[\s&-]*$"),
    re.compile("^[1-4]$"),
] + IGNORE_WORDS

def ignore_tag(tag):
    if not tag:
        return True
    return any(pattern.match(tag) for pattern in IGNORE_TAGS)

def name_to_tags(name):
    name = name.strip()
    if name.endswith((" a", " b", " 1", " 2")):
        name = name[:-2]

    tags = name.strip().split()
    tags = [tag for tag in tags if not ignore_tag(tag)]
    tags = [tag.strip("-&") for tag in tags]
    return tags

def fixup_name(name):
    prefixes = ("zz", "Hat", "hat")
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):].lstrip()
    return name.strip()

def get_data(paths):
    lead = paths[0]
    name = os.path.basename(lead)
    name = os.path.splitext(name)[0]
    name = fixup_name(name)
    tags = name_to_tags(name)

    img = get_image_size.get_image_metadata(lead)
    size = img.width, img.height

    print(name)

    return {
        "name": name,
        "thumbnails": paths,
        "tags": tags,
        "size": size,
    }

def main():
    # Quick and Dirty v0

    collection = {}

    for fn in sorted(os.listdir(HATS_DIR)):
        path = os.path.join(HATS_DIR, fn)
        if os.path.isfile(path):
            element = get_data([path])
        elif os.path.isdir(path):
            element = get_data([os.path.join(path, p) for p in os.listdir(path)])
        else:
            assert False, fn

        collection[fn] = element

    pictures = sum(len(e['thumbnails']) for e in collection.values())
    print(f"Saving metadata for {len(collection)} hats with {pictures} pictures")

    with open(JSON_OUTPUT, "w") as f:
        json.dump(collection, f)

if __name__ == "__main__":
    main()
