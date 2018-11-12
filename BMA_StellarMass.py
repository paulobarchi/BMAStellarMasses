# new libraries
from subprocess import Popen
import ConfigParser
from time import time
# imports from nike.py below
import smass
import helperfunctions
import clusterSMass_orig
import numpy as np
from joblib import Parallel, delayed

def getConfig(section, item, boolean=False,
		userConfigFile="BMA_StellarMass_Config.ini"):
	configFile = ConfigParser.ConfigParser()
	configFile.read(userConfigFile)
	if (not boolean):
		return configFile.get(section, item)
	else:
		return configFile.getboolean(section, item)

def isOperationSet(operation,section="Operations"):	
	return getConfig(boolean=True, section=section, 
		item=operation)	
	
def combineFits():
	from combineCat import combineBMAStellarMassOutput
	stellarMassOutPrefix = \
		getConfig("Files","stellarMassOutPrefix")
	combineBMAStellarMassOutput(stellarMassOutPrefix)

def computeStellarMass(batch, memPerJob):
    # For running the stellar masses (takes the longest)
    batchIndex = batch + memPerJob
    job = int(batchIndex / memPerJob)
    stellarMassOutFile = \
    	getConfig("Files","stellarMassOutPrefix") + \
    	"{:0>5d}.fits".format(job)
    inPath = getConfig("Paths","inputPath")
    membersInFile = getConfig("Files","membersInputFile")
    inputDataDict = helperfunctions.read_afterburner(
    	membersInFile, batch, batchIndex)
    smass.calc(inputDataDict, outfile=stellarMassOutFile, 
    	indir=inPath, lib="miles")

def computeClusterStellarMass():
	stellarMassFile = getConfig(
		"Files","stellarMassOutPrefix") + 'full.fits'
	clusterOutFile  = getConfig(
		"Files","clusterStellarMassOutFile")
	print "Compuing cluster stellar mass."
	clusterSMass_orig.haloStellarMass(
		filename=stellarMassFile,
		outfile=clusterOutFile)

''' Parallel Computing Instructions:

    There are two parameters that need to be entered 
    	for each batch submission
    1) batchStart = the starting member point 
    	for this batch out of all the members. 
    	The first batch should begin at 0
    2) batchMax = the ending member point 
    	for this batch out of all members. 
    	To avoid duplicates this number should
        increase by the same amount batchStart increases 
        when doing multiple batches.

    Two other parameters that can be adjusted as necessary are
    3) nJobs = the number of jobs the batch submission 
    	is split into. 100 is a good number.
    4) nCores = the total number of cores used by 
    	the computing machine at any given time. 
    	20 is suggested for the DES cluster.

'''
def parallelComputeStellarMass(batchStart=0,
		batchMax=25936, nJobs=100, nCores=20): 
		# nJobs is normally = 100
	batchesList = np.linspace(batchStart, batchMax, nJobs,
    		endpoint=False,dtype=int)
	print "Calling parallelism."
	Parallel(n_jobs=nCores)(delayed(computeStellarMass)
		(batch, (batchMax - batchStart) / nJobs) 
		for batch in batchesList)
	# generate concatenated fits file
	print "Combining fits."
	combineFits()

def writeStringToFile(fileName, toBeWritten):
        # create file if it does not exist
        if not path.isfile(fileName):
                with open(fileName, 'w') as f:
                        f.write( '{toBeWritten}\n'.format(
                                toBeWritten=toBeWritten) )
        # else, append to file  
        else:
             	with open(fileName, 'a') as f:
                        f.write( '{toBeWritten}\n'.format(
                                toBeWritten=toBeWritten) )

def main():
	print "Starting BMA Stellar Masses program."
	# get initial time
	total_t0 = time()

	# get output file to save time	
	timeFile = getConfig("Files","timeFile")

	# check and parallel compute stellar mass, 
	#	if it is the case
	if (isOperationSet(operation="stellarMass")):
		print "Starting parallel stellar masses operation."
		stellarMass_t0 = time()
		# get parallel information
		batchStart = int(getConfig("Parallel", "batchStart"))
		batchMax   = int(getConfig("Parallel", "batchMax"))
		nJobs 	   = int(getConfig("Parallel", "nJobs"))
		nCores 	   = int(getConfig("Parallel", "nCores"))
		
		# call function to parallel compute 
		parallelComputeStellarMass(batchStart=batchStart,
			batchMax=batchMax, nJobs=nJobs, nCores=nCores)
	
		# save time to compute stellar mass    
                stellarMassTime = time() - stellarMass_t0
                stellarMassMsg = "Stellar Mass (parallel) time: {}s".format(stella$
                writeStringToFile(timeFile, stellarMassMsg)

	# check and compute cluster stellar mass, 
	#	if it is the case
	if (isOperationSet(operation="clusterStellarMass")):
		print "Starting cluster stellar mass operation."
		clusterStellarMassTime_t0 = time()
		computeClusterStellarMass()

		# save time to compute cluster stellar mass
                clusterStellarMassTime = time() - \
                        clusterStellarMassTime_t0
                clusterStellarMassMsg = "Cluster Stellar Mass time: {}s".format(cl$
                writeStringToFile(timeFile, clusterStellarMassMsg)

	# save total computing time 
        totalTime = time() - total_t0
        totalTimeMsg = "Total time: {}s".format(totalTime)
        writeStringToFile(timeFile, totalTimeMsg)
					
	print "All done."

if __name__ == "__main__":
    main()
