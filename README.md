# html2Dash

html2Dash is an Documentation Set generator intended to be used with the [Dash.app](http://kapeli.com/dash/) API browser for OS X or one of its many clones. html2Dash is just like [doc2dash](https://github.com/hynek/doc2dash) but generating docset from any HTML documentations.

If you’ve never heard of Dash.app, you’re missing out: together with html2Dash it’s all your API documentation at your fingertips!

Third part library required:
   
    beautifulsoup4==4.3.2

It’s tested on Python 2.7, OS X 10.9.

# How to Use

The usage is as simple as:

	$ html2Dash <htmldir>

html2dash will create a new directory called `<htmldir>.docset` in `~/Library/Application Support/html2dash/DocSets` containing a Dash.app-compatible docset. When finished, the docset is automatically added to Dash.app.

**Options and Arguments**

The full usage is:

	$ doc2dash [OPTIONS] SOURCE  

The `SOURCE` is a directory containing the HTML documents you would like to convert.

Valid `OPTIONS` are the following:

* -n, --name  

	Name the docset explicitly instead of letting doc2dash guess the correct name from the directory name of the source.

* -d PATH, --destination PATH  

	Put the resulting docset into PATH. Default is the directory `~/Library/Application Support/html2dash/DocSets` 

* -i FILENAME, --icon FILENAME

	Add PNG icon FILENAME to docset that is used within Dash.app to represent the docset.
	
* -p INDEX_PAGE, --index-page INDEX_PAGE
	
	Set the file that is shown when the docset is clicked within Dash.app.
	
* -h, --help

	Show a brief usage summary and exit.

DEPENDENCIES:  
	
* BeautifulSoup HTML parsing library

# Demo

Generate the Docset for requests: `requests.docset`. Command：

    $ ./html2dash.py -n requests -i ~/Documents/requests-sidebar.png ~/Documents/requests  
    Create the Docset Folder!  
    Copy the HTML Documentation!  
    Create the SQLite Index    
    Create the Info.plist File  
    Create the Icon for the Docset!  
    Generate Docset Successfully!  


