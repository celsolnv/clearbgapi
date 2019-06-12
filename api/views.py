from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.RemoveBg import RemoveBg
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys

@csrf_exempt
def indexApi(request):
    if request.method == 'POST':
        print("---------------------------------")
        print("POST: ",request.POST['size'])
        print("files: ",request.FILES['image_file'])
        print("Headers: ",request.headers['X-Api-Key'])
        print("---------------------------------")
        print(request)

        # chave = request.headers['X-Api-Key']
        # tam = request.POST['size']
    
        fileUpload = request.FILES['image_file']
        image = fileUpload.read()

        modelType = "mobile_net_model" #Abordagem mais rápida
        removebg = RemoveBg(modelType)
        nameFileEdit = "no-bg.png"
        imgEditada = removebg.removeBackground(image) 

        # imgEditada = Image.fromarray(imageWithoutBg)

        tempfile_io =BytesIO()
        
        imgEditada.save(tempfile_io, format='PNG')
        
        cache = InMemoryUploadedFile(tempfile_io,None,nameFileEdit,"image/png", sys.getsizeof(imgEditada),None)

        response = HttpResponse(cache)
        return response        
        
    return HttpResponse("Hello, world. You're at the polls index.")

