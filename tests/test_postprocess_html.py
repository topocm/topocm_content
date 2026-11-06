"""Legacy links must follow the builder, including collisions and preview prefixes."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

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

    def test_export_copies_dynamic_library_and_license(self):
        with tempfile.TemporaryDirectory() as tmp:
            build = Path(tmp)
            (build / "index.html").write_text("<html><head></head><body>Course</body></html>")
            (build / "config.json").write_text(json.dumps({"projects": [{"index": "landing"}]}))
            with patch.object(postprocess, "BUILD_HTML", build), patch.dict(
                postprocess.os.environ, {"BASE_URL": "/preview"}
            ):
                postprocess.process_html()
            bundle = build / "_static" / "vendor" / postprocess.PLOTLY_BUNDLE
            self.assertTrue(bundle.is_file())
            self.assertTrue((bundle.parent / "plotly-LICENSE").is_file())
            self.assertIn(f"/preview/_static/vendor/{bundle.name}", (build / "index.html").read_text())

    def test_analytics_is_prefix_aware_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "index.html"
            page.write_text("<html><head></head><body>Course</body></html>")
            self.assertTrue(postprocess.inject_scripts(page, "/branch_test/"))
            self.assertFalse(postprocess.inject_scripts(page, "/branch_test/"))
            self.assertEqual(page.read_text().count('src="/branch_test/matomo.js"'), 1)
            self.assertEqual(page.read_text().count(postprocess.plotly_config("/branch_test/")), 1)
            self.assertLess(
                page.read_text().index(postprocess.plotly_config("/branch_test/")),
                page.read_text().index("</head>"),
            )
            self.assertNotIn("cdn.plot.ly", page.read_text())
            self.assertNotIn('<script src="https://cdn.jsdelivr.net', page.read_text())
            self.assertIn('/branch_test/_static/vendor/plotly-4.2.0.min.js', page.read_text())
            page.write_text('<meta http-equiv="refresh" content="0; url=/">')
            self.assertFalse(postprocess.inject_scripts(page))


if __name__ == "__main__":
    unittest.main()
