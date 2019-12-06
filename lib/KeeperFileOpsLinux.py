"""
KeeperFileOpsLinux

This class helps with the simple file operations required by draftman2
"""
import pipes
import subprocess

from lib.KeeperFileOps import KeeperFileOps

class KeeperFileOpsLinux(KeeperFileOps):

    def delete(self, src):
        rv = True
        reason = "OK"
        result = subprocess.run(['rm', '-f', src])
        if result.returncode != 0:
            rv = False
            reason = result.stderr
        return (rv, reason)

    def move(self, src, dst):
        rv = True
        reason = "OK"

        if src == dst:
            return (rv, reason)

        result = subprocess.run(['mv', src, dst])
        if result.returncode != 0:
            rv = False
            reason = result.stderr
        return (rv, reason)

    def copy_tutorial(self, dst):
        rv = True
        reason = "OK"

        dst = pipes.quote('%s/.' % dst)

        cmd = 'cp -r ./%s %s' % (pipes.quote('Draftman2 Tutorial'), dst)

        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            rv = False
            reason = e.output

        return (rv, reason)
