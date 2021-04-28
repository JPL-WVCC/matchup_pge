output "counter" {
  value = local.counter
}

output "dataset_bucket" {
  value = local.dataset_bucket
}

output "code_bucket" {
  value = local.code_bucket
}

output "isl_bucket" {
  value = local.isl_bucket
}

output "triage_bucket" {
  value = local.triage_bucket
}

output "lts_bucket" {
  value = local.lts_bucket
}

output "osl_bucket" {
  value = local.osl_bucket
}

output "key_name" {
  value = local.key_name
}

output "mozart" {
  value = aws_instance.mozart
}

output "mozart_pvt_ip" {
  value = aws_instance.mozart.private_ip
}

output "mozart_pub_ip" {
  value = aws_instance.mozart.private_ip
}

output "metrics" {
  value = aws_instance.metrics
}

output "metrics_pvt_ip" {
  value = aws_instance.metrics.private_ip
}

output "metrics_pub_ip" {
  value = aws_instance.metrics.private_ip
}

output "grq" {
  value = aws_instance.grq
}

output "grq_pvt_ip" {
  value = aws_instance.grq.private_ip
}

output "grq_pub_ip" {
  value = aws_instance.grq.private_ip
}

output "factotum" {
  value = aws_instance.factotum
}

output "factotum_pvt_ip" {
  value = aws_instance.factotum.private_ip
}

output "factotum_pub_ip" {
  value = aws_instance.factotum.private_ip
}

output "daac_proxy_cnm_r_sns_count" {
  value = local.daac_proxy_cnm_r_sns_count
}

output "e_misfire_metric_alarm_name" {
  value = local.e_misfire_metric_alarm_name
}

output "aws_cloudwatch_event_rule_l0a_timer" {
  value = aws_cloudwatch_event_rule.l0a_timer
}
