import os
import sys
import ntpath
import glob
import configparser

import oss2

endpoint = 'http://{region}.aliyuncs.com'.format(region='oss-cn-shanghai')

bucket_name = 'lc-frontend'

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        files = sys.argv[1:]
    else:
        files = glob.glob('build/lib/py_sourcemap/*.so')

    config = configparser.ConfigParser()
    config.read('.bumpversion.cfg')
    package_version = config['bumpversion']['current_version']

    access_key = os.environ.get('ALIYUN_ACCESS_KEY')
    access_token = os.environ.get('ALIYUN_ACCESS_TOKEN')

    auth = oss2.Auth(access_key, access_token)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    for file_path in files:
        basename = ntpath.basename(file_path)
        fp = open(file_path, 'rb')
        target_key = 'packages/py_sourcemap/{version}/{name}'.format(
            version=package_version, name=basename)
        print('Uploading {}...'.format(target_key))
        bucket.put_object(target_key, fp.read())
        fp.close()
    print('Uploaded all.')
