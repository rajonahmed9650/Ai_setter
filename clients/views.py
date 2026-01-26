from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Client
from sources.models import Source
from lead.models import Lead
from conversation.models import Conversation, Message
from lead.services.bot_service import send_to_bot
from notifications.services import handle_new_lead


class MessageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        external_id = request.data.get("external_id")
        if not external_id:
            return Response(
                {"error": "external_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        platform = request.data.get("platform", "test")
        text = request.data.get("message")

        if not text:
            return Response(
                {"error": "message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1️ Source
        source, _ = Source.objects.get_or_create(platform=platform)

        # 2️ Client
        client, _ = Client.objects.get_or_create(
            external_id=external_id,
            source_id=source
        )

        # 3️ Lead
        lead, _ = Lead.objects.get_or_create(
            client_id=client
        )

        # 4️ Conversation
        conversation, _ = Conversation.objects.get_or_create(
            lead_id=lead,
            source_id=source
        )

        # Ensure defaults
        # Ensure safe defaults BEFORE bot call
        if not conversation.current_state:
            conversation.current_state = "ENTRY"
        if not conversation.user_attributes:
            conversation.user_attributes = {}
        conversation.save()

        Message.objects.create(
            conversation_id=conversation,
            sender_type="client",
            message={"text": text}
        )
        handle_new_lead(
    client=client,
    user=request.user,
    source=source,
    text=text
)
       # BOT RESPONSE
        bot_response = send_to_bot(
            client_id=external_id,
            message=text,
            current_state=conversation.current_state,
            user_attributes=conversation.user_attributes,
        )
        # STATE UPDATE       
        conversation.current_state = bot_response.get(
            "next_state",
            conversation.current_state
        )

        # ATTRIBUTE MERGE ( CORE FIX)
    
        new_attrs = bot_response.get("extracted_attributes") or {}
        conversation.user_attributes.update(new_attrs)

        # SAVE MEMORY
        conversation.last_message = bot_response.get("reply")
        conversation.save()
        
        # 8️ Update Lead meta
        lead.last_response = timezone.now()
        lead.save()

        # 9️ Save BOT message
        Message.objects.create(
            conversation_id=conversation,
            sender_type="bot",
            message=bot_response
        )

        return Response(
            {
                "reply": bot_response.get("reply"),
                "next_state": conversation.current_state,
                "extracted_attributes": conversation.user_attributes,
            },
            status=status.HTTP_200_OK
        )
