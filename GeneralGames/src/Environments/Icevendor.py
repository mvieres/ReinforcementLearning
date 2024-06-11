class Icevendor:

    def __init__(self):
        self.maxInventory: int = 0
        self.costsForOneUnit: float = 0.0
        self.storage: int = 0
        self.storageCosts: float = 0.0
        self.revenue: float = 0.0
        self.amountSold: int = 0
        self.amountBought: int = 0
        self.price: float = 1.0
        pass

    def calculateRevenue(self) -> None:
        self.revenue = self.amountSold * self.price