# snapple
real facts [tm]

snapple is a screenshotting and light fingerprinting tool. this is similar to nmap's http-screenshot script, with the addition that it supports javascript (though the use of a phantomjs renderer) and preserves header information, allowing you to perform offline analysis

to launch this, run ./snapple [list], where [list] is a one-host-or-ip-per-line.

requires imagemagick (for 'convert') and phantomjs

