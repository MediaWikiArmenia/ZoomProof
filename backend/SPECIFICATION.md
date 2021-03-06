# Specification for ZoomProof backend server

* the backend provides a simple API for requesting the text content of a certain page of a `.djvu` or `.pdf` file and get a `JSON` response

## API
`/djvujson/sha1/page.json`
* sha1 is the sha1 checksum of the `.djvu` you want to have the `JSON` representation of
* page is a positive integer indicating the page you are querying for

`/pdfjson/sha1/page.json`
* sha1 is the sha1 checksum of the `.pdf` you want to have the `JSON` representation of
* page is a positive integer indicating the page you are querying for

* if sha1 is a string and page is a positive integer you will receive a `JSON` answer, if not you will get a `404`

## JSON format
* a succesful `JSON` response format is as in the following example

```python
{
"map":
[{"t": "Lorem", "c":[2488,72,665,57], "e":"w"},
...,],
"size": {"width": 4333, "height": 5653},
"statistics": {"min": [665, 51], "max": [984, 61], "average": [919.6, 55.2], "median": [983, 54], "mode": [983, 57]},
"errors": ""
}
```

* map is a list of text data
* size is a dict of the size of that particular page with entries "width" and "height"
* statistics is a dict of statistical information about all text objects on a page (currently min, max, average, median, mode) where each entry is a 2-element list [width, height]
* each text datapoint has three attributes: `t` (text as str), `c` (coordinates [left, top, width, height] as int list), `e` (type of text)
* the type of text is one of either (w, c, l, r, pc, ph) -> (WORD, CHARACTER, LINE, REGION, PAGECOLUMNS, PARAGRAPH)

* an unsuccesful `JSON` response format is as in the following example

```python
{
"map": [],
"size": {},
"statistics": {},
"errors": "error text"
}
```

* map is an empty list
* size in an empty dict
* statistics is an empty dict
* errors is a string describing the error that happened

### possible errors
* the desired page is not yet converted (this initiates the conversion process but temporarily returns with an error message telling you to check back in a minute)
* page is found but does not actually contain text
* the sha1 checksum is not of a .djvu/.pdf file on wikicommons
* the desired page is > than the maximum page in the file
* the sha1 can not be found via the wiki commons API

## backend pipeline
1. if the desired page for that sha1 is already cached, return it immediately by the webserver (don't even redirect to the flask app for that)
2. download metadata for the sha1 from wiki commons API
3. based on that metadata check if the the page or the sha1 are one of the aforementioned error cases, return an error [log error]
4. if the desired page and sha1 are valid, initiate the conversion of the entire document in a non-blocking fashion
	* return notification response to try and check back in a minute
	* download the .djvu/.pdf file
	* first convert the desired page and the +-x (config parameter) pages around it to JSON
	* then convert all the other pages from the .djvu/.pdf file to JSON
	* save all JSON files as `./djvujson|pdfjson/data/sha1/{page_number}.json`
	* clean up temporary files
	* [log success]
