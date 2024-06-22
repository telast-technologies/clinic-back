import logging

import viewflow
from drf_spectacular.utils import OpenApiExample, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from clinic.visits.api.v1.serializers import VisitDetailSerializer
from clinic.visits.flows import VisitFlow

logger = logging.getLogger(__name__)


class VisitFlowViewMixin:
    flow_class = VisitFlow

    @extend_schema(
        request=OpenApiTypes.OBJECT,
        responses={200: VisitDetailSerializer},
        examples=[
            OpenApiExample("Cancel Request", summary="Example of a cancel request", value={"reason": "string"}),
        ],
    )
    @action(detail=True, methods=["patch"])
    def cancel(self, request, pk, *args, **kwargs):
        flow = self.flow_class(self.get_object())

        try:
            flow.cancel(reason=request.data.get("reason"))
            serializer = VisitDetailSerializer(self.get_object(), context={"request": request}, read_only=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except viewflow.fsm.TransitionNotAllowed as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=None,
        responses={200: VisitDetailSerializer},
        examples=[OpenApiExample("Check-in Response", summary="Example of a check-in response", value={})],
    )
    @action(detail=True, methods=["patch"])
    def check_in(self, request, pk, *args, **kwargs):
        flow = self.flow_class(self.get_object())

        try:
            flow.check_in()
            serializer = VisitDetailSerializer(self.get_object(), context={"request": request}, read_only=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except viewflow.fsm.TransitionNotAllowed as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=None,
        responses={200: VisitDetailSerializer},
        examples=[OpenApiExample("Check-out Response", summary="Example of a check-out response", value={})],
    )
    @action(detail=True, methods=["patch"])
    def check_out(self, request, pk, *args, **kwargs):
        flow = self.flow_class(self.get_object())

        try:
            flow.check_out()
            serializer = VisitDetailSerializer(self.get_object(), context={"request": request}, read_only=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except viewflow.fsm.TransitionNotAllowed as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
