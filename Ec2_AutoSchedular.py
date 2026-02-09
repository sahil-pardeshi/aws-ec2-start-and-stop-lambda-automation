import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Identify instances with the tag
    filters = [{'Name': 'tag:Auto-Scheduler', 'Values': ['True']}]
    
    # Get the list of Instance IDs
    instances = ec2.describe_instances(Filters=filters)
    ids = [i['InstanceId'] for r in instances['Reservations'] for i in r['Instances']]

    if not ids:
        return "No tagged instances found."

    # Decide to Start or Stop based on the 'action' sent by EventBridge
    action = event.get('action')
    if action == 'start':
        ec2.start_instances(InstanceIds=ids)
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=ids)
        
    return f"Successfully {action}ed instances: {ids}"
