from __future__ import print_function

import os
import sys
import json
import errno
import types
import pickle
import pprint

import classad

import TaskWorker.Actions.PostJob as PostJob
import TaskWorker.Actions.PreJob as PreJob
import TaskWorker.Actions.PreDAG as PreDAG
import HTCondorUtils

import WMCore.Configuration as Configuration

def bootstrap():
    print("Entering TaskManagerBootstrap with args: %s" % sys.argv)
    command = sys.argv[1]
    if command == "POSTJOB":
        return PostJob.PostJob().execute(*sys.argv[2:])
    elif command == "PREJOB":
        return PreJob.PreJob().execute(*sys.argv[2:])
    elif command == "PREDAG":
        return PreDAG.PreDAG().execute(*sys.argv[2:])

    infile, outfile = sys.argv[2:]

    adfile = os.environ["_CONDOR_JOB_AD"]
    print("Parsing classad")
    with open(adfile, "r") as fd:
        ad = classad.parseOld(fd)
    print("..done")
    in_args = []
    if infile != "None":
        with open(infile, "rb") as fd:
            in_args = pickle.load(fd)

    config = Configuration.Configuration()
    config.section_("Services")
    config.Services.DBSUrl = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter/'
    
    ad['tm_taskname'] = ad.eval("CRAB_Workflow")
    ad['tm_split_algo'] = ad.eval("CRAB_SplitAlgo")
    ad['tm_dbs_url'] = ad.eval("CRAB_DBSURL")
    ad['tm_input_dataset'] = ad.eval("DESIRED_CMSDataset")
    ad['tm_outfiles'] = HTCondorUtils.unquote(ad.eval("CRAB_AdditionalOutputFiles"))
    ad['tm_tfile_outfiles'] = HTCondorUtils.unquote(ad.eval("CRAB_TFileOutputFiles"))
    ad['tm_edm_outfiles'] = HTCondorUtils.unquote(ad.eval("CRAB_EDMOutputFiles"))
    ad['tm_site_whitelist'] = HTCondorUtils.unquote(ad.eval("CRAB_SiteWhitelist"))
    ad['tm_site_blacklist'] = HTCondorUtils.unquote(ad.eval("CRAB_SiteBlacklist"))
    ad['tm_job_type'] = 'Analysis'
    print("TaskManager got this raw ad")
    print(ad)
    pure_ad = {}
    for key in ad:
        try:
            pure_ad[key] = ad.eval(key)
            if isinstance(pure_ad[key], classad.Value):
                del pure_ad[key]
            if isinstance(pure_ad[key], list):
                pure_ad[key] = [i.eval() for i in pure_ad[key]]
        except:
            pass
    ad = pure_ad
    ad['CRAB_AlgoArgs'] = json.loads(ad["CRAB_AlgoArgs"])
    ad['tm_split_args'] = ad["CRAB_AlgoArgs"]
    ad['tarball_location'] = os.environ.get('CRAB_TARBALL_LOCATION', '')
    print("TaskManagerBootstrap got this ad:")
    pprint.pprint(ad)

    results = task.execute(in_args, task=ad).result

    print(results)
    with open(outfile, "wb") as fd:
        pickle.dump(results, fd)

    return 0

if __name__ == '__main__':
    try:
        retval = bootstrap()
        print("Ended TaskManagerBootstrap with code %s" % retval)
        sys.exit(retval)
    except Exception as e:
        # TODO: make this propagate somewhere machine readable
        print("Got a fatal exception: %s" % e)
        raise
        
