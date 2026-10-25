"""Legacy links must follow the builder, including collisions and preview prefixes."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "postprocess", Path(__file__).parents[1] / "scripts/postprocess_html.py"
)
postprocess = importlib.util.module_from_spec(spec)
spec.loader.exec_module(postprocess)


class StaticExportTests(unittest.TestCase):
    def test_redirects_follow_emitted_slugs_and_base_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            build = Path(tmp)
            records = {
                "config": {"projects": [{"index": "landing"}]},
                "landing": {"location": "/landing.md", "slug": "landing"},
                "w1.d": {"location": "/w1/0d.md", "slug": "w1.d"},
                "w1.d-1": {"location": "/w1/1D.md", "slug": "w1.d-1"},
                "public": ["an-unrelated-asset"],
            }
            for name, value in records.items():
                (build / f"{name}.json").write_text(json.dumps(value))
            self.assertEqual(postprocess.write_redirects(build, "/branch_test/"), 3)
            for source, target in [
                ("landing", "/branch_test/"),
                ("w1/0d", "/branch_test/w1/d/"),
                ("w1/1D", "/branch_test/w1/d-1/"),
            ]:
                self.assertIn(  # codespell:ignore assertin
                    f"url={target}", (build / f"{source}.html").read_text()
                )
            self.assertEqual(postprocess.write_redirects(build, "/branch_test/"), 0)

    def test_analytics_is_prefix_aware_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "index.html"
            page.write_text("<html><head></head><body>Course</body></html>")
            self.assertTrue(postprocess.inject_scripts(page, "/branch_test/"))
            self.assertFalse(postprocess.inject_scripts(page, "/branch_test/"))
            self.assertEqual(page.read_text().count('src="/branch_test/matomo.js"'), 1)
            self.assertEqual(page.read_text().count(postprocess.MATHJAX_SNIPPET), 1)
            self.assertLess(
                page.read_text().index(postprocess.MATHJAX_SNIPPET),
                page.read_text().index("</head>"),
            )
            page.write_text('<meta http-equiv="refresh" content="0; url=/">')
            self.assertFalse(postprocess.inject_scripts(page))


if __name__ == "__main__":
    unittest.main()
