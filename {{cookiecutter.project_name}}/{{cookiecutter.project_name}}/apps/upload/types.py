"""
    Module to define the types of files
     for receive in upload request
"""
from enum import Enum


class PhotoDirectory(Enum):
    user_avatar = 'user/avatar/'


class PhotoDirectoryFactory:

    @staticmethod
    def factory(file_type):
        status = dict(
            user_avatar=PhotoDirectory.user_avatar,
        )

        return status[file_type]
