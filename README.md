# BMAStellarMasses

## BMA Stellar Masses (from vt-clustertools). Computes stellar masses and cluster stellar mass.

Updated and adjusted from previous version:
https://github.com/SSantosLab/vt-clustertools/tree/master/BMAStellarMasses

## Getting Started 

### File structure

Copy (or clone) the files in this repository to your directory ("/BMAStellarMass/", for example).

File structure needed:


	.
	|-- BMA_StellarMass_Config.ini
	|-- BMA_StellarMass.py
	|-- clusterSMass_orig.py
	|-- combineCat.py
	|-- CosmologicalDistance.py
	|-- fileStructureNeeded.txt
	|-- helperfunctions.py
	|-- loadPopColors.py
	|-- README.txt
	|-- runBMA_StellarMass.sh
	`-- smass.py


### Configuration File

A configuration file is required to run: 

    BMA_StellarMass_Config.ini.
    
This file is separated by the following sections: [Paths], [Files], [Operations] and [Parallel].
Probably a good practice is to save a "backup version" before changing this config file.

    cp  BMA_StellarMass_Config.ini BMA_StellarMass_Config_BCKP.ini

Specify your desired path, input and output filenames, operations to run, and parallel configuration.
In this file, comments (starting with ";") explain each config item.

Example for [Operations] section: 
If you desire to run only the stellar mass code, your [Operations] section would look like:

    stellarMass: True
    clusterStellarMass: False

Complete example of configuration file (without comments):

	[Paths]
	inputPath: /des/des61.a/data/pbarchi/clusters/test/

	[Files]
	membersInputFile: /des/des61.a/data/pbarchi/clusters/test/test_johnny_members.fits
	stellarMassOutPrefix: /des/des61.a/data/pbarchi/clusters/test/testStellarMasses_
	clusterStellarMassOutFile: /des/des61.a/data/pbarchi/clusters/test/testClusterStellarMasses_full.fits
	timeFile: /des/des61.a/data/pbarchi/clusters/test/BMA-StellarMass-Time.out

	[Operations]
	stellarMass: True
	clusterStellarMass: True

	[Parallel]
	batchStart: 0
	batchMax: 146737
	nJobs: 100
	nCores: 20


## Running

With the config file set up, run it with:

    bash runBMA_StellarMass_bckp.sh
    
This script activates the necessary environment and calls the main script BMA_StellarMass.py.
If you already have an activated astro environment you can just run the python script:

    python BMA_StellarMass.py

### Activating environment

In the bash script runBMA_StellarMass_bckp.sh there is a function to activate the environment:

	activateEnvironment() {
		# setting up anaconda
		export CONDA_DIR=/cvmfs/des.opensciencegrid.org/fnal/anaconda2
		source $CONDA_DIR/etc/profile.d/conda.sh
		# activating base
 		conda activate base
 		# activating astro environment
 		conda activate des18a
  	}

## Test in a minimal example

It would be good to have a minimal example to test (benchmark time and compare outputs).

## Authors

* DES Galaxy Clusters collaboration (https://github.com/SSantosLab/vt-clustertools/tree/master/BMAStellarMasses)
