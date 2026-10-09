"""Builds plan.html, the step-by-step Google Ads build guide, from guide.json (written by build-search.py)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "guide.json")))
tpl = open(os.path.join(HERE, "plan.template.html")).read()
open(os.path.join(HERE, "plan.html"), "w").write(tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)))
print("wrote plan.html", os.path.getsize(os.path.join(HERE, "plan.html")) // 1024, "KB")
