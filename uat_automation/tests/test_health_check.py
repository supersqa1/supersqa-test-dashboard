

import pytest
import logging as logger



@pytest.mark('healthcheck')
def test_healthcheck_1():
    logger.info("Healthcheck passed")