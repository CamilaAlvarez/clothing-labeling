from django.db.models.signals import post_save
from django.dispatch import receiver
from threading import Timer
from labeling_app_rest.models import ImageCategories
import logging
import sys

logger = logging.getLogger("clothing_labeling")
ch = logging.StreamHandler(sys.stderr)
logger.addHandler(ch)


@receiver(post_save, sender=ImageCategories)
def turn_timer(instance, *args, **kwargs):
    def timeout():
        instance.ict_taken_for_labeling = False
        instance.save()
        logger.info("Updated database beacuse of timer")
    logger.info("Timer On")
    t = Timer(120, timeout)
    t.start()