# Create this file as: your_app/management/commands/fix_chat_responses.py

from django.core.management.base import BaseCommand
from chatbot.models import Chat  # Replace 'your_app' with your actual app name
import re

class Command(BaseCommand):
    help = 'Fix existing chat responses by cleaning up formatting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without actually changing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Get all chats with responses that need cleaning
        chats = Chat.objects.filter(response__icontains='🤖 Gemini Response:')
        
        self.stdout.write(f"Found {chats.count()} chats that need updating")
        
        updated_count = 0
        
        for chat in chats:
            old_response = chat.response
            
            # Clean up the response
            new_response = self.clean_response(old_response)
            
            if old_response != new_response:
                if dry_run:
                    self.stdout.write(f"Would update chat {chat.id}:")
                    self.stdout.write(f"  Old: {old_response[:100]}...")
                    self.stdout.write(f"  New: {new_response[:100]}...")
                    self.stdout.write("---")
                else:
                    chat.response = new_response
                    chat.save()
                    self.stdout.write(f"Updated chat {chat.id}")
                
                updated_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'Dry run completed. Would update {updated_count} chats.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {updated_count} chats.')
            )

    def clean_response(self, response_text):
        """
        Clean up the response text by removing prefixes and excessive formatting
        """
        if not response_text:
            return response_text
        
        # Remove the Gemini prefix
        cleaned = response_text.replace("🤖 Gemini Response:", "").strip()
        
        # Remove excessive newlines
        cleaned = re.sub(r'\n{4,}', '\n\n\n', cleaned)
        
        # Clean up whitespace at the beginning of lines
        cleaned = re.sub(r'\n\s+', '\n', cleaned)
        
        return cleaned.strip()

# To run this command:
# python manage.py fix_chat_responses --dry-run  (to see what would change)
# python manage.py fix_chat_responses  (to actually make the changes)