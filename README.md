Read More: A Plugin for Pelican
===============================

[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/read-more/build)](https://github.com/pelican-plugins/read-more/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-read-more)](https://pypi.org/project/pelican-read-more/)
![License](https://img.shields.io/pypi/l/pelican-read-more?color=blue)

This Pelican plugin inserts an inline “Read More” link into the last HTML element of the summary.

For more information regarding why it was created, please visit: https://www.vuongnguyen.com/read-more-python-lxml/

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-read-more

Settings
--------

Following Settings are available, if not set, the Plugin will use default values.

String added to end of Summary before "read more" link:

	SUMMARY_END_SUFFIX = '...'

Summary length before "read more" link will be added:

    SUMMARY_MAX_LENGTH = 50

Text of "read more" link:

    READ_MORE_LINK = '<span>continue</span>'

Format of "read more" link:

    READ_MORE_LINK_FORMAT = '<a class="read-more" href="/{url}">{text}</a>'

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/read-more/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

Contributors
------------

Contributors include: [Vuong Nguyen](https://www.vuongnguyen.com), Dashie, [Justin Mayer](https://justinmayer.com), Kernc

License
-------

This project is licensed under the AGPL-3.0 license.
