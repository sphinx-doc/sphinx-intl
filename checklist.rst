.. release procedure

Procedure:

1. check GitHub Actions test results: https://github.com/sphinx-doc/sphinx-intl/actions
2. update release version/date in ``CHANGES.rst``
3. ``python -m build``, see details: setup.cfg
4. ``twine upload dist/<target-package-file>``
5. check PyPI page: https://pypi.org/p/sphinx-intl
6. tagging with version name that MUST following semver. e.g.: ``git tag 1.0.1``
7. ``git push --tags`` to push tag
8. bump version in ``sphinx_intl/__init__.py`` and ``CHANGES.rst`` then commit/push
   them onto GitHub
