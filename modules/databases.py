  # grab wav file from S3 location based on filename in JSON data pushed from SQS with Boto
  filename = json.loads(self.request.body)['filename']
  # conn = boto.connect_s3(options.AWS_KEY, options.AWS_SECRET)
  # bucket = conn.get_bucket(options.BUCKET_NAME)
  # key = bucket.get_key(filename)
  # wav_file = key.get_contents_to_filename('sound.wav')
  