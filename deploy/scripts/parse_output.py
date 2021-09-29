import json
import logging
import os

from github import Github
from pytablewriter import MarkdownTableWriter


def make_comment(commit, resource_counts):
    tables = []
    for k, v in resource_counts.items():
        if resource_counts[k]['delta'] > 0:
            resource_counts[k]['delta'] = f"+{resource_counts[k]['delta']}"
        if not isinstance(resource_counts[k]['delta-percent'], str):
            resource_counts[k]['delta-percent'] = f"{str(resource_counts[k]['delta-percent'] * 100)}%"
        tables.append(
            MarkdownTableWriter(
                table_name=f"Resource Counts",
                headers=['policy', 'new', 'original', 'delta', 'delta percentage'],
                value_matrix=[
                    [
                        k,
                        resource_counts[k]['new'],
                        resource_counts[k]['original'],
                        resource_counts[k]['delta'],
                        resource_counts[k]['delta-percent'],
                    ]
                ]
            ).dumps()
        )

    report = "\n".join(tables)
    commit.create_comment(
        body=report
    )
    return


def make_status(commit, resource_counts):
    status = "success"
    description = "Resource Check Threshold"

    with open('/tmp/new_policies.json') as f:
        new_policies = json.load(f)

    failed = 0

    for k, v in resource_counts.items():
        if k in new_policies["new"]:
            continue
        if v['delta'] >= os.environ['RESOURCE_THRESHOLD'] or v['delta-percent'] > os.environ['RESOURCE_THRESHOLD_PERCENT']:
            status = "failure"
            failed += 1

    if failed > 0:
        description = "Found {failed} policies over resource threshold limits"

    commit.create_status(
        state=status,
        description=description,
        context="cloud-custodian/resource-threshold"
    )
    pass


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
    if resource_counts[k]['original'] == 0:
        resource_counts[k]['delta-percent'] = "infinity"
    else:
        resource_counts[k]['delta'] = v['new']/v['original']

log.info(json.dumps(resource_counts, indent=2))

gh = Github(
    base_url=os.environ["GITHUB_API_URL"],
    login_or_token=os.environ["GITHUB_TOKEN"]
)
repo = gh.get_repo(full_name_or_id=os.environ["GITHUB_REPO"])
commit = repo.get_commit(sha=os.environ["CODEBUILD_RESOLVED_SOURCE_VERSION"])
make_comment(commit, resource_counts)
make_status(commit, resource_counts)
