data "aws_s3_bucket_object" "garfield_zip" {
  bucket = aws_s3_bucket.garfield_bucket.id
  key    = "garfieldbot.zip"
}

resource "aws_lambda_function" "garfield_lambda" {
  s3_bucket         = var.bucket_name
  s3_key            = data.aws_s3_bucket_object.garfield_zip.key
  s3_object_version = data.aws_s3_bucket_object.garfield_zip.version_id
  function_name     = "GarfieldBot"
  description       = "Will send a random Garfield gif to Discord every day at 9 AM EST"
  role              = aws_iam_role.garfield_lambda.arn
  handler           = "garfieldbot.lambda_handler"
  runtime           = "python3.8"
  timeout           = "30"
}