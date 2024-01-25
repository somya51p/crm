from rest_framework.viewsets import ModelViewSet
from .models import Lead
from .serializers import LeadSerializer
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class LeadAPIViewSet(ModelViewSet):
    """
        API endpoint that allows Leads to be viewed or edited.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'email', 'age', 'hotel_name', 'hotel_address', 'phone_number', 'url', 'description', 'category__name', 'agent__first_name']
    ordering_fields = ['first_name', 'last_name', 'email', 'age', 'hotel_name', 'hotel_address', 'phone_number', 'url', 'description', 'category__name', 'agent__first_name']
    filterset_fields = ['first_name', 'last_name', 'email', 'age', 'hotel_name', 'hotel_address', 'phone_number', 'url', 'description', 'category__name', 'agent__first_name']

    def list(self, request, *args, **kwargs):
        """
            Return a list of all Leads from database.
        """
        # give paginated response according to super user and normal user
        if request.user.is_superuser or request.user.role == 'admin':
            queryset = Lead.objects.all()
        elif request.user.is_authenticated:
            queryset = Lead.objects.filter(agent=request.user)
        else:
            queryset = Lead.objects.none()

        serializer = LeadSerializer(queryset, many=True)
        page=self.paginate_queryset(queryset)
        if page is not None:
            serializer = LeadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
            Create a Lead on database.
        """
        phone_number = request.data.get('phone_number')
        if phone_number:
            leads = Lead.objects.filter(phone_number=phone_number)
            if leads:
                lead = leads[0]
                serializer = LeadSerializer(lead)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
            Return a Lead from database.
        """
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
            Applies partial update to a Lead.
        """
        if request.user.is_superuser:
            return super().partial_update(request, *args, **kwargs)
        elif request.user.is_authenticated:
            lead = self.get_object()
            if lead.agent == request.user or request.user.role == 'admin':
                return super().partial_update(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    def destroy(self, request, *args, **kwargs):
        """
            Delete a Lead from database.
        """
        if request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        elif request.user.is_authenticated:
            lead = self.get_object()
            if lead.agent == request.user or request.user.role == 'admin': 
                return super().destroy(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)