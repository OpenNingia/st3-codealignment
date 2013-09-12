Code Alignment for Sublime Text 3
========================================

Select the text you want to align and hit <pre>CTRL+ALT+=</pre>

<p>Code Alignment plugin allow you to convert this code: </p>
    int magic_number=4;
    std::string person_name="Mario";
    static const char* DEFAULT_COUNTRY = "Italy";
<p>to this: </p>
    int magic_number                   = 4;
    std::string person_name            = "Mario";
    static const char* DEFAULT_COUNTRY = "Italy";

<p>Looks good? You can also choose the separator to use:</p>

![Screenshot](https://raw.github.com/OpenNingia/st3-codealignment/master/screenshot.png "More than a million words")

## Supported Sublime Text versions
Code Alignment plugin supports Sublime Text 3

## Installation
In Sublime Text 3 - clone project from [Github](https://github.com/OpenNingia/st3-codealignment.git) into Packages folder.

## Feedback & Support
Available on [Github](https://github.com/OpenNingia/st3-codealignment)

## Contribution
...is always welcome! Same place - [Github](https://github.com/OpenNingia/st3-codealignment)

## License
This software is distributed under GPLv3 license (see LICENSE for details)

## Changelog

v 0.2
    * Added Settings configuration
    * Added Block alignment in single selection ( blocks are separated by an empty line )
    * If separator is prefixed or suffixed by known symbols ( e.g. <= >= != ) then the line is not aligned
