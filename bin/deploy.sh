#!/bin/bash +x

ENVIRONMENT=$1

# Use source branch for PRs, current branch for PR merges
BRANCH_NAME="${GITHUB_HEAD_REF:-$GITHUB_REF_NAME}"

# Convert the branch name into a string that can be turned into a valid URL
BRANCH_RELEASE_NAME=$(echo $BRANCH_NAME | tr '[:upper:]' '[:lower:]' | sed 's:^\w*\/::' | tr -s ' _/[]().' '-' | cut -c1-18 | sed 's/-$//')

# Pull ranges from shared LAA IP ranges and then remove spaces,
# replace linebreaks with commas, remove last comma, and escape commas for helm input
SHARED_IP_RANGES_LAA=$(curl -s https://raw.githubusercontent.com/ministryofjustice/laa-ip-allowlist/main/cidrs.txt | tr -d ' ' | tr '\n' ',' | sed 's/,/\\,/g' | sed 's/\\,$//')
PINGDOM_IPS="$(python3 bin/pingdom_ips.py)"

deploy_branch() {
# Set the deployment host, this will add the prefix of the branch name e.g el-257-deploy-with-circleci or just main
  RELEASE_HOST="$BRANCH_RELEASE_NAME-fala-staging.cloud-platform.service.justice.gov.uk"
# Set the ingress name, needs <release name>-<chart name>-<namespace>-green
  IDENTIFIER="$BRANCH_RELEASE_NAME-laa-fala-$K8S_NAMESPACE-green"
  echo "Deploying commit: $GITHUB_SHA under release name: '$BRANCH_RELEASE_NAME'..."

  helm upgrade $BRANCH_RELEASE_NAME ./helm_deploy/laa-fala/. \
                --install --wait \
                --namespace=${K8S_NAMESPACE} \
                --values ./helm_deploy/laa-fala/values/fala-uat.yaml \
                --set image.repository="$ECR_ENDPOINT" \
                --set image.tag="branch-$GITHUB_SHA" \
                --set ingress.annotations."external-dns\.alpha\.kubernetes\.io/set-identifier"="$IDENTIFIER" \
                --set ingress.hosts[0].host="$RELEASE_HOST" \
                --set-string pingdomIPs=$PINGDOM_IPS \
                --set-string sharedIPRangesLAA=$SHARED_IP_RANGES_LAA
}

deploy_main() {
  helm upgrade fala ./helm_deploy/laa-fala/. \
                          --install --wait \
                          --namespace=${K8S_NAMESPACE} \
                          --values ./helm_deploy/laa-fala/values/fala-$ENVIRONMENT.yaml \
                          --set-string pingdomIPs=$PINGDOM_IPS \
                          --set-string sharedIPRangesLAA=$SHARED_IP_RANGES_LAA \
                          --set image.repository="${ECR_ENDPOINT}" \
                          --set image.tag="main-$GITHUB_SHA"
}


if [ "$BRANCH_NAME" == "main" ]; then
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
