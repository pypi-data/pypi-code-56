from os.path import join, dirname
import glob


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs
    from numpy.distutils.misc_util import get_info as get_misc_info
    from scipy._build_utils.system_info import get_info
    from scipy._build_utils import combine_dict, uses_blas64
    from scipy._build_utils.compiler_helper import set_cxx_flags_hook
    from distutils.sysconfig import get_python_inc

    config = Configuration('spatial', parent_package, top_path)

    config.add_data_dir('tests')

    # spatial.transform
    config.add_subpackage('transform')

    # qhull
    qhull_src = sorted(glob.glob(join(dirname(__file__), 'qhull_src',
                                    'src', '*.c')))

    inc_dirs = [get_python_inc()]
    if inc_dirs[0] != get_python_inc(plat_specific=1):
        inc_dirs.append(get_python_inc(plat_specific=1))
    inc_dirs.append(get_numpy_include_dirs())
    inc_dirs.append(join(dirname(dirname(__file__)), '_lib'))
    inc_dirs.append(join(dirname(dirname(__file__)), '_build_utils', 'src'))

    if uses_blas64():
        lapack_opt = get_info('lapack_ilp64_opt')
    else:
        lapack_opt = get_info('lapack_opt')

    cfg = combine_dict(lapack_opt, include_dirs=inc_dirs)
    config.add_extension('qhull',
                         sources=['qhull.c', 'qhull_misc.c'] + qhull_src,
                         **cfg)

    # cKDTree
    ckdtree_src = ['query.cxx',
                   'build.cxx',
                   'query_pairs.cxx',
                   'count_neighbors.cxx',
                   'query_ball_point.cxx',
                   'query_ball_tree.cxx',
                   'sparse_distances.cxx']

    ckdtree_src = [join('ckdtree', 'src', x) for x in ckdtree_src]

    ckdtree_headers = ['ckdtree_decl.h',
                       'coo_entries.h',
                       'distance_base.h',
                       'distance.h',
                       'ordered_pair.h',
                       'partial_sort.h',
                       'rectangle.h']

    ckdtree_headers = [join('ckdtree', 'src', x) for x in ckdtree_headers]

    ckdtree_dep = ['ckdtree.cxx'] + ckdtree_headers + ckdtree_src
    ext = config.add_extension('ckdtree',
                         sources=['ckdtree.cxx'] + ckdtree_src,
                         depends=ckdtree_dep,
                         include_dirs=inc_dirs + [join('ckdtree', 'src')])
    ext._pre_build_hook = set_cxx_flags_hook

    # _distance_wrap
    config.add_extension('_distance_wrap',
                         sources=[join('src', 'distance_wrap.c')],
                         depends=[join('src', 'distance_impl.h')],
                         include_dirs=[get_numpy_include_dirs()],
                         extra_info=get_misc_info("npymath"))

    config.add_extension('_voronoi',
                         sources=['_voronoi.c'])

    config.add_extension('_hausdorff',
                         sources=['_hausdorff.c'])

    # Add license files
    config.add_data_files('qhull_src/COPYING.txt')

    # Type stubs
    config.add_data_files('*.pyi')

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
