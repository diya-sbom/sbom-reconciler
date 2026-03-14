class VerificationModule:
    """
    Base class for engine plug-in modules.
    Modules inspect the subject and return structured results.
    """

    name = "base_module"

    def run(self, context: dict) -> dict:
        """
        Execute module verification.

        context: shared verification context from the engine
        return: structured result dictionary
        """

        raise NotImplementedError("Module must implement run()")
