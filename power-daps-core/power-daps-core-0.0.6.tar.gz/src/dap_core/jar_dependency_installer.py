
#  Copyright 2016-2020 Prasanna Pendse <prasanna.pendse@gmail.com>
#
#  This file is part of power-daps.
#
#  power-daps is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  power-daps is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with power-daps.  If not, see <https://www.gnu.org/licenses/>.
import os, re, io
from xml.etree import ElementTree

from dap_core import common
import urllib.request

BASE_URL = "https://repo1.maven.org/maven2/"

class MavenCentralInstallerOld:
  # https://search.maven.org/remotecontent?filepath=
  def __init__(self, base_url=BASE_URL, lib_dir="lib"):
    self.base_url = base_url
    self.lib_dir = lib_dir
    self.latest_versions_cache = {}
    return

  def install(self, name, version, details):
    if not self.has_already_been_downloaded(details["group_id"], name, version, "jar"):
      self.install_file(name, version, details, "jar")
      self.install_file(name, version, details, "pom")
      self.install_transitive_dependencies(name, version, details, "pom")

  def install_transitive_dependencies(self, name, version, details, extension):
    if self.local_pom_exists(details["group_id"], name, version):
      namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}
      tree = ElementTree.parse(self.local_location(details["group_id"], name, version, "pom"))
      root = tree.getroot()

      deps = root.findall("./xmlns:dependencies/xmlns:dependency", namespaces=namespaces)
      for d in deps:
        version = "latest"
        groupId = d.find("xmlns:groupId", namespaces=namespaces).text
        artifactId = d.find("xmlns:artifactId", namespaces=namespaces).text
        version_elem = d.find("xmlns:version", namespaces=namespaces)
        if version_elem is not None:
          if self.value_references_variable(version_elem.text):
            version_var_name = re.findall("\$\{(.*?)\}", version_elem.text)[0]
            common.print_verbose("Looking for property " + version_var_name)
            props = root.findall("./xmlns:properties", namespaces=namespaces)
            for el in props[0].iter():
              if el.tag == "{http://maven.apache.org/POM/4.0.0}" + version_var_name:
                version = el.text
                common.print_verbose("Found property " + version_var_name + " = " + version)
          else:
            version = version_elem.text
        self.install(artifactId, version, {"group_id": groupId})

  def value_references_variable(self, value):
    return value.startswith("${")

  def install_file(self, name, version, details, extension):
    remote_loc = self.remote_location(details["group_id"], name, version, extension)
    local_lib_dir = self.local_lib_directory(details["group_id"], name, version)
    local_loc = self.local_location(details["group_id"], name, version, extension)
    if not self.has_already_been_downloaded(details["group_id"], name, version, extension):
      common.print_info("Downloading " + remote_loc + " to " + local_loc)
      common.run_command(["mkdir", "-p", local_lib_dir])
      self.fetch(remote_loc, local_loc)
    else:
      common.print_verbose("Dependency found at " + local_loc)
    return 0, ""

  def remote_location(self, group_id, artifact_id, version, file_extension):
    group_id_with_slashes = group_id.replace(".", "/")

    if version != "latest":
      return self.base_url + "/".join(
        [group_id_with_slashes, artifact_id, version, artifact_id]) + "-" + version + "." + file_extension
    else:
      metadata_file = self.metadata_local_location(group_id, artifact_id)
      # TODO: If metadata file is present, don't fetch again
      metadata_url = self.base_url + "/".join([group_id_with_slashes, artifact_id]) + "/maven-metadata.xml"
      self.fetch(metadata_url, metadata_file)
      # TODO: Parse metadata file and return the latest version.
      namespaces = {'xmlns': ''}
      tree = ElementTree.parse(metadata_file)
      root = tree.getroot()
      latest_version = root.find(".//latest").text
      self.add_latest_version_to_cache(group_id, artifact_id, version, file_extension, latest_version)
      return self.base_url + "/".join(
        [group_id_with_slashes, artifact_id, latest_version, artifact_id]) + "-" + latest_version + "." + file_extension

  def add_latest_version_to_cache(self, group_id, artifact_id, version, file_extension, latest_version):
    self.latest_versions_cache["_".join([group_id, artifact_id, version, file_extension])] = latest_version

  def get_latest_version_from_cache(self, group_id, artifact_id, version, file_extension):
    key = "_".join([group_id, artifact_id, version, file_extension])
    if key in self.latest_versions_cache:
      return self.latest_versions_cache[key]
    else:
      return "latest"

  def metadata_local_location(self, group_id, artifact_id):
    group_id_with_slashes = group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, artifact_id]) + \
           "/" + "maven-metadata.xml"

  def local_location(self, group_id, artifact_id, version, file_extension):
    v = version
    if version == "latest":
      v = self.get_latest_version_from_cache(group_id, artifact_id, version, file_extension)

    return self.local_lib_directory(group_id, artifact_id, v) + \
           "/" + artifact_id + "-" + v + "." + file_extension

  def local_lib_directory(self, group_id, artifact_id, version):
    group_id_with_slashes = group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, artifact_id, version])

  def fetch(self, remote_loc, local_loc):
    urllib.request.urlretrieve(remote_loc, local_loc)

  def has_already_been_downloaded(self, group_id, artifact_id, version, file_extension):
    return os.path.exists(self.local_location(group_id, artifact_id, version, file_extension))

  def local_pom_exists(self, group_id, artifact_id, version):
    return os.path.exists(self.local_location(group_id, artifact_id, version, "pom"))


