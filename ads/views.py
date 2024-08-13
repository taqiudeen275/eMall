# views.py
from django.http import JsonResponse
from django.utils import timezone
from dashboard.models import Ad
import random

def get_popup_ad(request):
    now = timezone.now()
    active_ads = Ad.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now,
        position='popup'  # Add this position to your POSITION_CHOICES in the Ad model
    )
    
    if active_ads.exists():
        ad = random.choice(active_ads)
        ad.impressions += 1
        ad.save()
        
        return JsonResponse({
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'image_url': ad.image.url,
            'url': ad.url
        })
    else:
        return JsonResponse({}, status=404)

def record_ad_click(request, ad_id):
    try:
        ad = Ad.objects.get(id=ad_id)
        ad.clicks += 1
        ad.save()
        return JsonResponse({'status': 'success'})
    except Ad.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)