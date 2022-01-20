#!/bin/bash
( cd ../;protodep up -f -u --basic-auth-username $GITHUB_ACCOUNT --basic-auth-password $GITHUB_TOKEN )
