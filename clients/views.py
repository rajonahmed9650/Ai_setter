from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from sources.models import Source
from .models import Client
from lead.models import Lead
from conversation.models import Conversation
from .services.fetch_client_info import fetch_sender_name

from .services.message_buffer import buffer_message, start_debounce,process_combined_message



class MessageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        external_id = request.data.get("external_id")
        text = request.data.get("message")
        platform = request.data.get("platform", "test")
        page_id = request.data.get("page_id")

        if not external_id or not text:
            return Response(
                {"error": "external_id and message required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        source, _ = Source.objects.get_or_create(
            platform=platform,
            defaults={"page_id": page_id}
        )
        source.app_id = page_id
        source.save()

        client, _ = Client.objects.get_or_create(
            external_id=external_id,
            source_id=source
        )

        if not client.name:
            name = fetch_sender_name(external_id)
            if name:
                client.name = name
                client.save()

        lead, _ = Lead.objects.get_or_create(client_id=client)

        conversation, _ = Conversation.objects.get_or_create(
            lead_id=lead,
            source_id=source
        )

        if not conversation.current_state:
            conversation.current_state = "ENTRY"
        if not conversation.user_attributes:
            conversation.user_attributes = {}
        conversation.save()

        # 🔹 BUFFER + DEBOUNCE
        buffer_message(platform, external_id, text)

        start_debounce(
            platform,
            external_id,
            process_func=lambda combined_text: process_combined_message(
                combined_text=combined_text,
                external_id=external_id,
                source=source,
                client=client,
                lead=lead,
                conversation=conversation,
                request_user=request.user,
            )
        )

        return Response(
            {"status": "buffered"},
            status=status.HTTP_200_OK
        )
