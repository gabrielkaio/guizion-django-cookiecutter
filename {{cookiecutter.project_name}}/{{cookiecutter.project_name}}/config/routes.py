from rest_framework.routers import DefaultRouter

from {{cookiecutter.project_name}}.apps.accounts.api import UserViewSet


router = DefaultRouter()
router.register(r'v1/users', UserViewSet)
