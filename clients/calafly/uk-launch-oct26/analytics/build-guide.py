"""Builds guide.html (GA4 + Microsoft Clarity setup guide) from guide.template.html with the shared guide styling."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "guide.template.html")).read()
style = open(os.path.join(HERE, "..", "meta-ads", "_style.html")).read()
open(os.path.join(HERE, "guide.html"), "w").write(tpl.replace("<!--STYLE-->", style))
print("wrote guide.html")
