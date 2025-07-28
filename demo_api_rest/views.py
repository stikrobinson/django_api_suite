from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
   name = "Demo REST API"

   def get(self, request):
      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)
    
   def post(self, request):
      data = request.data

      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

class DemoRestApiItem(APIView):
    """
    Vista para manejar PUT, PATCH y DELETE sobre un elemento identificado por su id.
    """

    def get_object(self, item_id):
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None

    def put(self, request, item_id):
        item = self.get_object(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if 'id' not in data or data['id'] != item_id:
            return Response({'error': 'El campo id es obligatorio y debe coincidir.'}, status=status.HTTP_400_BAD_REQUEST)
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        # Reemplaza todos los campos excepto el id
        item.update({
            'name': data['name'],
            'email': data['email'],
            'is_active': data.get('is_active', True)
        })
        return Response({'message': 'Elemento actualizado correctamente.', 'data': item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        item = self.get_object(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        # Solo actualiza los campos presentes en la petición
        for field in ['name', 'email', 'is_active']:
            if field in data:
                item[field] = data[field]
        return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        item = self.get_object(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        if not item.get('is_active', True):
            return Response({'error': 'El elemento ya está inactivo.'}, status=status.HTTP_400_BAD_REQUEST)
        item['is_active'] = False
        return Response({'message': 'Elemento eliminado lógicamente.'}, status=status.HTTP_200_OK)