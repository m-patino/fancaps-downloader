import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url', nargs='?', help='Url to start download')
args = parser.parse_args()
