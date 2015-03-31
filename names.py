#!/usr/bin/python

from random import randint

nazis = [
    "Heinrich Himmler",
    "Adolf Hitler",
    "Reinhard Heydrich",
    "Joseph Mengele",
    "Adolf Eichmann",
    "Odilo Globocnik",
    "Oskar Dirlewanger",
    "Friedrich Jeckeln",
    "Ernst Kaltenbrunner",
    "Josef Kramer",
    "Paul Blobel",
    "Franz Stangl",
    "Joseph Goebbels",
    "Ilse Koch",
    "Hermann Goering",
]

nice = [
    "Adoring",
    "Dreamy",
    "Elegant",
    "Happy",
    "Modest",
    "Nostalgic",
    "Romantic",
    "Friednly",
    "Admirable",
    "Amiable",
    "Gentle",
    "Helpful",
    "Kind",
    "Polite",
    "Well-mannered",
    "Simpatico",
]


def generate_name():
    global nice
    global nazis

    name = nice[randint(0, len(nice)-1)] + " " + nazis[randint(0, len(nazis)-1)]
    return name.replace(' ', '_')
