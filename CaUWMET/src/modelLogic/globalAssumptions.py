from src.modelLogic.readGlobalAssumptions import contractorsList, historicHydrologyYears, futureYear, contractorDf, reclassYearType, UWMPhydrologicYearType, hydroYearType

class GlobalAssumptions:
    def __init__(self):
        self.contractorsList = contractorsList
        self.historicHydrologyYears = historicHydrologyYears
        self.futureYear = futureYear
        self.contractorDf = contractorDf
        self.reclassYearType = reclassYearType
        self.UWMPhydrologicYearType = UWMPhydrologicYearType
        self.hydroYearType = hydroYearType
        
        