class MavenCentralInstaller:
  def __init__(self, base_url=BASE_URL, lib_dir="lib"):
    self.base_url = base_url
    self.lib_dir = lib_dir
    self.latest_versions_cache = {}
    return

  def install(self, artifact_id, version, details):
    group_id = details["group_id"]
    jar_dependency = JarDependency(group_id, artifact_id, version)

    jar_dependency.install(self.base_url)


class MavenCentralArtifact:
  def __init__(self, group_id, artifact_id, version):
    self.group_id = group_id
    self.artifact_id = artifact_id
    self.version = version
    self.latest_versions_cache = {}

  def latest_version_from_metadata(self):
    latest_version_from_cache = self.get_latest_version_from_cache()
    if latest_version_from_cache != "latest":
      return latest_version_from_cache
    else:
      tree = ElementTree.parse(self.metadata_file())
      root = tree.getroot()
      latest_version = root.find(".//latest").text
      self.add_latest_version_to_cache(latest_version)

      return latest_version

  def metadata_file(self):
    metadata_file = self.metadata_local_location(self.group_id, self.artifact_id)
    if os.path.exists(metadata_file):
      return metadata_file
    else:
      group_id_with_slashes = self.group_id.replace(".", "/")
      metadata_url = self.base_url + "/".join([group_id_with_slashes, self.artifact_id]) + "/maven-metadata.xml"
      self.fetch(metadata_url, metadata_file)
      return metadata_file

  def relative_remote_location(self):
    if not self.file_extension:
      common.print_error("File extension is not set for " + self.artifact_id)
      self.file_extension.length

    group_id_with_slashes = self.group_id.replace(".", "/")

    return "/".join(
      [group_id_with_slashes, self.artifact_id, self.version, self.artifact_id]
    ) + "-" + self.version + "." + self.file_extension

  def local_location(self):
    return self.local_lib_directory() + \
           "/" + self.artifact_id + "-" + self.version + "." + self.file_extension

  def local_lib_directory(self):
    group_id_with_slashes = self.group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, self.artifact_id, self.version])

  def add_latest_version_to_cache(self, latest_version):
    self.latest_versions_cache["_".join([self.group_id, self.artifact_id, self.specified_version, self.file_extension])] = latest_version

  def get_latest_version_from_cache(self):
    key = "_".join([self.group_id, self.artifact_id, self.specified_version, self.file_extension])
    if key in self.latest_versions_cache:
      return self.latest_versions_cache[key]
    else:
      return "latest"

  def has_been_installed(self):
    installed = os.path.exists(self.local_location())
    return installed

  def install(self, base_url):
    if not self.has_been_installed():
      common.run_command(["mkdir", "-p", self.local_lib_directory()])
      fetch(base_url + self.relative_remote_location(), self.local_location(), self.error_callback)


