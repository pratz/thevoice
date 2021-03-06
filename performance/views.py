from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.exceptions import PermissionDenied
from django.db.models import Avg
import logging

from .serializers import PerformanceSerializer
from .models import Performance

# Module logger
logger = logging.getLogger(__name__)


class PerformanceViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceSerializer

    @list_route(url_name='candidate', url_path='candidate/(?P<candidate_id>[0-9]+)')
    def list_by_candidate(self, request, candidate_id=None):
        """
        List performances for given candidate
        """

        queryset = Performance.objects.select_related('team').filter(
            team__candidate=candidate_id).order_by('-date').annotate(
                performance_avg=Avg('score__score'))

        if not request.user.is_superuser:
            logger.debug("Fetching performances by candidates for non-admin user")
            queryset = queryset.filter(team__team__mentor=request.user)

        serializer = self.serializer_class(queryset,
                                           context={'request': request},
                                           many=True)

        logger.debug("Fetched performances for candidate ID {0}".format(
            candidate_id))
        return Response(serializer.data)

    def get_queryset(self):
        """
        NOTE: This isn't required for UI
        List performances for user/admin
        """

        queryset = Performance.objects.select_related('team').order_by(
            '-date').annotate(performance_avg=Avg('score__score'))

        if not self.request.user.is_superuser:
            logger.debug("Fetching performances for non-admin user")
            queryset = queryset.filter(
                team__team__mentor=self.request.user)

        return queryset

    def get_object(self):
        """
        NOTE: This isn't required for UI
        Get performance for user/admin
        """
        # TODO: Try to combine .get() and .annotate() together

        queryset = Performance.objects.filter(
            id=self.kwargs.get('pk')).annotate(
                performance_avg=Avg('score__score'))

        if not self.request.user.is_superuser:
            logger.debug("Fetching performance for non-admin user")
            queryset = queryset.filter(team__team__mentor=self.request.user)

        if not queryset:
            raise PermissionDenied("Its not performed by your team member")

        return queryset[0]
