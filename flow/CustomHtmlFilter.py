import BeautifulSoup
import re

def escape(html):
        """
        Returns the given HTML with ampersands, quotes and angle brackets 
        encoded to prevent XSS attacks.

        This is mostly from the Django project.
        http://www.djangoproject.com/
        and probably needs its copy of the BSD license:

Copyright (c) Django Software Foundation and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
 
   2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

   3. Neither the name of Django nor the names of its contributors may be used
     to endorse or promote products derived from this software without
     specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        """
        return html.replace('&', '&amp;').replace('<', '&lt;').replace(
            '>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def url_only(url):
    """This either returns the valid url or nothing depending on whether it 
    matches
    a regular expression.
    I got the regular expression from:
    http://flanders.co.nz/2009/11/08/a-good-url-regular-expression-repost/    

    but I altered it to prevent ftps.

    >>> url_only("http://flanders.co.nz/2009/11/08/a-good-url-regular-expression-repost/")
    'http://flanders.co.nz/2009/11/08/a-good-url-regular-expression-repost/'
    >>> url_only("http://www.youtube.com/watch?v=OCPY-zD6e-I&feature=PlayList&p=D9190C56D4C5332C")
    'http://www.youtube.com/watch?v=OCPY-zD6e-I&feature=PlayList&p=D9190C56D4C5332C'
    >>> url_only("javascript:alert('XSS');")
    ''
    >>> url_only("http://javascript:alert('XSS');")
    ''
    """
    #http://flanders.co.nz/2009/11/08/a-good-url-regular-expression-repost/
    #except altered to prevent ftp
    url_pattern = r"^(?#Protocol)(?:http(?:s?)\:\/\/|~\/|\/)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:\/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|\/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?$"
    if re.match(url_pattern, url) != None:
        return url
    else:
        return ''

class CustomHTMLFilter:
    """
    This class allows you to dynamically create a custom HTML filter. You create
    a factory and add tags to it using bracket syntax. The value
    you specify is another dictionary that contains valid attribute names as 
    keys and filter literals as values.

    The exception is inner_html which is treated as inner_html instead of
    an attribute.

    If you set an attribute's value to an empty string, the attribute will be
    deleted.

    If the HTML is too malformed, it will throw a SyntaxError, or you can
    specify an escape error filter to call.


    >>> x = CustomHTMLFilter()
    >>> soria_only = lambda text: text == "soria" and "soria" or ""
    >>> x.add_tags("body p")
    >>> x["body"]["id"] = (soria_only,)
    >>> x["p"]["inner_html"] = (soria_only,)
    >>> x["p"]["id"] = (soria_only,)
    >>> x(r'''<BODY ID = "soria" ONLOAD = "alert('XSS')"><p id= 'tundra'>inner html that isn't soria</p></BODY>''')
    u'<body id="soria"><p></p></body>'

    >>> x(r'''<BODY bad code"><p>inner html that isn't soria</p></BODY>''')
    Traceback (most recent call last):
    ...
    SyntaxError: The HTML is too malformed

    >>> x = CustomHTMLFilter(parse_error_filter = escape)
    >>> x(r'''<BODY bad code"><p>inner html</p></BODY>''')
    u'&lt;BODY bad code&quot;&gt;&lt;p&gt;inner html&lt;/p&gt;&lt;/BODY&gt;'

    >>> x = CustomHTMLFilter()
    >>> x['inner_html'] = (escape,)
    >>> x.add_tags('body p')
    >>> x(r'''&<BODY><p>inner html</p>&</BODY>''')
    u'&amp;<body><p>inner html</p>&amp;</body>'
    """
    def __init__(self, tags = "", parse_error_filter = None):
        """tags is an optional string of tags to add like the add_tags method.
        
        parse_error_filter is the filter you'd like to call if the html is too
        malformed to parse (I recomend escaping it with escape). 
        If parse_error_filter is not defined, this class will instead throw a 
        SyntaxError when parsing fails.
        """
        self.whitelist = {}
        self.parse_error_filter = parse_error_filter
        self.add_tags(tags)

    def __getitem__(self, key):
        '''This returns the whitelisted tag by that name'''
        return self.whitelist[key]

    def __setitem__(self, key, value):
        '''This assigns the whitelisted key to the value. The value should be
        an empty dictionary or a dictionary with valid attribute names as keys
        that point to sequences of filters you wish to apply to the attribute
        value.
        >>> x = CustomHTMLFilter()
        >>> soria_only = lambda text: text == "soria" and "soria" or ""
        >>> x["body"] = {"id":(soria_only,)}'''
        self.whitelist[key] = value

    def __call__(self, text):
        '''This applies the filters to the text and returns the text'''
        #try to parse it
        #If it fails, throw an error or call the parse_error_filter if it's
        #defined
        try:
            soup = BeautifulSoup.BeautifulSoup(text)
        except(BeautifulSoup.HTMLParseError):
            if self.parse_error_filter == None:
                raise SyntaxError("The HTML is too malformed")
            else:
                return unicode(self.parse_error_filter(text))

        #Go through all the tags, if they're not in the white list, remove them.
        #Also, delete all bad or empty attributes.
        for tag in soup.findAll(True):
            if tag.name not in self.whitelist:
                tag.hidden = True
            else:
                for attr, val in tag.attrs:
                    if attr in self.whitelist[tag.name]:
                        for filter in self.whitelist[tag.name][attr]:
                            tag[attr] = filter(val)
                        if tag[attr] == '':
                            del(tag[attr])
                    else:
                        del(tag[attr])

        #Find all the inner_html. If its parent has an inner_html
        #filter defined, filter it. Else, filter it with the main inner_html
        #filter
        for text in soup.findAll(text = True, recursive = True):
            parent = text.findParent()
            if self.whitelist.has_key(parent.name) and \
               self.whitelist[parent.name].has_key("inner_html"):
                for filter in self.whitelist[parent.name]["inner_html"]:
                    text.replaceWith(filter(text))
            elif self.whitelist.has_key("inner_html"):
                for filter in self.whitelist["inner_html"]:
                    text.replaceWith(filter(text))
        return unicode(soup)

    def add_tags(self, tags):
        '''This whitelists one or more tags without specifying attributes or
        filters. (It's good if you want to add a lot of empty tags)
        >>> z = CustomHTMLFilter()
        >>> z.add_tags("p i em strong b u h1")
        >>> z.whitelist == \
        {'p': {}, 'i': {}, 'em': {}, 'strong': {}, 'b': {}, 'u': {}, 'h1': {}} 
        True'''
        for tag in tags.split():
            self.whitelist[tag] = {}

    def remove_tags(self, tags):
        '''This removes one or more tags from the whitelist.
        >>> y = CustomHTMLFilter()
        >>> y.add_tags("p i em strong b u h1")
        >>> y.whitelist == \
        {'p': {}, 'i': {}, 'em': {}, 'strong': {}, 'b': {}, 'u': {}, 'h1': {}} 
        True
        >>> y.remove_tags("p i em strong b u h1")
        >>> y.whitelist
        {}
        >>> y.remove_tags("p i em strong b u h1")
        >>> y.whitelist
        {}'''
        for tag in tags.split():
            if self.whitelist.has_key(tag):
                del(self.whitelist[tag])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
