from ipware import get_client_ip

def get_ip(request):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        # it's necessary LOG this information
        return request.META.get('REMOTE_ADDR')
    else:
        return client_ip
