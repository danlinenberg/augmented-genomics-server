# Augmented Genomics Server-Side

## How to set up the server

Create an AWS account and follow these instructions:
### Credentials
  - Go to "My Security Credentials"->"Access Keys"
  - Generate an Access Key and Secret, and save them. They will be the CLIENT_ID and CLIENT_SECRET we use on the client. 
### IAM
  - Create a role for lambda execution under "Roles". Give it the permissions "AWSLambdaFullAccess". This will be used as your Lambda role later on.
  - Make sure you have Auth/UnAuth roles for your user pool.
### Cognito
  - Create a Federated Identity, and enable access to unauthenticated identities.
  - Create a new User Pool and add some users (username is the ID)
  - Save the ARN of the Federated Identity (Under "Sample Code"->"Get AWS Credentials"). This will be the USER_POOL_ID we use on the client.
### DynamoDB
  - Create a table named "Patient" with hash key "id" (Number)
  - Create a table named "Doctor" with hash key "id" (Number)
  - Create a table named "GeneAverageScore" with hash key "Gene.refGene" (String)
  - Create a table named "GenesVIP" with hash key "Gene.refGene" (String)
  - Create a table named "VCF" with has key "id" (Number) and sort key "Gene.refGene" (String)
  - Set the Write capacity for "VCF" table to 20 (all other tables can have 5)
  - Save the ARN of the 
  
### S3
(bucket name is unique across AWS, so you will need to change the reference to that bucket throughtout ALL of the lambda/client code)
  - Create a bucket that corresponds to "s3-tau-bucket-vcf" 
  - Create a bucket that corresponds to "s3-tau-bucket-general" 
  - Place the files located in "S3" folder in this project, in the corresponding buckets.

### Lambda
  - Copy all the scripts located in "Lambda" folder in this project, and create a script for each on on your Lambda dashboard.
  - Set each script as Python 2.7
  - Give each script a 5-min timeout in the settings, and set the role to the one you previously created in IAM.
  
| Script Name | Description |
| ------ | ------ |
| access_control_controller | checks the requester's permissions for the specific request and the patient's settings|
| access_control_handler | returns the user's access control level (0-3) for every position (super-doctor doctor, nurse, other)|
| query_handler | compares access control levels and redirects to appropriate queries|
| verify_qr | Receives data from client and transfers to relevant query type|
|set_access_control | sets a patient's access control|
| table_maker | appends vcf data the the table under the a given ID|
| average_associations_maker |Creates a table with average association scores for each gene (inset a csv with calculated average scores above 0.35 from DisgeNet)|
| table_prepare | checks if data exists and redirects to table_maker|
| data_delete | deletes vcf data|
| device_whitelist | whitelists a device|
| table_init | creates the VCF table|
| find_gene_score | finds a score for a specific gene. returns 0 if it's below the sensitivity threshold|
| drug_genes_maker | Used to import csv content to a table (inset a genes.csv file containing vip genes from pharmgkb, to s|
| is_vcf_exist | checks if a patient has vcf da|
| find_vip_genes | returns VIP genes associated with the drug and located in VCF, otherwise returns false|
| insert_gene_disease | insert a disease score for gene|
| query_naive_eas | returns data for 1000genom for south-east-asia|
| query_naive_amr | returns data for 1000genom for america|
| query_naive_all | returns data for 1000genom for all superpopulations|
| query_naive_afr | returns data for 1000genom for africa|
| query_naive_eur | returns data for 1000genom for europe|


### Users

Password for all users is 12345678

- 3 -> Full permissions without user's consent
- 2 -> Full permissions with user's consent
- 1 -> Limited permissions with user's consent
- 0 -> No permissions, read only

| ID | Role | Permission Level |
| ------ | ------ | ------ |
| 204146161 | Patient | - |
| 302870753 | Patient | - |
| 302858410 | Patient | - |
| 3028584100 | Treater | 3 |
| 2041461610 | Treater | 2 |
| 3028707530 | Treater | 1 |
| 12345678   | Treater | 0 |

