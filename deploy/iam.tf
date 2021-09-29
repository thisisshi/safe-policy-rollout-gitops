resource "aws_iam_role" "codebuild_executor" {
  name = "C7NPolicyCIRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "codebuild.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "codebuild_executor" {
  role       = aws_iam_role.codebuild_executor.name
  policy_arn = var.ci_policy_arn
}
