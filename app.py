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

from collections import defaultdict

from flask import Flask
from flask import render_template, send_from_directory
from flask_caching import Cache


print("Setting up Hats controller")

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


COLLECTION_FN = "HatsV1.json"

# TODO add back later
# def add_tags(element):
#     """ Add list of [(tag1, style1), (tag2, style2)]"""
#     tags = []
#
#     n = wu["n"]
#     for under in [10, 100, 200]:
#         if n <= under * 1000:
#             tags.append((f"Under {under}k", "secondary"))
#             break
#
#     if wu["num_factors"] == 0:
#         tags.append((f"NF", "warning"))
#
#     if wu["num_factors"] > 5:
#         tags.append(("MF", "info"))
#
#     wu["tags"] = tags


# NOTE: status file is small (XXX kb) but avoid loading it on each request.
@cache.cached(timeout=5 * 60)
def get_collection():
    collection_path = os.path.join(app.root_path, COLLECTION_FN)
    if not os.path.exists(collection_path):
        return None

    with open(collection_path) as collection_file:
        return json.load(collection_file)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def main_page():
    collection = get_collection()

    collection = {k: v for k, v in list(collection.items())[:30]}

    # TODO ensure thumbnails start with static

    return render_template(
        "index.html",
        collection=collection,
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
