import Task_3.run_cases as rc
import Task_3.scanner as scanner

for module, name, value in rc.PATCHES:
    setattr(module, name, value)
rc.quality.evaluate = rc.fake_evaluate
rc.pipeline.health_check = rc.fake_health

rc.fresh()
rc.put("return_shipping.txt", rc.GOOD)


def show(label):
    m = scanner.load_manifest()
    print(label, "| active:", m["active_version"], "| previous:", m.get("previous_version"),
          "| files:", len(m["files"]), "| pending:", m.get("pending"))


show("1 start           ")
scanner.ensure_baseline()
show("2 after baseline  ")
r = rc.pipeline.run_update()
show("3 after run_update")
print("state:", r["state"], "| version folders:", sorted(p.name for p in rc.VERSIONS.iterdir()))