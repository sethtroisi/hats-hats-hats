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
import datetime

from collections import defaultdict

from flask import Flask
from flask import render_template, send_from_directory
from flask_caching import Cache


print("Setting up Hats controller")

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


COLLECTION_FN = "HatsV1.json"

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

    #collection = {k: v for k, v in list(collection.items())[:30]}

    # TODO ensure thumbnails start with static

    last_update = datetime.datetime.fromtimestamp(
            os.path.getmtime(os.path.join(app.root_path, COLLECTION_FN)))

    return render_template(
        "index.html",
        collection=collection,
        name="Brenda's Bonnets",
        count_tags=sum(len(v["tags"]) for v in collection.values()),
        last_update=last_update,
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
