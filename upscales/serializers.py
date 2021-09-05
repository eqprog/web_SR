from rest_framework import serializers
from .models import Upscale


class UpscaleSerializer(serializers.ModelSerializer):
    gt = serializers.ImageField(allow_empty_file=False)
    name = serializers.CharField(
        required=False, allow_blank=True, max_length=100)
    upscale_model = serializers.ChoiceField(
        choices=Upscale.upscale_model_choices())
    upscaled_image = serializers.ImageField(
        allow_empty_file=True, required=False, read_only=True)

    class Meta:
        model = Upscale
        fields = ('gt', 'name', 'upscale_model', 'upscaled_image')
        # read_only_fields = ['upscaled_image', ]

    def create(self, validated_data):
        return Upscale.objects.create(**validated_data)
