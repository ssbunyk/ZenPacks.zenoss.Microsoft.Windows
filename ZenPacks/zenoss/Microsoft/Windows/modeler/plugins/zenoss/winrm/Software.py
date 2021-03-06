##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

'''
Windows Installed Software

Models list of installed software by querying Win32_Product via WMI.
'''

from Products.DataCollector.plugins.DataMaps import MultiArgs

from ZenPacks.zenoss.Microsoft.Windows.modeler.WinRMPlugin import WinRMPlugin


class Software(WinRMPlugin):
    compname = 'os'
    relname = 'software'
    modname = 'Products.ZenModel.Software'

    queries = {
        'Win32_Product': "SELECT Name, InstallDate, Vendor FROM Win32_Product",
    }

    def process(self, device, results, log):
        log.info(
            "Modeler %s processing data for device %s",
            self.name(), device.id)

        rm = self.relMap()

        for item in results.values()[0]:
            if not item.Name:
                continue

            om = self.objectMap()
            # prepId don't care about __ in resulting id
            # this results OFS ObjectManaget checkValidId() to fail
            om.id = self.eliminate_underscores(self.prepId(item.Name))
            om.title = item.Name
            if not item.Vendor:
                item.Vendor = 'Unknown'
            om.setProductKey = MultiArgs(item.Name, item.Vendor)

            if item.InstallDate:
                om.setInstallDate = '{0}/{1}/{2} 00:00:00'.format(
                    item.InstallDate[0:4],
                    item.InstallDate[4:6],
                    item.InstallDate[6:8])

            rm.append(om)

        return rm

    def eliminate_underscores(self, val):
        """Eliminates double underscores in object ID"""
        return val.replace('__', '')
