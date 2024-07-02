#!/bin/bash +x

ENVIRONMENT=$1
# Convert the branch name into a string that can be turned into a valid URL
BRANCH_RELEASE_NAME=$(echo $CIRCLE_BRANCH | tr '[:upper:]' '[:lower:]' | sed 's:^\w*\/::' | tr -s ' _/[]().' '-' | cut -c1-18 | sed 's/-$//')

deploy_branch() {
# Set the deployment host, this will add the prefix of the branch name e.g el-257-deploy-with-circleci or just main
  RELEASE_HOST="$BRANCH_RELEASE_NAME-fala-staging.cloud-platform.service.justice.gov.uk"
# Set the ingress name, needs <release name>-<chart name>-<namespace>-green 
  IDENTIFIER="$BRANCH_RELEASE_NAME-laa-fala-$K8S_NAMESPACE-green"
  echo "this is the identifer ingress name $IDENTIFIER"
  echo "Deploying CIRCLE_SHA1: $CIRCLE_SHA1 under release name: '$BRANCH_RELEASE_NAME'..."

  helm upgrade $BRANCH_RELEASE_NAME ./helm_deploy/laa-fala/. \
                --install --wait \
                --namespace=${K8S_NAMESPACE} \
                --values ./helm_deploy/laa-fala/values/fala-uat.yaml \
                --set image.repository="$ECR_ENDPOINT" \
                --set image.tag="$IMAGE_TAG" \
                --set ingress.annotations."external-dns\.alpha\.kubernetes\.io/set-identifier"="$IDENTIFIER" \
                --set ingress.hosts[0].host="$RELEASE_HOST"
}

deploy_main() {
  helm upgrade fala ./helm_deploy/laa-fala/. \
                          --install --wait \
                          --namespace=${K8S_NAMESPACE} \
                          --values ./helm_deploy/laa-fala/values/fala-$ENVIRONMENT.yaml \
                          --set image.repository="${ECR_ENDPOINT}" \
                          --set image.tag="$CIRCLE_SHA1"
}


if [ "$CIRCLE_BRANCH" == "main" ]; then
  deploy_main
else
  deploy_branch
  if [ $? -eq 0 ]; then
    echo "Deploy succeeded"
  else
    # If a previous `helm upgrade` was cancelled this could have got the release stuck in
    # a "pending-upgrade" state (c.f. https://stackoverflow.com/a/65135726). If so, this
    # can generally be fixed with a `helm rollback`, so we try that here.
    echo "Deploy failed. Attempting rollback"
    helm rollback $BRANCH_RELEASE_NAME
    if [ $? -eq 0 ]; then
      echo "Rollback succeeded. Retrying deploy"
      deploy_branch
    else
      echo "Rollback failed. Consider manually running 'helm delete $BRANCH_RELEASE_NAME'"
      exit 1
    fi
  fi
fi
