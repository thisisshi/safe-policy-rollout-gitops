import json
import logging
import os

from github import Github

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("policystream:ParseOutput")

output_dir = os.environ["OUTPUT_DIR"]

resource_counts = dict()

for subdir in ["new", "original"]:
    for root, dirs, files in os.walk(output_dir + f"/{subdir}"):
        for name in files:
            if name != "resources.json":
                continue
            policy_name = root.rsplit("/", 1)[-1]
            with open(os.path.join(root, name)) as f:
                resources = json.load(f)
            log.info(
                f"found: {len(resources)} resources for policy:{policy_name} in run:{subdir}"
            )
            resource_counts.setdefault(policy_name, {})
            resource_counts[policy_name][subdir] = len(resources)

for k, v in resource_counts.items():
    if "original" not in v:
        resource_counts[k]["original"] = 0
    if "new" not in v:
        resource_counts[k]["new"] = 0
    resource_counts[k]["delta"] = v["new"] - v["original"]

log.info(json.dumps(resource_counts, indent=2))

gh = Github(
    # base_url=os.environ["GITHUB_API_URL"],
    login_or_token=os.environ["GITHUB_TOKEN"]
)
repo = gh.get_repo(full_name_or_id=os.environ["GITHUB_REPO"])
commit = repo.get_commit(sha=os.environ["CODEBUILD_RESOLVED_SOURCE_VERSION"])
commit.create_status(
    context="c7n/ci",
    state="success",
    description="C7N CI Completed"
)
