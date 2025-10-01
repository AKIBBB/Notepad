from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'accounts/home.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
from django.http import HttpResponse
from django.utils.html import strip_tags

@login_required
def notes_view(request):
    if request.method == "POST":
        form = NoteForm(request.POST,request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.text = strip_tags(note.text)
            # Handle canvas drawing
            drawing_data = request.POST.get('drawing')
            if drawing_data:
                format, imgstr = drawing_data.split(';base64,')
                ext = format.split('/')[-1]
                note.drawing.save(f'note_{request.user.id}_{Note.objects.count()}.{ext}',
                                  ContentFile(base64.b64decode(imgstr)), save=False)
            note.save()
            return redirect('notes')
    else:
        form = NoteForm()

    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/notes.html', {'form': form, 'notes': notes})



from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from .models import Note
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import NoteForm
from .models import Note
from django.core.files.base import ContentFile
import base64
@login_required
def notes(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            drawing_data = request.POST.get("drawing", "")
            if drawing_data and drawing_data != "data:,":
                try:
                    format, imgstr = drawing_data.split(';base64,')
                    ext = format.split('/')[-1]  # png
                    file_name = f"drawing_{note.id}.{ext}"
                    note.drawing.save(file_name, ContentFile(base64.b64decode(imgstr)), save=False)
                    note.save()
                except Exception as e:
                    print("Error saving drawing:", e)

            return redirect("notes")
    else:
        form = NoteForm()

    user_notes = Note.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "accounts/notes.html", {"form": form, "notes": user_notes})


@login_required
def download_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=note_{note.id}.pdf'

    pdf = pdf_canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Draw the text
    text_object = pdf.beginText(50, height - 50)
    text_object.setFont("Helvetica", 12)
    for line in note.text.splitlines():
        text_object.textLine(line)
    pdf.drawText(text_object)

    # Draw the image if exists
    if note.drawing:
        drawing_path = note.drawing.path
        if os.path.exists(drawing_path):
            img = ImageReader(drawing_path)
            pdf.drawImage(img, 50, height/2 - 100, width=500, height=200)  # Adjust size & position

    pdf.showPage()
    pdf.save()
    return response



# views.py
@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes')
    else:
        form = NoteForm(instance=note)
    return render(request, 'accounts/edit_note.html', {'form': form, 'note': note})



@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect("notes")




