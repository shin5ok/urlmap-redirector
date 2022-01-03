#!/bin/bash
echo -n dog | gcloud beta secrets create --data-file=- URLMAP_API
# echo -n kotori | gcloud beta secrets versions add URLMAP_API --data-file=-
