#!bin/bash
APP_DIR=$1
BASE_DESTINATION=$HOME/webapps
DESTINATION=${BASE_DESTINATION}/
STATIC=${DESTINATION}/static
ENV=${DESTINATION}/clothing-labeling-env

if[ ! -d ${BASE_DESTINATION} ]
	then
	mkdir ${BASE_DESTINATION}
fi

if[ -d ${DESTINATION} ]
	then
	rm -r ${DESTINATION}
fi

if[ -z "$APP_DIR" ]
	then
	APP_DIR=.
fi

cp -r ${APP_DIR} ${DESTINATION} && \
echo "CREATING VIRTUALENV" && \
virtualenv ${ENV} && \
source "${ENV}/bin/activate" && \
echo "INSTALLING DEPENDENCIES" && \
pip install -r requirements.txt && \
echo "yes" | python manage.py collecstatic && \
deactivate && \
echo "SUCCESS"


