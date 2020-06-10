import stat
import os

import robosignatory.utils as utils

import logging
log = logging.getLogger("robosignatory.work")


def process_atomic(signer, ref, commitid, key, directory, doref=True):
    commitpath = os.path.join(directory, 'objects', commitid[:2],
                              commitid[2:] + '.commit')
    commitmetapath = commitpath + 'meta'

    if not os.path.exists(commitpath):
        log.info('Commit file at %s not found. Skipping' % commitpath)
        return
    if os.path.exists(commitmetapath):
        log.info('Commitmeta file at %s found. Skipping' % commitmetapath)
        return

    log.info('All checks passed, signing %s with %s' % (commitid, key))
    cmdline = signer.build_atomic_cmdline(key,
                                          commitid,
                                          commitpath,
                                          commitmetapath)
    log.info('Signing command line: %s' % cmdline)

    ret, stdout, stderr = utils.run_command(cmdline)
    if ret != 0:
        log.error('Error signing! Signing output: %s, stdout: %s, '
                  'stderr: %s', ret, stdout, stderr)
        return

    log.info('Fixing commitmeta file permissions')

    # Sigul writes it as 0600, which makes a lot of sense as a general file
    # mode for it, but this is just a signature file that we want published
    os.chmod(commitmetapath, (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP
                              | stat.S_IROTH))

    log.info('Commit was succesfully signed, writing ref %s' % ref)

    refpath = os.path.join(directory, 'refs', 'heads', ref)
    if os.path.exists(refpath):
        with open(refpath, 'r') as f:
            log.info('Previous commit for %s: %s'
                     % (ref, f.read().replace('\n', '')))

    dirname_refpath = os.path.dirname(refpath)
    if doref and not os.path.exists(dirname_refpath):
        log.info("Creating the directories for the refpath")
        # Set the umask to be more permissive so directories get group write
        # permissions. See https://pagure.io/releng/issue/8811#comment-629051
        oldumask = os.umask(0o0002)
        try:
            os.makedirs(dirname_refpath)
        finally:
            os.umask(oldumask)

    if doref:
        log.info('Writing %s to %s' % (commitid, refpath))

        with open(refpath, 'w') as f:
            f.write(commitid + '\n')

    log.info('Done')
