_“This project repository is created in partial fulfillment of the requirements for the Big Data Analytics course offered by the Master of Science in Business Analytics program at the Carlson School of Management, University of Minnesota.”_

# Team 7 Analyse Terms and Conditions of A Scanned Document using Textract

## Team Members
* Wen-Ling Ku
* Amlendu Kumawat
* Maria Moy
* Raghuram Sirigiri
* Aditya Tomar
* Kexin Yang

## Setup FrontEnd
The front end of the application contains the interface used to intrecta with the application. The application is developed using python flask and the same can be found in FrontEnd Folder. Use the main.py to start the application. Get security keys from AWS S3 and replace thme in the application.

## AWS LAMBDA Backend
The AWS Lambda conatins the code of LAMBDA functions.

Steps to implement the demo:

1. First we create an S3 bucket where we create the following folders:
            - Files: Where we add our template and the filled form which we want to compare
            - Textract Output: This is where the log files are stored once our textract operation runs
            - CSV: Where our output gets stored
            - Templates: Where our template gets stored
            
2. After this, we create and grant permissions for accepting and running the operation on the files. This is done through IAM - where we create the following roles: 
            - AWSServiceRoleForSupport: The AWSServiceRoleForSupport service-linked role enables all AWS Support API calls to be visible to customers                     through AWS CloudTrail. This helps with monitoring and auditing requirements, because it provides a transparent way to understand the actions               that AWS Support performs on your behalf.

            - AWSServiceRoleForTrustedAdvisor: This role trusts the Trusted Advisor service to assume the role to access AWS services on your behalf. The                 role permissions policy allows Trusted Advisor read-only access for all AWS resources.

            - ec2-s3-access: It is designed to make web-scale computing easier by enabling you to store and retrieve any amount of data, at any time, from               within Amazon EC2 or anywhere on the web.

            - lambda_textract_async: Allows Lambda functions to call AWS services on your behalf - adding a file triggers this and the function is called

            - textract_sns_async: Allows Lambda functions to call AWS services on your behalf.

3. We also use the SNS - Simple Notification Service for the textract-async-notification: With the help of this, as soon as the textract output is created, it sends a notification to AWS for the next steps to generate the output of the file with respect to the template.

4. Lambda Functions: 2 functions: 
                    - 	textract_sync_job_creation: To create an job once we upload the file to the bucket.
                    - 	textract-response-process: This is the function which scrapes the file and helps in finding the differences.


5. After this process has been completed - we simply upload the master file and after this upload the scanned document via the front end service. After clicking the submit button we get a document where the differences are hghlighted.

## Video Link
https://youtu.be/VZZ7y82Xjy4

## Credits & Bibliography

1. AWS Textract Homepage - https://aws.amazon.com/textract/
2. Setup & Implementation - https://www.youtube.com/watch?v=L6vdd9OYF_8&t=2056s&ab_channel=SrceCde
3. Setup & Implementation - https://www.youtube.com/watch?v=IRmeekfUZeA&ab_channel=CloudGuru
4. https://docs.aws.amazon.com/managedservices/latest/userguide/textract.html
5. https://nanonets.com/blog/aws-textract-teardown-pros-cons-review/
