
#### Python script to take an edge list of interactions and generate a flareplot
#### inputs: list of V2R amino acid pairs, gpcrdb lookup table
#### output: json file as input for the flareplot tree
import json
import re

""" function for mapping all GPCRdb numbers based on uniprot id """
def Get_GPCRdb_Numbers():
	generic_numbers_dict = {}
	gpcrdb_generic_numbers_file = "/Users/ajvenkatakrishnan/projects/others/dmitry_vasopressin_bias/data/2018Mar24/V2R_HUMAN_gpcrdb_commGsArr.txt"
	with open(gpcrdb_generic_numbers_file) as GENERIC:
		for line in GENERIC:

			(aaNum, aaName, gpcrdb, track_color) = line.rstrip().split("\t")
			# (uniprot, aaNum, aaName, TM, generic_num) = line.rstrip().split("\t")
			# generic_num = re.sub("\.\d+", "", generic_num)

			if aaNum in generic_numbers_dict.keys():
				generic_numbers_dict[aaNum]['gpcrdb'] = gpcrdb
				generic_numbers_dict[aaNum]['secStr'] = gpcrdb		
				generic_numbers_dict[aaNum]['aaName'] = aaName
				generic_numbers_dict[aaNum]['track_color'] = track_color
			else:
				generic_numbers_dict[aaNum] = {}
				generic_numbers_dict[aaNum]['gpcrdb'] = gpcrdb
				generic_numbers_dict[aaNum]['secStr'] = gpcrdb
				generic_numbers_dict[aaNum]['aaName'] = aaName				
				generic_numbers_dict[aaNum]['track_color'] = track_color

	return generic_numbers_dict

def Get_interaction_residues(interacting_residues_file):
	interacting_residues_dict = {}

	with open(interacting_residues_file) as INTERACTING:
		for line in INTERACTING:
			(dist_descriptor, aanum_i, aanum_j) = line.rstrip().split(" ")
			if aanum_i in interacting_residues_dict.keys():
				interacting_residues_dict[aanum_i][aanum_j] = 1
			else:
				interacting_residues_dict[aanum_i] = {}
				interacting_residues_dict[aanum_i][aanum_j] = 1

	return interacting_residues_dict

def main():

	interacting_residues_file = "/Users/ajvenkatakrishnan/projects/others/dmitry_vasopressin_bias/data/2018Mar24/CommGsArr.txt"

	generic_numbers_dict = Get_GPCRdb_Numbers()
	interacting_residues_dict = Get_interaction_residues(interacting_residues_file)

	## The flareplot json file
	ret = {
		"edges": []
	}

	for aaNum_i in interacting_residues_dict.keys():
		gpcrdb_num_i = generic_numbers_dict[aaNum_i]['gpcrdb']
		for aaNum_j in interacting_residues_dict[aaNum_i].keys():
			# res_i = generic_numbers_dict[aaNum_i]['aaName'] + aaNum_i
			# res_j = generic_numbers_dict[aaNum_j]['aaName'] + aaNum_j
			gpcrdb_num_j = generic_numbers_dict[aaNum_j]['gpcrdb']

			res_i = generic_numbers_dict[aaNum_i]['aaName'] + gpcrdb_num_i
			res_j = generic_numbers_dict[aaNum_j]['aaName'] + gpcrdb_num_j

			edge = {"name1": res_i, "name2": res_j, "frames": [0]}
			ret["edges"].append(edge)


	track = {"trackLabel": "DefaultTrack", "trackProperties": []}
	ret["tracks"] = [track]

	tree = {"treeLabel": "DefaultTree", "treeProperties": []}
	ret["trees"] = [tree]

	aaNum_list = generic_numbers_dict.keys()
	aaNum_list.sort()

	for aaNum in aaNum_list:
		secStr = generic_numbers_dict[aaNum]['secStr']
		gpcrdb_num = generic_numbers_dict[aaNum]['gpcrdb']

		if 'x' in secStr:
			secStr = re.sub("x\d+", "", secStr)

			tree["treeProperties"].append({
					"path": "root" + "." + secStr + "." + generic_numbers_dict[aaNum]['aaName'] + gpcrdb_num,
					"key": aaNum
				})

			track["trackProperties"].append({
					"nodeName": generic_numbers_dict[aaNum]['aaName'] + gpcrdb_num,
					"color": generic_numbers_dict[aaNum]['track_color'],
					"size": 0.5
				})

	# Convert string to pretty printed JSON
	pretty_json = json.dumps(ret, indent=2)	
	print(pretty_json)	

if __name__ == "__main__":
	main()


