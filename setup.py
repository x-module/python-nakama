from setuptools import setup, find_packages

# 读取requirements.txt自动生成install_requires
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='python-nakama',
      version='1.0.0',
      description='Python client for Nakama server',
      packages=find_packages(),
      install_requires=install_requires,
      license='MIT',
      author='tudou',
      author_email='244395692@qq.com',
      url='https://github.com/x-module/python-nakama',
      keywords='nakama',
      zip_safe=False,
      )
