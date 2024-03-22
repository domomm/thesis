## To do
- Get Joris git metr and concat
    - Check v5 and below to make sure the duplicates are actual duplicates
    - has concatted but there are duplicates, these duplicates should be compared to v10, take the one that has the same is_vulnerable attr. If is none or sumn, then print it out, check it manually.
        - One problem is there are some whose neutrality and label is weong
        - Another is that only the neutrality is wrong
        - Another is that actually duplicates
        - Maybe there are others???
        

## Files explanations
- php_metrics_extraction_tools.py -> functions needed for extraction
- php_metrics_extraction_exec.py -> overarching execution (+ a bit of testing)
- extra_scripts -> as the name suggests, explanation of what exactly it is for is in the file itself
- clean_concat_data -> Cleaning the data once all metrics are gathered
- extracting_joris_commits -> anything to do with it
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
10. Concatted with joris_filtered_v5
11. Merged with the git metrics commits
12. Removed some duplicates (NOT DONE, the duplicates have diff labels lmao)

## joris_commits(_filtered)
Joris mined extra random commits for non-vulnerable commits. It's from joris_jsons/random-commits... In the folder there are multiple jsons, one for each app. It had to be concat. joris_commits.json is the result of the first concat, resulting in 4410 commits in total (this includes commits that are already from Yeska). 

This needs to be filtered, so that php metrics extraction is only done in non-Yeska commits, in other words commits that are not in tabulated_commits_v6^. The result is the filtered version
### (Filtered) Versions
1. First filtration using extractin_joris_commits.remove_overlaps()
2. Actually same as the first one, just used different method to filter which is extractin_joris_commits.remove_overlaps_v2()
3. Added php_metrics_extracted to track errors
4. Everything extracted.
5. Cleaned

## Extra notes
- Apparently there are duplicates in the joris_commits, but it's removed with remove_overlaps().
- There's only 38 projects here! Two turned out didnt have any references_transformed (see cvv extraction)
- Hestia and Vesta are the same applications???