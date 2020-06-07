"""
This module implements the various google add types that can 
be shown on MyCMS. 

It creates HTML for the adds where an example is as shown below:

    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
        <!-- DefaultHorizontal -->
        <ins class="adsbygoogle"
        style="display:block"
        data-ad-client="ca-pub-9449210019187312"
        data-ad-slot="1816544788"
        data-ad-format="auto"
        data-full-width-responsive="true"></ins>
    </script>

The above HTML is mostly the same for each type of add but some adds
have more parameters while some have less. 

The following two values are always present and never changes. This is 
specific to each mycms instance. This could be stored in the database 
or in the settings.py of mycms

        data-ad-client="ca-pub-9449210019187312"
        data-ad-slot="1816544788"

Since only a few things change, we have a base class and for each type of 
add we inheret from the base class and just add or override the required
parameters. 

The adds class then provides a dictionary to the template. 


"""





class BaseAdds(object):

    def __init__(self, dataadclient, dataadslot):
        self.dataadclient = dataadclient
        self.dataadslot = dataadslot

    def html(self):
        raise NotImplementedError("Implement in child class")

    def __str__(self):   
        raise NotImplementedError("Implement this in chlid class")



class MyCMSGoogleAdds(BaseAdds):

    def __init__(self, dataadclient, dataadslot):
        pass

    def html(self):
        pass


