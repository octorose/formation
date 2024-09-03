from django.core.management.base import BaseCommand
from django.db.models import Count
from api.models import Agent

class Command(BaseCommand):
    help = 'Fix redundant emails by appending the user ID to each redundant email'

    def handle(self, *args, **kwargs):
        # Get all email counts greater than 1 (i.e., redundant emails)
        redundant_emails = (
            Agent.objects.values('email')
            .annotate(email_count=Count('email'))
            .filter(email_count__gt=1)
        )

        for email_entry in redundant_emails:
            email = email_entry['email']
            agents_with_email = Agent.objects.filter(email=email)
            
            # Skip the first occurrence
            first = True
            for agent in agents_with_email:
                if not first:
                    new_email = f"{email.split('@')[0]}+{agent.id}@{email.split('@')[1]}"
                    agent.email = new_email
                    agent.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated email for Agent ID {agent.id}: {new_email}'))
                else:
                    first = False
        
        self.stdout.write(self.style.SUCCESS('All redundant emails have been fixed.'))
