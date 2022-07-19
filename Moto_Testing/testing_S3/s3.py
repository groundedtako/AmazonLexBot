import boto3

class MyS3Client:
    def __init__(self, region_name="us-east-1"):
        self.client = boto3.client("s3", region_name=region_name)

    def list_buckets(self):
        """Returns a list of bucket names."""
        response = self.client.list_buckets()
        print("\nListing All S3 Buckets : ")
        buckets =  [bucket["Name"] for bucket in response["Buckets"]]
        print(buckets)
        print("-------------------")
        return buckets

    def list_objects(self, bucket_name, prefix):
        """Returns a list of object names in the bucket."""
        response = self.client.list_objects(Bucket=bucket_name, Prefix=prefix)
        print(f"\nListing All S3 Objects inside {bucket_name} with prefix : {prefix} : ")
        objects = [obj["Key"] for obj in response.get("Contents", [])]
        print(objects)
        print("-------------------")
        return objects