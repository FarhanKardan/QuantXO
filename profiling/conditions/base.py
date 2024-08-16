class Condition:
    """
    Base class for conditions that can be applied to the profile.
    """

    def __init__(self):
        self.reset()

    def check(self, trade, profile_info):
        """
        Check the condition with the given trade data and profile info.

        Args:
            trade: Trade object with trade data.
            profile_info: Dictionary containing profile information.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def reset(self):
        """
        Reset the condition state if needed.
        """
        pass
