"""
Resolve the original version of the changed policy from policystream
"""

import os
import logging
import json
import yaml

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("policystream:ResolveOriginal")


with open("/tmp/policystream.yaml", "r") as f:
    policies = yaml.safe_load(f)

changed_policy_names = [p["name"] for p in policies["policies"]]
log.info(f"Changed policy names: {changed_policy_names}")

base_dir = os.environ["POLICY_DIR"]

original_policies = {"policies": []}
original_policy_names = []

for root, dirs, files in os.walk(base_dir):
    for name in files:
        with open(os.path.join(root, name)) as f:
            log.info(os.path.join(root, name))
            # skip non yaml/json files
            if (
                not name.endswith("yaml")
                and not name.endswith("yml")
                and not name.endswith("json")
            ):
                continue
            try:
                policies = yaml.safe_load(f)
            except Exception as e:
                log.error(e)
                continue
            if not policies:
                continue
            if policies.get("policies"):
                policy_name_map = {p["name"]: p for p in policies["policies"]}
                changed = set(changed_policy_names).intersection(
                    set(policy_name_map.keys())
                )
                original_policy_names.extend(list(changed))
                for c in changed:
                    original_policies["policies"].append(policy_name_map[c])

log.info(f"Original Policies: {json.dumps(original_policies, indent=2)}")
new_policies = list(set(changed_policy_names).difference(set(original_policy_names)))
log.info(f"New Policies: {new_policies}")

with open("/tmp/policystream-original.yaml", "w+") as f:
    yaml.dump(original_policies, f)

with open("/tmp/new_policies.json", "w+") as f:
    json.dump({"new": new_policies}, f)
