#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# #############################################################################
#    Apache2 2020 - manatlan manatlan[at]gmail(dot)com
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    more: https://github.com/manatlan/guy
# #############################################################################

import guy,sys
from .tag import Tag
import typing as T


_gg=lambda x: x.get() if isinstance(x,ReactiveProp) else x #TODO: rename to value() ?

def log(*a):
    # print(*a)
    pass


class CSS(Tag):
    def __init__(self,content):
        if content.startswith("http"):
            self.tag="link"
            super().__init__(type="text/css",rel="stylesheet",href=content)
        else:
            self.tag="style"
            super().__init__(content,type="text/css")

class JS(Tag):
    tag="script"
    def __init__(self,content):
        if content.startswith("http"):
            super().__init__(type="text/javascript",src=content)
        else:
            super().__init__(content,type="text/javascript")




class ReactiveProp:
    def __init__(self,dico:dict,attribut:str):
        self.__instance=dico
        self.__attribut=attribut
    def set(self,v):
        self.__instance[self.__attribut]=v
    def get(self):
        return self.__instance[self.__attribut]


    def __eq__(self, v):
        return self.get() == _gg(v)

    def __ne__(self, v):
        return self.get() != _gg(v)

    def __lt__(self, v):
        return self.get() < _gg(v)

    def __le__(self, v):
        return self.get() <= _gg(v)

    def __ge__(self, v):
        return self.get() >= _gg(v)

    def __gt__(self, v):
        return self.get() > _gg(v)


    def __iadd__(self,v):
        vv=self.get() + _gg(v)
        self.set( vv )
        return self

    def __int__(self):
        return int(self.get())
    def __bool__(self):
        return bool(self.get())
    def __str__(self):
        return str(self.get())

    def __repr__(self):
        iid=self.__instance.id if hasattr(self.__instance,"id") else str(self.__instance)
        return "<%s instance=%s attr=%s>" % (self.__class__.__name__,iid,self.__attribut)
    #TODO: add a lot of __slot__ ;-)


class ReactiveMethod:
    """ like ReactiveProp, but for gtag.method wchich can return binded tag
        (object created by @bind decorator)
    """
    def __init__(self,instance,method,args,kargs):
        self.__instance=instance
        self.__method=method
        self.__a=args
        self.__k=kargs

    def __call__(self):
        return self.__method(self.__instance,*self.__a,**self.__k)

    def __str__(self) -> str:
        return str(self())


def bind( method ): # gtag.method decorator -> ReactiveMethod
    """ Decorator to make a gtag.method() able to return a "Reactive Tag" !
        (like 'computed vars' in vuejs)
    """
    def _(gtagInstance,*a,**k):
        assert isinstance(gtagInstance,GTag)
        return ReactiveMethod(gtagInstance,method,a,k)
    return _


class GtagProxy:
    """ Expose props(as ReactiveProps)/method from a gtag """
    def __init__(self,instance):
        self.__instance=instance
    def __getattr__(self,name:str):
        if name in self.__instance.__dict__.keys(): # bind a data attribut  -> return a ReactiveProp
            o=self.__instance.__dict__[name]
            if isinstance(o,ReactiveProp):
                return o
            else:
                return ReactiveProp(self.__instance.__dict__,name)
        elif name in dir(self.__instance):   # bind a self.method    -> return a js/string for a guy's call in js side
            def _(*a,**k):
                method=getattr(self.__instance,name)
                return method(*a,**k)
            return _
        else:
            raise Exception("Unknown method/attribut '%s' in '%s'"%(name,repr(self.__instance)))
    def __repr__(self):
        return repr(self.__instance)


