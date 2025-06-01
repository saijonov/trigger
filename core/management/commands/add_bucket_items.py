from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import BucketListItem

class Command(BaseCommand):
    help = 'Adds predefined bucket list items to the database'

    def handle(self, *args, **options):
        # Get or create a system user for these items
        system_user, created = User.objects.get_or_create(
            username='system',
            defaults={'is_staff': True}
        )
        
        bucket_items = [
            "Record a 'day in your life' on camera",
            "Visit a cemetery to reflect on time and life",
            "Go to the cinema early in the morning when it's empty",
            "Watch the sunrise from a high point",
            "Take a trip without a plan",
            "Spend a night under the stars",
            "Make something with your own hands",
            "Attend a charity event",
            "Go to a play or concert",
            "Watch a cult classic movie",
            "Spend a day without the internet",
            "Create a vision board",
            "Make a photo album",
            "Write a letter to your future self",
            "Re-read an inspiring book",
            "Learn and cook a new dish",
            "Plant a tree or plant",
            "Declutter and make your space cozy",
            "Try meditation",
            "Make a gratitude list",
            "Have a spa day (sauna, massage)",
            "Visit a museum",
            "Spend a day on a farm",
            "Start journaling",
            "Revisit an old hobby",
            "Create a family tree",
            "Order flowers for yourself",
            "Learn a poem you like",
            "Have a day of silence",
            "Visit an unusual restaurant",
            "Go to a stand-up comedy show",
            "Visit a temple or cathedral",
            "Write down your life goals",
            "Take a course on a topic that interests you",
            "Start collecting something",
            "Try a dance or singing class (private session)",
            "Take psychological tests",
            "Take the best bath of your life",
            "Create a playlist of motivational songs",
            "Try a vipassana retreat",
            "Watch a documentary about our planet",
            "Get a notebook and write everything that comes to mind",
            "Learn a new skill",
            "Create a mood board for your clothing style",
            "Host your own tea ceremony",
            "Write your own short book",
            "Try waking up at 5 AM",
            "Learn origami",
            "Ask for forgiveness if needed",
            "Do a random act of kindness"
        ]

        for item in bucket_items:
            BucketListItem.objects.get_or_create(
                title=item,
                defaults={
                    'description': f"A bucket list item to {item.lower()}",
                    'created_by': system_user,
                    'is_approved': True
                }
            )
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {len(bucket_items)} bucket list items')
        ) 