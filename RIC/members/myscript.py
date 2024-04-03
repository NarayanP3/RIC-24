
from models import RICEvent, IC, WorkshopBio


# Create your views here.

from django.contrib.auth import get_user_model

def update_workshop_bio():
    bios = WorkshopBio.objects.all()
    counts = 0
    for bio in bios:
        user = User.objects.get(email=bio.owner.email)
        bio.email = user.email
        bio.name = user.get_full_name()
        bio.save()
        counts +=1
    # return render(request, 'members/registrations_count.html', {'counts': counts})
    # return HttpResponse('WorkshopBio objects updated successfully.')

User = get_user_model()

def update_names_and_emails():
    events = RICEvent.objects.all()
    count = 0
    for event in events:
        count+=1
        owner = User.objects.get(id=event.owner_id)
        if event.name == 'Name':
            event.name = owner.get_full_name()
            event.email = owner.email
        event.save()
    # return HttpResponse("Names and emails updated successfully"+str(count))


def update_ic_fees():
    # Filter participants with "EMPRENDIMIENTO" event
    participants = IC.objects.filter(event__name="EMPRENDIMIENTO")

    # Update fees for each participant
    for participant in participants:
        participant.total = 50000  # Update fee to 1000 (or whatever value you want)
        participant.save()

    # return HttpResponse(f"Fees updated for {len(participants)} participants.")


update_ic_fees()
update_names_and_emails()
update_workshop_bios()

