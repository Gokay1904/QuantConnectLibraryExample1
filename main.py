# region imports
from AlgorithmImports import *
# endregion

class FirstAlgorithmOnQuantitiveAnalysis(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 1, 1)  # Set Start Date
        self.SetEndDate(2021, 5, 5)
        self.SetCash(100000)  # Set Strategy Cash

        self.UniverseSettings.Resolution = Resolution.Daily
        
        self.AddUniverse(self.MyCoarseFilterFunction,self.FineFilterFunction)

    def MyCoarseFilterFunction(self,coarse):

        sortedByDollarVolume = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)
        filtered = [x.Symbol for x in sortedByDollarVolume if x.Price > 10 and x.DollarVolume > 10000000  if x.HasFundamentalData]
        return filtered[:10]

    def FineFilterFunction(self,fine):
        sortedByPEnROE = sorted(fine,key = lambda x: x.ValuationRatios.PERatio and (x.ValuationRatios.ForwardROE > 15 and x.ValuationRatios.ForwardROE < 20), reverse=True) 
        return [x.Symbol for x in sortedByPEnROE[:5]]



    def OnData(self, data: Slice):
       
       self.Log(self.Time)

       for sec in self.Securities.Values:
        if not data.ContainsKey(sec.Symbol) or not data[sec.Symbol]:
                return

        self.Log(f"{data[sec.Symbol].Symbol}: {data[sec.Symbol].Open}$")

        self.Log("-----------------------------")

    def OnSecuritiesChanged(self, changes):

        self._changes = changes
        self.Log(f"OnSecuritiesChanged({self.UtcTime}):: {changes}$")

        for sec in changes.RemovedSecurities:
            self.Liquidate(sec.Symbol)
            self.Log(f"SOLD:{sec}$")

        for sec in changes.AddedSecurities:
            self.SetHoldings(sec.Symbol, 0.1)
            self.Log(f"BOUGHT: {sec}$")

    

