function addTobyLogo(main) {
    $('body').append($('</br></br><div align="left">&nbsp;<img src="toby_logo.png" width=120 height=53>&nbsp;&nbsp;&nbsp;<small><i>(developed and used by Juniper Test Engineering using the Robot Test Framework)</i></small></div>'),
                     $.tmpl('suiteTemplate', main));
}