class GTag:
    """
    The magic thing ;-)
    """
    size=None
    """ size of the windowed runned gtag (tuple (width,height) or guy.FULLSCREEN or None) """

    # implicit parent version (don't need to pass self(=parent) when creating a gtag)
    def __init__(self,*a,**k):
        if "dontGuessParent" in k.keys(): # clonage (only main tags, so parent is None)
            del k["dontGuessParent"]
            parent=None
        else:
            # guess parent
            frame = sys._getframe(1)
            arguments = frame.f_code.co_argcount
            if arguments == 0:
                parent=None
            else:
                caller_calls_self = frame.f_code.co_varnames[0]
                parent=frame.f_locals[caller_calls_self]
                assert isinstance(parent,GTag)
                if parent is self: parent=None  #for TU only

        self._id="%s_%s" % (self.__class__.__name__,hex(id(self))[2:])
        self._childs={}

        self._args=a
        self._kargs=k

        self._parent=parent

        log("INIT",repr(self))
        self.init(*self._args,**self._kargs)
        self._tag = self.build()

        # Store the instance in the main._childs
        main=self._getMain()
        main._childs[self.id]=self # so, childs should die when main dies, in GC ;-)

    def _getChild(self,id):
        assert self._parent is None,"You are not on the main instance, you can't get a child"
        return self._childs[id]

    def _getMain(self):
        x=self
        while x._parent is not None:
            x=x._parent
        return x

    @property
    def id(self):
        return self._id


    @property
    def parent(self)-> any:
        """ return caller/binder to parent instance (None if gtag is the main) """
        if self._parent is None:
            return None
        else:
            return GtagProxy( self._parent )


    @property
    def main(self)-> any:
        """ return caller/binder to main instance """
        return GtagProxy( self._getMain() )


    @property
    def bind(self) -> any:
        """ to bind attribute or method !"""
        class Binder:
            def __getattr__(this,name:str):
                if name in self.__dict__.keys(): # bind a data attribut  -> return a ReactiveProp
                    o=self.__dict__[name]
                    if isinstance(o,ReactiveProp):
                        return o
                    else:
                        return ReactiveProp(self.__dict__,name)
                elif name in dir(self):   # bind a self.method    -> return a js/string for a guy's call in js side
                    def _(*args):
                        if args:
                            return "self.bindUpdate('%s',GID,'%s',%s)" % (self.id,name,",".join([str(i) for i in args]) ) #TODO: escaping here ! (and the render/str ?) json here !
                        else:
                            return "self.bindUpdate('%s',GID,'%s')" % (self.id,name)
                    return _
                else:
                    raise Exception("Unknown method/attribut '%s' in '%s'"%(name,self.__class__.__name__))
        return Binder()


    def _clone(self):
        props={k:v for k,v in self.__dict__.items() if k[0]!="_"}
        gtag = self.__class__(*self._args,**self._kargs,dontGuessParent=True)
        gtag.__dict__.update(props)
        assert isinstance(gtag,GTag)
        log("^^^ CLONED ^^^",repr(self),"-->",repr(gtag))
        return gtag


    def _guessHeaders(self):
        """ try to found the headers of the main tag used by the gtag component, and return the html elements to include in header
            (downside: importing css/js will depends only on first tag returned by the gtag)
            (downside: as tag can be produce by a reactivemethod, we need to execute it)
        """
        mklist=lambda x: x if isinstance(x,list) else [x]
        ll=[]
        if self._tag:
            tag=self._tag
            if isinstance(tag,ReactiveMethod): tag=tag()    # <- dangerous
            if hasattr(tag,"css"):
                ll.extend( [CSS(i) for i in mklist(getattr(tag,"css")) if i] )
            if hasattr(tag,"js"):
                ll.extend( [JS(i) for i in mklist(getattr(tag,"js")) if i] )
        return ll


    def init(self,*a,**k):
        """ Override to make inits (replace the __init__(), but same role)"""
        pass

    def build(self) -> T.Union[Tag,None]:
        """ Override for static build
            SHOULD RETURN a "Tag" (not a GTag)
        """
        pass

    def script(self):
        """ Override to get back some js code"""
        pass


    def __str__(self):
        o= self._tag
        if isinstance(o,ReactiveMethod):
            o=o()
        if o is None:
            return ""
        else:
            assert isinstance(o,Tag), "'%s' doesn't produce a Tag, wtf?!" % self.__class__.__name__ # can't produce a gtag (non-sense !)
            o.id=self.id # set an id for js interactions (cf update()/bindUpdate())
            return str(o)

    def __repr__(self):
        return "<GTAG:%s %s (parent:%s)>" % (self.__class__.__name__, self.id,self._parent.id if self._parent else "no")

    def __setattr__(self,k,v):
        # current="%s_%s" % (self.__class__.__name__,id(self))
        o=self.__dict__.get(k)
        if isinstance(o,ReactiveProp):
            # print("Maj %s ReactProp %s <- %s" % (current,k,repr(v)))
            o.set( _gg(v) )
        else:
            # print("Maj %s Prop %s <- %s" % (current,k,repr(v)))
            super().__setattr__(k,v)

    def _getScripts(self) -> str:
        ll=[]
        for k,v in self._childs.items():
            js=v and v.script() or None
            if js:
                if isinstance(js,ReactiveMethod): js=js() # dangerous ?
                ll.append( "(function(tag){%s})(document.getElementById('%s'))" % (str(js),k) )
        return ";".join(ll)


    def update(self) -> dict:
        h=str(self)
        s=self._getScripts()
        log(">>>UPDATE:",repr(self))
        log("   and childs:",len(self._childs),self._childs.keys())
        return dict(script="""document.querySelector("#%s").innerHTML=`%s`;%s""" % (
            self.id, h,s
        ))

    def run(self,*a,**k) -> any:
        """ Run as Guy App (using Chrome) """
        return GTagApp(self,False).run(*a,**k)

    def runCef(self,*a,**k) -> any:
        """ Run as Guy App (using Cef) """
        return GTagApp(self,False).runCef(*a,**k)

    def serve(self,*a,**k) -> any:
        """ Run as Guy Server App """
        return GTagApp(self,True).serve(*a,**k)



