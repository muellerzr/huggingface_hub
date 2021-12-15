# Copyright 2020 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

# import requests
from huggingface_hub.utils.tags import AttributeDictionary, GeneralTags


# DatasetTags,
# ModelTags,


class AttributeDictionaryCommonTest(unittest.TestCase):
    _attrdict = AttributeDictionary()


class AttributeDictionaryTest(AttributeDictionaryCommonTest):
    def test_adding_item(self):
        self._attrdict["itemA"] = 2
        self.assertEqual(self._attrdict.itemA, 2)
        self.assertEqual(self._attrdict["itemA"], 2)
        # We should be able to both set a property and a key
        self._attrdict.itemB = 3
        self.assertEqual(self._attrdict.itemB, 3)
        self.assertEqual(self._attrdict["itemB"], 3)

    def test_removing_item(self):
        self._attrdict["itemA"] = 2
        self._attrdict.itemB = 3
        delattr(self._attrdict, "itemA")
        with self.assertRaises(KeyError):
            _ = self._attrdict["itemA"]

        del self._attrdict["itemB"]
        with self.assertRaises(AttributeError):
            _ = self._attrdict.itemB

    def test_dir(self):
        # Since we subclass dict, dir should have everything
        # from dict and the atttributes
        _dict_keys = dir(dict) + [
            "__dict__",
            "__getattr__",
            "__module__",
            "__weakref__",
        ]
        self._attrdict["itemA"] = 2
        self._attrdict.itemB = 3
        _dict_keys += ["itemA", "itemB"]
        _dict_keys.sort()

        full_dir = dir(self._attrdict)
        full_dir.sort()
        self.assertEqual(full_dir, _dict_keys)

    def test_repr(self):
        self._attrdict["itemA"] = 2
        self._attrdict.itemB = 3
        repr_string = "Available Attributes:\n * itemA\n * itemB\n"
        self.assertEqual(repr_string, repr(self._attrdict))


class GeneralTagsCommonTest(unittest.TestCase):
    # Similar to the output from /api/***-tags-by-type
    # id = how we can search hfapi, such as `'id': 'languages:en'`
    # label = A human readable version assigned to everything, such as `"label":"en"`
    _tag_dictionary = {
        "languages": [
            {"id": "itemA", "label": "Item A"},
            {"id": "itemB", "label": "Item B"},
        ],
        "license": [
            {"id": "itemC", "label": "Item C"},
            {"id": "itemD", "label": "Item D"},
        ],
    }


class GeneralTagsTest(GeneralTagsCommonTest):
    def test_init(self):
        _tags = GeneralTags(self._tag_dictionary)
        self.assertTrue(all(hasattr(_tags, kind) for kind in ["languages", "license"]))
        languages = getattr(_tags, "languages")
        licenses = getattr(_tags, "license")
        # Ensure they have the right bits

        self.assertEqual(
            languages,
            AttributeDictionary({"ItemA": "itemA", "ItemB": "itemB"}),
        )
        self.assertEqual(
            licenses, AttributeDictionary({"ItemC": "itemC", "ItemD": "itemD"})
        )

    def test_filter(self):
        _tags = GeneralTags(self._tag_dictionary, keys=["license"])
        self.assertTrue(hasattr(_tags, "license"))
        with self.assertRaises(AttributeError):
            _ = getattr(_tags, "languages")
        self.assertEqual(
            _tags.license, AttributeDictionary({"ItemC": "itemC", "ItemD": "itemD"})
        )