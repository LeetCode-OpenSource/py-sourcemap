import sys
import time
import platform
from urllib import request


PING_TIMEOUT = 3


def _get_download_urls(version):
    s3_url_template = 'https://github.com/LeetCode-OpenSource/py-sourcemap/releases/download/{tag}/py_sourcemap.{py_ver}-{platform}.{ext}'
    aliyun_url_template = 'https://static.leetcode-cn.com/packages/py_sourcemap/{package_ver}/py_sourcemap.{py_ver}-{platform}.{ext}'

    version_tag = 'v{}'.format(version)
    (major, minor, _) = platform.python_version_tuple()
    if major != '3' or not(minor in ['5', '6', '7']):
        raise Exception('Only python 3.5, 3.6, 3.7 are supported')
    system = platform.system()
    if system == 'Linux':
        py_version = 'cpython-{}{}m'.format(major, minor)
        usr_platform = 'x86_64-linux-gnu'
        ext = 'so'
    elif system == 'Darwin':
        py_version = 'cpython-{}{}m'.format(major, minor)
        usr_platform = 'x86_64-apple-darwin'
        ext = 'so'
    elif system == 'Windows':
        py_version = 'cp{}{}'.format(major, minor)
        # from https://docs.python.org/3/library/platform.html
        is_64bits = sys.maxsize > 2**32
        usr_platform = 'win_amd64' if is_64bits else 'win32'
        ext = 'pyd'
    else:
        raise Exception('Your system is unrecognized: {}'.format(system))

    return {
        's3': s3_url_template.format(tag=version_tag,
                                     py_ver=py_version,
                                     platform=usr_platform,
                                     ext=ext),
        'aliyun': aliyun_url_template.format(package_ver=version,
                                             py_ver=py_version,
                                             platform=usr_platform,
                                             ext=ext)
    }


def _get_latency(url):
    req = request.Request(url, method="HEAD")
    try:
        start = time.perf_counter()
        request.urlopen(req, timeout=PING_TIMEOUT)
        end = time.perf_counter()
        return end - start
    except Exception:
        return 999


def get_remote_binary(version):
    urls = _get_download_urls(version)
    print('Try ping servers...')
    s3_time = _get_latency(urls['s3'])
    aliyun_time = _get_latency(urls['aliyun'])
    print('s3: {:.3f}s, aliyun: {:.3f}s'.format(s3_time, aliyun_time))
    url = urls['s3'] if s3_time <= aliyun_time else urls['aliyun']
    print('Start downloading {}...'.format(url))
    binary_fp = request.urlopen(url)
    print('Downloaded {}'.format(url))
    return binary_fp
