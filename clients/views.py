from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
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

        comment_id = request.data.get("comment_id")
        print("MESSAGEVIEW COMMENT_ID:", comment_id)

        external_id = request.data.get("external_id")
        text = request.data.get("message")
        platform = request.data.get("platform", "test")
        page_id = request.data.get("page_id")
        sender_name = request.data.get("sender_name")


        if not external_id or not text:
            return Response(
                {"error": "external_id and message required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if comment_id:
            source_type = "post_comment"
        else:
            source_type = "dm"
        source, _ = Source.objects.get_or_create(
            platform=platform,
            source_type=source_type,
        )
   
        # update app_id if missing
        if page_id and not source.app_id:
            source.app_id = page_id
            source.save()

        client, _ = Client.objects.get_or_create(
            external_id=external_id,
            source_id=source
        )

        if sender_name and not client.name:
            client.name = sender_name
            client.save()
                               
        elif not client.name:
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
                comment_id=comment_id
            )
        )

        return Response(
            {"status": "buffered"},
            status=status.HTTP_200_OK
        )
