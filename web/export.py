#!/usr/bin/env python
# ./manage.py shell < export.py
import codecs
import json
import re

from openeats.recipe.models import Recipe


AUTHORS = ["agil", "teresa", "escabechada"]
OUTPUT_FILE = "recipes.json"
CLEAN_HTML = re.compile("<.*?>")


def format_ing(ing):
    return (
        "%s %s - %s" % (ing.quantity, ing.measurement, ing.title)
        if ing.measurement
        else "%s - %s" % (ing.quantity, ing.title)
    )


def clean_directions(directions):
    s = (
        directions.replace("<p>", "")
        .replace("</p>\r\n", "\n")
        .replace("</p>", "\n")
        .replace("\r\n", "\n")
        .replace("<strong>", "__")
        .replace("</strong>", "__")
        .replace("<br />", "")
        .encode("utf-8")
        .replace("&aacute;", "á")
        .replace("&eacute;", "é")
        .replace("&iacute;", "í")
        .replace("&oacute;", "ó")
        .replace("&uacute;", "ú")
        .replace("&deg;", "°")
        .replace("&nbsp;", "")
    )
    return re.sub(CLEAN_HTML, "", s)


def create_recipe(recipe):
    ings = recipe.ingredients.all()
    new_recipe = {
        "author": str(recipe.author),
        "title": recipe.title,
        "photo": str(recipe.photo).decode("utf-8"),
        "ingredients": [format_ing(ing) for ing in ings],
        # html: remove <p>
        "directions": clean_directions(recipe.directions).decode("utf-8"),
    }
    return new_recipe


all_recipes = Recipe.objects.order_by("-pub_date")

recipe_list = filter(lambda r: str(r.author) in AUTHORS, all_recipes)

new_recipes = [create_recipe(recipe) for recipe in recipe_list]

with codecs.open(OUTPUT_FILE, "w", "utf-8") as f:
    json.dump(new_recipes, f, ensure_ascii=False, indent=4)