class JarDependency:
  def __init__(self, group_id, artifact_id, version):
    self.group_id = group_id
    self.artifact_id = artifact_id
    self.specified_version = version
    self.metadata = JarDependencyMetadata(group_id, artifact_id)
    self.version = self.determine_version()
    self.pom = Pom(group_id, artifact_id, self.version)
    self.jar = Jar(group_id, artifact_id, self.version)

  def determine_version(self):
    if self.specified_version != "latest":
      return self.specified_version
    return self.metadata.latest_version()

  def install(self, base_url):
    if not self.has_been_installed():
      common.print_info("Downloading " + self.group_id + "/" + self.artifact_id + " v" + self.version)
      self.pom.install(base_url)
      self.jar.install(base_url)

      for d in self.dependencies():
        d.install(base_url)

  def has_been_installed(self):
    common.print_verbose("Checking if " + self.group_id + "/" + self.artifact_id + " is installed.")
    common.print_verbose("           v" + self.version)
    installed = self.pom.has_been_installed() and self.jar.has_been_installed()
    if installed:
      common.print_verbose(self.group_id + "/" + self.artifact_id + " v" + self.version + " already installed.")
    else:
      common.print_verbose(self.group_id + "/" + self.artifact_id + " v" + self.version + " not installed.")
    return installed

  def dependencies(self):
    jar_deps = []
    namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}
    if self.pom.pom_file() is  None:
      return jar_deps

    root = self.pom.pom_tree().getroot()

    deps = root.findall("./xmlns:dependencies/xmlns:dependency", namespaces=namespaces)
    for d in deps:
      groupId = d.find("xmlns:groupId", namespaces=namespaces).text
      if groupId.startswith("${"):
        groupId = self.pom.resolve_property(groupId)

      artifactId = d.find("xmlns:artifactId", namespaces=namespaces).text
      version = "latest"

      version_elem = d.find("xmlns:version", namespaces=namespaces)
      if version_elem is not None:
        version = version_elem.text

      if version.startswith("${"):
        version = self.pom.resolve_property(version)

      scope_elem = d.find("xmlns:scope", namespaces=namespaces)
      if scope_elem is not None:
        scope = scope_elem.text
      else:
        scope = "unspecified"

      common.print_verbose(self.group_id + "/" + self.artifact_id + " v" + self.version + " depends on " + groupId + "/" + artifactId + " version " + version + " in scope " + scope)
      if scope in ["unspecified", "compile", "runtime"]:
        dep = JarDependency(groupId, artifactId, version)
        jar_deps.append(dep)
        
    return jar_deps

  def __eq__(self, other):
    """Overrides the default implementation"""
    if isinstance(self, other.__class__):
      return self.group_id == other.group_id and self.artifact_id == other.artifact_id and self.version == other.version

    return NotImplemented

  def __hash__(self):
    """Overrides the default implementation"""
    return hash(tuple(sorted([self.group_id, self.artifact_id, self.version])))

  def __repr__(self):
    return "JarDependency[" + self.group_id + "," + self.artifact_id + "," + self.version + "]"


class JarDependencyMetadata:

  def __init__(self, group_id, artifact_id):
    self.group_id = group_id
    self.artifact_id = artifact_id
    self.latest_versions_cache = {}
    self.base_url = BASE_URL

  def latest_version(self):
    latest_version_from_cache = self.get_latest_version_from_cache()
    if latest_version_from_cache != "latest":
      return latest_version_from_cache
    else:
      tree = ElementTree.parse(self.metadata_file())
      root = tree.getroot()
      latest_version = "cannot find"
      latest_version_element = root.find(".//latest")
      version_element = root.find(".//version")
      if latest_version_element is not None:
        latest_version = latest_version_element.text
      elif version_element is not None:
        latest_version = version_element.text

      self.add_latest_version_to_cache(latest_version)
      common.print_verbose("Determined version of " + self.group_id + "/" + self.artifact_id + " to be " + latest_version + " from metadata")
      return latest_version

  def metadata_file(self):
    metadata_file = self.metadata_local_location()
    if os.path.exists(metadata_file):
      return metadata_file
    else:
      common.run_command(["mkdir", "-p", self.metadata_local_directory()])
      fetch(self.metadata_remote_location(), self.metadata_local_location())
      return metadata_file

  def metadata_local_directory(self):
    group_id_with_slashes = self.group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, self.artifact_id]) + "/"

  def metadata_local_location(self):
    return self.metadata_local_directory() + "maven-metadata.xml"

  def metadata_remote_location(self):
    group_id_with_slashes = self.group_id.replace(".", "/")
    return self.base_url + "/".join([group_id_with_slashes, self.artifact_id]) + "/maven-metadata.xml"

  def add_latest_version_to_cache(self, latest_version):
    self.latest_versions_cache["_".join([self.group_id, self.artifact_id, "latest"])] = latest_version

  def get_latest_version_from_cache(self):
    key = "_".join([self.group_id, self.artifact_id, "latest"])
    if key in self.latest_versions_cache:
      return self.latest_versions_cache[key]
    else:
      return "latest"


