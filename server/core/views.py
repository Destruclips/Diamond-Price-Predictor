# from django.shortcuts import render
# from django.http import HttpResponse
# from rest_framework.views import APIView
# from .models import Dimaond
# from .serializer import DiamondSerializer
# from rest_framework.response import Response
# import pickle
# import joblib
# from django.http import JsonResponse
# from django.views import View

# # Create your views here.

# class DiamondView(APIView):
#     def get(self, request):
#         # Take last entry from the database

#         diamond = Dimaond.objects.last()

#         with open('KNN_model.pkl','rb') as f:
#             modelk = pickle.load(f)
#         diamond.price1 = modelk.predict([[diamond.carat,diamond.cut,diamond.color,diamond.clarity,diamond.depth,diamond.table,diamond.X,diamond.Y,diamond.Z]])[0]

#         #load joblib file with joblib.load
#         modell = joblib.load('polynomialDiamond.joblib')
#         diamond.price2 = modell.predict([[diamond.carat,diamond.cut,diamond.table,diamond.clarity,diamond.color,diamond.X,diamond.Y,diamond.Z]])[0]
        

#         diamond ={
#             "X":diamond.X,
#             "Y":diamond.Y,
#             "Z":diamond.Z,
#             "carat":diamond.carat,
#             "depth":diamond.depth,
#             "table":diamond.table,
#             "price1":diamond.price1,
#             "price2":diamond.price2,
#             "price3":diamond.price3,
#             "cut":diamond.cut,
#             "color":diamond.color,
#             "clarity":diamond.clarity,

#         }
#         # Take last entry from the database
#         d = Dimaond.objects.last()
#         print(d)
#         return Response(diamond)
    
#     def post(self,request):
#         # only take the last entry from the database
        
#         serializer = DiamondSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)

from django.http import JsonResponse  # Add this import statement

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import Dimaond
from .serializer import DiamondSerializer
from rest_framework.response import Response
import pickle
import joblib
from sklearn.metrics.pairwise import euclidean_distances  # Import if used in the pickled model

# Create your views here.

# Create your views here.

class DiamondView(APIView):
    def get(self, request):
        # Take the last entry from the database
        diamond = Dimaond.objects.last()

        try:
            # Load the KNN model with pickle
            with open('KNN_model.pkl', 'rb') as f:
                modelk = pickle.load(f)

            # Predict price1
            diamond.price1 = modelk.predict([[diamond.carat, diamond.cut, diamond.color, diamond.clarity, diamond.depth, diamond.table, diamond.X, diamond.Y, diamond.Z]])[0]

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error loading KNN model: {str(e)}'}, status=500)

        try:
            # Load the polynomial model with joblib
            modell = joblib.load('polynomialDiamond.joblib')

            # Predict price2
            diamond.price2 = modell.predict([[diamond.carat, diamond.cut, diamond.table, diamond.clarity, diamond.color, diamond.X, diamond.Y, diamond.Z]])[0]

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error loading polynomial model: {str(e)}'}, status=500)

        # Construct the response dictionary
        diamond_data = {
            "X": diamond.X,
            "Y": diamond.Y,
            "Z": diamond.Z,
            "carat": diamond.carat,
            "depth": diamond.depth,
            "table": diamond.table,
            "price1": diamond.price1,
            "price2": diamond.price2,
            "price3": diamond.price3,
            "cut": diamond.cut,
            "color": diamond.color,
            "clarity": diamond.clarity,
        }

        # Print the last entry for debugging purposes
        d = Dimaond.objects.last()
        print(d)

        return Response(diamond_data)

    def post(self, request):
        # Only take the last entry from the database
        serializer = DiamondSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



        
    
        
        
    

