from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from . models import Event, Venue
from . forms import VenueForm, EventForm
from django.http import HttpResponse
import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Generate PDF File Venue List
def venue_pdf(request):
    #Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    venues = Venue.objects.all()
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("=======================")
    # Loop
    for line in lines:
        textob.textLine(line)
    # Finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


# Generate CSV File Venue List
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate The Model
    venues = Venue.objects.all()

    # Add column headings to the csv file
    writer.writerow(['ID','Venue Name', 'Address', 'Zip Code', 'Phone', 'Website', 'Email'])

    # Create blank list
    lines = []
    # Loop and output
    for venue in venues:
        writer.writerow([venue.id, venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
    
    return response


# Generate Text File Venue List
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
# Designate The Model
    venues = Venue.objects.all()
    # Create blank list
    lines = []
    # Loop and output
    for venue in venues:
        lines.append(f'Venue Name: {venue.name}\nAddress: {venue.address}\nZip Code: {venue.zip_code}\nPhone: {venue.phone}\nWebsite: {venue.web}\nEmail: {venue.email_address}\n\n\n')
    # Write To TextFile
    response.writelines(lines)
    return response


# Delete Venue
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venues')


# Delete an Event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list_events')


def add_event(request):
    submitted = False
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    
    context = {
        'form': form,
        'submitted': submitted,
    }
    return render(request, 'events/add_event.html', context)


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list_events')
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'events/update_event.html', context)



def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')
    context = {
        'venue': venue,
        'form': form,
    }
    return render(request, 'events/update_venue.html', context)


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        context = {
            'searched': searched,
            'venues': venues,
        }
        return render(request, 'events/search_venues.html', context)
    else:
        return render(request, 'events/search_venues.html', {})



def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    context = {
        'venue': venue,
    }
    return render(request, 'events/show_venue.html', context)


def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')
    context = {
        'venue_list': venue_list,
    }
    return render(request, 'events/venue.html', context)


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    
    context = {
        'form': form,
        'submitted': submitted,
    }
    return render(request, 'events/add_venue.html', context)


def list_events(request):
    events = Event.objects.all().order_by('event_date')
    context = {
        'events': events,
    }
    return render(request, 'events/event_list.html', context)




def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = 'Nikola'
    month = month.title()
    # convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    #create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)
    now = datetime.now()
    current_year = now.year

    #get current time
    time = now.strftime('%I:%M %p')

    context = {
        'name': name,
        'year': year,
        'month': month,
        'month_number': month_number,
        'cal': cal,
        'current_year': current_year,
        'time': time,
    }
    
    return render(request, 'events/home.html', context)