from users.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action

from users.serializers import UserSerializer
from users.utils import create_users_from_excel_file
import mimetypes

CONTENT_TYPES = [
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
]


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [TemplateHTMLRenderer]

    @action(
        methods=["POST", "GET"],
        url_path="excel-upload",
        url_name="excel-upload",
        detail=False,
    )
    def excel_upload(self, request):
        error = None

        if "GET" == request.method:
            return Response({}, template_name="excel_upload.html")

        excel_file = request.data["file"]

        if not excel_file.content_type in CONTENT_TYPES:
            error = f"{excel_file.name} not allowed, please upload an excel file"

        if not error:
            excel_data, error = create_users_from_excel_file(excel_file)
        else:
            excel_data = []

        return Response(
            {"excel_data": excel_data, "error": error},
            template_name="excel_upload.html",
        )
