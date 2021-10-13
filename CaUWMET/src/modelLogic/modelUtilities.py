

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

class demandsAfterBaseConservation():
    def __init__(self, data):
        """
        :param data: pandas dataframe including columns ['contractor', 'YearType', '']
        """
        self.df = data

    def calcDemandsAfterBaseConservation(self):
        pass


def subtractSuppliesByPriority(suppliesDf, demandsDf, supplyPriorityNumber):
    suppliesPriorityNDf = suppliesDf[suppliesDf['Supply Priority'] == supplyPriorityNumber].copy()
    finalSuppliesPriorityNDf = suppliesPriorityNDf.reset_index()
    del finalSuppliesPriorityNDf['index']
    finaldemandsAfterPriorityNSuppliesDf = finalSuppliesPriorityNDf.copy()
    cols = finalSuppliesPriorityNDf.columns.difference(['Index', 'Contractor', 'Year', 'Supply Type', 'Supply Priority'])                        
    finaldemandsAfterPriorityNSuppliesDf[cols] = demandsDf[cols] - finalSuppliesPriorityNDf[cols]
    return finaldemandsAfterPriorityNSuppliesDf