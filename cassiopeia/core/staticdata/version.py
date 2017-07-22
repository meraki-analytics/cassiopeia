class VersionListData(list):
    @property
    def region(self):
        return self._region


Versions = VersionListData
