import json

"""
This file is here because I want to add extra attributes to the tabulated commits, 
namely appname and php_metrics_extracted (bool indicating if php metrics has been extracted or not, for now it's 0)

There are some functions that calculate things related to the execution: Count how many errors, count how many is not error.

Turns out there were duplicates in tabulated commits version 1-5. So there's a function here that removes em.
"""
# with open("/home/deck/Documents/masterGT/mt_git/thesis/dataset/php_metrics/jsons/phpAppsWithGithubLinks.json", 'r') as file:
#     appname_ghlink_data = json.load(file)
with open("jsons/phpAppsWithGithubLinks.json", 'r') as file:
    appname_ghlink_data = json.load(file)

# with open("/home/deck/Documents/masterGT/mt_git/thesis/dataset/php_metrics/jsons/tabulated_commits_v8_nov.json", 'r') as file:
#     tabulated_commits_v8 = json.load(file)

# with open("/home/deck/Documents/masterGT/mt_git/thesis/dataset/application_selection/cve_transformation_process/before_cvv_cves.json", 'r') as file:
#     before_vcc_cves = json.load(file)

# with open("/home/deck/Documents/masterGT/mt_git/thesis/dataset/php_metrics/jsons/joris_commits_filtered_v4.json", 'r') as file:
#     joris_commits_filtered_v4 = json.load(file)

with open("jsons/tabulated_commits_v9_nov.json", 'r') as file:
    tabulated_commits_v9 = json.load(file)
with open("jsons/joris_commits_filtered_v4.json", 'r') as file:
    joris_commits_filtered_v4 = json.load(file)
with open("jsons/tabulated_commits_v12_nov.json", 'r') as file:
    tabulated_commits_v12 = json.load(file)
with open("jsons/git_metrics_commits.json", 'r') as file:
    git_metrics_commits = json.load(file)

def search_appname(gh_link, appname_ghlink_data):
    for entry in appname_ghlink_data:
        if entry["github_href"] == gh_link:
            return entry["appname"]
    return None

def add_appname_delete_ov(tabulated_commits): #delete the original_vuln attribute because it makes it harder to read the json
    for commit in tabulated_commits:
        gh_link = commit["repo"]
        appname = search_appname(gh_link, appname_ghlink_data)
        commit["appname"] = appname
        commit["php_metrics_extracted"] = 0
        del commit["original_vuln"]
    with open('jsons/tabulated_commits_v2_nov.json', 'w') as file:
        json.dump(tabulated_commits, file, indent=4)

def add_appname(tabulated_commits):
    for commit in tabulated_commits:
        gh_link = commit["repo"]
        appname = search_appname(gh_link, appname_ghlink_data)
        commit["appname"] = appname
        commit["php_metrics_extracted"] = 0
    with open('jsons/tabulated_commits_v2.json', 'w') as file:
        json.dump(tabulated_commits, file, indent=4)

def count_extraction(tabulated_commits, error_code):
    if error_code != -1 and error_code != 1:
        print("ERROR: wrong error code")
        return    
    counter_vuln = 0
    counter_non_vuln = 0
    for commit in tabulated_commits:
        if commit["php_metrics_extracted"] == error_code:
            if commit["is_vulnerable"] == 1:
                counter_vuln += 1
            else:
                counter_non_vuln += 1
    total = counter_vuln + counter_non_vuln
    if error_code == -1:
        print("There are ", counter_vuln, " errors for vulnerable commits")
        print("There are ", counter_non_vuln, " errors for non-vulnerable commits")
        print("There are ", total, " errors in total")
    if error_code == 1:
        print("There are ", counter_vuln, " success for vulnerable commits")
        print("There are ", counter_non_vuln, " success for non-vulnerable commits")
        print("There are ", total, " success in total")
    return total, counter_vuln, counter_non_vuln
def count_extraction_apps(tabulated_commits, appnames, error_code):
    counter_vuln = 0
    counter_non_vuln = 0
    for commit in tabulated_commits:
        if commit["appname"] in appnames and commit["php_metrics_extracted"] == error_code:
            if commit["is_vulnerable"] == 1:
                counter_vuln += 1
            else:
                counter_non_vuln += 1
    total = counter_vuln + counter_non_vuln
    if error_code == -1:
        print("There are ", counter_vuln, " errors for vulnerable commits for ", appnames)
        print("There are ", counter_non_vuln, " errors for non-vulnerable commits for ", appnames)
        print("There are ", total, " errors in total for ", appnames)
    if error_code == 1:
        print("There are ", counter_vuln, " success for vulnerable commits for ", appnames)
        print("There are ", counter_non_vuln, " success for non-vulnerable commits for ", appnames)
        print("There are ", total, " success in total for ", appnames)
    if error_code == 0:
        print("There are ", counter_vuln, " non-extracted for vulnerable commits for ", appnames)
        print("There are ", counter_non_vuln, " non-extracted for non-vulnerable commits for ", appnames)
        print("There are ", total, " non-extracted in total for ", appnames)
    return total, counter_vuln, counter_non_vuln

def remove_duplicates(tabulated_commits, save_path):
    unique_shas = set()
    unique_entries = []

    for item in tabulated_commits:
        sha = item['commit_sha']
        if sha not in unique_shas:
            unique_shas.add(sha)
            unique_entries.append(item)
        else:
            print(sha)
    with open(save_path, 'w') as file:
        json.dump(unique_entries, file, indent=4)
    return unique_entries

def count_commits(tabulated_commits, appnames = []):
    count_vulnerable = 0
    count_non_vulnerable = 0
    for commit in tabulated_commits:
        if appnames:
            if commit["appname"] in appnames:
                if commit["is_vulnerable"] == 0:
                    count_non_vulnerable += 1
                else:
                    count_vulnerable += 1
        else:
            if commit["is_vulnerable"] == 0:
                    count_non_vulnerable += 1
            else:
                count_vulnerable += 1
    if appnames:
        print("The amount of vulnerable commits for app(s): ", appnames, " are ", count_vulnerable)
        print("The amount of non-vulnerable commits for app(s): ", appnames, " are ", count_non_vulnerable)
    else:
        print("The amount of vulnerable commits are ", count_vulnerable)
        print("The amount of non-vulnerable commits are ", count_non_vulnerable) 

def simple_overview():
    print("tabulated_commits_v9")
    count_extraction(tabulated_commits_v9, 1)
    count_extraction(tabulated_commits_v9, -1)
    print("In total there are ", len(tabulated_commits_v9), " commits")
    print("Joris commits filtered:")
    count_extraction(joris_commits_filtered_v4, 1)
    count_extraction(joris_commits_filtered_v4, -1)    
    print("In total there are ", len(joris_commits_filtered_v4), " commits") 


print(len(tabulated_commits_v12))