class GTagApp(guy.Guy):
    """ The main guy instance app, which cn run a gtag inside """

    def __init__(self,gtag,isMultipleSessionPossible=False):
        assert isinstance(gtag,GTag)
        self._originalGTag=gtag

        self.size=gtag.size

        if isMultipleSessionPossible:
            self._ses={}
        else:
            self._ses=None
        super().__init__()

    def render(self,path=None):
        o=self._originalGTag
        if isinstance(o,ReactiveMethod): o=o()  # TODO: not good here !
        hh=o._guessHeaders()

        return """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script>
            if(!sessionStorage["gtag"]) sessionStorage["gtag"]=Math.random().toString(36).substring(2);
            var GID=sessionStorage["gtag"];

            async function getSessionId() {return GID}
            async function _render(html,script) {
                document.body.innerHTML=html;
                if(script) eval(script)
            }
            function update() { return self.update(GID) /*promise*/ }
        </script>
        %s
        <style>
        div.hbox {display: flex;flex-flow: row nowrap;align-items:center}
        div.vbox {display: flex;flex-flow: column nowrap;}
        div.hbox > *,div.vbox > * {flex: 1 1 50%%;margin:1px}
        </style>
    </head>
    <body>
            <script src="guy.js"></script>
    </body>
</html>
        """ % "\n".join([str(h) for h in hh])

    async def init(self):
        if self._ses is not None:
            gid=await self.js.getSessionId()
            log("CREATE SESSION:",gid)
            gtag = self._ses.get(gid)
            if gtag is None:
                gtag = self._originalGTag._clone()
                self._ses[gid] = gtag
        else:
            gtag = self._originalGTag

        gtag.exit = self.exit

        log("SERVE",repr(gtag),gtag._childs)
        await self.js._render( str(gtag), gtag._getScripts() )

    def bindUpdate(self,id:str,gid:str,method:str,*args):
        """ inner (js exposed) guy method, called by gtag.bind.<method>(*args) """
        if self._ses is None:
            gtag=self._originalGTag
            gid=None
        else:
            gtag=self._ses[gid]

        #////////////////////////////////////////////////////////////////// THE MAGIC TODO: move to gtag
        obj=gtag._getChild(id)
        gtag._childs={gtag.id:gtag,obj.id:obj} # ULTRA IMPORTANT ;-)
        # keep the main tag, and the current object !
        # (others will be rebuild during rendering)

        log("BINDUPDATE on",repr(gtag),"---obj-->",repr(obj))
        r=getattr(obj,method)(*args)
        #////////////////////////////////////////////////////////////////// THE MAGIC
        return self.update(gid)

    def update(self, gid):
        """ exposed in guy context (to manually force a refresh) """
        gtag=self._ses[gid] if gid else self._originalGTag
        return gtag.update() #could update the obj gtag only !
