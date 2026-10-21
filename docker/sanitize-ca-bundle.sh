#!/bin/sh
# Remove the four roots and 16 published intermediate/cross-sign fingerprints:
# https://emudhra.we-have-a-problem.com/{roots,impacted-intermediates}.json
# Works with BusyBox too, so it can protect Kaniko before registry downloads.
set -eu
bundle=${1:?usage: sanitize-ca-bundle.sh CA_BUNDLE}
test -s "$bundle"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
awk -v dir="$tmp" '
  /-----BEGIN CERTIFICATE-----/ { n++; file = sprintf("%s/cert-%06d", dir, n); active = 1 }
  active { print > file }
  /-----END CERTIFICATE-----/ { close(file); active = 0 }
  END { if (!n || active) exit 1 }
' "$bundle"
: > "$tmp/bundle"
kept=0
for cert in "$tmp"/cert-*; do
    sed '/-----/d' "$cert" | tr -d '\r\n' | base64 -d > "$tmp/der"
    fingerprint=$(sha256sum "$tmp/der")
    fingerprint=${fingerprint%% *}
    case "$fingerprint" in
        7dd78d5f4f13459a83dff9abbba62edbaf6f2d102bf257fd712f4d9f2746ed8d|\
        f2edaaff3d9b701fb4d14c9f285f8c0bad90fc3bcc1fa07d47f4718edaba34a5|\
        d7a7a0fb5d7e2731d771e9484ebcdef71d5f0c3e0a2948782bc83ee0ea699ef4|\
        86a1ecba089c4a8d3bbe2734c612ba341d813e043cf9e8a862cd5c57a36bbe6b|\
        42c4accd12c4f59597925e1a08a7a90102608543809308d50ec427e118ba1493|\
        45a883f349aedfd5f3a649b5498ffb121712ba8b448f3f2a91dbc5a766fcddbe|\
        98b896625c0c230adeec3eb2cf6aad5001ecf9156a68644e82374ce5833bc25b|\
        5f1ded4dd590af74631290cf073b122a2aac6a1fa479778a0bd43579bd832699|\
        e7568fe6e12331f4fd7de61da4c7559d0f8eb192a218d4741a3ba75184333838|\
        579480aea166290bd3c643589e795fc0d0e54e86505d180f1dff99efd3199512|\
        0164d7ceae5bb909c272af151ff44b1177ae9b47d9424b94f1d9558c30934d19|\
        62b7f9868263f72f6911fc78ceaf72c1979158b7368bf648683bb2aa39b02e72|\
        cb6e15165ac802e9b3f993f16c25d41f4e81c21ebde71ae1b012ac00bf9c7c3f|\
        7485b51c0ed192878fa1d2f948fb529ae1842cc5086c4b67f7be5b2039de9489|\
        432ec25f0d28de9006d97bf752f17bbb2cd41f669933fcb072d9a1148d0261f3|\
        fd9d5c2dbbd4995ab69b8d50c439d9527b00529199c2fd01b2174eb58f07021f|\
        9e39de2881273acc225a149c72ba3e0f51424963669ab633ee1dc7df5db067b4|\
        a496e23ac0cab8155fc9b117b97eae368efcbb9041aec8804d5a308d2d01c2d8|\
        4b2460a466f95fd40113bcdcca2ceb29b3b093921de45474da7df48874c630b1|\
        84112972b8e59d14560ae7e7119654474aad119990cf3722bfc1e3b91615e1fd)
            ;;
        *) cat "$cert" >> "$tmp/bundle"; kept=$((kept + 1));;
    esac
done
test "$kept" -gt 0
# Write through symlinks: some environments link cert.pem to cacert.pem.
cat "$tmp/bundle" > "$bundle"
