from rest_framework import serializers

from labeling_app_rest.exceptions import InvalidImageCategory, InvalidBoundingBox
from labeling_app_rest.models import Image, ImageCategories, Category, BoundingBox


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.IntegerField(source='img_id', read_only=True)
    image_url = serializers.CharField(source='img_location', read_only=True)
    class Meta:
        model = Image
        fields = ('image', 'image_url')


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(source='cat_id', read_only=True)
    description = serializers.CharField(source='cat_description', read_only=True)
    class Meta:
        model = Category
        fields = ('category','description')


class ImageCategoriesSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=False, source='ict_cat')
    image = ImageSerializer(read_only=True, many=False, source='ict_img')
    image_category = serializers.IntegerField(read_only=True, source='ict_id')
    class Meta:
        model = ImageCategories
        fields = ('image', 'category','image_category')


class BoundingBoxRequestSerializer(serializers.ModelSerializer):
    image_category = serializers.IntegerField(source='bbx_img_cat_id')
    x = serializers.FloatField(source='bbx_x')
    y = serializers.FloatField(source='bbx_y')
    height = serializers.FloatField(source='bbx_height')
    width = serializers.FloatField(source='bbx_width')

    def save(self):
        try:
            image_category = ImageCategories.objects.get(pk=self.validated_data['bbx_img_cat_id'])
        except ImageCategories.DoesNotExist:
            raise InvalidImageCategory()

        if image_category.ict_added_bb:
            return

        image_category.ict_added_bb = True
        image_category.save()
        x = self.validated_data['bbx_x']
        y = self.validated_data['bbx_y']
        width = self.validated_data['bbx_width']
        height = self.validated_data['bbx_height']
        bb = BoundingBox(bbx_img_cat_id=image_category, bbx_x=x, bbx_y=y, bbx_height=height, bbx_width=width)
        bb.save()


    class Meta:
        model = BoundingBox
        fields = ('image_category', 'x', 'y', 'width', 'height')


class BoundingBoxSerializer(serializers.ModelSerializer):
    image_category = ImageCategoriesSerializer(source='bbx_img_cat_id')
    x = serializers.FloatField(source='bbx_x')
    y = serializers.FloatField(source='bbx_y')
    height = serializers.FloatField(source='bbx_height')
    width = serializers.FloatField(source='bbx_width')
    bb_id = serializers.IntegerField(source='bbx_id')

    class Meta:
        model = BoundingBox
        fields = ('image_category', 'x', 'y', 'width', 'height','bb_id')


class VerifiedBoundingBoxSerializer(serializers.Serializer):
    bb_id = serializers.IntegerField()
    correct = serializers.BooleanField()

    def create(self, validated_data):
        try:
            bounding_box = BoundingBox.objects.get(pk=validated_data['bb_id'])
        except BoundingBox.DoesNotExist:
            raise InvalidBoundingBox()

        bounding_box.bbx_reviewed = True
        bounding_box.bbx_verified = validated_data['correct']
        bounding_box.save()
        return bounding_box
    class Meta:
        fields = ('bb_id', 'correct')


class BoundingBoxWithCategorySerializer(serializers.Serializer):
    image_category = serializers.IntegerField()
    x = serializers.FloatField()
    y = serializers.FloatField()
    height = serializers.FloatField()
    width = serializers.FloatField()
    category = serializers.IntegerField()

    def create(self, validated_data):
        try:
            image_category = ImageCategories.objects.get(pk=validated_data['image_category'])
        except ImageCategories.DoesNotExist:
            raise InvalidImageCategory()
        try:
            new_category = Category.objects.get(pk=validated_data["category"])
        except Category.DoesNotExist:
            raise InvalidImageCategory()

        if image_category.ict_added_bb:
            return image_category

        image_category.ict_added_bb = True
        image_category.ict_cat = new_category
        image_category.save()
        x = validated_data['x']
        y = validated_data['y']
        width = validated_data['width']
        height = validated_data['height']
        bb = BoundingBox(bbx_img_cat_id=image_category, bbx_x=x, bbx_y=y, bbx_height=height, bbx_width=width)
        bb.save()
        return bb

    class Meta:
        fields = ('image_category', 'x', 'y', 'width', 'height', 'category')