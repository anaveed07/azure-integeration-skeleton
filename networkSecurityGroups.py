
def create_ngs(self, location, group_name, nsg_name, outports, network_client):
    """
    Create a Network Security Group
    """
    # Always add SSH port
    security_rules = [{'name': 'sr-Tcp-22-22',
                       'access': 'Allow',
                       'protocol': 'Tcp',
                       'destination_address_prefix': '*',
                       'source_address_prefix': '*',
                       'direction': 'Inbound',
                       'destination_port_range': '22',
                       'source_port_range': '*',
                       'priority': 100
                       }]
    cont = 200
    for outport in outports:
        sr = {'access': 'Allow',
              'protocol': outport.get_protocol(),
              'destination_address_prefix': '*',
              'source_address_prefix': '*',
              'direction': 'Inbound',
              'source_port_range': '*',
              'priority': cont
              }
        cont += 100
        if outport.is_range():
            sr['name'] = 'sr-%s-%d-%d' % (outport.get_protocol(),
                                          outport.get_port_init(),
                                          outport.get_port_end())
            sr['destination_port_range'] = "%d-%d" % (outport.get_port_init(), outport.get_port_end())
            security_rules.append(sr)
        elif outport.get_local_port() != 22:
            sr['name'] = 'sr-%s-%d-%d' % (outport.get_protocol(),
                                          outport.get_remote_port(),
                                          outport.get_local_port())
            sr['destination_port_range'] = str(outport.get_local_port())
            security_rules.append(sr)

    params = {
        'location': location,
        'security_rules': security_rules
    }

    ngs = None
    try:
        ngs = network_client.network_security_groups.create_or_update(group_name, nsg_name, params).result()
    except Exception:
        self.log_exception("Error creating NGS")

    return ngs