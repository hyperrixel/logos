"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: networking

Package workflow:
    - content in dict
    - content to binary
    - content sign
    - content to ascii
    - operation
    - make package ID
    - create package binary
    - send


Operations:
    login
    logout
    create log entry
    update log entry
    attach to log entry
    finish log entry
    get texts
    get tags
    get Descriptions
    ...
"""

from queue import Queue
import socket

from functiontools import get_package_template


class Client:
    """
    Singleton to provide client networking interface
    """

    __is_online = False
    __operation_lists = {}
    __package_queue = Queue()
    __responses = {}


    @classmethod
    def start(cls):
        """
        Start client networking
        =======================
        """


    @classmethod
    def send(cls, package_id : str, operation : str, content : bytes):
        """
        Send package
        ============

        Parameters
        ----------
        package_id : str
            ID of the package.
        operation : str
            Operation type of the package.
        content : bytes
            Content of the package.
        """

        package = get_package_template()
        package['PackageID'] = package_id
        package['Operation'] = operation
        package['Content'] = content
        cls.__package_queue.put(package)


    @classmethod
    def send_and_check(cls, package_id : str, operation : str, content : bytes
                       ) -> bool:
        """
        Send package and check success
        ==============================

        Parameters
        ----------
        package_id : str
            ID of the package.
        operation : str
            Operation type of the package.
        content : bytes
            Content of the package.
        """


    @classmethod
    def send_and_wait(cls, package_id : str, operation : str, content : bytes,
                      operation_to_watch : str) -> bytes:
        """
        Send package and wait until operation happen
        ============================================

        Parameters
        ----------
        package_id : str
            ID of the package.
        operation : str
            Operation type of the package.
        content : bytes
            Content of the package.
        operation_to_watch : str
            Response operation to watch for.
        """


    @classmethod
    def stop(cls):
        """
        Start client networking
        =======================
        """

"""
SEND BROADCAST:
from socket import *
s=socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.sendto('this is testing',('255.255.255.255',12345))
"""

"""
GET BROADCAST
from socket import *
s=socket(AF_INET, SOCK_DGRAM)
s.bind(('',12345))
m=s.recvfrom(1024)
print m[0]
"""

"""
"""
