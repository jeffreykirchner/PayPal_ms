
import logging
from main.models import Ip_whitelist

#check for IP on white list
def get_whitelist_ip(request):
    logger = logging.getLogger(__name__) 

    remote_ip = request.META["REMOTE_ADDR"]

    ip_whitelist=Ip_whitelist.objects.filter(ip_address=remote_ip)

    if ip_whitelist.count() == 0:
        logger.warning(f"get_whitelist_ip not found: {remote_ip}")
        return None
    else:
        logger.info(f"get_whitelist_ip : {remote_ip} {ip_whitelist}")
        return ip_whitelist.first()
        
    