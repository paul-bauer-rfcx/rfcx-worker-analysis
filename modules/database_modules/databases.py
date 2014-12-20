import boto
# import sys

class S3:
  def __init__(self):
    # import AWS DB settings from file for class' use only
    pass

  def connect(self):
    # conn = boto.connect_s3(options.AWS_KEY, options.AWS_SECRET)
    pass

  def get_bucket(self, bucket_name):
    # bucket = conn.get_bucket(options.BUCKET_NAME)
    pass

  def download_file(self, filename):
    '''Download S3 File. Takes in a filename and downloads it to the EC2 instance.'''
    # grab wav file from S3 location based on filename in JSON data pushed from SQS with Boto    
    # key = bucket.get_key(filename)
    # return key.get_contents_to_filename(filename)
    pass

  def upload_file(self):
    pass

  def validate(self):
    pass
  