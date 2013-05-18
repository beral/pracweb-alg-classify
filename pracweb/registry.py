# -*- coding: utf-8 -*-

import logging

# Registries
classifiers = {}
correctors = {}


def make_category(registry, registry_name):
    def category(name):
        def add_to_category(func):
            logging.debug("Adding %r to %s", name, registry_name)
            registry[name] = func
            func.__prac__ = {
                'category': registry_name,
                'name': name,
            }
            return func
        return add_to_category
    return category


classifier = make_category(classifiers, 'classifiers')
corrector = make_category(correctors, 'correctors')
