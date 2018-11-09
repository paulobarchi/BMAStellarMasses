#!/bin/bash

######################## pbarchi ########################
#################### 11/01/18 update ####################
####### This script is still a work in progress. ########
#########################################################
# Running the BMA stellar mass code						#
# (on mof photometry outputs of afterburner):			#
# 1. Adjust config file 								#
#       BMA_StellarMass_Config.ini						#
#       for desired steps, paths, files and				#
#	parallel configurations.							#
#       Remember to backup files with same names as		#
#	output files in config file before running this		#
#       (they will be overwritten).						#
# 2. run this code:										#
#	./runBMA_StellarMass.sh								#
#########################################################

# from: http://home.fnal.gov/~kadrlica/fnalstart.html
activateEnvironment() {
	# setting up anaconda
	export CONDA_DIR=/cvmfs/des.opensciencegrid.org/fnal/anaconda2
	source $CONDA_DIR/etc/profile.d/conda.sh
	# activating base
	conda activate base
	# activating astro environment
	conda activate des18a
}

activateEnvironment
# Run python script
python BMA_StellarMass.py