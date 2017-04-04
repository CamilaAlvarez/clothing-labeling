from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import UserSpecifics, ImageCategories, UserImages, UserCurrentImage, BoundingBox, Image, \
    MechanicalTurkCodes, Category
import utils
import uuid
from exceptions import NoImagesLeft, BlockedUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import decorators

#Pages
@login_required
@transaction.atomic
def index(request):
    user = request.user
    user_specifics = UserSpecifics.objects.get(usr=user)
    if user_specifics.usr_blocked:
        return redirect('blocked')
    show_fraude = user_specifics.usr_has_show_fraude_info
    try:
        if request.method == 'POST' and request.POST['more'] == 'true':
            user_images = utils.get_images_user(user)
        else:
            #nunca ha entrado
            user_images = UserImages.objects.filter(uim_evaluated=False, uim_user=user)
            if user_specifics.usr_times_finished == 0 and len(user_images)==0:
                user_images = utils.get_images_user(user)
    except NoImagesLeft:
        return redirect("final")

    if len(user_images) == 0:
        return redirect('end')
    next_image = user_images[0].uim_image_category
    image = next_image.ict_img
    #Si no esta setearlo
    try:
        current_image = UserCurrentImage.objects.get(uci_user=user)
        current_image.uci_image_category = next_image
    except UserCurrentImage.DoesNotExist:
        current_image = UserCurrentImage(uci_user=user, uci_image_category=next_image)
    current_image.save()
    category = next_image.ict_cat
    user_specifics.usr_has_show_fraude_info = True
    user_specifics.usr_finished = False
    user_specifics.save()
    #obtener uno sin etiquetar, si no quedan => mostrar pagina final
    return render(request, 'labeling_app/labeling.html', {'img': image,
                                                          'usr': user_specifics,
                                                          'show_fraude': not show_fraude,
                                                          'category': category})


@login_required
@transaction.atomic
def evaluate(request):
    if request.method == 'POST':
        bounding_box = request.POST
        x = bounding_box['x']
        y = bounding_box['y']
        width = bounding_box['width']
        height = bounding_box['height']
        image_height = bounding_box['imageHeight']
        image_width = bounding_box['imageWidth']
        user = request.user
        utils.set_has_seen_info(user)
        current_image_user = UserCurrentImage.objects.get(uci_user=user)
        image = current_image_user.uci_image_category
        image_user = UserImages.objects.filter(uim_user=user, uim_image_category=image, uim_evaluated=False)[0]
        image_user.uim_evaluated = True
        image_user.save()
        if image.ict_is_test and (not utils.is_valid_bbox(image, x, y, width, height) or not image.ict_valid):
            try:
                utils.set_user_commited_fraud(user)
            except BlockedUser:
                return redirect('blocked')
        else:
            try:
                bbox = BoundingBox.objects.get(bbx_img_cat_id=image)
                bbox.bbx_x = x
                bbox.bbx_y = y
                bbox.bbx_width = width
                bbox.bbx_height = height
                bbox.bbx_image_height = image_height
                bbox.bbx_image_width = image_width
                bbox.save()
            except ObjectDoesNotExist:
                bbox = BoundingBox(bbx_x=x, bbx_y=y, bbx_width=width, bbx_height=height, bbx_img_cat_id=image,
                                   bbx_image_height=image_height, bbx_image_width=image_width)
                bbox.save()
            image.ict_added_bb = True
            image.save()
        if not utils.check_end(user):
            return redirect('end')
    return redirect('index')



@login_required
@transaction.atomic
def invalidate_image(request):
    user = request.user
    utils.set_has_seen_info(user)
    current_image_user = UserCurrentImage.objects.get(uci_user=user)
    image = current_image_user.uci_image_category
    image_user = UserImages.objects.filter(uim_user=user, uim_image_category=image)[0]
    image_user.uim_evaluated = True
    image_user.save()
    if image.ict_is_test and image.ict_valid:
        try:
            utils.set_user_commited_fraud(user)
        except BlockedUser:
            return redirect('blocked')
    else:
        image.ict_valid = False
        image.save()
    if not utils.check_end(user):
        return redirect('end')
    return redirect('index')


