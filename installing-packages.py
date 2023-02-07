import subprocess

packages = ['pickle', 'glob2', 'json', 'logging', 'os', 'pprint', 'python-dateutil']

for package in packages:
    subprocess.call(['pip', 'install', package])