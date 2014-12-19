import tornado.options

# AWS Credentials 
tornado.options.define("AWS_KEY", default="YOURACCESSKEY")
tornado.options.define("AWS_SECRET", default="YOURSECRETKEY")
tornado.options.define("BUCKET_NAME", default="YOURBUCKETNAME")
