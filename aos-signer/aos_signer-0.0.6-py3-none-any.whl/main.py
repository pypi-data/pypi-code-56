import argparse

from aos_signer.signer.signer import Signer


def main():
    s = Signer(src_folder='src', package_folder='.')
    s.process()
    # p = service_config_parser.ServiceConfigParser('conf.yaml')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process service config.')
    parser.add_argument('--config', metavar='c', type=str,
                        help='an integer for the accumulator')

    args = parser.parse_args()
    main()
