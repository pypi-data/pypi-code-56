# pylint: disable=wildcard-import, unused-wildcard-import, too-few-public-methods
"""
Python Bindings for Storj (V3)
"""
from exchange import *

# Structure classes for go structure objects #

ERROR_INTERNAL = 0x02
ERROR_CANCELED = 0x03
ERROR_INVALID_HANDLE = 0x04
ERROR_TOO_MANY_REQUESTS = 0x05
ERROR_BANDWIDTH_LIMIT_EXCEEDED = 0x06

ERROR_BUCKET_NAME_INVALID = 0x10
ERROR_BUCKET_ALREADY_EXISTS = 0x11
ERROR_BUCKET_NOT_EMPTY = 0x12
ERROR_BUCKET_NOT_FOUND = 0x13

ERROR_OBJECT_KEY_INVALID = 0x20
ERROR_OBJECT_NOT_FOUND = 0x21
ERROR_UPLOAD_DONE = 0x22
"""Error defines"""


# Various handle structures:
class Handle(Structure):
    """ Handle structure """
    _fields_ = [("_handle", c_size_t)]


class Access(Structure):
    """ Access structure """
    _fields_ = [("_handle", c_size_t)]


# Various configuration structures:
class Config(Structure):
    """ Config structure """
    _fields_ = [("user_agent", c_char_p), ("dial_timeout_milliseconds", c_int32),
                ("temp_directory", c_char_p)]


class Bucket(Structure):
    """ Bucket structure """
    _fields_ = [("name", c_char_p), ("created", c_int64)]


class ListObjectsOptions(Structure):
    """ ListObjectsOptions structure """
    _fields_ = [("prefix", c_char_p), ("cursor", c_char_p), ("recursive", c_bool),
                ("system", c_bool), ("custom", c_bool)]


class ListBucketsOptions(Structure):
    """ ListBucketsOptions structure """
    _fields_ = [("cursor", c_char_p)]


class ObjectIterator(Structure):
    """ ObjectIterator structure """
    _fields_ = [("_handle", c_size_t)]


class BucketIterator(Structure):
    """ BucketIterator structure """
    _fields_ = [("_handle", c_size_t)]


class Permission(Structure):
    """ Permission structure """
    _fields_ = [("allow_download", c_bool), ("allow_upload", c_bool), ("allow_list", c_bool),
                ("allow_delete", c_bool), ("not_before", c_int64), ("not_after", c_int64)]


class SharePrefix(Structure):
    """ SharePrefix structure """
    _fields_ = [("bucket", c_char_p), ("prefix", c_char_p)]


# Various result structures:
class AccessResult(Structure):
    """ AccessResult structure """
    _fields_ = [("access", POINTER(Access)), ("error", POINTER(Error))]


class ProjectResult(Structure):
    """ ProjectResult structure """
    _fields_ = [("project", POINTER(Project)), ("error", POINTER(Error))]


class BucketResult(Structure):
    """ BucketResult structure """
    _fields_ = [("bucket", POINTER(Bucket)), ("error", POINTER(Error))]


class StringResult(Structure):
    """ StringResult structure """
    _fields_ = [("string", c_char_p), ("error", POINTER(Error))]


#########################################################
# Python Storj class with all Storj functions' bindings #
#########################################################

