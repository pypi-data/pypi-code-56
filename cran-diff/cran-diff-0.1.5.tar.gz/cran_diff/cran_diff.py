import datetime
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from .models import Packages
from .models import Imports
from .models import Suggests
from .models import Exports
from .models import Arguments
from .models import News
from .models import Tags
from .models import TagMembers


def make_querymaker(connect_string):
    """Instantiates QueryMaker class"""
    engine = create_engine(connect_string)
    Session = sessionmaker(bind=engine)
    query_maker = QueryMaker(Session())
    return query_maker


class NotFoundError(Exception):
    pass


class QueryMaker():
    def __init__(self, session):
        self.session = session


    def get_names(self):
        """Gets unique names of all packages in database

        return: list of package names
        """ 
        names = self.session.query(Packages.name).distinct()
        names = [element for tupl in names for element in tupl]
        return names

    
    def check_name_and_version(self, package_names, versions):
        """Checks that package names and corresponding versions are in database.
        Exception is raised if a package or a respective version is not.

        :params 
        package_names: list of package name strings
        versions: list of lists with package version number strings
        """
        query = (self.session.query(Packages.name, Packages.version)
                .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        for p_id, package in enumerate(package_names):
            for version in versions[p_id]:
                db_entry = [i for i in result if i == (package, version)]
                if len(db_entry) == 0:
                    raise NotFoundError(f"{package} v{version}")


    def get_latest_versions(self, package_names):
        """Lists all versions of a given list of packages

        :param package_names: list of package name strings
        :return: a dictionary with list of versions for each package
        """
        query = (self.session.query(Packages.name, Packages.version)
                            .filter(Packages.name.in_(package_names))
                            .order_by(Packages.date.desc()))
        result = query.all()
        version_dict = {}
        for package in package_names:
            versions = [i[1] for i in result if i[0] == package]
            if len(versions) == 0:
                raise NotFoundError(package)
            version_dict.update({package: versions})
        return version_dict


    def query_imports(self, package_names, versions):
        """Get dictionary of package imports
            
        :params
        package_names: list of package name strings
        versions: list of lists with package version number strings
        
        :return: a dictionary of imports with their version numbers
        """
        self.check_name_and_version(package_names, versions)
        query = (self.session.query(Imports.name, Imports.version, Packages.name, Packages.version)
                .join(Packages, Packages.id == Imports.package_id)
                .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        import_dict = {}
        for p_id, package in enumerate(package_names):
            package_dict = {}
            for version in versions[p_id]:
                imports = dict([i[:2] for i in result if i[2:] == (package, version)])
                package_dict.update({version: imports})
            import_dict.update({package: package_dict})
        return import_dict


    def query_suggests(self, package_names, versions):
        """Get dictionary of package suggests

        :params
        package_names: list of package name strings
        versions: list of lists with package version number strings

        :return: a dictionary of suggests with their version numbers
        """
        self.check_name_and_version(package_names, versions)
        query = (self.session.query(Suggests.name, Suggests.version, Packages.name, Packages.version)
                .join(Packages, Packages.id == Suggests.package_id)
                .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        suggest_dict = {}
        for p_id, package in enumerate(package_names):
            package_dict = {}
            for version in versions[p_id]:
                suggests = dict([i[:2] for i in result if i[2:] == (package, version)])
                package_dict.update({version: suggests})
            suggest_dict.update({package: package_dict})
        return suggest_dict


    def query_exports(self, package_names, versions):
        """Get dictionary of package exports

        :params
        package_names: list of package name strings
        versions: list of lists with package version number strings

        :return: a dictionary of exports, including type (function, class, etc)
        """
        self.check_name_and_version(package_names, versions)
        query = (self.session.query(Exports.name, Exports.type, Packages.name, Packages.version)
                .join(Packages, Packages.id == Exports.package_id)
                .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        export_dict = {}
        for p_id, package in enumerate(package_names):
            package_dict = {}
            for version in versions[p_id]:
                exports = dict([i[:2] for i in result if i[2:] == (package, version)])
                package_dict.update({version: exports})
            export_dict.update({package: package_dict})
        return export_dict
 

    def query_arguments(self, package_names, versions):
        """Get dictionary of package functions and their arguments

        :params
        package_names: list of package name strings
        versions: list of lists with package version number strings

        :return: a dictionary of functions and their arguments for each version
        """
        self.check_name_and_version(package_names, versions)
        query = (self.session.query(Packages.name, Packages.version, Arguments.function, Arguments.name, Arguments.default)
            .join(Arguments, Arguments.package_id == Packages.id)
            .filter(or_(and_(Packages.name == package_names[i], Packages.version.in_(versions[i])) for i in range(len(package_names)))))
        result = query.all()
        argument_dict = {}
        for p_id, package in enumerate(package_names):
            package_dict = {}
            for version in versions[p_id]:
                functions = set([row[2] for row in result if row[:2] == (package, version)])
                version_arguments = {}
                for function in functions:
                    arguments = dict([row[3:] for row in result if row[:3] == (package, version, function)])
                    version_arguments.update({function: arguments})
                package_dict.update({version: version_arguments})
            argument_dict.update({package: package_dict})
        return argument_dict


    def get_news(self):
        query = (self.session.query(Packages.name, Packages.version, Packages.date, Packages.title, Packages.description, News.category, News.text, News.type)
                .join(News, News.package_id == Packages.id))
        result = query.all()
        #Get list of dates, starting most recent
        dates = list(set([i[2].date() for i in result]))
        dates.sort(reverse = True)
        #Get all package updates and news for past five days
        new = {}
        updated = {}
        for date in dates[:5]:
            #Only include dates since update was applied (for now)
            if date < datetime.date(year = 2020, month = 5, day = 27):
                continue
            packages = list(set([i[0] for i in result if i[2].date() == date]))
            new_packages = []
            package_news = []
            for package in packages:
                package_data = [i for i in result if i[0] == package and i[2].date() == date]
                types = [i[-1] for i in package_data]
                #Check whether new package (and locate release version)
                if "new" in types:
                    release_data = [i for i in package_data if i[-1] == "new"][0]
                    package_dict = {"name": package}
                    package_dict.update({"initial_version": release_data[1]})
                    package_dict.update({"title": release_data[3]})
                    package_dict.update({"description": release_data[4]})
                    new_packages.append(package_dict)
                #Check for version updates
                if "update" in types:
                    update_data = [i for i in package_data if i[-1] == "update"]
                    update_versions = list(set([i[1] for i in update_data]))
                    for version in update_versions:
                        news = dict([i[5:7] for i in update_data if i[1] == version])
                        version_dict = {"name": package}
                        version_dict.update({"new_version": version})
                        categories = [i[5] for i in update_data if i[1] == version]
                        text = [i[6] for i in update_data if i[1] == version]
                        #Include version news if this exists
                        if categories[0] != "" or text[0] != "":
                            version_dict.update({"news": news})
                        package_news.append(version_dict)
            new.update({date.strftime('%Y/%m/%d'): new_packages})
            updated.update({date.strftime('%Y/%m/%d'): package_news})
        return new, updated


    def get_tags(self):
        tags = self.session.query(Tags.name, Tags.topic).distinct()
        tags = [{"name": i[0], "topic": i[1]} for i in tags]
        return tags


    def query_tag_members(self, tags):
        """Lists all packages belonging to a list of tags

        :param tags: list of tags
        :return: a dictionary with list of member-packages for each tag
        """
        query = (self.session.query(Packages.name, Tags.name)
                .join(TagMembers, Packages.id == TagMembers.package_id)
                .join(Tags, Tags.id == TagMembers.tag_id)
                .filter(Tags.name.in_(tags)))
        result = query.all()
        member_dict = {}
        for tag in tags:
            members = [i[0] for i in result if i[1] == tag]
            if len(members) == 0:
                if len([i for i in result if i[1] == tag]) == 0:
                    #Tag is not in database
                    raise NotFoundError(tag)
            member_dict.update({tag: members})
        return member_dict


    def query_package_tags(self, package_names):
        """Lists all tags of a given list of packages

        :param package_names: list of package name strings
        :return: a dictionary with list of tags for each package
        """
        query = (self.session.query(Tags.name, Tags.topic, Packages.name)
                .join(TagMembers, Tags.id == TagMembers.tag_id)
                .join(Packages, Packages.id == TagMembers.package_id)
                .filter(Packages.name.in_(package_names)))
        result = query.all()
        tag_dict = {}
        for package in package_names:
            tags = [{"name": i[0], "topic": i[1]} for i in result if i[2] == package]
            if len(tags) == 0:
                if len([i for i in result if i[2] == package]) == 0:
                    #Package is not in database
                    raise NotFoundError(package)
            tag_dict.update({package: tags})
        return tag_dict


def get_diff(result_dict, package_names, version_pairs):
    """Get dictionary of diffs for imports and suggests
        
    :params
    result_dict: output from query_imports() or query_suggests()
    package_names: names of CRAN packages
    version_pairs: pairs of package version numbers
    :return: a dictionary with added, removed and changed (version numbers) packages
    """
    diff_dict = {}
    for p_id, package in enumerate(package_names):
        package_dict = {}
        for pair in version_pairs[p_id]:
            set1 = set(result_dict[package][pair[0]].items())
            set2 = set(result_dict[package][pair[1]].items())
            diff1 = set1 - set2
            diff2 = set2 - set1
            #Check for version changes
            changed = []
            added = []
            removed = []
            for i in diff1:
                was_changed = False
                for j in diff2:
                    if i[0] == j[0]:
                        changed.append({'package': i[0], 'old': j[1], 'new': i[1]})
                        was_changed = True
                        break
                if not was_changed:
                    added.append(i)
            for i in diff2:
                was_changed = False
                for j in diff1:
                    if i[0] == j[0]:
                        was_changed = True
                        break
                if not was_changed:
                    removed.append(i)
            added = [list(elem) for elem in added]
            removed = [list(elem) for elem in removed]
            pair_diff = {'added': added,
                        'removed': removed,
                        'version changes': changed}
            pair_key = f"{pair[0]}_{pair[1]}"
            package_dict.update({pair_key: pair_diff})
        diff_dict.update({package: package_dict})
    return diff_dict


def get_export_diff(result_dict, package_names, version_pairs):
    """Get dictionary of export diffs for each package version-pair
        
    :params
    result_dict: output from query_exports()
    package_names: names of CRAN packages
    version_pairs: pairs of package version numbers
    :return: a dictionary with added and removed exports
    """
    diff_dict = {}
    for p_id, package in enumerate(package_names):
        package_dict = {}
        for pair in version_pairs[p_id]:
            set1 = set(result_dict[package][pair[0]].items())
            set2 = set(result_dict[package][pair[1]].items())
            diff1 = set1 - set2
            diff2 = set2 - set1
            #Check which exports have been added / removed
            added = []
            removed = []
            for i in diff1:
                added.append(i)
            for i in diff2:
                removed.append(i)
            added = [list(elem) for elem in added]
            removed = [list(elem) for elem in removed]
            pair_diff = {'added': added,
                        'removed': removed}
            pair_key = f"{pair[0]}_{pair[1]}"
            package_dict.update({pair_key: pair_diff})
        diff_dict.update({package: package_dict})
    return diff_dict


def get_argument_diff(result_dict, package_names, version_pairs):
    """Get dictionary of argument diffs for each package version-pair

    :params
    result_dict: output from query_arguments()
    package_names: names of CRAN packages
    version_pairs: pairs of package version numbers
    :return: a dictionary with added and removed functions and argument changes for retained functions
    """
    diff_dict = {}
    for p_id, package in enumerate(package_names):
        package_dict = {}
        for pair in version_pairs[p_id]:
            #Get functions of the two versions using dict keys
            new = result_dict[package][pair[0]].keys()
            old = result_dict[package][pair[1]].keys()
            #Check which functions have been added / removed
            added = new - old
            removed = old - new
            #Check argument difference for functions retained in latest version
            retained = new - added
            changed = []
            added_args = []
            removed_args = []
            for f in retained:
                set1 = set(result_dict[package][pair[0]][f].items())
                set2 = set(result_dict[package][pair[1]][f].items())
                diff1 = set1 - set2
                diff2 = set2 - set1
                #Check for added / removed arguments and changed default values
                for i in diff1:
                    was_changed = False
                    for j in diff2:
                        if i[0] == j[0]:
                            changed.append({'function': f, 'argument': i[0], 
                                            'old': j[1], 'new': i[1]})
                            was_changed = True
                            break
                    if not was_changed:
                        added_args.append({'function': f, 'argument': i[0]})
                for i in diff2:
                    was_changed = False
                    for j in diff1:
                        if i[0] == j[0]:
                            was_changed = True
                            break
                    if not was_changed:
                        removed_args.append({'function': f, 'argument': i[0]})
            pair_diff = {'added functions': list(added),
                        'removed functions': list(removed),
                        'new arguments': added_args,
                        'removed arguments': removed_args,
                        'argument value changes': changed}
            pair_key = f"{pair[0]}_{pair[1]}"
            package_dict.update({pair_key: pair_diff})
        diff_dict.update({package: package_dict})
    return diff_dict
