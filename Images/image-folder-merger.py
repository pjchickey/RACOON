from distutils.dir_util import copy_tree
import os

"""
How to use:
-----------
1. Make sure you're on your git branch
2. In the git command line (should be a button for it somewhere) type: git rebase master
OR
1. You can stay on main (just pull to get the latest images)
2. Copy the Images folder to somewhere else on your computer (so it's away from git)

After doing one of the above:
3. Copy this script to the Images folder
4. Replace categories in the dirs variable below with wanted ones
5. Run script
6. Use the new Merged_Categories folder for model stuff
7. Happy Data training!

"""

dirs = {
    "Cardboard": ["Cardboard-Boxes", "Cardboard-Other"],
    "Glass": ["Glass"],
    "Metal": ["Steel_and_Tin", "Aluminum"],
    "Paper": ["Paper-Junk_Mail", "Paper-Other"],
    "Plastic": ["Plastic-Bottles", "Plastic-Other"],
    "Trash": ["Pizza_Boxes", "Plastic_Bags", "Plastic_Wrap",
                      "Plasticware", "Plastic_Straws", "Dirty_Food_Containers",
                      "Drink_Cartons", "Other", "Styrofoam"]
}

for new_dir,old_dirs in dirs.items():
    for old_dir in old_dirs:
        try:
            os.makedirs("Merged_Categories/" + new_dir)
        except OSError:
            pass
        copy_tree(old_dir, "Merged_Categories/" + new_dir)

# dirs = {
#     "Recycling": ["Cardboard-Boxes", "Cardboard-Other", "Glass", "Steel_and_Tin",
#                   "Aluminum", "Paper-Junk_Mail", "Paper-Other", "Plastic-Bottles",
#                   "Plastic-Other"],
#     "Trash": ["Pizza_Boxes", "Plastic_Bags", "Plastic_Wrap", "Plasticware",
#               "Plastic_Straws", "Dirty_Food_Containers", "Drink_Cartons",
#               "Other", "Styrofoam"]
# }
#
# for new_dir,old_dirs in dirs.items():
#     for old_dir in old_dirs:
#         try:
#             os.makedirs("Merged_Categories2/" + new_dir)
#         except OSError:
#             pass
#         copy_tree(old_dir, "Merged_Categories2/" + new_dir)