class LibUplinkPy(DataExchange):
    """
    Python Storj class with all Storj functions' bindings
    """

    #
    def request_access_with_passphrase(self, ps_satellite, ps_api_key, ps_passphrase):
        """
        function requests satellite for a new access grant using a passphrase
        pre-requisites: none
        inputs: Satellite Address (String), API key (String) and Passphrase (String)
        output: AccessResult (Object), Error (String) if any else None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.request_access_with_passphrase.argtypes = [c_char_p, c_char_p, c_char_p]
        self.m_libuplink.request_access_with_passphrase.restype = AccessResult
        #
        # prepare the input for the function
        lc_satellite_ptr = c_char_p(ps_satellite.encode('utf-8'))
        lc_api_key_ptr = c_char_p(ps_api_key.encode('utf-8'))
        lc_passphrase_ptr = c_char_p(ps_passphrase.encode('utf-8'))

        # get access to Storj by calling the exported golang function
        lo_access_result = self.m_libuplink.request_access_with_passphrase(lc_satellite_ptr,
                                                                           lc_api_key_ptr,
                                                                           lc_passphrase_ptr)
        #
        # if error occurred
        if bool(lo_access_result.error):
            return lo_access_result, lo_access_result.error.contents.message.decode("utf-8")
        return lo_access_result, None

    def config_request_access_with_passphrase(self, po_config, ps_satellite, ps_api_key,
                                              ps_passphrase):
        """
        function requests satellite for a new access grant using a passphrase and
                        custom configuration
        pre-requisites: none
        inputs: Config (Object), Satellite Address (String), API key (String) and
                Passphrase (String)
        output: AccessResult (Object), Error (String) if any else None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.config_request_access_with_passphrase.argtypes = [Config, c_char_p,
                                                                           c_char_p, c_char_p]
        self.m_libuplink.config_request_access_with_passphrase.restype = AccessResult
        #
        # prepare the input for the function
        if po_config is None:
            lo_config = Config()
        else:
            lo_config = po_config
        lc_satellite_ptr = c_char_p(ps_satellite.encode('utf-8'))
        lc_api_key_ptr = c_char_p(ps_api_key.encode('utf-8'))
        lc_passphrase_ptr = c_char_p(ps_passphrase.encode('utf-8'))

        # get access to Storj by calling the exported golang function
        lo_access_result = self.m_libuplink.config_request_access_with_passphrase(lo_config,
                                                                                  lc_satellite_ptr,
                                                                                  lc_api_key_ptr,
                                                                                  lc_passphrase_ptr)
        #
        # if error occurred
        if bool(lo_access_result.error):
            return lo_access_result, lo_access_result.error.contents.message.decode("utf-8")
        return lo_access_result, None

    def open_project(self, po_access):
        """
        function opens Storj(V3) project using access grant.
        pre-requisites: request_access_with_passphrase or parse_access function
                        has been already called
        inputs: Access (Object)
        output: ProjectResult (Object), Error (String) if any else None
        """
        #
        # ensure access object is already created
        if po_access is None:
            ls_error = "Invalid access object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.open_project.argtypes = [POINTER(Access)]
        self.m_libuplink.open_project.restype = ProjectResult
        #
        # open project by calling the exported golang function
        lo_project_result = self.m_libuplink.open_project(po_access)
        #
        # if error occurred
        if bool(lo_project_result.error):
            return lo_project_result, lo_project_result.error.contents.message.decode("utf-8")
        return lo_project_result, None

    def config_open_project(self, po_config, po_access):
        """
        function opens Storj(V3) project using access grant and custom configuration.
        pre-requisites: request_access_with_passphrase or parse_access function
                        has been already called
        inputs: Config (Object), Access (Object)
        output: ProjectResult (Object), Error (String) if any else None
        """
        #
        # ensure access object is already created
        if po_access is None:
            ls_error = "Invalid access object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.config_open_project.argtypes = [Config, POINTER(Access)]
        self.m_libuplink.config_open_project.restype = ProjectResult
        #
        # prepare the input for the function
        if po_config is None:
            lo_config = Config()
        else:
            lo_config = po_config
        #
        # open project by calling the exported golang function
        lo_project_result = self.m_libuplink.config_open_project(lo_config, po_access)
        #
        # if error occurred
        if bool(lo_project_result.error):
            return lo_project_result, lo_project_result.error.contents.message.decode("utf-8")
        return lo_project_result, None

    def ensure_bucket(self, po_project, ps_bucket_name):
        """
        function creates a new bucket and ignores the error when it already exists
        pre-requisites: open_project function has been already called
        inputs: Project (Object) ,Bucket Name (String)
        output: BucketResult (Object), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.ensure_bucket.argtypes = [POINTER(Project), c_char_p]
        self.m_libuplink.ensure_bucket.restype = BucketResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # open bucket if doesn't exist by calling the exported golang function
        lo_bucket_result = self.m_libuplink.ensure_bucket(po_project, lc_bucket_name_ptr)
        #
        # if error occurred
        if bool(lo_bucket_result.error):
            return lo_bucket_result, lo_bucket_result.error.contents.message.decode("utf-8")
        return lo_bucket_result, None

    def stat_bucket(self, po_project, ps_bucket_name):
        """
        function returns information about a bucket.
        pre-requisites: open_project function has been already called
        inputs: Project (Object) ,Bucket Name (String)
        output: BucketResult (Object), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.stat_bucket.argtypes = [POINTER(Project), c_char_p]
        self.m_libuplink.stat_bucket.restype = BucketResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # get bucket information by calling the exported golang function
        lo_bucket_result = self.m_libuplink.stat_bucket(po_project, lc_bucket_name_ptr)
        #
        # if error occurred
        if bool(lo_bucket_result.error):
            return lo_bucket_result, lo_bucket_result.error.contents.message.decode("utf-8")
        return lo_bucket_result, None

    def stat_object(self, po_project, ps_bucket_name, ps_storj_path):
        """
        function returns information about an object at the specific key.
        pre-requisites: open_project
        inputs: Project (Object) ,Bucket Name (String) , Object Key(String)
        output: ObjectResult (Object), Error (string) if any else None
        """
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.stat_object.argtypes = [POINTER(Project), c_char_p, c_char_p]
        self.m_libuplink.stat_object.restype = ObjectResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))
        lc_storj_path_ptr = c_char_p(ps_storj_path.encode('utf-8'))

        # get object information by calling the exported golang function
        lo_object_result = self.m_libuplink.stat_object(po_project, lc_bucket_name_ptr,
                                                        lc_storj_path_ptr)
        #
        # if error occurred
        if bool(lo_object_result.error):
            return lo_object_result, lo_object_result.error.contents.message.decode("utf-8")
        return lo_object_result, None

    def create_bucket(self, po_project, ps_bucket_name):
        """
        function creates a new bucket.
        pre-requisites: open_project function has been already called
        inputs: Project (Object) ,Bucket Name (String)
        output: BucketResult (Object), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.create_bucket.argtypes = [POINTER(Project), c_char_p]
        self.m_libuplink.create_bucket.restype = BucketResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # create bucket by calling the exported golang function
        lo_bucket_result = self.m_libuplink.create_bucket(po_project, lc_bucket_name_ptr)
        #
        # if error occurred
        if bool(lo_bucket_result.error):
            return lo_bucket_result, lo_bucket_result.error.contents.message.decode("utf-8")
        return lo_bucket_result, None

    def close_project(self, po_project):
        """
        function closes the Storj(V3) project.
        pre-requisites: open_project function has been already called
        inputs: Project (Object)
        output: Error (Object) if any else None
        """
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.close_project.argtypes = [POINTER(Project)]
        self.m_libuplink.close_project.restype = POINTER(Error)
        #
        # close Storj project by calling the exported golang function
        lo_error = self.m_libuplink.close_project(po_project)
        #
        # if error occurred
        if bool(lo_error):
            return lo_error
        return None

    def list_buckets(self, po_project, po_list_bucket_options):
        """
        function lists buckets
        pre-requisites: open_project function has been already called
        inputs: Project (Object), ListBucketsOptions (Object)
        output: Bucket List (Python List), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.list_buckets.argtypes = [POINTER(Project), POINTER(ListBucketsOptions)]
        self.m_libuplink.list_buckets.restype = POINTER(BucketIterator)
        #
        self.m_libuplink.bucket_iterator_item.argtypes = [POINTER(BucketIterator)]
        self.m_libuplink.bucket_iterator_item.restype = POINTER(Bucket)
        #
        self.m_libuplink.bucket_iterator_next.argtypes = [POINTER(BucketIterator)]
        self.m_libuplink.bucket_iterator_next.restype = c_bool
        #
        # prepare the input for the function
        if po_list_bucket_options is None:
            lo_list_bucket_options = POINTER(ListBucketsOptions)()
        else:
            lo_list_bucket_options = byref(po_list_bucket_options)

        # get bucket list by calling the exported golang function
        lo_bucket_iterator = self.m_libuplink.list_buckets(po_project, lo_list_bucket_options)
        lo_bucket_list = list()
        while self.m_libuplink.bucket_iterator_next(lo_bucket_iterator):
            lo_bucket_list.append(self.m_libuplink.bucket_iterator_item(lo_bucket_iterator))

        #
        # if error occurred
        if len(lo_bucket_list) == 0:
            return None, "No bucket found!"
        return lo_bucket_list, None

    def list_objects(self, po_project, ps_bucket_name, po_list_object_options):
        """
        function lists objects
        pre-requisites: open_project function has been already called
        inputs: Project (Object), Bucket Name (String), ListObjectsOptions (Object)
        output: Bucket List (Python List), Error (String) if any else None
        """
        #
        # ensure project object is valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.list_objects.argtypes = [POINTER(Project), c_char_p,
                                                  POINTER(ListObjectsOptions)]
        self.m_libuplink.list_objects.restype = POINTER(ObjectIterator)
        #
        self.m_libuplink.object_iterator_item.argtypes = [POINTER(ObjectIterator)]
        self.m_libuplink.object_iterator_item.restype = POINTER(Object)
        #
        self.m_libuplink.object_iterator_next.argtypes = [POINTER(ObjectIterator)]
        self.m_libuplink.object_iterator_next.restype = c_bool
        #
        # prepare the input for the function
        if po_list_object_options is None:
            lo_list_object_options = POINTER(ListObjectsOptions)()
        else:
            lo_list_object_options = byref(po_list_object_options)
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # get object list by calling the exported golang function
        lo_object_iterator = self.m_libuplink.list_objects(po_project, lc_bucket_name_ptr,
                                                           lo_list_object_options)
        lo_object_list = list()
        while self.m_libuplink.object_iterator_next(lo_object_iterator):
            lo_object_list.append(self.m_libuplink.object_iterator_item(lo_object_iterator))

        #
        # if error occurred
        if len(lo_object_list) == 0:
            return None, "No object found!"
        return lo_object_list, None

    def delete_bucket(self, po_project, ps_bucket_name):
        """
        function deletes a bucket.
        pre-requisites: open_project function has been already called
        inputs: Project (Object), Bucket Name (String)
        output: BucketResult (Object), Error (String) if any else None
        """
        #
        # ensure project handle and encryption handles are valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.delete_bucket.argtypes = [POINTER(Project), c_char_p]
        self.m_libuplink.delete_bucket.restype = BucketResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))

        # delete bucket by calling the exported golang function
        lo_bucket_result = self.m_libuplink.delete_bucket(po_project, lc_bucket_name_ptr)
        #
        # if error occurred
        if bool(lo_bucket_result.error):
            return lo_bucket_result, lo_bucket_result.error.contents.message.decode("utf-8")
        return lo_bucket_result, None

    def delete_object(self, po_project, ps_bucket_name, ps_storj_path):
        """
        function deletes an object.
        pre-requisites: open_project function has been already called
        inputs: Project (Object), Bucket Name (String), Object Key (String)
        output: ObjectResult (Object), Error (String) if any else None
        """
        #
        # ensure project handle and encryption handles are valid
        if po_project is None:
            ls_error = "Invalid project object, please check the parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.delete_object.argtypes = [POINTER(Project), c_char_p, c_char_p]
        self.m_libuplink.delete_object.restype = ObjectResult
        #
        # prepare the input for the function
        lc_bucket_name_ptr = c_char_p(ps_bucket_name.encode('utf-8'))
        lc_storj_path_ptr = c_char_p(ps_storj_path.encode('utf-8'))

        # delete object by calling the exported golang function
        lo_object_result = self.m_libuplink.delete_object(po_project, lc_bucket_name_ptr,
                                                          lc_storj_path_ptr)
        #
        # if error occurred
        if bool(lo_object_result.error):
            return lo_object_result, lo_object_result.error.contents.message.decode("utf-8")
        return lo_object_result, None

    def parse_access(self, ps_serialized_access):
        """
        function to parses serialized access grant string
        pre-requisites: none
        inputs: Serialized Access (String)
        output: AccessResult (Object), Error (String) if any else None
        """
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.parse_access.argtypes = [c_char_p]
        self.m_libuplink.parse_access.restype = AccessResult
        #

        # get parsed access by calling the exported golang function
        lo_access_result = self.m_libuplink.parse_access(ps_serialized_access)
        #
        # if error occurred
        if bool(lo_access_result.error):
            return lo_access_result, lo_access_result.error.contents.message.decode("utf-8")
        return lo_access_result, None

    def access_serialize(self, po_access):
        """
        function serializes access grant into a string.
        pre-requisites: request_access_with_passphrase or parse_access function
                        has been already called
        inputs: Access (Object)
        output: StringResult (Object), Error (String) if any else None
        """
        #
        # ensure access object is valid
        if po_access is None:
            ls_error = "Invalid access object, please check parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.access_serialize.argtypes = [POINTER(Access)]
        self.m_libuplink.access_serialize.restype = StringResult
        #
        # get serialized access by calling the exported golang function
        lc_string_result = self.m_libuplink.access_serialize(po_access)
        #
        # if error occurred
        if bool(lc_string_result.error):
            return lc_string_result, lc_string_result.error.contents.message.decode("utf-8")
        return lc_string_result, None

    def access_share(self, po_access, po_permission, po_shared_prefix):
        """
        function creates new access grant with specific permission. Permission will
                        be applied to prefixes when defined.
        pre-requisites: request_access_with_passphrase or parse_access function has
                        been already called
        inputs: Access (Object), Permission (Object), Share Prefix (Python List of Dictionaries)
        output: String Result (Object), Error (String) if any else None
        """
        #
        # ensure access object is valid
        if po_access is None:
            ls_error = "Invalid access object, please check parameter passed and try again."
            return None, ls_error
        #
        # declare types of arguments and response of the corresponding golang function
        self.m_libuplink.access_share.argtypes = [POINTER(Access), Permission,
                                                  POINTER(SharePrefix), c_size_t]
        self.m_libuplink.access_share.restype = AccessResult
        #
        # prepare the input for the function
        # check and create valid Permission parameter
        if po_permission is None:
            lo_permission = Permission()
        else:
            lo_permission = po_permission
        # check and create valid Share Prefix parameter
        # po_shared_prefix = [{"bucket": "bucket01", "prefix": "uploadPath01/data"}]
        if po_shared_prefix is None:
            lo_shared_prefix = POINTER(SharePrefix)()
            lc_array_size = c_size_t(0)
        else:
            num_of_structs = len(po_shared_prefix)
            li_array_size = (SharePrefix * num_of_structs)()
            lo_array = cast(li_array_size, POINTER(SharePrefix))
            for i, val in enumerate(po_shared_prefix):
                lo_array[i] = SharePrefix(c_char_p(val['bucket'].encode('utf-8')),
                                          c_char_p(val['prefix'].encode('utf-8')))
            lo_shared_prefix = lo_array
            lc_array_size = c_size_t(num_of_structs)
        #
        # get shareable access by calling the exported golang function
        lo_access_result = self.m_libuplink.access_share(po_access, lo_permission, lo_shared_prefix,
                                                         lc_array_size)
        #
        # if error occurred
        if bool(lo_access_result.error):
            return lo_access_result, lo_access_result.error.contents.message.decode("utf-8")
        return lo_access_result, None
