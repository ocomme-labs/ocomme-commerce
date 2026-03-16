from rest_framework import generics, mixins


class OcommeListApiView(generics.ListAPIView):
    """Return ListAPIView"""


class OcommeMixinApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    """"""


class OcommeMixinInstanceApiView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """"""
