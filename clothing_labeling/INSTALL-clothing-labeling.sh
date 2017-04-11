#!bin/bash
APP_DIR=$1
BASE_DESTINATION=$HOME/webapps
DESTINATION=${BASE_DESTINATION}/clothing_labeling
STATIC=${DESTINATION}/static/clothing_labeling/static
ENV=${DESTINATION}/clothing-labeling-env

if [ ! -d ${BASE_DESTINATION} ]
	then
	mkdir ${BASE_DESTINATION}
fi

if [ -d ${DESTINATION} ]
	then
	rm -r ${DESTINATION}
fi

if [ -z "$APP_DIR" ]
	then
	APP_DIR=.
fi

cp -r ${APP_DIR} ${DESTINATION} && \
echo "CREATING VIRTUALENV" && \
virtualenv --python=python2.7 ${ENV} && \
source "${ENV}/bin/activate" && \
echo "INSTALLING DEPENDENCIES" && \
pip install -r requirements.txt && \
sed "s/'default': {[^}]*}$/'default': {'ENGINE': 'django.db.backends.mysql','NAME': 'clothingLabeling','USER': 'labelingassistant','PASSWORD': 'PASS-99a050c0-d3ce-44e4-a581-6a7c4b609a08','HOST': 'localhost','PORT': '',}/"  $DESTINATION/clothing_labeling/settings.py > $DESTINATION/clothing_labeling/temporal  && \
sed "s/DEBUG = True/DEBUG = False/" $DESTINATION/clothing_labeling/temporal > $DESTINATION/clothing_labeling/settings.py && \
sed '146iSTATIC_ROOT = "'$STATIC'"' -i $DESTINATION/clothing_labeling/settings.py && \
echo "yes" | python $DESTINATION/manage.py collectstatic && \
sed "s/templateUrl: '\/instructions\/',/templateUrl: '\/clothing-labeling\/instructions\/',/" -i $STATIC/labeling_app/js/app/basic_labeling/controllers/LabelingCtrl.js && \
sed "s/templateUrl: '\/anonymous-user-screen\/',/templateUrl: '\/clothing-labeling\/anonymous-user-screen\/',/" -i $STATIC/labeling_app/js/app/basic_labeling/controllers/RegistrationCtrl.js && \
sed "s/{'next_page': '\/login\/'}/{'next_page': '\/clothing-labeling\/login\/'}/" -i $DESTINATION/labeling_app/url_registration.py && \
cd ${DESTINATION} && \
python manage.py migrate
deactivate && \
echo "SUCCESS"


