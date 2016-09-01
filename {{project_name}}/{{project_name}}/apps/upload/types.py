from enum import Enum


class PhotoDirectory(Enum):
    user_avatar = 'user/avatar/'


class PhotoDirectoryFactory:

    avatar = 'avatar'
    
    @staticmethod
    def factory(type):

        status = dict(
            user_avatar=PhotoDirectory.user_avatar,
        )

        return status[type]
