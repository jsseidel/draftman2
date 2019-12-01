"""
KeeperFileOpsLinux

This class helps with the simple file operations required by draftman2
"""
import subprocess

from lib.KeeperFileOps import KeeperFileOps

class KeeperFileOpsLinux(KeeperFileOps):

    def delete(self, src):
        rv = True
        reason = "OK"
        result = subprocess.run(['rm', '-rf', src])
        if result.returncode != 0:
            rv = False
            reason = result.stderr
        return (rv, reason)

    def move(self, src, dst):
        rv = True
        reason = "OK"
        result = subprocess.run(['mv', src, dst])
        if result.returncode != 0:
            rv = False
            reason = result.stderr
        return (rv, reason)
        pass
