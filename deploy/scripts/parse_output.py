import json
import logging
import os

from github import Github
from pytablewriter import MarkdownTableWriter


def get_delta_percent_string(delta, delta_percent):
    if isinstance(delta_percent, str):
        return delta_percent
    delta_percent = 100 * delta_percent
    percent_str = "{:.2f}%".format(delta_percent)
    if delta > 0:
        return f"+{percent_str}"
    if delta < 0:
        return f"-{percent_str}"
    return percent_str


def get_delta_string(delta):
    if delta > 0:
        return f"\\+{delta}"
    return str(delta)


def make_comment(commit, resource_counts):
    value_matrix = []
    account_value_matrix = []
    for k, v in resource_counts.items():
        resource_counts[k]['delta-percent'] = get_delta_percent_string(
            resource_counts[k]['delta'],
            resource_counts[k]['delta-percent']
        )
        resource_counts[k]['delta'] = get_delta_string(
            resource_counts[k]['delta']
        )
        value_matrix.append([
            k,
            resource_counts[k]["new"],
            resource_counts[k]["original"],
            resource_counts[k]["delta"],
            resource_counts[k]["delta-percent"],
        ])

        for account in v['accounts'].keys():
            for region in v['accounts'][account].keys():
                new = v['accounts'][account][region]['new']
                original = v['accounts'][account][region]['original']
                delta = get_delta_string(
                    v['accounts'][account][region]['delta']
                )
                delta_percent = get_delta_percent_string(
                    v['accounts'][account][region]['delta'],
                    v['accounts'][account][region]['delta-percent']
                )
                account_value_matrix.append(
                    [
                        account,
                        region,
                        k,
                        new,
                        original,
                        delta,
                        delta_percent
                    ]
                )

    all_table = MarkdownTableWriter(
        table_name="Resource Counts",
        headers=["policy", "new", "original", "delta", "delta percentage"],
        value_matrix=value_matrix
    ).dumps()
    account_table = MarkdownTableWriter(
        table_name="Account/Region Resource Counts",
        headers=["account", "region", "policy", "new", "original", "delta", "delta percentage"],
        value_matrix=account_value_matrix
    ).dumps()
    table_body = "<details>\n\n" + all_table + "\n\n" + account_table + "\n</details>"
    commit.create_comment(body=":tada: Your Policy Execution results:\n" + table_body)
    return


def make_status(commit, resource_counts):
    status = "success"
    description = "Resource Check Threshold"

    with open("/tmp/new_policies.json") as f:
        new_policies = json.load(f)

    failed = 0

    for k, v in resource_counts.items():
        # Skip new policies as they will more than likely have
        # more resources than the threshold
        if k in new_policies["new"]:
            continue
        if (
            v["delta"] >= int(os.environ["RESOURCE_THRESHOLD"])
            or v["delta-percent"] > int(os.environ["RESOURCE_THRESHOLD_PERCENT"])
        ):
            status = "failure"
            failed += 1

    if failed > 0:
        description = f"Found {failed} policies over resource threshold limits"

    commit.create_status(
        state=status,
        description=description,
        context="cloud-custodian/resource-threshold",
    )
    pass


def get_delta(resource_counts):
    for k, v in resource_counts.items():
        if "original" not in v:
            resource_counts[k]["original"] = 0
        if "new" not in v:
            resource_counts[k]["new"] = 0
        resource_counts[k]["delta"] = v["new"] - v["original"]
        if resource_counts[k]["original"] == 0:
            resource_counts[k]["delta-percent"] = "infinity"
        else:
            percentage = abs(v['original'] - v['new'])/v['original']
            resource_counts[k]["delta-percent"] = percentage
    return resource_counts


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("policystream:ParseOutput")

output_dir = os.environ["OUTPUT_DIR"]

resource_counts = dict()

for subdir in ["new", "original"]:
    for root, dirs, files in os.walk(output_dir + f"/{subdir}"):
        for name in files:
            if name != "resources.json":
                continue
            _, __, account, region, policy_name = root.split("/")
            with open(os.path.join(root, name)) as f:
                resources = json.load(f)
            log.info(
                f"found: {len(resources)} resources for policy:{policy_name} in run:{subdir} in account:{account} region:{region}"  # noqa
            )

            resource_counts.setdefault(policy_name, {})
            resource_counts[policy_name].setdefault(subdir, 0)
            resource_counts[policy_name].setdefault('accounts', {})
            resource_counts[policy_name]['accounts'].setdefault(account, {})
            resource_counts[policy_name]['accounts'][account].setdefault(region, {})
            resource_counts[policy_name]['accounts'][account][region].setdefault(subdir, 0)

            resource_counts[policy_name][subdir] += len(resources)
            resource_counts[policy_name]['accounts'][account][region][subdir] += len(resources)

get_delta(resource_counts)
for k, v in resource_counts.items():
    for account in v['accounts'].keys():
        get_delta(v['accounts'][account])

log.info(json.dumps(resource_counts, indent=2))

gh = Github(
    base_url=os.environ["GITHUB_API_URL"], login_or_token=os.environ["GITHUB_TOKEN"]
)
repo = gh.get_repo(full_name_or_id=os.environ["GITHUB_REPO"])
commit = repo.get_commit(sha=os.environ["CODEBUILD_RESOLVED_SOURCE_VERSION"])
make_status(commit, resource_counts)
make_comment(commit, resource_counts)
