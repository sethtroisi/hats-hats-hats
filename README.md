## Hats Hats Hats

A frontend for displaying my mothers hat collection

```shell
pip install -r requirements.txt

# Setup
git clone https://github.com/sethtroisi/hats-hats-hats
cd hats-hats-hats

FLASK_APP=app.py FLASK_ENV=development flask run
```

A local server should now be running at http://localhost:5090

### TODO

* [ ] Clear button
* [ ] Show multiple images
* [ ] image size doesn't always work with rotation
* [x] Cards
* [x] Better filtering
* [x] CSS
* [x] Generic hat

##

Filter hats to directories

```
python tools/group_hats.py
```

Regenerate metadata

```
python tools/process_pictures_to_cards.py
```
