"""
A script that uses f2py to generate the signature files used to make
the Cython BLAS and LAPACK wrappers from the fortran source code for
LAPACK and the reference BLAS.

To generate the BLAS wrapper signatures call:
python _cython_signature_generator.py blas <blas_directory> <out_file>

To generate the LAPACK wrapper signatures call:
python _cython_signature_generator.py lapack <lapack_src_directory> <out_file>

This script expects to be run on the source directory for
the oldest supported version of LAPACK (currently 3.4.0).
"""

import glob
import os
from numpy.f2py import crackfortran

sig_types = {'integer': 'int',
             'complex': 'c',
             'double precision': 'd',
             'real': 's',
             'complex*16': 'z',
             'double complex': 'z',
             'character': 'char',
             'logical': 'bint'}


def get_type(info, arg):
    argtype = sig_types[info['vars'][arg]['typespec']]
    if argtype == 'c' and info['vars'][arg].get('kindselector') is not None:
        argtype = 'z'
    return argtype


def make_signature(filename):
    info = crackfortran.crackfortran(filename)[0]
    name = info['name']
    if info['block'] == 'subroutine':
        return_type = 'void'
    else:
        return_type = get_type(info, name)
    arglist = [' *'.join([get_type(info, arg), arg]) for arg in info['args']]
    args = ', '.join(arglist)
    # Eliminate strange variable naming that replaces rank with rank_bn.
    args = args.replace('rank_bn', 'rank')
    return '{0} {1}({2})\n'.format(return_type, name, args)


def get_sig_name(line):
    return line.split('(')[0].split(' ')[-1]


def sigs_from_dir(directory, outfile, manual_wrappers=None, exclusions=None):
    if directory[-1] in ['/', '\\']:
        directory = directory[:-1]
    files = sorted(glob.glob(directory + '/*.f*'))
    if exclusions is None:
        exclusions = []
    if manual_wrappers is not None:
        exclusions += [get_sig_name(l) for l in manual_wrappers.split('\n')]
    signatures = []
    for filename in files:
        name = os.path.splitext(os.path.basename(filename))[0]
        if name in exclusions:
            continue
        signatures.append(make_signature(filename))
    if manual_wrappers is not None:
        signatures += [l + '\n' for l in manual_wrappers.split('\n')]
    signatures.sort(key=get_sig_name)
    comment = ["# This file was generated by _cython_signature_generator.py.\n",
               "# Do not edit this file directly.\n\n"]
    with open(outfile, 'w') as f:
        f.writelines(comment)
        f.writelines(signatures)

# slamch and dlamch are not in the lapack src directory, but,since they
# already have Python wrappers, we'll wrap them as well.
# The other manual signatures are used because the signature generating
# functions don't work when function pointer arguments are used.


