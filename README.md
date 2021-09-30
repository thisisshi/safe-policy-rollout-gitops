# Safe Policy Rollouts with GitOps
KubeCon 2021 - Governance as Code Day with Cloud Custodian hosted by Stacklet

![Example](example.png)

## Installation

Before starting, create a Github personal access token and keep it handy while you
create the rest of the resources.

Then, create a c7n-org `accounts.yaml` file. This file will determine what accounts and
regions your policies will run against. For more details on how to create an `accounts.yaml`
file, click [here](https://docs.aws.amazon.com/codebuild/latest/userguide/access-tokens.html).

Example `accounts.yaml`:

```yaml
accounts:
  - name: "Sandbox"
    account_id: "123456789012"
    role: "arn:aws:iam::123456789012:role/C7NPolicyCIRole"
    regions:
      - "us-east-1"
      - "us-west-2"
  - name: "Sandbox2"
    account_id: "98765432101"
    role: "arn:aws:iam::98765432101:role/C7NPolicyCIRole"
    regions:
      - "us-east-1"
      - "us-west-2"
```

To install, reference the projects/ci directory. There you will see an example `main.tf`
that you can use to create your own c7n ci CodeBuild Job.

```bash
cd projects/ci
terraform init
cp settings.tfvars.example settings.tfvars
# Edit the settings.tfvars file, all vars can be found in deploy/vars.tf
terraform apply -var-file=settings.tfvars
```

Once this has completed, navigate to the CodeBuild console in AWS and set up the OAuth
connection between AWS and Github. This is necessary to enable Webhooks to trigger CodeBuild
jobs when Pull Requests are created/updated.

To set up OAuth:

1. Navigate to the CodeBuild console
2. Click on your Project
3. Click Edit
4. Click Source
5. Click Connect to GitHub
6. Follow the Steps on the pop-up window
7. Click Update Source

This project uses [c7n-policystream](https://cloudcustodian.io/docs/tools/c7n-policystream.html)
to detect changes between your commit and the base branch, as defined by `base_branch`. The
CodeBuild job then runs the changed policies as well as the original ones from `base_branch`
and compares the results of the two. You can also specify thresholds for the job to fail on,
with values for both total number of resources (e.g. if the delta is 5 resources for a given
policy, fail) or for a percentage (e.g. if the delta in percentage is greater than 50% fail).
