## Files explanations
- php_metrics_extraction_tools.py -> functions needed for extraction
- php_metrics_extraction_exec.py -> overarching execution (+ a bit of testing)
- extra_scripts -> as the name suggests, explanation of what exactly it is for is in the file itself
## Tabulated Commits files explanations

- nov = no original_vuln attribute
### Versions
1. v1 = the first one out of vcc_extraction (named cvv_extraction because I'm dumb)
2. Adds extra attributes: php_metrics_extracted and appname
3. First test of consolidation, tested on one app: Friendica. 
4. Kanboard and OwnCloud added
5. NextCloud, Microweber, Pimcore added
6. Duplicates are removed
7. Nextcloud is redone (to test differentiating error and no php file), plus tuleap, piwigo, and shopware
8. Every other application is added is added
9. Cleaned (see clean_concat_data.py)

## joris_commits(_filtered)
Joris mined extra random commits for non-vulnerable commits. It's from joris_jsons/random-commits... In the folder there are multiple jsons, one for each app. It had to be concat. joris_commits.json is the result of the first concat, resulting in 4410 commits in total (this includes commits that are already from Yeska). 

This needs to be filtered, so that php metrics extraction is only done in non-Yeska commits, in other words commits that are not in tabulated_commits_v6^. The result is the filtered version
### (Filtered) Versions
1. First filtration using extractin_joris_commits.remove_overlaps()
2. Actually same as the first one, just used different method to filter which is extractin_joris_commits.remove_overlaps_v2()
3. Added php_metrics_extracted to track errors
4. Everything extracted.