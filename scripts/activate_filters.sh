git config filter.cached-output.clean "./scripts/cache_filter_clean.sh"
git config filter.cached-output.smudge "./scripts/cache_filter_smudge.sh"

git config filter.remove-version.clean "./scripts/remove_version_filter.sh"
git config filter.remove-version.smudge "cat"
