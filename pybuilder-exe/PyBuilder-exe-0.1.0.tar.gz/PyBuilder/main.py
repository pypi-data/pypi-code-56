# -*- coding: utf-8 -*-
# @Time    : 2020-04-02 19:02
# @Author  : leocll
# @Email   : leocll@qq.com
# @File    : main.py

def run():
    import argparse
    from PyBuilder.config import default_config
    from PyBuilder.run import run4args

    parser = argparse.ArgumentParser(description='Python build tools')
    parser.add_argument('-n', '--name', required=True, help='the execution name.')
    parser.add_argument('-tf', '--target-file', default=default_config.target_file,
                        help='the target file path relative the sources dir.(default: %s)' % default_config.target_file)
    parser.add_argument('-sd', '--PyBuilder-dir', default=default_config.src_dir,
                        help='the sources dir path.(default: %s)' % default_config.src_dir)
    parser.add_argument('-bd', '--build-dir', default=default_config.build_dir,
                        help='the build dir path.(default: %s)' % default_config.build_dir)
    parser.add_argument('-hf', '--hook-file', help='the .py file of hook build.')
    parser.add_argument('-ef', '--excludes-file', default=default_config.excludes_file,
                        help='the excludes file path.(default: %s)' % default_config.excludes_file)
    parser.add_argument('-if', '--ignores-file', default=default_config.ignores_file,
                        help='the ignores file path.(default: %s)' % default_config.ignores_file)
    parser.add_argument('-F', action='store_true', default=default_config.single,
                        help='build a single file execution.(default: %s)' % default_config.single)
    parser.add_argument('-nc', '--no-compile', action='store_true', default=default_config.no_compile,
                        help='not compile, only build.(default: %s)' % default_config.no_compile)
    args = parser.parse_args()
    run4args(args)

if __name__ == '__main__':
    run()