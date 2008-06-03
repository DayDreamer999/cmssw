import FWCore.ParameterSet.Config as cms

process = cms.Process("ECALDQM")

import RecoLocalCalo.EcalRecProducers.ecalFixedAlphaBetaFitUncalibRecHit_cfi
process.ecalUncalibHit = RecoLocalCalo.EcalRecProducers.ecalFixedAlphaBetaFitUncalibRecHit_cfi.ecalFixedAlphaBetaFitUncalibRecHit.clone()

#import RecoLocalCalo.EcalRecProducers.ecalWeightUncalibRecHit_cfi
#process.ecalUncalibHit = RecoLocalCalo.EcalRecProducers.ecalWeightUncalibRecHit_cfi.ecalWeightUncalibRecHit.clone()

process.load("RecoLocalCalo.EcalRecProducers.ecalRecHit_cfi")

process.load("DQM.EcalEndcapMonitorModule.EcalEndcapMonitorModule_cfi")

process.load("DQM.EcalEndcapMonitorTasks.EcalEndcapMonitorTasks_cfi")

process.load("DQM.EcalEndcapMonitorTasks.mergeRuns_cff")

process.load("Geometry.CaloEventSetup.CaloGeometry_cfi")

process.load("Geometry.CaloEventSetup.EcalTrigTowerConstituents_cfi")

process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")

process.load("SimCalorimetry.EcalTrigPrimProducers.ecalTriggerPrimitiveDigis_cff")

process.load("Geometry.EcalMapping.EcalMapping_cfi")

import SimCalorimetry.EcalTrigPrimProducers.ecalTriggerPrimitiveDigis_cfi
process.ecalTriggerPrimitiveDigis2 = SimCalorimetry.EcalTrigPrimProducers.ecalTriggerPrimitiveDigis_cfi.ecalTriggerPrimitiveDigis.clone()

process.load("DQM.EcalEndcapMonitorClient.EcalEndcapMonitorClient_cfi")

process.load("RecoEcal.EgammaClusterProducers.ecalClusteringSequence_cff")

process.load("CalibCalorimetry.EcalLaserCorrection.ecalLaserCorrectionService_cfi")

process.load("DQMServices.Core.DQM_cfg")

process.preScaler = cms.EDFilter("Prescaler",
    prescaleFactor = cms.int32(1)
)

process.dqmInfoEE = cms.EDFilter("DQMEventInfo",
    subSystemFolder = cms.untracked.string('EcalEndcap')
)

process.dqmSaverEE = cms.EDFilter("DQMFileSaver",
    fileName = cms.untracked.string('EcalEndcap'),
    dirName = cms.untracked.string('.'),
    convention = cms.untracked.string('Online')
)

process.maxEvents = cms.untracked.PSet(
#    input = cms.untracked.int32(150)
    input = cms.untracked.int32(300)
)
process.source = cms.Source("PoolSource",
#---
    fileNames = cms.untracked.vstring('/store/users/dellaric/data/5E883D60-4B98-DC11-BD17-000423D6A6F4.root')
#---
#    fileNames = cms.untracked.vstring('/store/users/dellaric/data/muon_50GeV_allECAL_gain200.root')
#---
)

process.EcalTrivialConditionRetriever = cms.ESSource("EcalTrivialConditionRetriever",
    adcToGeVEBConstant = cms.untracked.double(0.035),
    adcToGeVEEConstant = cms.untracked.double(0.06),
#    adcToGeVEBConstant = cms.untracked.double(0.0875),     # 0.035
#    adcToGeVEEConstant = cms.untracked.double(0.015),      # 0.060
    pedWeights = cms.untracked.vdouble(0.333, 0.333, 0.333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    amplWeights = cms.untracked.vdouble(-0.333, -0.333, -0.333, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    jittWeights = cms.untracked.vdouble(0.041, 0.041, 0.041, 0.0, 1.325, -0.05, -0.504, -0.502, -0.390, 0.0)
)

process.MessageLogger = cms.Service("MessageLogger",
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('WARNING'),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        noTimeStamps = cms.untracked.bool(True),
        noLineBreaks = cms.untracked.bool(True),
        EcalEndcapMonitorModule = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        )
    ),
    categories = cms.untracked.vstring('EcalEndcapMonitorModule'),
    destinations = cms.untracked.vstring('cout')
)

