import falcon

from grab import Grab
from falcon_cors import CORS

from lib.middleware.JSONTranslator import JSONTranslator
from lib.middleware.RequireJSON import RequireJSON

from lib.listener.ExtractThreadURL import ExtractThreadURL
from lib.listener.ExtractPost import ExtractPost
from lib.listener.ExtractFirstPostId import ExtractFirstPostId
from lib.listener.ExtractCategoryLastPageURL import ExtractCategoryLastPageURL
from lib.listener.ExtractCategoryPrevPageURL import ExtractCategoryPrevPageURL
from lib.listener.ExtractThreadLastPageURL import ExtractThreadLastPageURL
from lib.listener.ExtractThreadPrevPageURL import ExtractThreadPrevPageURL
from lib.listener.ExtractThreadNextPageURL import ExtractThreadNextPageURL

from lib.listener.SaveForumPost import SaveForumPost
from lib.listener.SaveNewsArticle import SaveNewsArticle

from lib.listener.ExtractArticle import ExtractArticle
from lib.listener.ExtractArticleURL import ExtractArticleURL
from lib.listener.NewsInfoIsArticleDuplicate import NewsInfoIsArticleDuplicate

cors = CORS(
  allow_all_origins=True,
  allow_all_headers=True,
  allow_all_methods=True
)
api  = falcon.API(middleware=[cors.middleware, RequireJSON(), JSONTranslator()])

api.add_route("/spider/forum/extract/threadUrl", ExtractThreadURL())
api.add_route("/spider/forum/extract/post", ExtractPost())
api.add_route("/spider/forum/extract/post/firstPostId", ExtractFirstPostId())
api.add_route("/spider/forum/extract/category/lastPageUrl", ExtractCategoryLastPageURL())
api.add_route("/spider/forum/extract/category/prevPageUrl", ExtractCategoryPrevPageURL())
api.add_route("/spider/forum/extract/thread/lastPageUrl", ExtractThreadLastPageURL())
api.add_route("/spider/forum/extract/thread/prevPageUrl", ExtractThreadPrevPageURL())
api.add_route("/spider/forum/extract/thread/nextPageUrl", ExtractThreadNextPageURL())

api.add_route("/spider/forum/save/post", SaveForumPost())

api.add_route("/spider/news/extract/article", ExtractArticle())
api.add_route("/spider/news/extract/articleUrl", ExtractArticleURL())

api.add_route("/spider/news/info/isArticleDuplicate", NewsInfoIsArticleDuplicate())

api.add_route("/spider/news/save/article", SaveNewsArticle())