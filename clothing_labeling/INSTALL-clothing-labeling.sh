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
sed '124iSTATIC_ROOT = "'$STATIC'"' -i $DESTINATION/clothing_labeling/settings.py && \
echo "yes" | python $DESTINATION/manage.py collectstatic && \
sed 's/\/api/\/clothing-labeling\/api/' -i $STATIC/labeling_app/js/basic_labeling/app.js && \
deactivate && \
echo "SUCCESS"


