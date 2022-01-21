resource "aws_cloudwatch_event_rule" "garfield_daily" {
  name                = "daily"
  description         = "Fires at 9 AM EST each day"
  schedule_expression = "cron(0 9 * * ? *)"
}

resource "aws_cloudwatch_event_target" "garfield_target" {
  rule      = aws_cloudwatch_event_rule.garfield_daily.name
  target_id = "lambda"
  arn       = aws_lambda_function.garfield_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.garfield_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.garfield_daily.arn
}