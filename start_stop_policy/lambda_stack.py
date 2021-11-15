from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    core as cdk
)


class LambdaStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        publish_logs_to_cloudwatch = iam.ManagedPolicy(self, 'PublishLogsPolicy',
                                                       managed_policy_name='-'.join(
                                                           [construct_id, 'publish logs policy'.replace(' ', '-')]
                                                       ),
                                                       description='Policy to operate EC2 instances',
                                                       statements=[
                                                           iam.PolicyStatement(
                                                               sid='AllowPublishLogsToCloudwatch',
                                                               actions=[
                                                                   'logs:CreateLogGroup',
                                                                   'logs:CreateLogStream',
                                                                   'logs:PutLogEvents'
                                                               ],
                                                               resources=['arn:aws-cn:logs:*:*:*']
                                                           )
                                                       ]
                                                       )

        lambda_role = iam.Role(self, 'LambdaRole',
                               assumed_by=iam.ServicePrincipal('lambda.amazonaws.com.cn'),
                               description="IAM role for Lambda function",
                               managed_policies=[
                                   publish_logs_to_cloudwatch
                               ],
                               role_name='-'.join([construct_id, 'role'.replace(' ', '-')]),
                               )
        lambda_function = _lambda.Function(self, 'LambdaFunction',
                                           code=_lambda.Code.from_asset(path="./start_stop_policy/lambda"),
                                           handler="start_stop_policy.lambda_handler",
                                           runtime=_lambda.Runtime.PYTHON_3_8,
                                           memory_size=128,
                                           role=lambda_role,
                                           timeout=cdk.Duration.seconds(90)
                                           )
        lambda_function.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
