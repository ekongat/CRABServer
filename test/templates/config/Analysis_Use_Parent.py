from WMCore.Configuration import Configuration
config = Configuration()

#General section
config.section_("General")
config.General.requestName = 'CHANGE'
config.General.workArea = 'CHANGE'
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.instance = 'preprod'
config.General.activity = 'analysistest'

#Job Type Section
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'psets/pset_use_parent.py'
#config.JobType.psetName = 'psets/pset_tutorial_analysis.py'
config.JobType.disableAutomaticOutputCollection = False

#Data Section
config.section_("Data")
#config.Data.inputDataset = '/SingleMu/Run2012B-13Jul2012-v1/AOD'
config.Data.inputDataset = '/SingleMu/Run2012C-22Jan2013-v1/AOD'
#config.Data.inputDataset = '/MinimumBias/Run2012A-22Jan2013-v1/AOD'
config.Data.inputDBS = 'global'
config.Data.useParent = True
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 100
config.Data.totalUnits = 10000
config.Data.ignoreLocality = False
config.Data.publication = True
config.Data.publishDBS = 'phys03'
config.Data.outputDatasetTag = 'CHANGE'
config.Data.allowNonValidInputDataset =True

#Site Section
config.section_("Site")
config.Site.storageSite = 'CHANGE'