process.ecalEndcapDataSequence = cms.Sequence(process.preScaler*process.ecalUncalibHit*process.ecalRecHit*process.ecalTriggerPrimitiveDigis*process.ecalTriggerPrimitiveDigis2*process.islandBasicClusters*process.islandSuperClusters*process.hybridSuperClusters)
process.ecalEndcapMonitorSequence = cms.Sequence(process.ecalEndcapMonitorModule*process.dqmInfoEE*process.ecalEndcapMonitorClient*process.dqmSaverEE)

process.p = cms.Path(process.ecalEndcapDataSequence*process.ecalEndcapMonitorSequence)
process.q = cms.EndPath(process.ecalEndcapDefaultTasksSequence*process.ecalEndcapCosmicTask*process.ecalEndcapClusterTask)

process.ecalUncalibHit.MinAmplBarrel = 12.
process.ecalUncalibHit.MinAmplEndcap = 16.
process.ecalUncalibHit.EBdigiCollection = cms.InputTag("ecalDigis","ebDigis")
process.ecalUncalibHit.EEdigiCollection = cms.InputTag("ecalDigis","eeDigis")

process.ecalRecHit.EBuncalibRecHitCollection = cms.InputTag("ecalUncalibHit","EcalUncalibRecHitsEB")
process.ecalRecHit.EEuncalibRecHitCollection = cms.InputTag("ecalUncalibHit","EcalUncalibRecHitsEE")

process.ecalEndcapMonitorModule.mergeRuns = True
process.ecalEndcapMonitorModule.EEDigiCollection = cms.InputTag("ecalDigis","eeDigis")
process.ecalEndcapMonitorModule.runType = 3 # MTCC/PHYSICS

process.ecalTriggerPrimitiveDigis.Label = 'ecalDigis'
process.ecalTriggerPrimitiveDigis.InstanceEB = 'ebDigis'
process.ecalTriggerPrimitiveDigis.InstanceEE = 'eeDigis'

process.ecalTriggerPrimitiveDigis2.Label = 'ecalDigis'
process.ecalTriggerPrimitiveDigis2.InstanceEB = 'ebDigis'
process.ecalTriggerPrimitiveDigis2.InstanceEE = 'eeDigis'

process.ecalEndcapTriggerTowerTask.EcalTrigPrimDigiCollectionReal = 'ecalTriggerPrimitiveDigis2'

process.ecalEndcapMonitorModule.EcalTrigPrimDigiCollection = 'ecalTriggerPrimitiveDigis2'

process.ecalEndcapOccupancyTask.EEDigiCollection = cms.InputTag("ecalDigis","eeDigis")
process.ecalEndcapOccupancyTask.EcalTrigPrimDigiCollection = 'ecalTriggerPrimitiveDigis'

process.ecalEndcapPedestalOnlineTask.EEDigiCollection = cms.InputTag("ecalDigis","eeDigis")

process.ecalEndcapMonitorClient.maskFile = 'maskfile-EE.dat'
process.ecalEndcapMonitorClient.mergeRuns = True
process.ecalEndcapMonitorClient.location = 'H4'
process.ecalEndcapMonitorClient.baseHtmlDir = '.'
process.ecalEndcapMonitorClient.enabledClients = ['Integrity', 'Occupancy', 'PedestalOnline', 'Cosmic', 'Timing', 'TriggerTower', 'Cluster', 'Summary']

#process.islandBasicClusters.IslandBarrelSeedThr = 0.150 # 0.500
#process.islandBasicClusters.IslandEndcapSeedThr = 0.150 # 0.180

#process.hybridSuperClusters.HybridBarrelSeedThr = 0.150 # 1.000
#process.hybridSuperClusters.step = 1      # 17
#process.hybridSuperClusters.eseed = 0.150 # 0.350

process.DQM.collectorHost = ''

