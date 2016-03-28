# weakscraper
HTML scraper with templates

[![Build Status](https://travis-ci.org/michelbl/weakscraper.svg?branch=master)](https://travis-ci.org/michelbl/weakscraper)

## Description

Most HTML pages are generated using templates. Why not use templates too for scraping HTML pages? As for a template language, let's use HTML plus a few keywords. That way, the workflow with `weakscraper` is the following :
* Get the source of a HTML page you want to scrap.
* Using a few keywords, edit the HTML to select which information is of interest and which parts to discard.
* If complex processing is required, write additional callbacks.
* Run `weakscraper` on the template and on the HTML.


### Pros
* Observes the [rule of least power](https://en.wikipedia.org/wiki/Rule_of_least_power). A declarative language helps to focus on *what* to extract. *How* the information is scrapped is the job of the library.
* The template covers the whole page. If `weakscraper` encounters a part it is not aware of, it will throw an exception, allowing you to complete the template. There is little chance to miss information, even if a few pages contain a `div` you are not aware of at first.

### Cons
* To extract a bit of information, the whole parent list from the node root must be specified in the template. If you want to extract a few bits of information buried deep into the HTML tree, you probably want to use tools like `Beautiful Soup`.

## Examples



## How it works ?

## License

MIT (http://www.opensource.org/licenses/mit-license.php)
