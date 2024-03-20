import json


"""
This file is responsible for cleaning the dataset, mostly ensuring that every commit entry has the same features
Additionally, I will concatenate (and combine) different commit sets here.
"""
def clean_data(input_path_file, output_path_file, vuln_to_bool=True):
    with open(input_path_file, 'r') as file:
        tabulated_commits = json.load(file)

    for com in tabulated_commits:
        #add the neutrality attr
        com["neutral"] = False

        #change the vulnerability label to boolean, only for tab commits v8 and below
        if vuln_to_bool:
            if com["is_vulnerable"] == 1:
                com["is_vulnerable"] = True
            else:
                com["is_vulnerable"] = False

        #add the oop_php_files_exist attr
        if "average_loc" in com and com["average_loc"] == -1 and com["php_metrics_extracted"] != -1:
            com["oop_php_files_exist"] = False
        elif com["php_metrics_extracted"] != -1:
            com["oop_php_files_exist"] = True
        else:
            com["oop_php_files_exist"] = None

        #if it's error, add php metrics attribute and set to None
        if com["php_metrics_extracted"] == -1:
            com["average_loc"] = None
            com["average_ncloc"] = None
            com["average_dit"] = None
            com["average_nocc"] = None
            com["average_cbo"] = None
            com["average_wmc"] = None
            com["average_ccn"] = None
            com["average_hv"] = None

    with open(output_path_file, 'w') as file:
        json.dump(tabulated_commits, file, indent=4)


clean_data("jsons/tabulated_commits_v8_nov.json", "jsons/tabulated_commits_v9_nov.json", vuln_to_bool=True)


