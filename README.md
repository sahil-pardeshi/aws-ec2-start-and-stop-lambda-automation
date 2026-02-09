# aws-ec2-start-and-stop-lambda-automation
This project focuses on the lambda automation which automates the start and stop operation of AWS- EC2
<br>
Prerequisites: 
<br>
 - AWS Account
<br>

## Step-by-Step Implementation Guide

Step 1: Tag Your EC2 Instances
For the script to find your instances, they must have a specific "label."
 1 Open the EC2 Console.
 <br>
 2 Select the instances you want to automate.
 <br>
 3 Go to Tags -> Manage Tags.
 <br>
   Add a new tag:
   <br>
   - Key: Auto-Scheduler
     <br>
   - Value: True
   <br>
   Click Save.

Step 2: Create the IAM Execution Role
<br>
Lambda needs permission to "talk" to your EC2 instances.
<br>
 1 Go to the IAM Console -> Roles -> Create Role.
 <br>
 2 Select Lambda as the trusted entity.
 <br>
 3 Click Create Policy and paste this JSON in the JSON tab:
<br>
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
<br>
Step 3: Create the Lambda Function
<br>
 1 Go to AWS Lambda -> Create Function.
 <br>
 2 Runtime: Python 3.12.
 <br>
 3 Permissions: Select the IAM role you just created.
 <br>
 4 Paste the Automated Tag-Based Script below into the lambda_function.py editor.
 <br>
   ###Lambda Function Setup
   <br>
  Create a function using Python 3.12 and paste the following code:
  ```
   import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Filter for instances with the specific tag
    filters = [{'Name': 'tag:Auto-Scheduler', 'Values': ['True']}]
    
    # Discovery: Find the IDs of the tagged instances
    response = ec2.describe_instances(Filters=filters)
    instance_ids = [i['InstanceId'] for r in response['Reservations'] for i in r['Instances']]

    if not instance_ids:
        print("No tagged instances found.")
        return

    # Action: Determine whether to Start or Stop
    action = event.get('action')
    if action == 'start':
        ec2.start_instances(InstanceIds=instance_ids)
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=instance_ids)
        
    print(f"Successfully executed {action} for: {instance_ids}")
```

 5 Click Deploy.
<br>
Step 4: Automate with EventBridge (The Scheduler)
<br>
 1 Go to Amazon EventBridge -> Schedules.
 <br>
 2 Create a "Stop" schedule (e.g., 8 PM Daily).
 <br>
 3 Target: Select your Lambda function.
 <br>
 4 Input: Under "Constant JSON," enter: `{"action": "stop"}`.
 <br>
 5 Repeat for a "Start" schedule with the input: `{"action": "start"}`.
 <br>

Step 5 Testing.
<br>
 1 Navigate to the Test tab in your Lambda function.
 <br>
 2 Create a new test event with:
 <br>
   ` { "action": "stop" } `
   <br>
 3 Execute the test and verify the Execution Result and CloudWatch Logs.
<br>
 ### Advantage of this automation 
 <br>
   Cost Benefits:
   <br>
     By stopping a single t3.medium instance for 12 hours daily, you can save approximately 50% on that resource's monthly compute costs.
     <br>
