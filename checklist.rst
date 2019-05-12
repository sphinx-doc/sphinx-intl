.. release procedure

Procedure:

1. check travis-ci testing result: https://travis-ci.org/sphinx-doc/sphinx-intl
2. update release version/date in ``CHANGES.rst``
3. ``python setup.py release sdist bdist_egg``
4. ``twine upload dist/<target-package-file>``
5. check PyPI page: https://pypi.org/p/sphinx-intl
6. tagging with version name that MUST following semver. e.g.: ``git tag 1.0.1``
7. ``git push --tags`` to push tag
8. bump version in ``sphinx_intl/__init__.py`` and ``CHANGES.rst`` then commit/push
   them onto GitHub
