#  ############## Django and Django Rest Framework imports ################
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from django.db.utils import OperationalError
from rest_framework.response import Response


#  ######################### Local apps imports ###########################
from android.utils import find_nearest_location
from android.serializers import (
    TempClientLocationsSerializer,
    TempRecordsSerializer,
    CriminalsSerializer,
    CameraSerializer,
)
from android.models import (
    TempClientLocations,
    TempRecords,
    Criminals,
    UniqueKey,
    Camera,
)
import uuid


class AndroidRequestHandlerAPIView(ModelViewSet):
    model = TempClientLocations
    lookup_field = "pk"
    queryset = TempClientLocations.objects.all()
    serializer_class = TempClientLocationsSerializer

    def create(self, request, *args, **kwargs):
        uuid = request.headers.get("token", None)
        if uuid is None:
            return Response({"msg": "Token is not provided!"}, status=400)
        try:
            uuid_object = UniqueKey.objects.get(uuid=uuid)
        except UniqueKey.DoesNotExist:
            return Response({"msg": "Invalid token provided!"}, status=400)
        except Exception:
            return Response({"msg": "Unknown error occued, try again"}, status=422)
        uuid_object.delete()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        longitude = serializer.validated_data.get("longitude")
        latitude = serializer.validated_data.get("latitude")
        clients = list(self.queryset.values())
        print(clients)
        if (latitude not in [key.get("latitude") for key in clients]) and (
            longitude not in [key.get("longitude") for key in clients]
        ):
            try:
                pk = self.model.objects.create(longitude=longitude, latitude=latitude)
                return Response(
                    {"msg": "Client connected", "client_pk": pk.pk}, status=201
                )
            except Exception as error:
                print("Passing delete because of: ", error)
                pass
        return Response({"msg": "Error occured!"}, status=422)

    def list(self, request, *args, **kwargs):
        try:
            query = TempRecords.objects.all().first()
            headers = request.headers
            longitude = headers.get("longitude", None)
            latitude = headers.get("latitude", None)
            if longitude is None or latitude is None:
                return Response(
                    {"msg": "Longitude or Latitude is not provided in headers"}
                )

            clients = list(self.queryset.values())
            camera = TempRecords.objects.all().first()
            if camera is not None:
                print("Camera: ", camera)
                camera = camera.record.camera
            else:
                return Response({})
            camera_object = Camera.objects.get(pk=camera.pk)
            print("Camera object: ", camera_object)
            print("Long cm: ", camera_object.longitude)
            print("Lat cm: ", camera_object.latitude)
            target_location = {
                "longitude": camera_object.longitude,
                "latitude": camera_object.latitude,
            }
            print("Clients: ", clients)
            if not clients or clients is None:
                return Response({"msg": "No clients connected yet!"}, status=422)
            nearest_location = find_nearest_location(target_location, clients)
            if (float(nearest_location.get("longitude")) == float(longitude)) and (
                float(nearest_location.get("latitude") == float(latitude))
            ):
                TempRecords.objects.all().delete()
                return Response(TempRecordsSerializer(query).data)
            return Response({})
        except OperationalError:
            return Response({})

    def destroy(self, request, pk, *args, **kwargs):
        headers = request.headers
        if "longitude" not in headers.keys() or "latitude" not in headers.keys():
            return Response(
                {"msg": "Required headers not provided: longitude & latitude"}
            )

        client = TempClientLocations.objects.get(pk=pk)
        if not client:
            return Response({"msg": f"Client with id: {pk} not found!"}, status=404)
        client.delete()
        return Response(status=204)


@api_view(http_method_names=["GET"])
def fully_fetched_data(request):
    clients = TempClientLocations.objects.all()
    serializer = TempClientLocationsSerializer(instance=clients, many=True)
    return Response(serializer.data, status=200)


@api_view(http_method_names=["GET"])
def fetch_camera(request):
    clients = Camera.objects.all()
    serializer = CameraSerializer(instance=clients, many=True)
    return Response(serializer.data, status=200)


@api_view(http_method_names=["GET"])
def fetch_criminals(request):
    clients = Criminals.objects.all()
    serializer = CriminalsSerializer(instance=clients, many=True)
    return Response(serializer.data, status=200)


@api_view(http_method_names=["GET"])
def generate_token(request):
    token = uuid.uuid4()
    UniqueKey.objects.get_or_create(uuid=token)
    return Response({"token": token})
