from testserver.settings import UPSCALE_MODELS
from django.db import models
from django.db.models.fields import files
from django.conf import settings
import PIL
from django.db.models.signals import post_delete, post_save, pre_save
import glob
import os
import upscale as ups
import logging
from pathlib import Path


class Upscale(models.Model):

    def upscale_model_choices():
        UPSCALE_MODELS = 'G:/upscaling utils/ESRGAN/ESRGAN/testserver/upscale_models'
        current_path = os.getcwd()
        os.chdir(UPSCALE_MODELS)
        models = glob.glob('*.pth')
        os.chdir(current_path)

        choices = []
        models_1x = []
        models_2x = []
        models_4x = []
        models_8x = []

        for model in models:
            if model.startswith('1x'):
                models_1x.append((model, model[:-4]))
                continue
            if model.startswith('2x'):
                models_2x.append((model, model[:-4]))
                continue
            if model.startswith('4x'):
                models_4x.append((model, model[:-4]))
                continue
            if model.startswith('8x'):
                models_8x.append((model, model[:-4]))

        choices = [
            ('1x', tuple(models_1x)),
            ('2x', tuple(models_2x)),
            ('4x', tuple(models_4x)),
            ('8x', tuple(models_8x)),
        ]
        return choices

    def image_folder(instance, filename):
        folder = os.path.splitext(filename)[0]
        return 'images/{0}/{1}'.format(folder, filename)

    gt = models.ImageField(upload_to=image_folder,
                           help_text="Maximum Resolution: 1024x1024",
                           blank=True)
    name = models.CharField(max_length=100, blank=True)
    upscale_model = models.CharField(
        max_length=100, choices=upscale_model_choices(), default='4x_lollypop')
    upscaled_image = models.ImageField(upload_to=gt.upload_to, blank=True)

    def pre_save(self, *args, **kwargs):
        if not os.path.exists(self.gt.upload_to):
            os.makedirs(self.gt.upload_to)
        return super().pre_save(*args, **kwargs)

    def save(self, *args, **kwargs):

        if not self.name:
            self.name = self.gt.name
        return super().save(*args, **kwargs)

    def __str__(self):
        return os.path.basename(self.gt.name)


def upscale_image(sender, instance, **kwargs):
    log = logging.getLogger("rich")
    upscale_model_path = os.path.join(
        settings.UPSCALE_MODELS[0], instance.upscale_model)
    input_path = Path(os.path.split(instance.gt.path)[0])
    output_path = Path(os.path.join(input_path, 'upscaled'))
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    esr = ups.Upscale(upscale_model_path, input_path, output_path, False, False,
                      ups.SeamlessOptions(
                          "replicate"), False, False, 0, True, False, False,
                      0.1, 0.1, 2, log)
    esr.run()

    name = os.path.splitext(instance.name)[0]
    Upscale.objects.filter(id=instance.id).update(
        upscaled_image=f'images/{name}/upscaled/{instance.name}')


post_save.connect(upscale_image, sender=Upscale)
