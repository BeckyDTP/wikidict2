from configparser import NoSectionError

from article_parsers import DefaultArticleParser, ArticleParserWithLangnames, SectionAndArticleParser
from handlers import ConfigHandler, LogHandler

class Wiktionary(object):
    """ A class for handling one edition of Wiktionary """

    def __init__(self, wc, cfg_fn):
        """ 
        @param wc: Wiktionary code
        @param cfg_fn: name and path of the configuration file
        """
        #try:
        self.wc = wc
        self.cfg = ConfigHandler(wc, cfg_fn)
        self.log_handler = LogHandler(self.cfg)
        self.init_parser_of_type()
        self.dump_path = (self.cfg['dumpdir'] + '/' + self.cfg['fullname'] + '/' +
                self.wc + 'wiktionary.txt')
        #except NotImplementedError as e:
        #    raise NotImplementedError(e)
        #except KeyError as e:
        #    self.log_handler.error(str(e.message) + \
        #                           " parameter must be defined in config file ")
        #except NoSectionError as e:
        #    self.log_handler.error("Section not defined " + str(wc))
        #except Exception as e:
        #    self.log_handler.error("Unknown error " + str(e))

    def init_parser_of_type(self):
        """ Initialize the appropriate parser specified in the configuration file """
        type_ = self.cfg['parser_type']
        if type_ == 'default':
            self.article_parser = DefaultArticleParser(self)
        elif type_ == 'langnames':
            self.article_parser = ArticleParserWithLangnames(self)
        elif type_ == 'section_level':
            self.article_parser = SectionAndArticleParser(self)
        else:
            raise NotImplementedError(
                "Parser type " + str(type_) + " not implemented\n")

    def set_parser(self, parser):
        self.article_parser = parser

    def read_dump(self):
        """ Iterate through dump and yield each article 
        as a tuple of its title and text """
        txt_f = open(self.dump_path)
        page_sep = '%%#PAGE'        
        this_title = str()
        this_article = str()
        last_title = str()
        last_article = str()
        for l in txt_f:
            if l.startswith(page_sep):
                if this_article and this_title:
                    last_article = this_article
                    last_title = this_title
                    this_article = str()
                    this_title = l.split(page_sep)[-1].strip()
                    yield tuple([last_title, last_article])
                else:
                    this_title = l.split(page_sep)[-1].strip()
            else:
                this_article += l
        txt_f.close()
        yield tuple([this_title, this_article])

    def parse_all_articles(self):
        """ Calling parse_article for each article """
        for article in self.read_dump():
            self.article_parser.parse_article(article)

    def write_pairs(self):
        """ Writing the extracted translations to file """
        self.article_parser.write_word_pairs_to_file()

