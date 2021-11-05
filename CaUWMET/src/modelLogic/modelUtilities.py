

def lookupCorrespondingValue(df, item, colA, colB):
    """
    :param df: Pandas dataframe
    :param item: Item to look for in column A
    :param colA: Name of the column A
    :param colB: Name of the column B
    :return: Returns corresponding item in column B
    Note: This works only if there are no duplicates (there is only
    one 'item' in colA.
    """
    return df[df[colA] == item][colB].values[0]


def reclassifyYearType(yearType):
    """
    :param yearType: list or array of strings (W, AN, N, BN, D, C)
    :return rType: list or array of reclassified year type
     (NB - Normal or better, SD - Single Dry, MD - Multiple Dry)
    """
    dryYears = ['BN', 'D', 'C']
    yearType = list(yearType)
    length = len(yearType)
    rType = []
    for i in range(length):
        if yearType[i] in dryYears:
            if i == 1:
                if yearType[i+1] in dryYears:
                    rType.append('MD')
                    continue
            elif 1 < i < length-1:
                if yearType[i+1] in dryYears or yearType[i-1] in dryYears:
                    rType.append('MD')
                    continue
            else:
                if yearType[i-1] in dryYears:
                    rType.append('MD')
                    continue
            rType.append('SD')
        else:
            rType.append('NB')
    return rType

#TODO: Shorten function by iterating over supplies by priority dataframe columns
def meetDemandsBySupplyPriority(
    i, 
    contractorDemandsAfterSupplyPriority1,
    contractorSupplyPriority2, 
    contractorSupplyPriority3, 
    contractorSupplyPriority4, 
    contractorSupplyPriority5, 
    contractorSupplyPriority6, 
    contractorSupplyPriority7, 
    contractorSWPCVPSupply):

    contractorDemandsToBeMetBySWPCVP = 0
    contractorExcessSupply = 0
    contractorDemandsToBeMetByCarryover = 0

    if contractorDemandsAfterSupplyPriority1[i] > 0:
        contractorDemandsAfterSupplyPriority2 = contractorDemandsAfterSupplyPriority1[i] - contractorSupplyPriority2
        
        if contractorDemandsAfterSupplyPriority2 > 0:
            contractorDemandsAfterSupplyPriority3 = contractorDemandsAfterSupplyPriority2 - contractorSupplyPriority3
        
            if contractorDemandsAfterSupplyPriority3 > 0:
                contractorDemandsAfterSupplyPriority4 = contractorDemandsAfterSupplyPriority3 - contractorSupplyPriority4
            
                if contractorDemandsAfterSupplyPriority4 > 0:
                    contractorDemandsAfterSupplyPriority5 = contractorDemandsAfterSupplyPriority4 - contractorSupplyPriority5

                    if contractorDemandsAfterSupplyPriority5 > 0:
                        contractorDemandsAfterSupplyPriority6 = contractorDemandsAfterSupplyPriority5 - contractorSupplyPriority6

                        if contractorDemandsAfterSupplyPriority6 > 0:
                            contractorDemandsToBeMetBySWPCVP = contractorDemandsAfterSupplyPriority6 - contractorSupplyPriority7
                            
                            if contractorDemandsToBeMetBySWPCVP > 0:
                                contractorDemandsToBeMetByCarryover = contractorDemandsToBeMetBySWPCVP - contractorSWPCVPSupply
                            else:
                                contractorExcessSupply = -1*contractorDemandsToBeMetBySWPCVP
                                contractorDemandsToBeMetByCarryover= 0
                        else:
                            contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
                            contractorDemandsToBeMetBySWPCVP = 0
                            contractorDemandsToBeMetByCarryover = 0
                    else:
                        contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
                        contractorDemandsToBeMetBySWPCVP = 0
                        contractorDemandsToBeMetByCarryover = 0
                else:
                    contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority4 + contractorSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
                    contractorDemandsToBeMetBySWPCVP = 0
                    contractorDemandsToBeMetByCarryover = 0
            else:
                contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority3 + contractorSupplyPriority4 + contractorSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
                contractorDemandsToBeMetBySWPCVP = 0
                contractorDemandsToBeMetByCarryover = 0
        else:
            contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority2 + contractorSupplyPriority3 + contractorSupplyPriority4 + contractorSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
            contractorDemandsToBeMetBySWPCVP = 0
            contractorDemandsToBeMetByCarryover = 0
    else:
        contractorExcessSupply = -1*contractorDemandsAfterSupplyPriority1 + contractorSupplyPriority2 + contractorSupplyPriority3 + contractorSupplyPriority4 + contractorSupplyPriority5 + contractorSupplyPriority6 + contractorSupplyPriority7 + contractorSWPCVPSupply
        contractorDemandsToBeMetBySWPCVP = 0
    
    return [contractorDemandsToBeMetBySWPCVP, contractorExcessSupply, contractorDemandsToBeMetByCarryover]