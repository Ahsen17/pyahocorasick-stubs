"""Integration checks against the real C extension, not a mock."""

import ast
import importlib.metadata
import pickle
import tempfile
import unittest
from pathlib import Path

import ahocorasick as aho


class RuntimeTests(unittest.TestCase):
    def test_public_api_inventory(self):
        self.assertEqual(importlib.metadata.version("pyahocorasick"), "2.3.1")
        source = Path(__file__).parents[1] / "src/ahocorasick-stubs/__init__.pyi"
        tree = ast.parse(source.read_text())
        declared = {
            node.name
            for node in tree.body
            if isinstance(node, (ast.ClassDef, ast.FunctionDef))
        }
        declared.update(
            node.target.id
            for node in tree.body
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
        )
        exported = {name for name in dir(aho) if not name.startswith("_")}
        self.assertEqual(
            exported, {name for name in declared if not name.startswith("_")}
        )
        cls = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "Automaton"
        )
        methods = {node.name for node in cls.body if isinstance(node, ast.FunctionDef)}
        members = {name for name in dir(aho.Automaton) if not name.startswith("_")}
        self.assertEqual(
            members, {name for name in methods if not name.startswith("_")}
        )
        self.assertTrue(
            {"__iter__", "__contains__", "__len__", "__sizeof__", "__reduce__"}
            <= methods
        )

    def test_trie_and_dictionary_api(self):
        a = aho.Automaton()
        self.assertEqual(a.kind, aho.EMPTY)
        self.assertEqual(a.store, aho.STORE_ANY)
        with self.assertRaises(ValueError):
            a.add_word("cat")
        self.assertTrue(a.add_word("cat", "cat"))
        self.assertFalse(a.add_word("cat", "CAT"))
        a.add_word("cats", "cats")
        self.assertTrue(a.exists("cat"))
        self.assertTrue("cat" in a)
        self.assertTrue(a.match("ca"))
        self.assertFalse(a.exists("ca"))
        self.assertEqual(a.longest_prefix("catsup"), 4)
        self.assertEqual(a.get("cat"), "CAT")
        self.assertIsNone(a.get("missing", None))
        with self.assertRaises(KeyError):
            a.get("missing")
        self.assertEqual(set(a.keys("cat")), {"cat", "cats"})
        self.assertEqual(list(a.keys("ca?", "?")), ["cat"])
        self.assertEqual(
            set(a.keys("ca?", "?", aho.MATCH_AT_LEAST_PREFIX)), {"cat", "cats"}
        )
        self.assertEqual(set(a.values()), {"CAT", "cats"})
        self.assertEqual(dict(a.items()), {"cat": "CAT", "cats": "cats"})
        self.assertEqual(set(a), {"cat", "cats"})
        self.assertEqual(a.pop("cat"), "CAT")
        self.assertFalse(a.remove_word("cat"))
        self.assertTrue(a.remove_word("cats"))
        a.clear()
        self.assertEqual(len(a), 0)

    def test_search_and_streaming_iterators(self):
        a = aho.Automaton()
        for word in ("he", "her", "here"):
            a.add_word(word, word)
        a.make_automaton()
        self.assertEqual(a.kind, aho.AHOCORASICK)
        hits = list(a.iter(string="here", start=0, end=4))
        self.assertEqual(hits, [(1, "he"), (2, "her"), (3, "here")])
        self.assertEqual(list(a.iter_long("here")), [(3, "here")])
        self.assertEqual(list(a.iter("h e", ignore_white_space=True)), [(2, "he")])
        collected = []
        a.find_all("here", lambda end, value: collected.append((end, value)))
        self.assertEqual(collected, hits)
        for factory in (a.iter, a.iter_long):
            iterator = factory("")
            self.assertIs(iter(iterator), iterator)
            self.assertTrue(hasattr(iterator, "set"))
            iterator.set("here", True)
            self.assertTrue(list(iterator))
        iterator = a.iter("h")
        self.assertEqual(list(iterator), [])
        iterator.set("e")
        self.assertEqual(list(iterator), [(1, "he")])

    def test_storage_and_sequence_modes(self):
        integers = aho.Automaton(aho.STORE_INTS)
        integers.add_word("x")
        self.assertIsInstance(integers.get("x"), int)
        integers.add_word("y", 42)
        self.assertEqual(integers.get("y"), 42)
        lengths = aho.Automaton(aho.STORE_LENGTH)
        lengths.add_word("abc")
        self.assertEqual(lengths.get("abc"), 3)
        # STORE_LENGTH ignores an explicitly supplied value in 2.3.1.
        lengths.add_word("xy", 99)
        self.assertEqual(lengths.get("xy"), 2)
        for store in (aho.STORE_ANY, aho.STORE_INTS, aho.STORE_LENGTH):
            a = aho.Automaton(store, aho.KEY_SEQUENCE)
            if store == aho.STORE_ANY:
                a.add_word((97, 98), "ab")
            else:
                a.add_word((97, 98))
            a.make_automaton()
            self.assertEqual(next(a.iter((0, 97, 98)))[0], 2)
            self.assertEqual(list(a.keys()), ["ab"])
            self.assertEqual(list(a.keys("a")), ["ab"])
            with self.assertRaises(TypeError):
                list(a.keys((97,)))

    def test_stats_dump_and_readonly_properties(self):
        a = aho.Automaton()
        self.assertIsNone(a.dump())
        a.add_word("a", 1)
        a.make_automaton()
        stats = a.get_stats()
        self.assertEqual(
            set(stats),
            {
                "nodes_count",
                "words_count",
                "longest_word",
                "links_count",
                "sizeof_node",
                "total_size",
            },
        )
        self.assertTrue(all(isinstance(v, int) for v in stats.values()))
        nodes, edges, failure = a.dump()
        self.assertTrue(nodes)
        self.assertTrue(failure)
        self.assertIsInstance(edges[0][1], bytes)
        self.assertIsInstance(a.__sizeof__(), int)
        for name in ("kind", "store"):
            with self.assertRaises(AttributeError):
                setattr(a, name, 0)

    def test_save_load_and_pickle(self):
        with tempfile.TemporaryDirectory() as directory:
            for store in (aho.STORE_ANY, aho.STORE_INTS, aho.STORE_LENGTH):
                a = aho.Automaton(store)
                if store == aho.STORE_ANY:
                    a.add_word("a", "a")
                else:
                    a.add_word("a")
                a.make_automaton()
                path = str(Path(directory) / f"{store}.bin")
                if store == aho.STORE_ANY:
                    a.save(path, pickle.dumps)
                else:
                    a.save(path)
                restored = aho.load(path, pickle.loads)
                self.assertEqual(restored.get("a"), a.get("a"))
                self.assertEqual(pickle.loads(pickle.dumps(a)).get("a"), a.get("a"))
                constructor, arguments = a.__reduce__()
                self.assertEqual(constructor(*arguments).get("a"), a.get("a"))
        self.assertEqual(aho.Automaton().__reduce__()[1], ())

    def test_keyword_and_path_conventions(self):
        a = aho.Automaton()
        a.add_word("a", "a")
        a.make_automaton()
        with self.assertRaises(TypeError):
            a.get("missing", default=None)
        with self.assertRaises(TypeError):
            a.keys(prefix="a")
        with self.assertRaises(TypeError):
            a.iter_long(string="a")
        with self.assertRaises(TypeError):
            a.iter("a").set("a", reset=True)
        # Constructor keywords do not configure the runtime mode.
        self.assertEqual(aho.Automaton(value_type=aho.STORE_INTS).store, aho.STORE_ANY)
        with self.assertRaises(TypeError):
            a.save(Path("unused.bin"), pickle.dumps)


if __name__ == "__main__":
    unittest.main(verbosity=2)
