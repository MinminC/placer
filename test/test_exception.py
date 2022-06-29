from unittest import TestCase

from web import app
from config import appcfgs
from mods import exception as EX
from mods import ERROR_OPENDATA_CONFIG_ERROR_MSG


class TestException(TestCase):
    def create_app(self):
        app.config.from_object(appcfgs.TestingConfig)
        self.app = app.test_client()

    def setUp(self):
        self.create_app()

    def test_imgproc_error(self):
        """
        ImgprocError 테스트
        :return:
        """
        # Given
        expect = ERROR_OPENDATA_CONFIG_ERROR_MSG

        # When
        actual = EX.ConfigError()

        # Then
        self.assertEqual(expect, actual.msg)
        self.assertEqual(expect, str(actual))
