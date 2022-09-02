#!/usr/bin/env bash
set -e

# On the Git protocol side, unencrypted git:// offers no integrity or authentication, making it subject to tampering.
# We expect very few people are still using this protocol, especially given that you can’t push (it’s read-only on GitHub).
# We’ll be disabling support for this protocol.
# https://github.blog/2021-09-01-improving-git-protocol-security-github/#no-more-unauthenticated-git
git config --global url."https://".insteadOf git://
npm install
git config --global url."git://".insteadOf https://
