kubectl create serviceaccount --namespace urlmap urlmap-redirector
gcloud iam service-accounts create urlmap-redirector
gcloud projects add-iam-policy-binding $PROJECT     --member "serviceAccount:urlmap-redirector@$PROJECT.iam.gserviceaccount.com"     --role "roles/secretmanager.secretAccessor"
gcloud projects add-iam-policy-binding $PROJECT     --member "serviceAccount:urlmap-redirector@$PROJECT.iam.gserviceaccount.com"     --role "roles/pubsub.publisher"
gcloud iam service-accounts add-iam-policy-binding     --role roles/iam.workloadIdentityUser     --member "serviceAccount:$PROJECT.svc.id.goog[urlmap/urlmap-redirector]"     urlmap-redirector@$PROJECT.iam.gserviceaccount.com
