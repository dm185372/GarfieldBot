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

#user for CI/CD flow
resource "aws_iam_user" "garfield_uploader" {
  name = "garfield-uploader"
  path = "/"

  tags = {
    Name = "garfield-uploader"
  }
}

resource "aws_iam_policy" "garfield_uploader" {
  name        = "garfield-uploader"
  path        = "/"
  description = "Allows read and write access to discord-garfield-code bucket"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListAllMyBuckets"
            ],
            "Resource": "arn:aws:s3:::*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::discord-garfield-code"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:GetBucketLocation",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::discord-garfield-code",
                "arn:aws:s3:::discord-garfield-code/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:ListFunctions",
                "lambda:ListLayerVersions",
                "lambda:ListLayers"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:UpdateFunctionCode",
                "lambda:ListProvisionedConcurrencyConfigs",
                "lambda:InvokeFunction",
                "lambda:GetFunction",
                "lambda:GetFunctionEventInvokeConfig",
                "lambda:ListAliases",
                "lambda:UpdateFunctionConfiguration",
                "lambda:GetFunctionConfiguration",
                "lambda:PublishVersion",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::*",
                "${aws_lambda_function.garfield_lambda.arn}"
            ]
        }
    ]
}
EOF

  tags = {
    Name = "garfield-uploader"
  }
}

resource "aws_iam_user_policy_attachment" "garfield_uploader_attach" {
  user       = aws_iam_user.garfield_uploader.name
  policy_arn = aws_iam_policy.garfield_uploader.arn
}
