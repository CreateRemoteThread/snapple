var system = require('system');
var page = require('webpage').create();
page.settings.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36';
page.viewportSize = { width: 1024, height: 768 };
page.clipRect = { top: 0, left: 0, width: 1024, height: 768 };
page.onResourceReceived = function(response)
{
  console.log(JSON.stringify(response));
}
page.open(system.args[1], function() {
  page.render(system.args[2]);
  phantom.exit();
});

