import logging
import viewflow

from drf_spectacular.utils import (
    OpenApiTypes,
    extend_schema,
    OpenApiExample
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


from clinic.visits.flows import VisitFlow


logger = logging.getLogger(__name__)

class VisitFlowViewMixin:
    flow_class = VisitFlow
    
    @extend_schema(
        request=OpenApiTypes.OBJECT,
        responses=None,
        examples=[
            OpenApiExample(
                'Cancel Request',
                summary='Example of a cancel request',
                value={'reason': 'string'}
            ),
        ]
    )
    @action(detail=True, methods=["patch"])
    def cancel(self, request, pk, *args, **kwargs):
        flow = self.flow_class(self.get_object())
        
        try:
            flow.cancel(reason=request.data.get("reason"))
            return Response(status=status.HTTP_200_OK)
        except viewflow.fsm.TransitionNotAllowed as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=None,
        responses=None,
        examples=[
            OpenApiExample(
                'Check-in Response',
                summary='Example of a check-in response',
                value={}
            )
        ]
    )
    @action(detail=True, methods=["patch"])
    def check_in(self, request, pk, *args, **kwargs):
        flow = self.flow_class(self.get_object())
        
        try:
            flow.check_in()
            return Response(status=status.HTTP_200_OK)
        except viewflow.fsm.TransitionNotAllowed as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=None,
        responses=None,
        examples=[
            OpenApiExample(
                'Check-out Response',
                summary='Example of a check-out response',
                value={}
            )
        ]
    )
    @action(detail=True, methods=["patch"])
    def check_out(self, request, pk, *args, **kwargs):
        flow = self.flow_class(self.get_object())
        
        try:
            flow.check_out()
            return Response(status=status.HTTP_200_OK)
        except viewflow.fsm.TransitionNotAllowed as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(
        request=None,
        responses=None,
        examples=[
            OpenApiExample(
                'Financially Clear Response',
                summary='Example of a financially clear response',
                value={}
            )
        ]
    )
    @action(detail=True, methods=["patch"])
    def financially_clear(self, request, pk, *args, **kwargs):
        flow = self.flow_class(self.get_object())
        
        try:
            flow.financially_clear()
            return Response(status=status.HTTP_200_OK)
        except viewflow.fsm.TransitionNotAllowed as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)