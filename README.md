# Opensearch Operational Review by Lambda

User needs to collect metadata for OpenSearch Service Operational Review. The utility script can be run on an EC2 instance. 

This project shows how to run the script in an Lambda and upload the metadata to a S3 bucket.
You may need to increase the ephemeral storage for the Lambda function, which has a default of 512MB, to house the metadata.


## Amazon OpenSearch Service Operational Review Metadata Collector Instructions

Amazon OpenSearch Operational Review is a proactive, targeted assessment of your identified AOS workload against infrastructure, scaling, indexing, security, sharding and use case-specific best practices. This review takes a phased approach in understanding your workload, gathering metadata and generating a detailed report, and finally providing and reviewing prescriptive recommendations for you to achieve operational success with AOS.

**The collector package will not** collect any customer data, only metadata as detailed below.  **The collector package will not** alter any cluster configuration or any data in any form. **The collector package will not** automatically share anything. You will have the opportunity to review everything prior to sharing.

The following Amazon OpenSearch SDK and APIs are used to collect the metadata for review:

```
OpenSearch SDK: DomainConfig
/_cluster/health
/_cluster/settings
/_cluster/state
/_cluster/stats
/_cat/nodes
/_nodes/stats/indices/fielddata
/_cat/indices
/_cat/indices/_hot
/_cat/indices/_warm
/_cat/shards
/_cat/shards/_hot
/_cat/shards/_warm
/_cat/fielddata
/_cat/allocation
/_cat/pending_tasks
```

 

 

### Step 1: Launch an EC2 instance and install the AOS metadata collector package

**Install Python 3 and the AOS metadata collector manually**

- Configure an EC2 instance with Internet access. If your target AOS domain is in a VPC, then you will need to place this EC2 instance in the same VPC.
- SSH to your EC2 instance and and install Python 3. 
- Then install the AOS metadata collector using the following command:

```
$ pip3 install aos-metadata-collector
```

- Verify that the AOS metadata collector package is properly configured by running the following command:

```
$ metadata_collector -h
```

### Step 2: List all domains

In the EC2 shell prompt run the following command to list all of the domains in a region. Replace **{region}** with the region where your target AOS clusters are running.

```
$ metadata_collector list_domains -r {region}
```

Note the name of domain name for which you want to collect metadata.

### Step 3: Collect metadata

Determine whether your **domain** is in **Public access** or **VPC** and which **access control policy** your domain is configured with. 

 Amazon OpenSearch Service security has three main layers:

**Network:** The first security layer is the network, which determines whether requests reach an Amazon OpenSearch domain. If you chose **Public access** when you created the domain, requests from any internet-connected client can reach the domain endpoint. If you chose **VPC access**, clients must connect to the VPC and have the necessary security groups to permit requests to reach the endpoint.

**Domain access policy:** The second security layer is the domain access policy. The access policy accepts or rejects requests at the edge of the domain, before they reach OpenSearch itself.  If your domain policy is set to anything other than **Allow open access to the domain**, then you may need to add your metadata collector EC2 instance to the Condition list in your domain access policy.

**Fine-grained access control:** The third and final security layer is fine-grained access control. Fine-grained access control evaluates the user credentials and either authenticates the user or denies the request. If fine-grained access control is disabled, then requests do not require further authentication.

**EC2 Instance Role:** If your domain has an active access policy, then make sure the EC2 instance role can access the AOS domain. If you used the CloudFormation template in Step 1 - Option 1, then the EC2 instance role is “OpenSearchReviewIAMRole.”

 Depending on your cluster setup and the access policy, you will need to run one of the following commands to collect metadata:

 For domains that have **fine-grained access control disabled**, run the following command:

```
$ metadata_collector collect_data -r {region} -d {domain_name} -o {output_dir}
```

For domains that have **fine-grained access control enabled and are using IAM ARN as master user**, run the following command:

```
$ metadata_collector collect_data -r {region} -d {domain_name} -c -i -o {output_dir}
```

For domains that have **fine-grained access control enabled and are using internal user database**, run the following command:

```
$ metadata_collector collect_data -r {region} -d {domain_name} -c -b -u {user_name} -p {password} -o {output_dir}
```

### Step 4: Share the collected metadata

The metadata collector will place  **{output_dir}.zip** into your working directory.

 Share this zip file with your AWS Technical Account Manager to continue the AOS Operational Review process.

 

> **References:**

> Domain access policy: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html

> Fine-grained access policy: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html
