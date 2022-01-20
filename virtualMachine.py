from client import AzureClient




def stop(self, vm, auth_data):
    return self.vm_action(vm, 'stop')

def start(self, vm, auth_data):
    return self.vm_action(vm, 'start')

def reboot(self, vm, auth_data):
    return self.vm_action(vm, 'reboot')

def vm_action(self, vm, action):
    try:
        group_name = vm.id.split('/')[0]
        vm_name = vm.id.split('/')[1]
        compute_client = AzureClient().compute_client()
        if action == 'stop':
            compute_client.virtual_machines.power_off(group_name, vm_name)
        elif action == 'start':
            compute_client.virtual_machines.start(group_name, vm_name)
        elif action == 'reboot':
            compute_client.virtual_machines.restart(group_name, vm_name)
    except Exception as ex:
        self.log_exception("Error restarting the VM")
        return False, "Error restarting the VM: " + str(ex)

    return True, ""