lapack_manual_wrappers = '''void cgees(char *jobvs, char *sort, cselect1 *select, int *n, c *a, int *lda, int *sdim, c *w, c *vs, int *ldvs, c *work, int *lwork, s *rwork, bint *bwork, int *info)
void cgeesx(char *jobvs, char *sort, cselect1 *select, char *sense, int *n, c *a, int *lda, int *sdim, c *w, c *vs, int *ldvs, s *rconde, s *rcondv, c *work, int *lwork, s *rwork, bint *bwork, int *info)
void cgges(char *jobvsl, char *jobvsr, char *sort, cselect2 *selctg, int *n, c *a, int *lda, c *b, int *ldb, int *sdim, c *alpha, c *beta, c *vsl, int *ldvsl, c *vsr, int *ldvsr, c *work, int *lwork, s *rwork, bint *bwork, int *info)
void cggesx(char *jobvsl, char *jobvsr, char *sort, cselect2 *selctg, char *sense, int *n, c *a, int *lda, c *b, int *ldb, int *sdim, c *alpha, c *beta, c *vsl, int *ldvsl, c *vsr, int *ldvsr, s *rconde, s *rcondv, c *work, int *lwork, s *rwork, int *iwork, int *liwork, bint *bwork, int *info)
void dgees(char *jobvs, char *sort, dselect2 *select, int *n, d *a, int *lda, int *sdim, d *wr, d *wi, d *vs, int *ldvs, d *work, int *lwork, bint *bwork, int *info)
void dgeesx(char *jobvs, char *sort, dselect2 *select, char *sense, int *n, d *a, int *lda, int *sdim, d *wr, d *wi, d *vs, int *ldvs, d *rconde, d *rcondv, d *work, int *lwork, int *iwork, int *liwork, bint *bwork, int *info)
void dgges(char *jobvsl, char *jobvsr, char *sort, dselect3 *selctg, int *n, d *a, int *lda, d *b, int *ldb, int *sdim, d *alphar, d *alphai, d *beta, d *vsl, int *ldvsl, d *vsr, int *ldvsr, d *work, int *lwork, bint *bwork, int *info)
void dggesx(char *jobvsl, char *jobvsr, char *sort, dselect3 *selctg, char *sense, int *n, d *a, int *lda, d *b, int *ldb, int *sdim, d *alphar, d *alphai, d *beta, d *vsl, int *ldvsl, d *vsr, int *ldvsr, d *rconde, d *rcondv, d *work, int *lwork, int *iwork, int *liwork, bint *bwork, int *info)
d dlamch(char *cmach)
void ilaver(int *vers_major, int *vers_minor, int *vers_patch)
void sgees(char *jobvs, char *sort, sselect2 *select, int *n, s *a, int *lda, int *sdim, s *wr, s *wi, s *vs, int *ldvs, s *work, int *lwork, bint *bwork, int *info)
void sgeesx(char *jobvs, char *sort, sselect2 *select, char *sense, int *n, s *a, int *lda, int *sdim, s *wr, s *wi, s *vs, int *ldvs, s *rconde, s *rcondv, s *work, int *lwork, int *iwork, int *liwork, bint *bwork, int *info)
void sgges(char *jobvsl, char *jobvsr, char *sort, sselect3 *selctg, int *n, s *a, int *lda, s *b, int *ldb, int *sdim, s *alphar, s *alphai, s *beta, s *vsl, int *ldvsl, s *vsr, int *ldvsr, s *work, int *lwork, bint *bwork, int *info)
void sggesx(char *jobvsl, char *jobvsr, char *sort, sselect3 *selctg, char *sense, int *n, s *a, int *lda, s *b, int *ldb, int *sdim, s *alphar, s *alphai, s *beta, s *vsl, int *ldvsl, s *vsr, int *ldvsr, s *rconde, s *rcondv, s *work, int *lwork, int *iwork, int *liwork, bint *bwork, int *info)
s slamch(char *cmach)
void zgees(char *jobvs, char *sort, zselect1 *select, int *n, z *a, int *lda, int *sdim, z *w, z *vs, int *ldvs, z *work, int *lwork, d *rwork, bint *bwork, int *info)
void zgeesx(char *jobvs, char *sort, zselect1 *select, char *sense, int *n, z *a, int *lda, int *sdim, z *w, z *vs, int *ldvs, d *rconde, d *rcondv, z *work, int *lwork, d *rwork, bint *bwork, int *info)
void zgges(char *jobvsl, char *jobvsr, char *sort, zselect2 *selctg, int *n, z *a, int *lda, z *b, int *ldb, int *sdim, z *alpha, z *beta, z *vsl, int *ldvsl, z *vsr, int *ldvsr, z *work, int *lwork, d *rwork, bint *bwork, int *info)
void zggesx(char *jobvsl, char *jobvsr, char *sort, zselect2 *selctg, char *sense, int *n, z *a, int *lda, z *b, int *ldb, int *sdim, z *alpha, z *beta, z *vsl, int *ldvsl, z *vsr, int *ldvsr, d *rconde, d *rcondv, z *work, int *lwork, d *rwork, int *iwork, int *liwork, bint *bwork, int *info)'''


# Exclude scabs and sisnan since they aren't currently included
# in the scipy-specific ABI wrappers.
blas_exclusions = ['scabs1', 'xerbla']