class Pom(MavenCentralArtifact):

  def __init__(self, group_id, artifact_id, version):
    super().__init__(group_id, artifact_id, version)
    self.file_extension = "pom"
    self.namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}
    self.tree = ""
    self.error_callback = common.print_warning

  def pom_file(self):
    if os.path.exists(self.local_location()):
      return self.local_location()
    else:
      common.print_warning("POM for " + self.group_id + "/" + self.artifact_id + " v" + self.version + " was not found locally. Assuming it has no dependencies.")
      return None

  def resolve_property(self, property_name):
    prop_name = property_name.strip("${}")
    prop_value = "dunno"
    root = self.pom_tree().getroot()

    common.print_verbose("Looking for property " + prop_name + " in " + self.local_location())

    if prop_name.startswith("${project.") or prop_name.startswith("project."):
      common.print_verbose("Looking for project property " + prop_name)
      project_property = prop_name.split(".")[1].rstrip("}")
      prop_value = self.project_property(project_property)
      common.print_verbose("Project property " + prop_name + " = " + prop_value)
      return prop_value
    else:
      props = root.findall("./xmlns:properties", namespaces=self.namespaces)
      if len(props) > 0:
        for el in props[0].iter():
          if el.tag == "{http://maven.apache.org/POM/4.0.0}" + prop_name:
            prop_value = el.text
            common.print_verbose("Found property " + prop_name + " = " + prop_value)
            if prop_value.startswith("${"):
              return self.resolve_property(prop_value)
            else:
              return prop_value
    common.print_verbose("Property " + prop_name + " is not defined in pom. Looking at parent.")
    parent_pom = self.parent_pom()
    if parent_pom:
      prop_value = parent_pom.resolve_property(prop_name)
      common.print_verbose("Parent says " + prop_name + " is " + prop_value)
    else:
      common.print_verbose("No parent found?!")
    return prop_value

  def pom_tree(self):
    if not self.tree:
      self.tree = ElementTree.parse(self.pom_file())
    return self.tree

  def project_property(self, prop_name):
    root = self.pom_tree().getroot()
    # find the project version - need to figure out the xpath
    props = root.findall(".", namespaces=self.namespaces)
    if len(props) > 0:
      for el in props[0].iter():
        if el.tag == "{http://maven.apache.org/POM/4.0.0}" + prop_name:
          prop_value = el.text
          common.print_verbose("Found property " + prop_name + " = " + prop_value)
          return prop_value

      return "no clue"
    return "don't know"

  def parent_pom(self):
    root = self.pom_tree().getroot()
    parents = root.findall("./xmlns:parent", namespaces=self.namespaces)

    if not parents:
      common.print_verbose("No parent found in " + self.local_location())
      return None

    parent_group_id = ""
    parent_artifact_id = ""
    parent_version = ""

    for el in parents[0].iter():
      if el.tag == "{http://maven.apache.org/POM/4.0.0}" + "groupId":
        parent_group_id = el.text
      elif el.tag == "{http://maven.apache.org/POM/4.0.0}" + "artifactId":
        parent_artifact_id = el.text
      elif el.tag == "{http://maven.apache.org/POM/4.0.0}" + "version":
        parent_version = el.text

    if parent_group_id:
      parent = Pom(parent_group_id, parent_artifact_id, parent_version)
      parent.install("https://repo1.maven.org/maven2/")
      return parent
    else:
      return None


class Jar(MavenCentralArtifact):

  def __init__(self, group_id, artifact_id, version):
    super().__init__(group_id, artifact_id, version)
    self.file_extension = "jar"
    self.error_callback = common.exit_with_error_message


def fetch(remote_location, local_location, error_callback=common.exit_with_error_message):
  try:
    common.print_verbose("Fetching " + remote_location + " to " + local_location)
    urllib.request.urlretrieve(remote_location, local_location)
  except urllib.error.HTTPError as err:
    error_callback(str(err.code) + " - Could not retrieve " + remote_location)