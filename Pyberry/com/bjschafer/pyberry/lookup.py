import urllib.request as urllib

class Lookup(object):
    '''
    Looks up book information online.  Currently only uses Google Books API.
    Also, currently only allows searching by ISBN.
    
    Searching is accomplished using the RESTful API from Google Books.  This
    is relatively simple for sending the search request but rather more troublesome
    for processing the received data.  
    
    @TODO: less hardcoding of searching (1.0)
    @TODO: add other search resources (2.0)
    @TODO: allow search by any attribute (1.0)
    @TODO: better error handling. (1.0)
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.BASE_URL = '''https://www.googleapis.com/books/v1/volumes?q='''
        
    def _search(self, searchterm):
        '''Does the dirty work of searching.  It should be flexible enough
        to allow for any kind of search given the proper calling method.
        It's "private" because it shouldn't be called by the UI, the UI
        should call a helper method.
        
        It returns a dictionary, with each attribute as a key.  This is
        helpful because the dictionary with a little tweaking can be stuck
        right into Book's createFromDict method.
        
        Calls _process() to process, that way each method does more of what
        it should.
        '''
        url = self.BASE_URL + searchterm
        info = []
        for line in urllib.urlopen(url):
            info.append(line)
        returnMe = self._process(info)
        returnMe = self._cleanAuthor(returnMe)
        return returnMe
    
    def _process(self, info):
        '''
        Okay, this processes what's downloaded.
        '''
        returnMe = {}
        for i in range(0, len(info)-1):
            line = str(info[i])
            line.strip()
            print(line)
            l = line.split('"')[1::2]
            try: # still trying something like this...
                if l[0] == "title":
                    returnMe["title"] = l[1]
                elif l[0] == "authors":
                    returnMe["author"] = info[i+1] # potential for out of bounds.
                elif l[0] == "pageCount":
                    returnMe["pages"] = l[1]
                elif l[0] == "publishedDate":
                    returnMe["publ_year"] = l[1][0:4]
                elif l[0] == "publisher":
                    returnMe["publisher"] = l[1]
                elif l[0] == "description":
                    returnMe["description"] = l[1]
                    
            except:
                pass
        return returnMe
        
    def _cleanAuthor(self, bookInfo):
        '''
        Cleans up the author attribute in the dict.
        '''
        author = bookInfo["author"]
        author = str(author)
        author = author[8:-5] # bad idea.
        bookInfo["author"] = author
        return bookInfo
            
    def byISBN(self, isbn):
        '''
        Search by ISBN.  Mostly just calls the _search method.
        
        Returns a somewhat tweaked dictionary, see above.
        '''
        if len(isbn) != 10 and len(isbn) != 13:
            raise ValueError("Invalid ISBN length.")
        else:
            searchterm = "isbn:" + isbn
            myReturn = self._search(searchterm)
            myReturn["isbn"] = isbn
        return myReturn
            