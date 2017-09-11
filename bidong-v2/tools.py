import os
import json
import argparse
import importlib

from docs.mpdocs import mpspec
from docs.pndocs import pnspec

BASEDIR = os.path.dirname(os.path.abspath(__file__))


def parse_args():
    parser = argparse.ArgumentParser(description="Generate swagger api")
    parser.add_argument("options", type=str, choices=["gendoc", "loaddata"],
                        help="what to do")
    parser.add_argument("--api", type=str,
                        help="which api to generate, project or platform")
    parser.add_argument("--fixture", type=str,
                        help="fixtures to load, e.g tests.fixtures.billing")
    return parser.parse_args()


def load_fixtures(path):
    module = importlib.import_module(path)
    func = getattr(module, 'load')
    func()


def gen_swagger_doc(api):
    filename = os.path.join(BASEDIR, 'docs/api', api+'.json')
    if api == "platform":
        spec = mpspec
    elif api == "project":
        spec = pnspec
    else:
        spec = None

    if spec:
        with open(filename, 'w') as writer:
            json.dump(spec.to_dict(), writer, indent=4, ensure_ascii=False)
        print('Generate swagger doc {} success'.format(filename))
    else:
        print("Could not generate doc for {}".format(api))


if __name__ == "__main__":
    args = parse_args()
    if args.options == "gendoc":
        gen_swagger_doc(args.api)
    elif args.options == "loaddata":
        load_fixtures(args.fixture)
