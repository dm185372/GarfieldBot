resource "aws_iam_role" "garfield_lambda" {
  name = "garfield-lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "garfield_ssm_read" {
  name        = "garfield-ssm-readonly"
  path        = "/"
  description = "Allows the GarfieldBot lambda function to read ssm parameters"

  policy = <<EOF
{
    "Statement": [
        {
            "Action": [
                "ssm:GetParameters",
                "ssm:GetParameter"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:ssm:*:*:parameter/*",
            "Sid": "VisualEditor0"
        },
        {
            "Action": "ssm:DescribeParameters",
            "Effect": "Allow",
            "Resource": "*",
            "Sid": "VisualEditor1"
        }
    ],
    "Version": "2012-10-17"
}
EOF
}

resource "aws_iam_role_policy_attachment" "garfield-attach" {
  for_each = toset([
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
    aws_iam_policy.garfield_ssm_read.arn
  ])
  role       = aws_iam_role.garfield_lambda.name
  policy_arn = each.value

  depends_on = [
    aws_iam_policy.garfield_ssm_read
  ]
}