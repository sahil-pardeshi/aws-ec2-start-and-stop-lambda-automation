# aws-ec2-start-and-stop-lambda-automation
This project focuses on the lambda automation which automates the start and stop operation of AWS- EC2
Prerequisites: AWS Account, Python 3.11

## Step-by-Step Implementation Guide

Step 1: Tag Your EC2 Instances
For the script to find your instances, they must have a specific "label."
 1 Open the EC2 Console.
 2 Select the instances you want to automate.
 3 Go to Tags -> Manage Tags.
   Add a new tag:
   - Key: Auto-Scheduler
   - Value: True
   Click Save.

Step 2: Create the IAM Execution Role
Lambda needs permission to "talk" to your EC2 instances.
 1 Go to the IAM Console -> Roles -> Create Role.
 2 Select Lambda as the trusted entity.
 3 Click Create Policy and paste this JSON in the JSON tab:

### Configure the IAM Policy
Copy the following JSON and save it as `iam_policy.json` to give Lambda the required permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StartInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "logs:CreateLogGroup",
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```
 4 Name the policy `EC2StartStopPolicy` and attach it to your role.

Step 3: Create the Lambda Function
 1 Go to AWS Lambda -> Create Function.
 2 Runtime: Python 3.x.
 3 Permissions: Select the IAM role you just created.
 4 Paste the Automated Tag-Based Script we discussed into the lambda_function.py editor.
 5 Click Deploy.

Step 4: Automate with EventBridge (The Scheduler)
 1 Go to Amazon EventBridge -> Schedules.
 2 Create a "Stop" schedule (e.g., 8 PM Daily).
 3 Target: Select your Lambda function.
 4 Input: Under "Constant JSON," enter: `{"action": "stop"}`.
 5 Repeat for a "Start" schedule with the input: `{"action": "start"}`.
