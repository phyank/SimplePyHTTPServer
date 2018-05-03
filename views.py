
import os,json,threading



SESSION_STATUS = {0: 'NOT_INIT', 1: 'INIT', 2: 'LOGIN_SUCCESS', 3: 'TEMPORARY_LOGIN_FAILED',
                  4: 'FAILED_AND_QUIT', 5: 'TIME_OUT', 6: 'UNKNOWN_ERROR',7:'NEED_SLEEP'}

ELECTOR_STATUS = {0:'NOT_INIT',1:'INIT',2:'SUBMIT_SUCCEES',3:'SUBMIT_FAILED',4:'UNKNOWN_ERROR',5:'CONFLICT'}


class MainStatus: #This class is created only for demo. It shows that you can use the way we work in python to work with this http server.
    def __init__(self):
        self.id=1
        self.article_list={}
        self.security_code=51033218

    def insert_article(self,data):
        self.article_list[self.id]=data
        self.id+=1
        return self.id-1

    def get_article_by_id(self,id):
        try:
            return self.article_list[id]
        except:
            return -1

    def reinit(self,passphrase):
        if passphrase==self.security_code:
            self.id=1
            self.article_list={}
            return True
        else:
            return False






mainStatusMutex=threading.Lock()
mainStatus=MainStatus()



TEST_PAGE="""<!DOCTYPE html>
<html>
<head>
<link href="static/css/test.css" rel="stylesheet" />
</head>
<body>
<div class="test">
<p>灰化肥不会挥发</p>
<p>黑化肥挥发使灰化肥发黑</p>
</div>
<div>
<img src="/static/image/test.jpg" />
</div>
</body>
</html>
"""

DEFAULT_ERROR_MESSAGE = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: %(code)d</p>
        <p>Message: %(message)s.</p>
        <p>Error code explanation: %(code)s - %(explain)s.</p>
    </body>
</html>
"""




class FileOpeningError:
    pass



class ViewsResponse:
    def __init__(self, content, head={}, status=200):
        self.status=status
        self.head=head
        self.content=content.encode("UTF-8")
        if status==200:
            self.head["Content-type"] = "text/html;charset=UTF-8"
        if len(self.content)!=0:
            self.head["Content-Length"]=str(len(self.content))


class ViewsAjaxResponse(ViewsResponse):
    def __init__(self,dict):
        ViewsResponse.__init__(self,json.dumps(dict),{})

class ViewsRedirect(ViewsResponse):
    def __init__(self,url="/"):
        ViewsResponse.__init__(self,"",head={"Location":url},status=301)




def open_file_as_string(filepath):

    filepath=os.path.dirname(__file__)+filepath

    if os.path.exists(filepath):
        try:
            f=open(filepath, "rb")
            result = (f.read()).decode('utf-8','ignore')
            f.close()
            return result
        except:
            raise FileOpeningError
    else:
        raise FileNotFoundError


def command_selector(command,method,data):

    if command=="/test":
        return test(method,data)

    elif command=="/post":
        return post_article(method,data)

    elif command=="/result":
        return get_result(method,data)

    elif command=="/clean":
        return clean_records(method,data)

    elif command=="/":
        return index(method,data)


    else:
        return


### Demo of Views starts here:


def clean_records(method,data):#one dynamic page
    try:
        result=mainStatus.reinit(int(data['pass']))
        if result:
            return ViewsResponse("Success")
        else:
            return ViewsResponse("Incorrect passphrase",{},403)
    except:
        return ViewsResponse("",{},500)


def post_article(method,data):#one dynamic page
    if method=="GET":
        return ViewsResponse("",{},403)
    elif method=="POST":
        article=data['article']

        id=mainStatus.insert_article(article)

        if id:
            return ViewsResponse(str(id))
        else:
            return ViewsResponse("",{},500)
    else:
        return ViewsResponse("",{},403)

def get_result(method,data):#one dynamic page
    if method=="GET":
        print(data)
        article = ""
        try:
            with mainStatusMutex:
                article=mainStatus.get_article_by_id(int(data['id']))
        except:
            return ViewsResponse("",{},404)
        print(article)
        try:
            return ViewsResponse(str(len(article)))
        except:
            return ViewsResponse("",{},500)
    else:
        return ViewsResponse("",{},403)


def index(method,data):#one dynamic page
    return ViewsRedirect("/test")


def test(method,data):#one dynamic page

    if method=="POST":
        for i in data:
            print("key:"+i+"\n"+"value:"+data[i])
        return ViewsResponse(TEST_PAGE)
    elif method=="GET":
        if not data:
            return ViewsResponse(TEST_PAGE)
        else:
            c=""
            for i in data:
                c += i + ':' + data[i] + "\r\n"
            return ViewsResponse(c)
    else:
        return ViewsRedirect('/css/test.css')