# Exclude all routines that do not have consistent interfaces from
# LAPACK 3.4.0 through 3.6.0.
# Also exclude routines with string arguments to avoid
# compatibility woes with different standards for string arguments.
lapack_exclusions = [
              # Not included because people should be using the
              # C standard library function instead.
              # sisnan is also not currently included in the
              # ABI wrappers.
              'sisnan', 'dlaisnan', 'slaisnan',
              # Exclude slaneg because it isn't currently included
              # in the ABI wrappers
              'slaneg',
              # Excluded because they require Fortran string arguments.
              'ilaenv', 'iparmq', 'lsamen', 'xerbla',
              # Exclude XBLAS routines since they aren't included
              # by default.
              'cgesvxx', 'dgesvxx', 'sgesvxx', 'zgesvxx',
              'cgerfsx', 'dgerfsx', 'sgerfsx', 'zgerfsx',
              'cla_gerfsx_extended', 'dla_gerfsx_extended',
              'sla_gerfsx_extended', 'zla_gerfsx_extended',
              'cla_geamv', 'dla_geamv', 'sla_geamv', 'zla_geamv',
              'dla_gercond', 'sla_gercond',
              'cla_gercond_c', 'zla_gercond_c',
              'cla_gercond_x', 'zla_gercond_x',
              'cla_gerpvgrw', 'dla_gerpvgrw',
              'sla_gerpvgrw', 'zla_gerpvgrw',
              'csysvxx', 'dsysvxx', 'ssysvxx', 'zsysvxx',
              'csyrfsx', 'dsyrfsx', 'ssyrfsx', 'zsyrfsx',
              'cla_syrfsx_extended', 'dla_syrfsx_extended',
              'sla_syrfsx_extended', 'zla_syrfsx_extended',
              'cla_syamv', 'dla_syamv', 'sla_syamv', 'zla_syamv',
              'dla_syrcond', 'sla_syrcond',
              'cla_syrcond_c', 'zla_syrcond_c',
              'cla_syrcond_x', 'zla_syrcond_x',
              'cla_syrpvgrw', 'dla_syrpvgrw',
              'sla_syrpvgrw', 'zla_syrpvgrw',
              'cposvxx', 'dposvxx', 'sposvxx', 'zposvxx',
              'cporfsx', 'dporfsx', 'sporfsx', 'zporfsx',
              'cla_porfsx_extended', 'dla_porfsx_extended',
              'sla_porfsx_extended', 'zla_porfsx_extended',
              'dla_porcond', 'sla_porcond',
              'cla_porcond_c', 'zla_porcond_c',
              'cla_porcond_x', 'zla_porcond_x',
              'cla_porpvgrw', 'dla_porpvgrw',
              'sla_porpvgrw', 'zla_porpvgrw',
              'cgbsvxx', 'dgbsvxx', 'sgbsvxx', 'zgbsvxx',
              'cgbrfsx', 'dgbrfsx', 'sgbrfsx', 'zgbrfsx',
              'cla_gbrfsx_extended', 'dla_gbrfsx_extended',
              'sla_gbrfsx_extended', 'zla_gbrfsx_extended',
              'cla_gbamv', 'dla_gbamv', 'sla_gbamv', 'zla_gbamv',
              'dla_gbrcond', 'sla_gbrcond',
              'cla_gbrcond_c', 'zla_gbrcond_c',
              'cla_gbrcond_x', 'zla_gbrcond_x',
              'cla_gbrpvgrw', 'dla_gbrpvgrw',
              'sla_gbrpvgrw', 'zla_gbrpvgrw',
              'chesvxx', 'zhesvxx',
              'cherfsx', 'zherfsx',
              'cla_herfsx_extended', 'zla_herfsx_extended',
              'cla_heamv', 'zla_heamv',
              'cla_hercond_c', 'zla_hercond_c',
              'cla_hercond_x', 'zla_hercond_x',
              'cla_herpvgrw', 'zla_herpvgrw',
              'sla_lin_berr', 'cla_lin_berr',
              'dla_lin_berr', 'zla_lin_berr',
              'clarscl2', 'dlarscl2', 'slarscl2', 'zlarscl2',
              'clascl2', 'dlascl2', 'slascl2', 'zlascl2',
              'cla_wwaddw', 'dla_wwaddw', 'sla_wwaddw', 'zla_wwaddw',
              # Removed between 3.3.1 and 3.4.0.
              'cla_rpvgrw', 'dla_rpvgrw', 'sla_rpvgrw', 'zla_rpvgrw',
              # Signatures changed between 3.4.0 and 3.4.1.
              'dlasq5', 'slasq5',
              # Routines deprecated in LAPACK 3.6.0
              'cgegs', 'cgegv', 'cgelsx',
              'cgeqpf', 'cggsvd', 'cggsvp',
              'clahrd', 'clatzm', 'ctzrqf',
              'dgegs', 'dgegv', 'dgelsx',
              'dgeqpf', 'dggsvd', 'dggsvp',
              'dlahrd', 'dlatzm', 'dtzrqf',
              'sgegs', 'sgegv', 'sgelsx',
              'sgeqpf', 'sggsvd', 'sggsvp',
              'slahrd', 'slatzm', 'stzrqf',
              'zgegs', 'zgegv', 'zgelsx',
              'zgeqpf', 'zggsvd', 'zggsvp',
              'zlahrd', 'zlatzm', 'ztzrqf']


if __name__ == '__main__':
    from sys import argv
    libname, src_dir, outfile = argv[1:]
    if libname.lower() == 'blas':
        sigs_from_dir(src_dir, outfile, exclusions=blas_exclusions)
    elif libname.lower() == 'lapack':
        sigs_from_dir(src_dir, outfile, manual_wrappers=lapack_manual_wrappers,
                      exclusions=lapack_exclusions)
