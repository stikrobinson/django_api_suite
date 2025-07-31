from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "solicitudes"

    def get(self, request):
      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      # get: Obtiene todos los elementos de la col ección
      data = ref.get()

      # Devuelve un arreglo JSON
      return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        # Obtiene los datos del cuerpo de la solicitud
        data = request.data

        # Agrega un campo de fecha y hora actual
        current_time  = datetime.now()
        data['timestamp'] = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')

        # push: Agrega un nuevo elemento a la colección
        new_resource = ref.push(data)

        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
