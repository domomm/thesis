import php_metrics_extraction_tools as my_tools
import os
import time
import json

def get_commit_metrics(appname, commit_sha):
    start_time = time.time()  # Record the start time
    repo_path = os.path.join("C:\\", "MT_dataset_repos", appname)
    temp_dir = os.path.join(repo_path, "temp")
    xml_path = os.path.join("C:\\", "MT_dataset_repos", "sum.xml")
    
    print("PREPARING FILES...")
    try:        
        my_tools.prepare_files(appname, commit_sha)
    except Exception as e:
        print("Error in preparing files: ", str(e))
        raise

    print("RUNNING PDEPEND...")
    try:
        my_tools.run_pdepend(temp_dir)
    except Exception as e:
        print("Error in running pdepend: ", str(e))
        raise

    print("PARSING RESULT XML...")
    try:
        result = my_tools.parse_xml(xml_path)
    except Exception as e:
        print("Error parsing sum.xml: ", str(e))
        raise

    print("CLEANING UP...")
    try:
        my_tools.clear_temp_files(appname)
    except Exception as e:
        print("Error cleaning up ", str(e))
        raise
    
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print("Elapsed time is ", elapsed_time)
    if result:
        return result
    else:
        raise Exception("Result not found")

def test_get_commit_metrics():
    appname_test = "Pimcore"
    sha_test = "5769658b609008c46b49ea72a5139769c9375af2"
    sha_test_2 = "d91747f92aedf1accc6f64ad0977d8ed05cdcc1a" #pimcore
    repo_path = os.path.join("C:\\", "MT_dataset_repos", appname_test)
    temp_dir = os.path.join(repo_path, "temp")
    xml_path = os.path.join("C:\\", "MT_dataset_repos", "sum.xml")
    # my_tools.prepare_files(appname_test, sha_test)
    # my_tools.run_pdepend(temp_dir)
    # print(my_tools.parse_xml(xml_path))
    # my_tools.clear_temp_files(appname_test)
    print(get_commit_metrics(appname_test, sha_test_2))

#Currently opening v4, saving to v5
start_time = time.time()  # Record the start time
with open("jsons/tabulated_commits_v4_nov.json", 'r') as file:
    tabulated_commits = json.load(file)
test_apps = ["NextCloud", "Pimcore", "Microweber"]
for commit in tabulated_commits:
    if commit["php_metrics_extracted"] == 0 and commit["appname"] in test_apps:
        try:
            result = get_commit_metrics(commit["appname"], commit["sha"])
            commit["average_loc"] = result["average_loc"]
            commit["average_ncloc"] = result["average_ncloc"]
            commit["average_dit"] = result["average_dit"]
            commit["average_nocc"] = result["average_nocc"]
            commit["average_cbo"] = result["average_cbo"]
            commit["average_wmc"] = result["average_wmc"]
            commit["average_ccn"] = result["average_ccn"]
            commit["average_hv"] = result["average_hv"]
            commit["php_metrics_extracted"] = 1
        except Exception as e:
            print("ERROR getting commit metrics: ", str(e))
            commit["php_metrics_extracted"] = -1
with open('jsons/tabulated_commits_v5_nov.json', 'w') as file:
        json.dump(tabulated_commits, file, indent=4)
end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate elapsed time
print("In total, the whole extraction takes ", elapsed_time," seconds")