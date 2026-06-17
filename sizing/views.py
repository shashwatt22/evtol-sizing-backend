from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .main import (calculate_multirotor, calculate_tiltrotor, calculate_lift_plus_cruise, calculate_smr)

@csrf_exempt
def home(request):
    print("[DEBUG] Received a request at / with method:", request.method)
    print("[INFO] Server is running!")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({'message': 'POST received at root!', 'data': data})
        except Exception as e:
            return JsonResponse({'error': f'JSON parse error: {str(e)}'}, status=400)

    return HttpResponse("Backend is running")

@csrf_exempt
def rotor_sizing_api(request):
    print("[DEBUG] /api/size/ called with method:", request.method)
    print("[DEBUG] Headers:", dict(request.headers))
    print("[DEBUG] Body:", request.body)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("[DEBUG] Parsed JSON:", data)
        except Exception as e:
            print("[ERROR] JSON parse error:", str(e))
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

        config_type = data.get('config_type')
        if not config_type:
            print("[ERROR] Missing config_type in data")
            return JsonResponse({'error': 'config_type is required'}, status=400)

        try:
            if config_type == "multirotor":
                results = calculate_multirotor(data)
            elif config_type == "liftpluscruise":
                results = calculate_lift_plus_cruise(data)
            elif config_type == "tiltrotor":
                results = calculate_tiltrotor(data)
            elif config_type == "single_main_rotor":
                results = calculate_smr(data)
            else:
                print("[ERROR] Invalid config_type:", config_type)
                return JsonResponse({'error': 'Invalid config_type'}, status=400)
        except Exception as e:
            print("[ERROR] Calculation error:", str(e))
            return JsonResponse({'error': f'Calculation error: {str(e)}'}, status=500)

        print("[DEBUG] Calculation successful, results:", results)
        return JsonResponse({'results': results, 'message': 'Calculation successful'})

    print("[INFO] Non-POST request received at /api/size/")
    return HttpResponse("Rotor Sizing API. Send a POST request with JSON input.")