@login_required
@transaction.atomic
def end(request):
    user = request.user
    code = uuid.uuid4()
    user_specifics = UserSpecifics.objects.get(usr=user)
    if user_specifics.usr_is_mechanical_turk and not user_specifics.usr_finished:
        code_turk = MechanicalTurkCodes(mtc_usr=user, mtc_code=code)
        code_turk.save()
    #A user has ended when he/she labels 10 images and receives a code
    #This means that there are not valid images without bbox
    user_images = UserImages.objects.filter(uim_evaluated=False)
    if len(user_images) == 0 and not user_specifics.usr_finished :
        user_specifics.usr_finished = True
        user_specifics.usr_times_finished += 1
        user_specifics.save()
    end_image = Image.last_image()
    return render(request, 'labeling_app/labeling-end.html', {'usr': user_specifics,
                                                              'code' : code,
                                                              'img' : end_image})


@login_required
def blocked_user(request):
    user_specifics = UserSpecifics.objects.get(usr=request.user)
    return render(request, 'labeling_app/blocked.html', {'usr': user_specifics})

@login_required
def no_images_left(request):
    user = request.user
    user_specifics = UserSpecifics.objects.get(usr=user)
    user_specifics.usr_has_seen_info = True
    last_image = Image.last_image()
    return render(request, 'labeling_app/no-images-left.html', {'img':last_image, 'usr' : user_specifics})


@login_required
def get_codes(request):
    user = request.user
    user_specifics = UserSpecifics.objects.get(usr=user)
    if user_specifics.usr_is_mechanical_turk:
        codes = MechanicalTurkCodes.objects.filter(mtc_usr=user)
        return render(request, 'labeling_app/current-codes.html', {'codes': codes})

@login_required
def get_instructions(request):
    user = request.user
    user_specifics = UserSpecifics.objects.get(usr=user)
    if user_specifics.usr_is_mechanical_turk:
        pages = 10
    else:
        pages = 7
    return render(request, 'labeling_app/instructions.tpl.html', {'pages': pages})


def verifier(request):
    return render(request, 'labeling_app/verifier.html', {'request_controller': 'VerifierController',
                                                          'app': 'Verifier',
                                                          'controller': 'BoundingBoxController',
                                                          'controller_short': 'bbx'
                                                          })


def transformer(request):
    return render(request, 'labeling_app/category-labeling.html', {'controller': 'DrawerController',
                                                                    'controller_short': 'drawer',
                                                                    'app': "Labeling",
                                                                    "request_controller": "CategoryLabelingController"
                                                                   })


@decorators.login_by_ip
def transform_category(request):
    if 'invalid' in request.POST:
        try:
            image_category_id = request.POST['image-category']
            image_category = ImageCategories.objects.get(ict_id=image_category_id)
            image_category.ict_valid = False
            image_category.save()
        except Exception as e:
            print e
    elif 'next' in request.POST:
        try:
            image_category_id = request.POST['image-category']
            category_id = request.POST['category']
            image_category = ImageCategories.objects.get(ict_id=image_category_id)
            category = Category.objects.get(cat_id=category_id)
            image_category.ict_cat = category
            image_category.save()
        except Exception as e:
            print e

    main_categories = Category.objects.filter(cat_main=True)
    image_category_not_main = ImageCategories.objects.filter(ict_cat__cat_main=False, ict_valid=True)
    if len(image_category_not_main) == 0:
        return render(request, 'labeling_app/over-transform-category.html')
    image_category_id = image_category_not_main[0].ict_id
    image = image_category_not_main[0].ict_img.img_location
    category = image_category_not_main[0].ict_cat.cat_description

    return render(request, 'labeling_app/transform-category.html', {'image': image,
                                                                    'category': category,
                                                                    'main_categories': main_categories,
                                                                    'image_category':image_category_id
                                                                   })