"""
Provides the ability to save and update log values during the learning process.
"""

class Meter:
    def __init__(self):
        self.reset()
        
        
    def reset(self):
        """
        initialization method
        """
        self.total = 0.
        self.count = 0.

        
    def update(self, val, n = 1):
        """
        Method to update log values
        
        Parameters:
            val: log value
            n: step
        """
        self.total += val
        self.count += n

        
    def value(self):
        """
        Method for outputting log values
        """
        if self.count == 0:
            return 0.0
        
        return self.total
    
    
class LossMeter(Meter):
    """
    Class that inherits the Meter class to store and update loss values.
    
    Args:
        loss_fn: Loss function
    """
    def __init__(self, loss_fn):
        super().__init__()
        
        self.l_fn = loss_fn
        
    
    def calculate(self, preds, targets):
        """
        Method to calculate loss value
        """
        loss = self.l_fn(preds, targets)
        loss.backward()
        
        # Reflected in Meter's update method
        super().update(val = loss)
        
        
    def value(self):
        if self.count == 0:
            return super().value()
        
        return self.total.item() / self.count
    

class MetricMeter(Meter):
    """
    Class that inherits the Meter class to store and update metric scores.
    
    Args:
        metric_fn: Metric function
    """
    def __init__(self, metric_fn):
        super().__init__()
        
        self.m_fn = metric_fn
        
    
    def calculate(self, preds, targets):
        """
        Method to calculate metric score
        """
        score = self.m_fn(preds, targets)
        
        # Reflected in Meter's update method
        super().update(val = score)
        
        
    def value(self):
        if self.count == 0:
            return super().value()
        
        return self.total / self.count







