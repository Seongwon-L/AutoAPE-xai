# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import paramiko
from xai.common.crypto.AES256 import AES256
from xai.common.sftp.PySFTPAuthException import PySFTPAuthException


class PySFTPClient(object):
    # class : PySFTPClient
    def __init__(self, host: str, port: int, username: str, password: str):
        try:
            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username=AES256().decrypt(username), password=AES256().decrypt(password))
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except paramiko.ssh_exception.AuthenticationException:
            raise PySFTPAuthException

    def open(self, filename, option="r", ) -> paramiko.SFTPFile:
        return self.sftp.open(filename, option)

    def rename(self, src, dst) -> None:
        self.sftp.rename(src, dst)

    def close(self) -> None:
        self.sftp.close()
        self.transport.close()

    def remove(self, filename) -> None:
        self.sftp.remove(filename)

    def is_exist(self, filename) -> bool:
        try:
            self.sftp.stat(filename)
            return True
        except FileNotFoundError:
            return False


if __name__ == '__main__':
    sftp_client = PySFTPClient("localhost", 22, "Kmw/y3YWiiO7gJ/zqMvCuw==", "jTf6XrqcYX1SAhv9JUPq+w==")
    with sftp_client.open("/home/seculayer/temp.tmp", "w") as f:
        f.write("test.1" + "\n")

    with sftp_client.open("/home/seculayer/temp.tmp", "r") as f:
        for line in f.readlines():
            print(line)
    sftp_client.close()
