# -----------------------------------------------------------------------
# OpenXenManager
#
# Copyright (C) 2009 Alberto Gonzalez Rodriguez alberto@pesadilla.org
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MER-
# CHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# -----------------------------------------------------------------------
import xmlrpclib, urllib
import asyncore, socket
import select
import gtk
from os import chdir
import platform
import sys, shutil
import datetime
from threading import Thread
from configobj import ConfigObj
import xml.dom.minidom 
from operator import itemgetter
import pdb
import rrdinfo
import time
import gobject
from openxenmanager.messages import messages, messages_header

class oxcSERVERvmnetwork:
    def vm_remove_interface(self, vm_ref, vif_ref):
        res = self.connection.VIF.unplug(self.session_uuid, vif_ref)
        if "Value" in res:
            self.track_tasks[res['Value']] = vm_ref 
            self.vif_plug.append(res['Value'])
        res = self.connection.VIF.destroy(self.session_uuid, vif_ref)
        if "Value" in res:
            self.track_tasks[res['Value']] = vm_ref 
            self.vif_plug.append(res['Value'])
        else:
            print res
    def fill_addinterface_network(self, list):
        list.clear()
        for network in self.all_network:
            if self.all_network[network]['bridge'] != "xapi0":
                    #if self.all_pif[self.all_network[network]['PIFs'][0]]['bond_slave_of'] == "OpaqueRef:NULL":
                list.append([network, self.all_network[network]['name_label'].replace('Pool-wide network associated with eth','Network ')]) 

    def fill_editinterface_network(self, list, network_ref):
        list.clear()
        i = 0 
        current = 0
        for network in self.all_network:
            if self.all_network[network]['bridge'] != "xapi0":
                #if self.all_pif[self.all_network[network]['PIFs'][0]]['bond_slave_of'] == "OpaqueRef:NULL":
                if network == network_ref:
                    current = i
                list.append([network, self.all_network[network]['name_label'].replace('Pool-wide network associated with eth','Network ')]) 
                i = i + 1
        return current
 
    def vm_add_interface(self, vm_ref, network_ref, mac, limit):
        userdevices = [0]
        for vif in self.all_vms[vm_ref]['VIFs']:
                userdevices.append(self.all_vif[vif]['device'])
        vif_cfg = {
            'uuid': '',
            'allowed_operations': [],
            'current_operations': [],
            'device': str(int(max(userdevices))+1),
            'MAC': '',
            'MTU': '0',
            "qos_algorithm_type":   "ratelimit",
            "qos_algorithm_params": {},
            "other_config":         {},
            "MAC_autogenerated":         "False",
            "currently_attached":   False
        }    
        if limit:
            vif_cfg["qos_algorithm_params"]["kbps"] = limit
        vif_cfg['network'] = network_ref
        vif_cfg['VM'] = vm_ref
        if mac:
            vif_cfg["MAC_autogenerated"] = "False"
            vif_cfg["MAC"] = mac
        else:
            vif_cfg["MAC_autogenerated"] = "True"
        self.flag_vif_plug = False
        res = self.connection.Async.VIF.create(self.session_uuid, vif_cfg)
        if "Value" in res:
            self.track_tasks[res['Value']] = vm_ref 
            self.vif_plug.append(res['Value'])
        else:
            print "**", res


