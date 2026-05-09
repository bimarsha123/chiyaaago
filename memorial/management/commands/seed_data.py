from django.core.management.base import BaseCommand
from memorial.models import Martyr, TimelineEvent, WitnessAccount, Pillar, SiteSetting


class Command(BaseCommand):
    help = "Seed the database with initial memorial data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Create Pillars
        pillars_data = [
            {
                "title": "Remember",
                "description": "We carry the names, the faces, the stories of those who gave everything. Their sacrifice is the foundation of our memory.",
                "icon": "Megaphone",
                "order": 1,
            },
            {
                "title": "Honour",
                "description": "Not with empty words, but with action. Every demand they had, every injustice they fought — we continue that fight.",
                "icon": "Shield",
                "order": 2,
            },
            {
                "title": "Rebuild",
                "description": "From the ashes of that September, a new Nepal rises. The generation they believed in is building the future they deserved.",
                "icon": "HandHeart",
                "order": 3,
            },
        ]

        for p in pillars_data:
            Pillar.objects.get_or_create(title=p["title"], defaults=p)

        # Create Timeline Events
        sept8_events = [
            {"time_of_day": "Morning", "event": "Gen Z protesters gathered across Nepal demanding accountability", "order": 1},
            {"time_of_day": "Afternoon", "event": "Peaceful demonstrations grew as thousands joined the streets", "order": 2},
            {"time_of_day": "Evening", "event": "Confrontation escalated — the first martyrs fell", "order": 3},
        ]

        for e in sept8_events:
            TimelineEvent.objects.get_or_create(
                date=TimelineEvent.DateChoice.SEPT_8,
                time_of_day=e["time_of_day"],
                defaults={"event": e["event"], "order": e["order"]},
            )

        sept9_events = [
            {"time_of_day": "Dawn", "event": "Fires broke out across multiple locations in the aftermath", "order": 1},
            {"time_of_day": "Morning", "event": "Emergency services overwhelmed as the flames spread", "order": 2},
            {"time_of_day": "Night", "event": "The nation grieved — more lives were lost to the fire", "order": 3},
        ]

        for e in sept9_events:
            TimelineEvent.objects.get_or_create(
                date=TimelineEvent.DateChoice.SEPT_9,
                time_of_day=e["time_of_day"],
                defaults={"event": e["event"], "order": e["order"]},
            )

        # Create Site Settings
        settings_data = [
            {"key": "hero_title", "value": "They Stood. We Remember.", "description": "Main hero heading"},
            {"key": "memorial_location", "value": "Jhamsikhel, Lalitpur, Nepal", "description": "Memorial location"},
            {"key": "memorial_hours", "value": "Open daily, dawn to dusk", "description": "Memorial operating hours"},
        ]

        for s in settings_data:
            SiteSetting.objects.get_or_create(key=s["key"], defaults=s)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
        self.stdout.write(f"  - {Pillar.objects.count()} pillars created")
        self.stdout.write(f"  - {TimelineEvent.objects.count()} timeline events created")
        self.stdout.write(f"  - {SiteSetting.objects.count()} site settings created")
